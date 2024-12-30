# imported from "C:\Users\Heng2020\OneDrive\Python NLP\NLP 06_ffmpeg\ffmpeg_01.py"
from typing import Union,List,Tuple, Literal, Callable, Dict
from pathlib import Path
import sys
import datetime
import python_wizard as pw
import os_toolkit as ost
# import dataframe_short as ds
import pkg_resources

import pandas as pd
import seaborn as sns
from pydub import AudioSegment
from beartype import beartype

alarm_done_path = pkg_resources.resource_filename(__name__, 'assets/Sound Effect positive-logo-opener.wav')
sound_error_path = pkg_resources.resource_filename(__name__, 'assets/Sound Effect Error.wav')

CODEC_DICT = {'.mp3': "libmp3lame",
                  'mp3' : "libmp3lame",
                  '.wav': "pcm_s24le",
                  'wav' : "pcm_s24le"
                  }

# v02 => add extract_audio2, extract_subtitle, _extract_media_setup,extract_sub_1_video
# get_metadata2, get_all_metadata, get_metadata
# get_subtitle_index,get_audio_index,get_video_index,_get_media_index,get_subtitle_extension,
# get_audio_extension,get_video_extension, _get_media_extension

@beartype
def create_media_info_df(
    input_video_folder:str|Path  
    ,input_video_pattern: str
    ,ep_seasons: list[str]| str
    ,media_types: list[str]
    ,input_media_folders: list[str]
    ,input_filname_patterns: list[str]
    ,titles: list[str]
    ,lang_code_3chrs: list[str]
    ,output_folder:str
    ) -> pd.DataFrame:
    """
    helper function to create media_info combinations(pd.df) to feed in to merge_media_to_video
    there's no output_name because it uses the default name
    use <> to replace the episode_season pattern
    
    """
    # took about 2.5 hr to write & test all of this
    # medium tested(generated the whole season6)
    import pandas as pd
    def _replace_with_filename(patterns:list[str],new:str, old:str = "<>") -> list[str]:
        result: list[str] = patterns.copy()
        for i, x in enumerate(patterns):
            x_new = x.replace(old,new)
            result[i] = x_new
        return result

    lengths: list[int] = [len(media_types), len(input_media_folders), len(input_filname_patterns), len(titles), len(lang_code_3chrs)]
    if len(set(lengths)) > 1:
        raise ValueError(f"All input lists must have the same length, but got lengths: {lengths}")

    media_per_ep = len(media_types)
    out_df = pd.DataFrame()

    for i, ep_season_text in enumerate(ep_seasons):
        input_filenames = _replace_with_filename(input_filname_patterns,ep_season_text)
        input_video_name = input_video_pattern.replace("<>",ep_season_text)
        
        input_media_paths = []
        for i, filename in enumerate(input_filenames):
            input_media_paths.append(input_media_folders[i] + "/" + filename)
        
        input_video_path = [input_video_folder + "/" + input_video_name]* media_per_ep
        
        output_folder_rep = [output_folder] * media_per_ep
        df_curr_ep = pd.DataFrame({
            'input_video_name': [input_video_name]*media_per_ep,
            'input_video_path': input_video_path,
            'media_type': media_types,
            'input_media_path':input_media_paths,
            'title': titles,
            'lang_code_3alpha': lang_code_3chrs,
            'output_folder': output_folder_rep,
            'output_name': [input_video_name]*media_per_ep,
            
        })
        out_df = pd.concat([out_df,df_curr_ep])
    return out_df

@beartype
def ass_to_srt_1file(ass_path:str| Path, output_folder:Path|str = "") -> None:
    # medium tested(1 file, with Path tested both srt_path & output_folder as Path)
    file_name = Path(str(ass_path)).stem + ".srt"
    sub_df = ass_to_df(ass_path)
    df_to_srt(df = sub_df, output_name = file_name,output_folder=output_folder)

@beartype
def ass_to_srt(
        ass_paths: Union[str,Path,list[str|Path]],
        output_folder: str|Path,
        ) -> None:
    import os
    import os_toolkit as ost
    from tqdm import tqdm
    import warnings
    """
    SIGNATURE FUNCTION
    
    Convert ASS subtitle files to SRT format.
    
    This function converts one or more ASS (Advanced SubStation Alpha) subtitle files to SRT (SubRip Subtitle) format. 
    It supports individual files, directories containing multiple ASS files, or a list of file paths.
    
    Parameters
    ----------
    srt_paths : str, Path, or list of str or Path
        The input ASS file(s) to convert. It can be:
        - A single file path.
        - A list of file paths.
        - A folder path containing multiple `.ass` files.
    
    output_folder : str or Path
        The folder where the converted SRT files will be saved.
    
    Returns
    -------
    None
        The converted SRT files are saved in the specified output folder.
    
    Notes
    -----
    - If `srt_paths` is a folder, all `.ass` files within the folder are converted.
    - Existing warnings during the conversion process are temporarily suppressed for cleaner output.
    
    Examples
    --------
    Convert a single ASS file:
    >>> ass_to_srt("example.ass", "./output")
    
    Convert multiple ASS files:
    >>> ass_to_srt(["file1.ass", "file2.ass"], "./output")
    
    Convert all ASS files in a folder:
    >>> ass_to_srt("./subtitles", "./output")
    """

    # medium tested(with List and folder)
    if isinstance(ass_paths, list):
        for i, srt_path in tqdm(enumerate(ass_paths), total = len(ass_paths), desc = "Converting ass to srt..."):
            warnings.filterwarnings('ignore')
            ass_to_srt_1file(srt_path,output_folder)
            warnings.filterwarnings('default')
    elif os.path.isdir(str(ass_paths)):
        # if it's folder path
        full_ass_paths = ost.get_full_filename(ass_paths,".ass")
        ass_name = ost.get_filename(ass_paths,".ass")
        for i, srt_path in tqdm(enumerate(full_ass_paths), total = len(full_ass_paths), desc = "Converting ass to srt..."):
            warnings.filterwarnings('ignore')
            ass_to_srt_1file(srt_path,output_folder)
            warnings.filterwarnings('default')
    elif isinstance(ass_paths,(Path,str)):
        warnings.filterwarnings('ignore')
        ass_to_srt_1file(ass_paths,output_folder)
        warnings.filterwarnings('default')

@beartype
def df_to_srt(df: pd.DataFrame, output_name: str, output_folder: Union[str, Path] = "") -> None:
    """
    Converts a DataFrame with subtitle data into an SRT file.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the subtitles with columns: "sentence", "start", "end".
    output_name : str
        The name of the output SRT file (e.g., "subtitles.srt").
    output_folder : str or Path, optional
        The folder where the SRT file will be saved. Defaults to the current directory.

    Returns
    -------
    None
    """
    # medium tested
    
    # Ensure output folder is a Path object
    output_folder = Path(output_folder)
    output_path = output_folder / output_name
    
    df_in = df.copy()
    # Write the SRT file
    with open(output_path, 'w', encoding='utf-8') as f:
        df_in['start'] = df_in['start'].astype(str)
        df_in['end'] = df_in['end'].astype(str)
        for index, row in df_in.iterrows():
            # Write subtitle index
            f.write(f"{index + 1}\n")

            # Format and write time stamps
            start_time = row['start'].replace('.', ',')[:-3]
            end_time = row['end'].replace('.', ',')[:-3]
            f.write(f"{start_time} --> {end_time}\n")

            # Write the subtitle sentence
            f.write(f"{row['sentence']}\n\n")

@beartype
def split_audio_by_sub(
    media_paths: Union[str,Path,  list[str|Path]] ,
    sub_paths: Union[str,Path, list[str|Path]],
    output_folder: Union[str,Path],
    prefix_names: None|str | list[str] = None,
    out_audio_ext:str = "wav",
    include_sentence:bool = True,
    alarm_done:bool = False,
    verbose:int = 1,
    modify_sub:bool = False,
    progress_bar:bool = True
        ) -> None:
    """
    Split audio files based on associated subtitle files.

    This function takes audio (or video with only audio tested) files and their corresponding subtitle files, 
    splitting the audio based on subtitle timestamps. Outputs segmented audio files to a specified folder.

    Parameters
    ----------
    media_paths : str or Path or list of str or Path
        Paths to audio or video files. Can be a single file, a single folder, or a list of files.

    sub_paths : str or Path or list of str or Path
        Paths to subtitle files (either `.ass` or `.srt`). Should align with `media_paths`.

    output_folder : str or Path
        Destination folder where the split audio files will be saved.

    prefix_names : None, str or list of str, default None
        Optional prefix for output file names. If a list, should match the number of media files.

    out_audio_ext : str, default "wav"
        File extension for the output audio files.

    include_sentence : bool, default True
        Whether to include the sentence from the subtitle in the output file metadata.

    alarm_done : bool, default False
        If True, play an alarm sound upon completion.

    verbose : int, default 1
        Verbosity level. Higher values provide more detailed output.

    modify_sub : bool, default False
        If True, allows modification of subtitle timing during processing.

    progress_bar : bool, default True
        Whether to display a progress bar for the splitting process.

    Raises
    ------
    ValueError
        If `media_paths` and `sub_paths` lists have mismatched lengths.

    Notes
    -----
    - This function handles both single file paths and folders. When given folders, all audio or video files 
    within are processed if they match specified extensions.
    - To ensure correct matching of audio and subtitle files, ensure files are sorted consistently or explicitly matched.
    """
    import os
    import os_toolkit as ost
    from tqdm.auto import tqdm
    # high tested
    
    # convert every input: using_folder_path will print out the audio and sub it uses for splitting
    media_use_folder_path:bool = False
    sub_use_folder_path:bool = False
    prefix_names_in = list(prefix_names) if isinstance(prefix_names, list) else [prefix_names]

    if isinstance(media_paths,list):
        media_path_list = list(media_paths)
    elif isinstance(media_paths,(str,Path)):
        if ost.is_folder_path(media_paths):
            media_path_list = ost.get_full_filename(media_paths,extension=[".mp3",".mp4",".wave",".mkv"])
            media_name_list = ost.get_filename(media_paths,extension=[".mp3",".mp4",".wave",".mkv"])
            media_use_folder_path = True
        else:
            media_path_list = [media_paths]


    if isinstance(sub_paths,list):
        sub_path_list = list(sub_paths)
    elif isinstance(sub_paths,(str,Path)):
        if ost.is_folder_path(sub_paths):
            sub_path_list = ost.get_full_filename(sub_paths,extension=[".ass",".srt"])
            sub_name_list = ost.get_filename(sub_paths,extension=[".mp3",".mp4",".wave",".mkv"])
            sub_use_folder_path = True
        else:
            sub_path_list = [sub_paths]

    len_media_paths = len(media_path_list)
    len_sub_paths = len(sub_path_list)
    len_prefix_names = len(prefix_names_in)

    if len_media_paths != len_sub_paths:
        raise ValueError(f"Please check length of video_paths and sub_paths. They should be the same.\n Currently video_paths has {len_media_paths} and sub_paths has {len_sub_paths}")
    if len_media_paths != len_prefix_names:
        raise ValueError(f"Please check length of video_paths and prefix_names. They should be the same.\n Currently video_paths has {len_media_paths} and prefix_names has {len_prefix_names}")
    
    
    if verbose >= 1:
        should_exit_if = False
        if (media_use_folder_path is True) and (sub_use_folder_path is True):
            media_sub_names = list(zip(media_name_list,sub_name_list))
        elif (media_use_folder_path is True) and (sub_use_folder_path is False):
            media_sub_names = list(zip(media_name_list,sub_path_list))

        elif (media_use_folder_path is False) and (sub_use_folder_path is True):
            media_sub_names = list(zip(media_path_list,sub_name_list))
        else:
            # this is the case where they will specify manually so you don't have to worry about anything
            should_exit_if = True

        if should_exit_if is False:
            for name in media_sub_names:
                print(name)

    if progress_bar:
        loop_object = tqdm(range(len_media_paths), desc="Splitting the audio")
    else:
        loop_object = range(len_media_paths)
    
    for i in loop_object:
        curr_media_path = Path(str(media_path_list[i]))
        curr_sub_path = Path(str(sub_path_list[i]))
        media_name = curr_media_path.stem
        # this has been handled by  split_1audio_by_subtitle
        # curr_output_folder = str(output_folder) + "/" + media_name
        # os.makedirs(curr_output_folder,exist_ok=True)
        split_1audio_by_subtitle(curr_media_path,curr_sub_path,output_folder,
                            prefix_name = prefix_names_in[i],
                            out_audio_ext = out_audio_ext,
                            alarm_done = alarm_done,
                            verbose = 0,
                            include_sentence = include_sentence,
                            modify_sub = modify_sub)

@beartype
def modify_sub_df_time(sub_df:pd.DataFrame) -> pd.DataFrame:
    # the result from this is promising. This works well with subttile created by whisper
    # just simply use the next 'start' as 'end' time
    
    # it works well already but the next step is the have the cut_off where we will stop if next 'start' and current 'end'
    # is too long
    # see S01E01_009 for example
    
    from datetime import timedelta
    sub_df_copy = sub_df.copy()
    sub_df_copy['start_ori'] = sub_df_copy['start'].copy()
    sub_df_copy['end_ori'] = sub_df_copy['end'].copy()
    
    sub_df_copy['end'] = sub_df_copy['start'].shift(-1)
    
    # replace last row with the same value
    sub_df_copy.loc[sub_df_copy.index[-1], 'end'] = sub_df_copy.loc[sub_df_copy.index[-1], 'end_ori']
    return sub_df_copy

@beartype
def sub_to_df(sub_path,
              remove_stopwords=True,
              stopwords=["♪", "\n", "<i>", "</i>", "<b>", "</b>"]) -> pd.DataFrame | List[pd.DataFrame]:
    """
    Convert a subtitle file (.ass or .srt) or multiple subtitle files in a directory to pandas DataFrame(s).

    Parameters
    ----------
    sub_path : str or Path
        The path to the subtitle file or a directory containing subtitle files.
    remove_stopwords : bool, optional
        If True, specified stopwords will be removed from the sentences. Default is True.
    stopwords : list of str, optional
        A list of stopwords to remove from the sentences. Default is ["♪", "\\n", "<i>", "</i>", "<b>", "</b>"].

    Returns
    -------
    pd.DataFrame or list of pd.DataFrame
        A DataFrame if a single file is processed, or a list of DataFrames if multiple files are processed.

    Notes
    -----
    - Determines the file type based on the file extension.
    - Calls `ass_to_df` if the file is `.ass`, `srt_to_df` if `.srt`.
    - Raises an error if the file is neither `.ass` nor `.srt`.
    """
    from pathlib import Path

    sub_path = Path(sub_path)

    def process_file(file_path):
        if file_path.suffix.lower() == '.ass':
            return ass_to_df(file_path, remove_stopwords=remove_stopwords, stopwords=stopwords)
        elif file_path.suffix.lower() == '.srt':
            return srt_to_df(file_path, remove_stopwords=remove_stopwords, stopwords=stopwords)
        else:
            raise ValueError(f"Unsupported file extension: {file_path.suffix}")

    if sub_path.is_file():
        # Single file case
        return process_file(sub_path)

    elif sub_path.is_dir():
        # Directory containing multiple subtitle files
        ass_files = list(sub_path.glob('*.ass'))
        srt_files = list(sub_path.glob('*.srt'))
        all_files = ass_files + srt_files
        if not all_files:
            raise ValueError("No .ass or .srt files found in the directory.")
        df_list = []
        for file in all_files:
            df = process_file(file)
            df_list.append(df)
        return df_list

    else:
        raise ValueError("The provided path must be a .ass or .srt file or a directory containing such files.")

@beartype
def ass_to_df(ass_path: str | Path,
              remove_stopwords:bool =True,
              stopwords=["♪", "\n", "<i>", "</i>", "<b>", "</b>"]) -> pd.DataFrame | List[pd.DataFrame]:
    

    """
    Convert an ASS subtitle file or multiple ASS files in a directory to pandas DataFrame(s).

    Parameters
    ----------
    ass_path : str or Path
        The path to the .ass file or a directory containing .ass files.
    remove_stopwords : bool, optional
        If True, specified stopwords will be removed from the sentences. Default is True.
    stopwords : list of str, optional
        A list of stopwords to remove from the sentences. Default is ["♪", "\\n", "<i>", "</i>", "<b>", "</b>"].

    Returns
    -------
    pd.DataFrame or list of pd.DataFrame
        A DataFrame if a single file is processed, or a list of DataFrames if multiple files are processed.

    Notes
    -----
    - Uses pysubs2 to parse .ass files.
    - Times are converted from milliseconds to seconds.
    - Handles both single file and directory input.
    """

    # seems to work now

    import pandas as pd
    from pathlib import Path
    import pysubs2
    from datetime import timedelta, datetime
    import re

    # Convert ass_path to a Path object
    ass_path = Path(ass_path)

    def process_file(file_path):
        # Read the .ass file using pysubs2
        subs = pysubs2.load(file_path, encoding="utf-8")
        sentences = []
        start_times = []
        end_times = []

        for sub in subs:
            text = sub.text
            # Replace '\N' with a single space
            text = text.replace("\\N", " ")
            if remove_stopwords:
                # Remove specified stopwords
                for word in stopwords:
                    text = text.replace(word, "")
                # Remove ASS style overrides like {\an8}
                text = re.sub(r"{.*?}", "", text)
            sentences.append(text)
            start_time = (datetime.min + timedelta(milliseconds=sub.start)).time()
            end_time = (datetime.min + timedelta(milliseconds=sub.end)).time()
            start_times.append(start_time)  # Convert milliseconds to seconds
            end_times.append(end_time)

        # Create a DataFrame
        df = pd.DataFrame({
            'sentence': sentences,
            'start': start_times,
            'end': end_times
        })
        return df

    if ass_path.is_file() and ass_path.suffix == '.ass':
        # Single file case
        return process_file(ass_path)

    elif ass_path.is_dir():
        # Directory containing multiple .ass files
        ass_files = list(ass_path.glob("*.ass"))
        df_list = []
        for file in ass_files:
            df = process_file(file)
            df_list.append(df)
        return df_list

    else:
        raise ValueError("The provided path must be a .ass file or a directory containing .ass files.")

@beartype
def ms_to_time_text(milliseconds: Union[int, float]) -> str:
    """
    Convert milliseconds to time text format.

    Args:
    milliseconds (Union[int, float]): Time in milliseconds.

    Returns:
    str: Time in format "hr.min.sec" or "min.sec".

    Examples:
    272000 => "4.32" (4 min 32 sec)
    6032000 => "1.40.32" (1 hr 40 min 32 sec)
    """
    if not isinstance(milliseconds, (int, float)):
        raise ValueError("Input must be an integer or float representing milliseconds.")

    total_seconds = int(milliseconds / 1000)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f"{hours}.{minutes:02d}.{seconds:02d}"
    else:
        return f"{minutes}.{seconds:02d}"

@beartype
def text_to_milisecond(time_text:Union[str,int,float],delimiter:str = ".") -> Union[int,float]:
    """
    time_text should be seperated by dot for :
    convert strings to miliseconds to easily convert back and forth between video view and pydub input
    if it's already int it would return the same
    
    Convert time text to milliseconds.

    Args:
    time_text (Union[str, int, float]): Time in format "hr.min.sec" or "min.sec" or milliseconds.

    Returns:
    Union[int, float]: Time in milliseconds.

    Examples:
    "4.32" => (4*60 + 32) * 1000 = 272000 ms (4 min 32 sec)
    "1.40.32" => (1*3600 + 40*60 + 32) * 1000 = 6032000 ms (1 hr 40 min 32 sec)
    """
    if isinstance(time_text, (int, float)):
        return time_text

    if not isinstance(time_text, str):
        raise ValueError("Input must be a string, int, or float.")

    parts = time_text.split(delimiter)
    
    if len(parts) == 2:
        minutes, seconds = map(int, parts)
        return (minutes * 60 + seconds) * 1000
    elif len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
        return (hours * 3600 + minutes * 60 + seconds) * 1000
    else:
        raise ValueError("Invalid time format. Use 'min.sec' or 'hr.min.sec'.")

@beartype
def clean_subtitle(string:str):
    import re
    pattern1 = r"<.*?>"
    
    pattern2 = r"<\/[a-zA-Z]>"
    
    string1 = re.sub(pattern1, "", string)
    string2 = string1.replace("\n"," ")
    new_string = re.sub(pattern2,"",string2)
    return new_string

@beartype
def audio_duration(media_path: str | Path | AudioSegment):
    from pydub import AudioSegment
    from datetime import datetime, timedelta

    if isinstance(media_path,str, Path):
        video_audio = AudioSegment.from_file(str(media_path))
    elif isinstance(AudioSegment):
        video_audio = media_path

    # Get the duration of the audio segment in milliseconds
    duration_ms = len(video_audio)

    # Convert the duration from milliseconds to a timedelta object
    duration = timedelta(milliseconds=duration_ms)

    # Create a dummy datetime object with a zero timestamp
    dummy_datetime = datetime(1, 1, 1, 0, 0, 0)

    # Add the duration to the dummy datetime to get the final datetime
    final_datetime = dummy_datetime + duration

    return final_datetime.time()

@beartype
def split_1audio_by_sub_df(
    media_path: Union[str,Path],
    subs_df: pd.DataFrame,
    output_folder,
    prefix_name = None,
    out_audio_ext = "wav",
    alarm_done:bool = False,
    verbose:int = 1,
    include_sentence:bool = True,
    modify_sub:bool = False,
        ) -> None:
    # the reason I need to create this function because I want to manipulate time directly in df not in subtitle file

    import time
    import os
    from pydub import AudioSegment
    from playsound import playsound
    from pathlib import Path

    import video_toolkit as vt
    import python_wizard as pw
    import py_string_tool as pst
    import datetime

    # alarm done path still have an error
    # took about 1 hr(including testing)
    # Add feature: input as video_folder_path and subtitle_folder_path, then 
    # it would automatically know which subttile to use with which video(using SxxExx)
    
    # split_audio_by_subtitle
    media_name = Path(media_path).stem
    if prefix_name is None:
        prefix_name_in = Path(media_path).stem
    else:
        prefix_name_in = str(prefix_name)
        
    # with dot and no dots supported
    # but only tested with no dots out_audio_ext
    
    out_audio_ext_dot = out_audio_ext if out_audio_ext[0] == "." else ("." + out_audio_ext)
    out_audio_ext_no_dot = out_audio_ext[1:] if out_audio_ext[0] == "." else ( out_audio_ext)
    

    # TODO: write a function input is video/video path & subs/sub path
    t01 = time.time()
    video_audio = AudioSegment.from_file(media_path)
    t02 = time.time()
    t01_02 = t02-t01

    if verbose in [1]:
        print("Load video time: ", end = " ")
        pw.print_time(t01_02)
    
    if alarm_done:
        playsound(alarm_done_path)

    t03 = time.time()
    video_length = audio_duration(video_audio)
    # Iterate over subtitle sentences
    
    if modify_sub:
        subs_df_in = modify_sub_df_time(subs_df)
    else:
        subs_df_in = subs_df.copy()

    n = subs_df_in.shape[0]
    t04 = time.time()
    for i in range(n):
        start_time = subs_df_in.loc[i,'start']
        end_time = subs_df_in.loc[i,'end']
        sentence_text:str = str(subs_df_in.loc[i,'sentence'])

        if start_time > video_length:
            break

        start_time_ms = to_ms(start_time)
        end_time_ms = to_ms(end_time)

        # Extract audio segment based on timestamps
        sentence_audio = video_audio[start_time_ms:end_time_ms]
        
        num_str = pst.num_format0(i+1,n+1)
        # Save the audio segment to a file
        if sentence_text[-1] in [".",","]:
            sentence_no_dots = sentence_text[:-1]
        else:
            sentence_no_dots = sentence_text

        if include_sentence:
            audio_name = f'{prefix_name_in}_{num_str}_{sentence_no_dots}{out_audio_ext_dot}'
        else:
            audio_name = f'{prefix_name_in}_{num_str}{out_audio_ext_dot}'
        
        audio_name_clean = pst.clean_filename(audio_name)
        audio_output = os.path.join(output_folder,audio_name_clean)
        sentence_audio.export(audio_output, format=out_audio_ext_no_dot)
    t05 = time.time()

    t04_05 = t05-t04
    if alarm_done:
        try:
            playsound(alarm_done_path)
        except:
            pass

@beartype
def split_1audio_by_subtitle(
    media_path: str | Path,
    subtitle_path,
    output_folder,
    prefix_name = None,
    out_audio_ext = "wav",
    alarm_done:bool = False,
    verbose:int = 1,
    include_sentence:bool = True,
    modify_sub:bool = False,
        ) -> None:
    
    """
    Split an audio file into multiple audio files based on a subtitle file.

    Parameters
    ----------
    video_path : str or Path
        Path to the video file.
    subtitle_path : str or Path
        Path to the subtitle file.
    output_folder : str or Path
        Path to the output folder where the audio files will be saved.
    prefix_name : str, optional
        Prefix of the audio file names. If None, the prefix will be the stem of the video file name.
    out_audio_ext : str, optional
        File extension of the output audio files. Default is 'wav'.
    alarm_done : bool, optional
        If True, play a sound when the function is done. Default is False.
    verbose : int, optional
        Verbosity level. If 1, the time taken to load the video and split the audio will be printed.
    include_sentence : bool, optional
        If True, include the sentence in the audio file name. Default is True.
    modify_sub : bool, optional
        If True, modify the time of subtitle(from whisper)

    Notes
    -----
    The subtitle file should be in the format of a pandas DataFrame with columns 'start', 'end', and 'sentence'.
    The 'start' and 'end' columns should be in the format of a datetime object.
    The 'sentence' column should be a string.

    The audio files will be saved in the format of {prefix_name}_{num_str}_{sentence_no_dots}{out_audio_ext_dot}
    where num_str is the number of the audio file and sentence_no_dots is the sentence without any dots.
    """

    import time
    import os
    from pydub import AudioSegment
    from playsound import playsound
    from pathlib import Path
    import re

    import video_toolkit as vt
    import python_wizard as pw
    import py_string_tool as pst
    import datetime
    # Added01: remove the tags in sentence
    #   eg: '<font face="sans-serif" size="71">Sei o que procurar.</font>' => Sei o que procurar.

    # alarm done path still have an error
    # took about 1 hr(including testing)
    # Add feature: input as video_folder_path and subtitle_folder_path, then 
    # it would automatically know which subttile to use with which video(using SxxExx)
    
    # split_audio_by_subtitle
    media_name = Path(media_path).stem
    if prefix_name is None:
        prefix_name_in = Path(media_path).stem
    else:
        prefix_name_in = str(prefix_name)
        
    # with dot and no dots supported
    # but only tested with no dots out_audio_ext
    
    out_audio_ext_dot = out_audio_ext if out_audio_ext[0] == "." else ("." + out_audio_ext)
    out_audio_ext_no_dot = out_audio_ext[1:] if out_audio_ext[0] == "." else ( out_audio_ext)
    
    subs_ori: pd.DataFrame = vt.sub_to_df(subtitle_path)

    if modify_sub:
        subs: pd.DataFrame = modify_sub_df_time(subs_ori)
    else:
        subs: pd.DataFrame = subs_ori.copy()

    
    # TODO: write a function input is video/video path & subs/sub path
    t01 = time.time()
    video_audio = AudioSegment.from_file(media_path)
    t02 = time.time()
    t01_02 = t02-t01

    if verbose in [1]:
        print("Load video time: ", end = " ")
        pw.print_time(t01_02)
    
    if alarm_done:
        playsound(alarm_done_path)

    t03 = time.time()
    video_length = audio_duration(video_audio)
    # Iterate over subtitle sentences
    n: int = subs.shape[0]
    t04: float = time.time()
    new_folder = output_folder + "/" + media_name
    os.makedirs(new_folder,exist_ok=True)
    
    for i in range(n):
        start_time: datetime.time = subs.loc[i,'start']
        end_time: datetime.time = subs.loc[i,'end']

        PATTERN_TO_REMOVE = [r'</?font[^>]*>']

        sentence_text = str(subs.loc[i,'sentence'])

        sentence_text_cleaned = sentence_text
        for pattern in PATTERN_TO_REMOVE:
            sentence_text_cleaned: str = re.sub(pattern, '', sentence_text_cleaned)

        if start_time > video_length:
            break

        start_time_ms = to_ms(start_time)
        end_time_ms = to_ms(end_time)

        # Extract audio segment based on timestamps
        sentence_audio = video_audio[start_time_ms:end_time_ms]
        
        num_str = pst.num_format0(i+1,n+1)
        # Save the audio segment to a file
        if sentence_text_cleaned[-1] in [".",","]:
            sentence_no_dots = sentence_text_cleaned[:-1]
        else:
            sentence_no_dots = sentence_text_cleaned

        if include_sentence:
            audio_name = f'{prefix_name_in}_{num_str}_{sentence_no_dots}{out_audio_ext_dot}'
        else:
            audio_name = f'{prefix_name_in}_{num_str}{out_audio_ext_dot}'
        
        audio_name_clean = pst.clean_filename(audio_name)
        audio_output = os.path.join(new_folder,audio_name_clean)
        sentence_audio.export(audio_output, format=out_audio_ext_no_dot)
    t05 = time.time()

    t04_05 = t05-t04
    if alarm_done:
        playsound(alarm_done_path)

@beartype
def make_1_season_Excel_unaligned(EN_folder_path: Union[str,Path],
                                  PT_folder_path: Union[str,Path], 
                                  out_excel_name: Union[str,Path],
                                  output_folder: None | str = None,
                                  drop_timestamp: bool = True,
                                  ):
    # medium tested
    # based on pd. 2.1.3
    # imported from NLP 09_SenMem Pipeline
    """
    

    Parameters
    ----------
    EN_folder_path : TYPE
        the path contains many Excel files of script in 1 episode(in English)
    PT_folder_path : TYPE
        the path contains many Excel files of script in 1 episode(in Portuguese)
    out_excel_name : TYPE
        DESCRIPTION.
    output_folder : TYPE
        DESCRIPTION.
     : TYPE
        DESCRIPTION.
    
    drop_timestamp: remove the timestamp from the output script
    (Not implemented)

    Returns
    -------
    out_df : TYPE
        DESCRIPTION.

    """
    import pandas as pd
    import sys
    from pathlib import Path

    
    import dataframe_short as ds
    import dataframe_short.move_column as mc
    import video_toolkit as vt
    import python_wizard as pw
    import os_toolkit as ost
    
    en_df: pd.DataFrame  = combine_files_1_season(str(EN_folder_path))
    en_df = en_df.add_suffix('_EN')
    # en_df.rename(columns = {'sentence':'sentence_EN',
    #                                 'start':'start_EN',
    #                                 'end':'end_EN',
    #                                 'NoSentence':'NoSentence_EN',
    #                                 },
    #              inplace = True,
                 
    #              )
    en_df["Episode"] = en_df["Episode_EN"]
    en_df = en_df.drop(columns = ["Episode_EN"])
    
    en_df['NoSentence_EN'] = en_df['NoSentence_EN'].astype('int')
    en_df['NoSentence_EN'] = en_df['NoSentence_EN'] + 1
    en_df = en_df.reset_index(drop = True)



    pt_df = combine_files_1_season(str(PT_folder_path))
    pt_df = pt_df.add_suffix('_PT')
    pt_df["Episode"] = pt_df["Episode_PT"]
    pt_df = pt_df.drop(columns = ["Episode_PT"])
    # pt_df.rename(columns = {'sentence':'sentence_PT',
    #                                 'start':'start_PT',
    #                                 'end':'end_PT',
    #                                 'NoSentence':'NoSentence_PT',
    #                                 },
    #              inplace = True,
    #              )
    pt_df['NoSentence_PT'] = pt_df['NoSentence_PT'].astype('int')
    pt_df['NoSentence_PT'] = pt_df['NoSentence_PT'] + 1
    pt_df = pt_df.reset_index(drop = True)

    out_df:pd.DataFrame

    pt_df_music = pt_df[pt_df['sentence_PT'].str.contains('♪', na=False) ]
    en_df_music = en_df[en_df['sentence_EN'].str.contains('♪', na=False) ]


    # Filter out rows where 'Column1' contains '♪'
    en_df_filter = en_df[~en_df['sentence_EN'].str.contains('♪', na=False)]
    pt_df_filter = pt_df[~pt_df['sentence_PT'].str.contains('♪', na=False)]
    en_df_music = en_df_filter[en_df_filter['sentence_EN'].str.contains('♪', na=False) ]


    out_df = ds.index_aligned_append(en_df_filter,pt_df_filter,"Episode")
    out_df = out_df.reset_index(drop = True)
    out_df.index = out_df.index + 1
    # keep only the first occurrence of each column (Episode is duplicated)
    out_df = out_df.loc[:, ~out_df.columns.duplicated()]
    
    # automatically add .xlsx extension to the file 
    out_excel_name_in:str = str(out_excel_name) if ".xlsx" in str(out_excel_name) else (str(out_excel_name) + ".xlsx")
    
    mc.to_first_col(out_df, "Episode")

    
    if output_folder is None:
        out_excel_path = str(out_excel_name_in)
    else:
        out_excel_path = str(Path(output_folder) / Path(out_excel_name_in))
    
    if drop_timestamp:
        out_df = out_df.drop(columns = ['start_EN','end_EN','start_PT','end_PT'])
    
    out_df['Episode'] = out_df['Episode'].ffill()
    out_df.to_excel(str(out_excel_path))
    
    return out_df

# read the link here of how to use Lingtrain
# https://habr.com/ru/articles/586574/

@beartype
def read_sentences_from_excel(
        file_path: str | Path
        ,sheet_name: str
        ,portuguese_col: str
        ,english_col: str
        ,nrows: None |int = None):
    # imported from NLP 09_SenMem Pipeline
    """
    Reads Portuguese and English sentences from an Excel file.
    
    :param file_path: Path to the Excel file.
    :param sheet_name: Name of the sheet containing the sentences.
    :param portuguese_col: Column letter for Portuguese sentences.
    :param english_col: Column letter for English sentences.
    :return: Tuple of two lists containing Portuguese and English sentences.
    """
    import dataframe_short as ds

    df: pd.DataFrame = pd.read_excel(file_path,sheet_name=sheet_name,nrows=nrows,usecols=[portuguese_col,english_col])

    portuguese_sentences = df.iloc[:,0].tolist()
    english_sentences = df.iloc[:,1].tolist()


    return portuguese_sentences, english_sentences

@beartype
def read_movie_script2(
        file_path :str | Path
        ,sheet_name:str = "Sheet1"
        ,portuguese_col:int|str = 0
        ,english_col:int|str = 1):
    # imported from NLP 09_SenMem Pipeline
    # middle tested 
    # dependency: pd_by_column, pd_split_into_dict_df, pd_regex_index
    # work with format that use title to seperate the episode
    import pandas as pd
    import re
    from openpyxl.utils import column_index_from_string
    import dataframe_short as ds
    
    # Load the dataset from the Excel file
    
    if pw.is_convertible_to_num(portuguese_col):
        portuguese_col_no = int(portuguese_col)
    else:
        portuguese_col_no = column_index_from_string(portuguese_col) - 1
        
    
    if pw.is_convertible_to_num(english_col):
        english_col_no = int(english_col)
    else:
        english_col_no = column_index_from_string(english_col) - 1
    
    # If it's the column name eg A, G,H
    
    data_ori = ds.read_excel(file_path, sheet_name=sheet_name)
    # playsound(alarm_path)
    
    data = ds.by_col(data_ori,[portuguese_col_no, english_col_no])
    

    # Function to check if a cell value matches the episode identifier pattern (e.g., S01E01)
    # r'[Ss]\d{2}[Ee]\d{2}' => S01E01
    df_dict = ds.split_into_dict_df(data,r'[Ss]\d{2}[Ee]\d{2}',0)
    # df_dict = pd_split_into_dict_df(data,index_list=episode_start_indices)
    return df_dict

@beartype
def read_movie_script(
        file_path: str | Path
        ,sheet_name: str | int
        ,portuguese_col: str
        ,english_col: str):
    # the main function that I should use from now on
    # imported from NLP 09_SenMem Pipeline
    from openpyxl.utils import column_index_from_string
    import dataframe_short as ds
    df: pd.DataFrame = ds.read_excel(file_path, sheet_name=sheet_name)
    # df = pd_by_column(df_ori, [portuguese_col,english_col])
    
    """
    Extracts content from a DataFrame based on 'Episode' information.

    Parameters
    ----------
    df : pandas.DataFrame
        The original DataFrame containing an 'Episode' column with format 'SxxExx',
        and columns for content ('sentence_PT', 'sentence_EN').

    Returns
    -------
    pandas.DataFrame
        A new DataFrame with 'season' and 'episode' as MultiIndex.
        Each row contains a DataFrame in the 'content' column, which itself
        contains 'sentence_PT' and 'sentence_EN' from the original DataFrame.

    Examples
    --------
    >>> main_df = pd.DataFrame({
    ...     'Episode': ['S06E08', 'S06E08', 'S01E01'],
    ...     'sentence_PT': ['sentence1_PT', 'sentence2_PT', 'sentence3_PT'],
    ...     'sentence_EN': ['sentence1_EN', 'sentence2_EN', 'sentence3_EN']
    ... })
    >>> read_movie_script2(main_df)
    """
    
    if pw.is_convertible_to_num(portuguese_col):
        portuguese_col_no = int(portuguese_col)
    else:
        portuguese_col_no = column_index_from_string(portuguese_col) - 1
        
    
    if pw.is_convertible_to_num(english_col):
        english_col_no = int(english_col)
    else:
        english_col_no = column_index_from_string(english_col) - 1
    
    # Extract season and episode numbers from the 'Episode' column
    df['season'] = df['Episode'].str.extract(r'S(\d+)E\d+').astype(int)
    df['episode'] = df['Episode'].str.extract(r'S\d+E(\d+)').astype(int)
    
    # Prepare the data for the new DataFrame
    data = []
    
    # Group by 'season' and 'episode', then iterate over each group
    for (season, episode), group in df.groupby(['season', 'episode']):
        # Create a DataFrame for this group's content
        content_df = ds.by_col(group, [portuguese_col_no, english_col_no]).reset_index(drop=True)
        
        # Append season, episode, and content DataFrame to the list
        data.append({'season': season, 'episode': episode, 'content': content_df})
    
    # Convert the list to a DataFrame
    new_df = pd.DataFrame(data)
    
    # Set 'season' and 'episode' as the index
    new_df.set_index(['season', 'episode'], inplace=True)
    
    return new_df

@beartype
def align_1_season(
        excel_1_season_script: str | Path,
        out_excel_name: Union[str,Path],
        output_folder: None | str = None,
        sheet_name:str = 'Sheet1',
        
        n_episodes: Union[str,int] = "all",
        portuguese_col:str = "F",
        english_col:str = "D",
        lang_from:str ="PT",
        lang_to:str ="EN",
        alarm_done:bool = True,
                   
                   ) -> pd.DataFrame:
    
    # imported from NLP 09_SenMem Pipeline
    """
    
    it would take about 1.2 min per 1 episode of BigBang(20 min)
    about 20 min in 1 whole season
    
    create the Excel file for "aligned" sentences for 1 season for series

    Parameters
    ----------
    excel_1_season_script : TYPE
        Excel that has 1 sheet containing all episodes script
        
    out_excel_name : Union[str,Path]
        output Excel name, only ".xlsx" supported at the moment
        
    output_folder : TYPE, optional
        DESCRIPTION. The default is None.
    sheet_name : TYPE, optional
        DESCRIPTION. The default is 'Sheet1'.
    portuguese_col : TYPE, optional
        DESCRIPTION. The default is "F".
    english_col : TYPE, optional
        DESCRIPTION. The default is "D".
    lang_from : TYPE, optional
        DESCRIPTION. The default is "PT".
    lang_to : TYPE, optional
        DESCRIPTION. The default is "EN".

    Returns
    -------
    you need to set this saved as variable otherwise it would output df.head()
    it would export the Excel file and return pd.df at the same time
    pd.DataFrame

  """
    
    import pandas as pd
    import time
    from playsound import playsound
    from tqdm import tqdm
    import dataframe_short as ds
    import dataframe_short.move_column as mc

    episode_aligned: pd.DataFrame
    
    ts_start = time.perf_counter()
    
    df_script = read_movie_script(excel_1_season_script, sheet_name, portuguese_col, english_col)
    season_aligned = pd.DataFrame()
    ts_read  = time.perf_counter()
    error_episode = []
    
    
    
    # using 1-index system
    i = 1
    for curr_index in df_script.index:
        
        if isinstance(n_episodes, int):
            if i > n_episodes:
                break
            
        season, episode = curr_index
        episode_str = f'S{season:02d}E{episode:02d}'
        single_episode = df_script.loc[curr_index,"content"]
        
        try:
            
            # slow from here
            episode_aligned = sen_alignment_df(single_episode,lang_from=lang_from,lang_to=lang_to,alarm_done = False)
    
            episode_aligned.index = episode_aligned.index + 1
            episode_aligned['sentence_' + lang_from  ] = episode_aligned[lang_from]
            episode_aligned['sentence_' + lang_to  ] = episode_aligned[lang_to]
            
            episode_aligned = episode_aligned.drop(columns = [lang_from,lang_to])
            
            episode_aligned['Season'] =  season
            episode_aligned['Episode'] =  episode
            episode_aligned = episode_aligned.drop_duplicates(subset=['sentence_' + lang_from ,'sentence_' + lang_to])
            mc.to_first_col(episode_aligned, ['Season','Episode'])
            # drop rows that are empty
            episode_aligned = episode_aligned.dropna(subset = ['sentence_' + lang_from] )
            
            season_aligned = pd.concat([season_aligned,episode_aligned])
            print(f"{episode_str} Done Aligning !!! ----------------------------------------")
        except:
            print(f"Error at {episode_str} was found !!! ########################")
            error_episode.append(episode_str)
        
        i += 1
            
    out_excel_name_in:str = str(out_excel_name) if ".xlsx" in str(out_excel_name) else (str(out_excel_name) + ".xlsx")
    
    
    if output_folder is None:
        out_excel_path = str(out_excel_name_in)
    else:
        out_excel_path = str(Path(output_folder) / Path(out_excel_name_in))
    season_aligned.to_excel(str(out_excel_path))
    
    if len(error_episode) > 0:
        print("Errors occurred at these episodes")
        print(error_episode)
    
    ts_end = time.perf_counter()
    duration_read = ts_read - ts_start
    total_duration = ts_end - ts_start
    # i = counted episodes
    
    avg_per_ep = total_duration / i
    avg_per_ep /= 60

    print("\nTotal processing time")
    pw.print_time(total_duration)
    
    print(f"{avg_per_ep:.2f} min per episode\n")    
    if alarm_done:
        playsound(alarm_done_path)
    
    return season_aligned

@beartype
def sen_alignment_df(
        df: pd.DataFrame
        ,lang_from: None |str = None
        ,lang_to: None |str = None,
        alarm_done:bool = True,
                ) -> pd.DataFrame:
    # medium tested
    if lang_from is None: lang_from = df.columns[0]
    if lang_to is None: lang_to = df.columns[1]
    
    text_list_from = df.iloc[:, 0].tolist()
    text_list_to = df.iloc[:, 1].tolist()
    # assume that text from is
    result = sentence_alignment(text_list_from,text_list_to,lang_from,lang_to,alarm_done=alarm_done)
    
    return result
    
@beartype
def sentence_alignment(
        text_from: list[str] | str
        ,text_to: list[str] | str
        ,lang_from:str = "pt"
        , lang_to:str = "en",
        alarm_done:bool = True,
                       
        ) -> pd.DataFrame:
    # v02 => add alarm parameter
    # text_from, text_to are expected to be text or list
    # medium tested, seem to work pretty well now
    
    import os
    from lingtrain_aligner import preprocessor, splitter, aligner, resolver, reader, helper, vis_helper
    from pathlib import Path
    import lingtrain_aligner
    from playsound import playsound
    import numpy as np
    from time import time
    

    folder = Path.cwd()
    db_name = "book.db"
    
    db_path = folder / db_name

    
    models = ["sentence_transformer_multilingual", "sentence_transformer_multilingual_labse"]
    model_name = models[0]
    
    # convert to list of text_from,text_to is not list
    
        
    ts01 = time()
    if not isinstance(text_from, list):
        text1_prepared = preprocessor.mark_paragraphs(text_from)
        splitted_from = splitter.split_by_sentences_wrapper(text1_prepared, lang_from)
    else:
        splitted_from = [str(x) for x in text_from if x is not np.nan ]
        # splitted_from = splitter.split_by_sentences_wrapper(text_from, lang_from)
    
    if not isinstance(text_to, list):
        
        text2_prepared = preprocessor.mark_paragraphs(text_to)
        splitted_to = splitter.split_by_sentences_wrapper(text2_prepared, lang_to)
    else:
        splitted_to = [str(x) for x in text_to if x is not np.nan ]
        # splitted_to = splitter.split_by_sentences_wrapper(text_to, lang_to)

    # temp adding title, author, h1, h2 to make it work first,.... we'll look into it when this is not avaliable later
    
    
    # if lang_from == "pt" and lang_to == "en":
    #     marker = ["(No title)%%%%%title." , 
    #                "(No author)%%%%%author.", 
    #                "(No header_)%%%%%h1.", 
    #                "(No header_)%%%%%h2."]
    #     splitted_from = marker + splitted_from
    #     splitted_to = marker + splitted_to
        
        
    # Create the database and fill it.
    if os.path.isfile(db_path):
        os.unlink(db_path)
        
    aligner.fill_db(db_path, lang_from, lang_to, splitted_from, splitted_to)
    
    # batch_ids = [0,1]
    
    aligner.align_db(db_path, \
                    model_name, \
                    batch_size=100, \
                    window=40, \
                    # batch_ids=batch_ids, \
                    save_pic=False,
                    embed_batch_size=10, \
                    normalize_embeddings=True, \
                    show_progress_bar=True
                    )
    pic_name = "alignment_vis.png"
    pic_path = folder / pic_name
    vis_helper.visualize_alignment_by_db(db_path, output_path=pic_path, lang_name_from=lang_from, lang_name_to=lang_to, batch_size=400, size=(800,800), plt_show=True)
    
    # Explore the conflicts
    
    conflicts_to_solve, rest = resolver.get_all_conflicts(db_path, min_chain_length=2, max_conflicts_len=6, batch_id=-1)
    
    resolver.get_statistics(conflicts_to_solve)
    resolver.get_statistics(rest)
    
    # resolver.show_conflict(db_path, conflicts_to_solve[8])
    
    
    steps = 10
    batch_id = -1 
    
    for i in range(steps):
        conflicts, rest = resolver.get_all_conflicts(db_path, min_chain_length=2+i, max_conflicts_len=6*(i+1), batch_id=batch_id)
        resolver.resolve_all_conflicts(db_path, conflicts, model_name, show_logs=False)
        vis_helper.visualize_alignment_by_db(db_path, output_path="img_test1.png", lang_name_from=lang_from, lang_name_to=lang_to, batch_size=400, size=(600,600), plt_show=True)
    
        if len(rest) == 0: break
    
    paragraphs = reader.get_paragraphs(db_path)[0]
    
    paragraph_from_2D = paragraphs['from']
    paragraph_to_2D = paragraphs['to']

    paragraph_from_result = [item for list_1D in paragraph_from_2D for item in list_1D]
    paragraph_to_result = [item for list_1D in paragraph_to_2D for item in list_1D]
    
    paragraph_result = pd.DataFrame({lang_from:paragraph_from_result,
                                     lang_to:paragraph_to_result
                                     })
    
    ts02 = time()
    total_time = ts02-ts01
    pw.print_time(total_time)
    
    if alarm_done:
        playsound(alarm_done_path)
    
    return paragraph_result

@beartype
def combine_files_1_season(folder_path: str | Path) -> pd.DataFrame:
    from functools import partial
    import dataframe_short as ds
    
    func = partial(ds.combine_files_to_df, 
                   extract_pattern = r'S\d+E\d+',
                   filename_col_name = "Episode",
                   )
    out_df: pd.DataFrame = func(folder_path)
    out_df.columns.values[1] = 'NoSentence'
    return out_df

@beartype
def crop_video(
        video_path: str, 
        t_start: str, 
        t_end: str, 
        # time_slice: List[Tuple[str, str]],
        output_extension: Literal["mp3", ".mp3",".mp4","mp4","mkv",".mkv","wav",".wav"] | None = None,
        alarm_done:bool = True
        ) -> None:
    # tested only input(mkv) => output(mkv)
    import subprocess
    import os
    from playsound import playsound
    
    
    # Construct the base output filename
    base_name = os.path.splitext(video_path)[0]
    
    if output_extension is None:
        extension_in = os.path.splitext(video_path)[1][1:]
    else:
        extension_in = (output_extension.split(".")[1]) if "." in output_extension else output_extension
    # Find an unused file name
    i = 1
    while os.path.exists(f"{base_name}_{i:02d}.{extension_in}"):
        i += 1
    output_path = f"{base_name}_{i:02d}.{extension_in}"
    # FFmpeg command
    command = [
        'ffmpeg', '-ss', t_start, '-to', t_end,
        '-i', video_path,
        '-c', 'copy' if extension_in in ["mp4","mkv"] else '-vn',
        output_path
    ]
    
    result = subprocess.run(command, text=True, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        print("Error encountered:")
        print(result.stderr)
    
    elif result.returncode == 0:
        print("Extract audio successfully!!!")
        
        if alarm_done:
            playsound(alarm_done_path)
    
    return output_path  # Return the output file path

@beartype
def srt_to_df(
    srt_path: str | Path,
    remove_stopwords:bool = True,
    stopwords: list[str] = ["♪","\n","<i>","</i>","<b>","</b>"]) -> pd.DataFrame | List[pd.DataFrame]:
    # df = pd.DataFrame({
        #     'sentence': sentences,
        #     'start': start_times,
        #     'end': end_times
        # })

# remove_newline will remove '\n' from the extracted text
    import pysrt
    import pandas as pd
    import py_string_tool as pst
    import os_toolkit as ost

    if ".srt" in str(srt_path):
        # 1 file case
        subs = pysrt.open(srt_path)
        # Initialize empty lists for storing data
        sentences = []
        start_times = []
        end_times = []
    
        # Extract data from each subtitle sentence
        for sub in subs:
            sentences.append(sub.text)
            start_times.append(sub.start.to_time())
            end_times.append(sub.end.to_time())
    
        # Create a DataFrame
        if remove_stopwords:
            #FIX it's still can't replace properly 
            sentences = [pst.replace(sentence,stopwords,"") for sentence in sentences]
        df = pd.DataFrame({
            'sentence': sentences,
            'start': start_times,
            'end': end_times
        })
        return df
    else:
        # many srt's file using folder
        
        str_file_names = ost.get_full_filename(srt_path,".srt")
        df_list = []
        for str_file_name in str_file_names:
            each_df = srt_to_df(str_file_name)
            df_list.append(each_df)
        return df_list

@beartype
def srt_to_csv(
        srt_path: str| Path
        ,output_path: str |Path
        ,encoding:str ='utf-8-sig'
        ,index:bool = False) -> None:
    # output should be total_path
    df_sub: pd.DataFrame  = srt_to_df(srt_path)
    # encoding='utf-8-sig' for Portuguese
    df_sub.to_csv(output_path, encoding=encoding,index=index)

@beartype
def srt_to_Excel(
        srt_path: str| Path
        ,output_path: str| Path
        ,encoding:str ='utf-8-sig'
        ,index:bool = True) -> None:
    import pandas as pd
    import os
    """ 
    Wrote on Aug 27, 2023
    I already wrote it for 1 file but it took me about 3 additional hrs to 
    make it work with multiple files in folder
    """
    # output should be total_path
    df_sub: pd.DataFrame | List[pd.DataFrame] = srt_to_df(srt_path)
    pd_ver = pw.package_version("pandas")
    
    if isinstance(df_sub,pd.DataFrame):
    # encoding='utf-8-sig' for Portuguese
        if pd_ver < (2,0,0):
            df_sub.to_excel(output_path, encoding=encoding,index=index)
        else:
            df_sub.to_excel(output_path, index=index)
            
    elif isinstance(df_sub,list):
        short_names = ost.get_filename(srt_path,".srt")
        out_full_name = [os.path.join(output_path,short_name).replace(".srt",".xlsx") for short_name in short_names]
        
        if pd_ver < (2,0,0):
            for i,df in enumerate(df_sub):
                df.to_excel(out_full_name[i], encoding=encoding,index=index)
                
        else:
            for i,df in enumerate(df_sub):
                df.to_excel(out_full_name[i], index=index)

@beartype
def to_ms(time_obj: datetime.time) -> float:
    time_obj_ms = (time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second) * 1000 + time_obj.microsecond // 1000
    return time_obj_ms


# from typing import Union,List,Tuple, Literal, Callable, Dict
# from pathlib import Path
# import sys
# import datetime
# import python_wizard as pw
# import os_toolkit as ost
# import dataframe_short as ds
# import pkg_resources

del Union
del List
del Tuple
del Literal
del Callable
del Dict

del AudioSegment
del sys, datetime, pw, pd, sns
del beartype, ost, pkg_resources

# TODO: srt_to_Excel => similar to srt_to_csv but output as excel
# srt_to_Excel(srt_path,sub_output)

# n_file = len(srt_to_df(srt_folder_path))
# srt_to_Excel(srt_folder_path,output_folder)

# print(f"Done converting srt to Excel in Total {n_file} files ")
# playsound(alarm_path)




