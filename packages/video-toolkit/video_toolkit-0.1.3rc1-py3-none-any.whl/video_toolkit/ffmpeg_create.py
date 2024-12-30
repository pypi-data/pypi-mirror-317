from pydub import AudioSegment
from typing import Union,List,Tuple, Literal, Callable, Dict, Any
from pathlib import Path
from video_toolkit.ffmpeg_extract import *
import pandas as pd
from beartype import beartype
import pkg_resources

alarm_done_path = pkg_resources.resource_filename(__name__, 'assets/Sound Effect positive-logo-opener.wav')
sound_error_path = pkg_resources.resource_filename(__name__, 'assets/Sound Effect Error.wav')

@beartype
def _create_media_dict_info(df: pd.DataFrame) -> List[Dict[str, Any]]:
    info_dict_list: List[Dict[str, Any]] = []
    group_cols = ["input_video_name", "input_video_path", "output_folder", "output_name"]

    for keys, grp in df.groupby(group_cols):
        input_video_name, input_video_path, output_folder, output_name = keys
        media_df = grp[["media_type", "input_media_path", "title", "lang_code_3alpha"]]

        info_dict: Dict[str, Any] = {
            "input_video_name": input_video_name,
            "input_video_path": input_video_path,
            "output_folder": output_folder,
            "output_name": output_name,
            "media": media_df
        }

        info_dict_list.append(info_dict)

    return info_dict_list

@beartype
def merge_media_to_video(info_df:pd.DataFrame,errors:Literal["raise","warn","ignore"] = "warn") -> None:
    
    """
    SIGNATURE FUNCTION
    
    Merge additional media streams into multiple video files.
    
    This function merges audio and subtitle tracks into a video file, preserving the existing video streams. 
    The metadata (language code and title) for the added media streams can also be specified.
    
    Parameters
    ----------

    
    input_info_df : pd.DataFrame
        A DataFrame containing information about the media streams to be added.\n
        The DataFrame must have the following columns:\n
        - `input_video_name` (str): Input video file name.(Not used in the function, just for debugging purposes) \n
        - `input_video_path` (str): Path to the input video file to which the media streams will be added. \n
        - `media_type` (str): The type of media stream, either 'audio' or 'subtitle'. Any other value will raise an error.\n
        - `input_media_path` (str): The file path of the media stream to be added.\n
        - `title` (str): The title of the media stream (e.g., language or description).\n
        - `lang_code_3alpha` (str): The 3-letter language code for the media stream (e.g., "eng", "spa").\n
        - `output_folder` (str): Path to the folder where the output video file will be saved..\n
        - `output_name` (str): The name of the output video file. If not specified, the original video's name is retained.\n
        
        Misspelling of column names or invalid values in `media_type` will result in an error.\n
    
    Returns
    -------
    None
        The merged video file is saved to the specified output folder.
    
    Raises
    ------
    ValueError
        If the DataFrame `input_info_df` is missing required columns or contains invalid values for `media_type`.
    
    Notes
    -----
    - The input video file is retained as-is, and the additional media streams are appended.
    - Metadata such as language and title for each media stream is applied during the merging process.
    - The function uses `ffmpeg` for processing; ensure it is installed and available in the system's PATH.
    
    """
    # medium tested
    # took about 30 min to write and tested
    
    
    
    from tqdm import tqdm
    info_dict_list = _create_media_dict_info(info_df)
    
    for i, curr_info_dict in tqdm(enumerate(info_dict_list), total=len(info_dict_list), desc="Creating Videos"):
        try:
            merge_media_to1video(
                input_video_path = curr_info_dict["input_video_path"]
                , input_info_df = curr_info_dict["media"]
                , output_folder = curr_info_dict["output_folder"]
                ,output_name = curr_info_dict["output_name"]
                ,errors = "raise"
                )
        except (TypeError,UnboundLocalError) as e:
            print(f"There's an error in while processing: {curr_info_dict['input_video_path']}\n")
            print(e)
            print()
        except Exception as e:
            print("This is new Error Type")
            print(e)
            print(type(e))
            print(f"There's an error in while processing: {curr_info_dict['input_video_path']}\n")

@beartype
def merge_media_to1video(
    input_video_path: Union[str, Path],
    input_info_df:pd.DataFrame,
    output_folder: str,
    output_name: Union[str, Path] = "",
    errors:Literal["raise","warn","ignore"] = "warn"
) -> None:
    
    """
    Merge additional media streams into a video file.
    
    This function merges audio and subtitle tracks into a video file, preserving the existing video streams. 
    The metadata (language code and title) for the added media streams can also be specified.
    
    Parameters
    ----------
    input_video_path : str or Path
        Path to the input video file to which the media streams will be added.
    
    input_info_df : pd.DataFrame
        A DataFrame containing information about the media streams to be added.\n
        The DataFrame must have the following columns:\n
        - `media_type` (str): The type of media stream, either 'audio' or 'subtitle'. Any other value will raise an error.\n
        - `input_media_path` (str): The file path of the media stream to be added.\n
        - `title` (str): The title of the media stream (e.g., language or description).\n
        - `lang_code_3alpha` (str): The 3-letter language code for the media stream (e.g., "eng", "spa").\n
        Misspelling of column names or invalid values in `media_type` will result in an error.\n
    
    output_folder : str
        Path to the folder where the output video file will be saved.
    
    output_name : str or Path, optional, default ""
        The name of the output video file. If not specified, the original video's name is retained.
    
    Returns
    -------
    None
        The merged video file is saved to the specified output folder.
    
    Raises
    ------
    ValueError
        If the DataFrame `input_info_df` is missing required columns or contains invalid values for `media_type`.
    
    Notes
    -----
    - The input video file is retained as-is, and the additional media streams are appended.
    - Metadata such as language and title for each media stream is applied during the merging process.
    - The function uses `ffmpeg` for processing; ensure it is installed and available in the system's PATH.
    
    Examples
    --------
    >>> input_video_path = "example.mp4"
    >>> input_info_df = pd.DataFrame({
    ...     "media_type": ["audio", "subtitle"],
    ...     "input_media_path": ["example_audio.mp3", "example_subtitle.srt"],
    ...     "title": ["English Audio", "English Subtitles"],
    ...     "lang_code_3alpha": ["eng", "eng"]
    ... })
    >>> output_folder = "./output"
    >>> output_name = "merged_video.mp4"
    >>> merge_media_to1video(input_video_path, input_info_df, output_folder, output_name)
    """

    
    # tested with 1 video
    
    
    import subprocess
    from pathlib import Path

    video_path = Path(input_video_path)
    output_path = Path(output_folder) / output_name

    command = ['ffmpeg', '-i', str(video_path)]

    for _, row in input_info_df.iterrows():
        command.extend(['-i', str(row['input_media_path'])])

    command.append('-map')
    command.append('0')

    audio_count = count_audio(input_video_path) 
    sub_count = count_subtitle(input_video_path) 
    total_media = len(input_info_df)

    # Mapping
    for idx, row in enumerate(input_info_df.itertuples(), start=1):
        if row.media_type == 'audio':
            command.append('-map')
            command.append(f'{idx}:a')
        elif row.media_type == 'subtitle':
            command.append('-map')
            command.append(f'{idx}:s')

    # Metadata
    for row in input_info_df.itertuples():
        lang = row.lang_code_3alpha
        title = row.title
        if row.media_type == 'audio':
            command.extend([f'-metadata:s:a:{audio_count}', f'language={lang}'])
            command.extend([f'-metadata:s:a:{audio_count}', f'title={title}'])
            audio_count += 1
        elif row.media_type == 'subtitle':
            command.extend([f'-metadata:s:s:{sub_count}', f'language={lang}'])
            command.extend([f'-metadata:s:s:{sub_count}', f'title={title}'])
            sub_count += 1

    command.extend(['-c', 'copy', str(output_path)])
    result = subprocess.run(command, text=True, stderr=subprocess.PIPE)
    if errors in ["warn"]:
        if result.returncode != 0:
            print("Error encountered:")
            print(result.stderr)
    elif errors in ["raise"]:
        if result.returncode != 0:
            raise Exception(result.stderr)

@beartype
def export_audio(audio_segment:AudioSegment,
                 start_end_time_dict: Dict[int,Tuple[int,int]],
                 output_names:Dict[int,str],
                 output_folder:str = "",
                 progress_bar:bool = True,
                 ) -> None:
    
    # medium tested
    """
    Key feature: 
        1) Remove the invalid path in output_names automatically
    the timestamp should be in miliseconds units(for now)
    export multiple audio_segments
    make sure that index in output_names is also in start_end_time_dict
    
    example of start_end_time_dict
        start_end_time_dict = {
        6:  [14_633 , 15_933],
        7:  [24_455 , 25_534],
        8:  [25_700 , 27_550],
        9:  [27_899 , 30_000],
        10: [31_075 , 32_863],
        11: [33_439 , 36_188],
        12: [37_280 , 42_100],
        14: [42_865 , 47_224],
        
        }

    TOADD: replace => it would check if file already exists, if so depending on it's True or False, it would replace the file
    """
    import py_string_tool as pst
    clean_output_names = {}
    for inx, output_name in output_names.items():
        clean_output_names[inx] = pst.clean_filename(output_name)
    
    from tqdm import tqdm
    if progress_bar:
        loop_obj = tqdm(start_end_time_dict.items())
    else:
        loop_obj = start_end_time_dict.items()
    
    for inx, time_stamp in loop_obj:
        start_time, end_time = time_stamp
        try:
            output_name = clean_output_names[inx]
        except KeyError:
            raise KeyError(f"there's no index {inx} in your output_names(Dict). Please check your index again.")
        output_path = output_folder + "/" + output_name
        curr_audio = audio_segment[start_time:end_time]
        
        try:
            curr_audio.export(output_path)
        except PermissionError:
            raise KeyError(f"Please close the file {output_path} first.")

@beartype
def merge_sub_to_video(
    input_video_path: Union[str, Path],
    input_subtitle_path: Union[List[Union[str, Path]], Union[str, Path]],
    sub_lang_code_3alpha: Union[List[str], str],
    sub_title: Union[List[str], str],
    output_name: str,
    output_folder: Union[str, Path] = "",
    replace:bool = False,
) -> None:
    """
    Merges a video file with additional subtitle tracks, assigning metadata such as language and title to each subtitle track.

    Parameters
    ----------
    input_video_path : str or Path
        The path to the input video file.
    input_subtitle_path : list of str/Path or str/Path
        The path(s) to the input subtitle file(s). Can be a single path or a list of paths.
    subtitle_lang_code_3alpha : list of str or str
        The language code(s) for the subtitle track(s) (e.g., 'fre' for French). Can be a single code or a list.
    subtitle_title : list of str or str
        The title(s) for the subtitle track(s) (e.g., 'French'). Can be a single title or a list.
    output_folder : str or Path
        The folder where the output video file will be saved.
    output_name : str
        The name of the output video file.

    Returns
    -------
    None
    """
    import subprocess
    # Ensure inputs are lists for consistent processing
    # tested input_subtitle_path as list and single string, 
    # tested replace = True
    if isinstance(input_subtitle_path, (str, Path)):
        input_subtitle_path = [input_subtitle_path]
    if isinstance(sub_lang_code_3alpha, str):
        sub_lang_code_3alpha = [sub_lang_code_3alpha]
    if isinstance(sub_title, str):
        sub_title = [sub_title]

    # Check for consistent lengths of inputs
    if not (len(input_subtitle_path) == len(sub_lang_code_3alpha) == len(sub_title)):
        raise ValueError("The lengths of input_subtitle_path, subtitle_lang_code_3alpha, and subtitle_title must match.")

    video_path = Path(input_video_path)
    output_path = Path(output_folder) / output_name

    # Construct the ffmpeg command
    if replace:
        command = ['ffmpeg', '-y', '-i', str(video_path)]
    else:
        command = ['ffmpeg', '-i', str(video_path)]

    # Add all subtitle inputs
    for subtitle in input_subtitle_path:
        command.extend(['-i', str(subtitle)])

    # Add mapping for video and subtitles
    command.append('-map')
    command.append('0')  # Map all streams from video
    for idx in range(len(input_subtitle_path)):
        command.append('-map')
        command.append(f'{idx + 1}:s')  # Map each subtitle file

    # Add metadata for each subtitle track
    start_index = get_sub_index_latest(input_video_path) + 1
    
    for idx, (lang, title) in enumerate(zip(sub_lang_code_3alpha, sub_title), start=start_index):
        command.extend(['-metadata:s:s:' + str(idx), f'language={lang}'])
        command.extend(['-metadata:s:s:' + str(idx), f'title={title}'])

    # Add codec settings and output file
    command.extend(['-c', 'copy', str(output_path)])

    # cmd_line is just for debugging
    cmd_line = ' '.join(command)

    # Execute the command
    result = subprocess.run(command, text=True, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print("Error encountered:")
        print(result.stderr)

@beartype
def merge_audio_to_video(
    input_video_path: Union[str, Path],
    input_audio_path: Union[List[Union[str, Path]], Union[str, Path]],
    audio_lang_code_3alpha: Union[List[str], str],
    audio_title: Union[List[str], str],
    output_folder: Union[str, Path],
    output_name: str
) -> None:
    """
    Merges a video file with additional audio tracks, assigning metadata such as language and title to each audio track.

    Parameters
    ----------
    input_video_path : str or Path
        The path to the input video file.
    input_audio_path : list of str/Path or str/Path
        The path(s) to the input audio file(s). Can be a single path or a list of paths.
    audio_language_code_3alpha : list of str or str
        The language code(s) for the audio track(s) (e.g., 'fre' for French). Can be a single code or a list.
    audio_title : list of str or str
        The title(s) for the audio track(s) (e.g., 'French'). Can be a single title or a list.
    output_folder : str or Path
        The folder where the output video file will be saved.
    output_name : str
        The name of the output video file.

    Returns
    -------
    None
    """
    
    # medium tested for input_audio_path as list and single_string
    from pathlib import Path
    import subprocess
    
    # Ensure inputs are lists for consistent processing
    if isinstance(input_audio_path, (str, Path)):
        input_audio_path = [input_audio_path]
    if isinstance(audio_lang_code_3alpha, str):
        audio_lang_code_3alpha = [audio_lang_code_3alpha]
    if isinstance(audio_title, str):
        audio_title = [audio_title]

    # Check for consistent lengths of inputs
    if not (len(input_audio_path) == len(audio_lang_code_3alpha) == len(audio_title)):
        raise ValueError("The lengths of input_audio_path, audio_language_code_3alpha, and audio_title must match.")

    video_path = Path(input_video_path)
    output_path = Path(output_folder) / output_name

    # Construct the ffmpeg command
    command = ['ffmpeg', '-i', str(video_path)]

    # Add all audio inputs
    for audio in input_audio_path:
        command.extend(['-i', str(audio)])

    # Add mapping for video and audio
    command.append('-map')
    command.append('0')  # Map all streams from video
    for idx in range(len(input_audio_path)):
        command.append('-map')
        command.append(f'{idx + 1}:a')  # Map each audio file

    # Add metadata for each audio track
    for idx, (lang, title) in enumerate(zip(audio_lang_code_3alpha, audio_title), start=2):
        command.extend(['-metadata:s:a:' + str(idx), f'language={lang}'])
        command.extend(['-metadata:s:a:' + str(idx), f'title={title}'])

    # Add codec settings and output file
    command.extend(['-c', 'copy', str(output_path)])

    # cmd_line is just for debugging
    cmd_line = ' '.join(command)

    # Execute the command
    result = subprocess.run(command, text=True, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print("Error encountered:")
        print(result.stderr)

del Union,List,Tuple, Literal, Callable, Dict, Any, Path
del AudioSegment
del beartype, pkg_resources