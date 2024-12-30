from typing import Union,List,Tuple, Literal, Callable, Dict
from pathlib import Path
import pkg_resources
import os_toolkit as ost
from beartype import beartype

alarm_done_path = pkg_resources.resource_filename(__name__, 'assets/Sound Effect positive-logo-opener.wav')
sound_error_path = pkg_resources.resource_filename(__name__, 'assets/Sound Effect Error.wav')

CODEC_DICT = {'.mp3': "libmp3lame",
                  'mp3' : "libmp3lame",
                  '.wav': "pcm_s24le",
                  'wav' : "pcm_s24le"
                  }

@beartype
def count_audio(media_path,language = None,file_extension = None):
    # right now language has to be 3-chr code only
    # low tested
    
    # TOADD1, support when language is not 3-chr code
    selected_media = get_metadata(media_path, media = "audio", language = language, file_extension = file_extension)
    n_audio = len(selected_media)
    return n_audio

@beartype
def count_subtitle(media_path,language = None,file_extension = None):
    # right now language has to be 3-chr code only
    # low tested
    
    # TOADD1, support when language is not 3-chr code
    selected_media = get_metadata(media_path, media = "subtitle", language = language, file_extension = file_extension)
    n_sub = len(selected_media)
    return n_sub

@beartype
def get_sub_index_latest(media_path):
    # medium tested
    sub_index = get_subtitle_index(media_path)
    # normalize the index(index start with 0)
    if isinstance(sub_index, list):
        latest_sub_index = max(sub_index) - min(sub_index)
    else:
        latest_sub_index = 0
    return latest_sub_index

@beartype
def is_ffmpeg_installed():

    import subprocess
    try:
        # Run the 'ffmpeg -version' command
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True)
        # If the above command runs successfully, FFmpeg is installed and in PATH
        print("FFmpeg is installed and accessible in PATH.")
    except subprocess.CalledProcessError:
        # An error occurred while running FFmpeg, it might not be installed or in PATH
        print("FFmpeg is not installed.")
    except FileNotFoundError:
        # FFmpeg is not in PATH
        print("FFmpeg is installed but not in PATH.")

@beartype
def extract_audio(
        video_folder:     Union[Path,str],
        output_folder:    Union[Path,str],
        video_extension:  Union[list,str] = [".mp4",".mkv"],
        output_extension: Union[list,str] = ".mp3",
        overwrite_file:   bool = True,
        n_limit:          int = 150,
        output_prefix:    str = "",
        output_suffix:    str = "",
        alarm_done:       bool = True,

        one_output_per_lang: bool = True,
        languages: Union[List[str],None] = None,
):
    # extract_audio3 is highly tested now
    # this is from extract_audio3(it's already tested through time seems pretty stable)
    """
    the diff between 
    extract_audio1 - use manually code to loop through folder
    extract_audio2 - powered by _extract_media_setup while 
    extract_audio3 - use extract_audio_1file as a base(which is more general than extract_audio1 & extract_audio2), but need more testing to see if it works
    
    # after testing I would then rename extract_audio3 to just extract_audio
    
    """


    _extract_media_setup(
        input_folder = video_folder,
        output_folder = output_folder,
        input_extension = video_extension,
        output_extension = output_extension,
        extract_1_file_func = extract_audio_1file,
        overwrite_file = overwrite_file,
        n_limit = n_limit,
        output_prefix = output_prefix,
        output_suffix = output_suffix,
        alarm_done = alarm_done,

        one_output_per_lang = one_output_per_lang,
        languages = languages

    )

@beartype
def extract_audio_1file(
        video_path:     Union[str,Path],
        output_folder:  Union[str,Path],
        output_name:    Union[str,Path, None] = None, 
        output_extension: Union[str,list] = ".mp3",
        alarm_done: bool = False,
        overwrite_file: bool = True,
        one_output_per_lang: bool = True,
        languages: Union[List[str],None] = None,
        
        progress_bar:bool = True,
        encoding = "utf-8-sig",
                    ) -> None:
    # time spend 5 hr
    # this support multiple output_extension
    # medium tested
    
    
    #  tested Parameters:
        # all default parameters
        # when languages is str
    
    # untested Parameters
        # output_extension as list
        # overwrite_file = False
        # one_output_per_lang = False
        # languages as list
        
    # Not Done 
    # Next right now I got a name BigBang_FR_S06E01.mp3_EN which is wrong
    
    from langcodes import Language
    """
    Extract audio from a video file. If video has multiple audio in different languages,
    this function also support that
    
    it's more general than extract_audio. These functions need to be tested and merge in the future

    Parameters
    ----------
    video_path : Union[str,Path]
        DESCRIPTION.
    output_folder : Union[str,Path]
        DESCRIPTION.
    output_name : Union[str,Path]
        DESCRIPTION.
    file_extension : Union[str,list], optional
        DESCRIPTION. The default is ".mp3".
    alarm_done : bool, optional
        DESCRIPTION. The default is True.
    overwrite_file : bool, optional
        DESCRIPTION. The default is True.
    
    one_output_per_lang : bool, optional
        If there are more than 1 audio files for each langauge, if True then it would one extract 1 file per
        language, if not it would extract all of them seperately.
        The default is True.
        False is still not in production because I have to create index suffix at the end
    Returns
    -------
    bool
        DESCRIPTION.

    """
    from tqdm import tqdm
    from langcodes import Language
    from pathlib import Path
    import subprocess
    from playsound import playsound
    import os

    
    codec = CODEC_DICT[output_extension]
    
    output_folder_in = Path(output_folder)
    
    file_extension_in = [output_extension] if isinstance(output_extension, str) else list(output_extension)
    

    if output_name is None:
        output_name_in = Path(video_path).stem
    else:
        output_name_in = output_name
    
    filter_lang = [languages] if isinstance(languages,str) else languages
    
    if languages is None:
        filter_lang_3chr = None
    else:
        filter_lang_3chr = []
    
        for language in filter_lang:
            lang_obj =  closest_language_obj(language)
            # variant = "B" would return fre for french
            filter_lang_3chr.append(lang_obj.to_alpha3(variant = "B"))
    
    audio_index = get_audio_index(video_path)
    metadata = get_metadata(video_path,"audio",language=filter_lang_3chr)
    
    if one_output_per_lang:
        metadata_filter = metadata.drop_duplicates(subset=['language'], keep='first')
    else:
        metadata_filter = metadata.copy()
    
    audio_index = list(metadata_filter.index)
    video_lang_list = metadata_filter['language'].tolist()


    output_name_list = []
    output_path_list = []

    if progress_bar:
        loop_obj = tqdm(enumerate(video_lang_list),total=len(video_lang_list))
    else:
        loop_obj = enumerate(video_lang_list)

    for i, language_3_str in loop_obj:
        
        lang_obj =  Language.get(language_3_str)
        language_2_str = str(lang_obj).upper()
        lang_obj.to_alpha3()
        for j, curr_file_ext in enumerate(file_extension_in):
            
            if curr_file_ext not in output_name_in:
                if "." not in curr_file_ext:
                    file_extension_in[j] = "." + curr_file_ext
                else:
                    file_extension_in[j] = curr_file_ext
                curr_output_name = output_name_in + "_" + language_2_str + file_extension_in[j]
                output_name_list.append(curr_output_name)
                output_path = output_folder_in / curr_output_name
                output_path_list.append(output_path)
                
                command = [
                    "ffmpeg",
                    "-i", str(video_path),
                    "-map", f"0:{audio_index[i]}",
                    "-c:a", codec,
                    "-q:a", "0",
                    str(output_path)
                ]
                # keep command_line for debugging
                command_line = " ".join(command)
 
                if os.path.exists(str(output_path)):
                    if overwrite_file:
                        os.remove(str(output_path))
                    else:
                        print("\nThe output path is already existed. Please delete the file or set the overwrite parameter to TRUE")
                        return False
                try:
                    result = subprocess.run(command, text=True, stderr=subprocess.PIPE,encoding=encoding)
                except UnicodeDecodeError:
                    raise UnicodeDecodeError(f"\nError encountered: {curr_output_name}. Please change the encoding parameter to ensure that the function works properly.")

                
                if result.returncode != 0:
                    print(f"\nError encountered: {curr_output_name}")
                    print(result.stderr)
                
                elif result.returncode == 0:
                    print(f"\nExtract audio successfully: {curr_output_name}!!!")
                    
                    if alarm_done:
                        playsound(alarm_done_path)


# Sub
@beartype
def _extract_media_setup(
        input_folder: Union[str,Path],
        output_folder: Union[str,Path],
        extract_1_file_func: Callable,
        input_extension: Union[list[str],str],
        output_extension: Union[list[str],str],
        # input_param_name: list[str],
        overwrite_file:   bool = True,
        n_limit: int = 150,
        output_prefix:    str = "",
        output_suffix:    str = "",
        alarm_done: bool = True,

        one_output_per_lang: bool = True,
        languages: Union[List[str],None] = None,
        # errors: Literal["ignore","raise"] = "ignore",
) -> None :
    # 
    
    """
    helper function to reduce code redundancy
    it would setup which/ how many files should be extracted in inputs
    how many files should be created in output 

    extract_1_file_func that are compatible with this function will contain these parameters(no more no less)
    
    (video_path ,output_extension ,output_folder ,output_name,alarm_done,overwrite_file)

    if extract_1_file_func doesn't have this requirement you need to modify the code in this function to support that manually

    """
    import inspect_py as inp
    import python_wizard as pw
    import python_wizard.pw_list as pwl
    import sys
    from pathlib import Path
    from playsound import playsound
    from time import time, perf_counter
    from tqdm import tqdm


    ts01 = time()
    output_extension = [output_extension]
    output_extension_in = []
    
    # add . to extension in case it doesn't have .
    if output_extension[0] is not None:
        for extension in output_extension:
            if not "." in extension:
                output_extension_in.append("."+extension)
            else:
                output_extension_in.append(extension)
    else:
        output_extension_in = [None]


    filename_list_ext = ost.get_filename(input_folder,input_extension)
    path_list = ost.get_full_filename(input_folder,input_extension)
    # warrus operator, makes it usuable only for python >= 3.8
    (n_file := min(len(filename_list_ext),n_limit))
    filename_list_ext = filename_list_ext[:n_file]
    path_list = path_list[:n_file]

    filename_list = [filename.split('.')[0] for filename in filename_list_ext]

    for i, filename in tqdm(enumerate(filename_list),total = len(filename_list)):
        
            
        output_name = output_prefix + filename_list[i] + output_suffix
        # original_stdout = sys.stdout
        # sys.stdout = open('nul', 'w')
         
        # the problem here is that the input parameter name in extract_1_file_func
        # could be different and 

        # extract_1_file_func should support only 1 output
        # if multiple output is supported in extract_1_file_func, it could create multiple files(not tested)

        for j, extension in enumerate(output_extension_in):
            # input_dict = {
            #     input_param_name[0]:path_list[i],
            #     input_param_name[1]:extension,
            # }
            extract_1_file_params = inp.input_params(extract_1_file_func)
            try:
                if "languages" in extract_1_file_params:
                    
                    if pwl.contain_all_items(extract_1_file_params,["one_output_per_lang","progress_bar"]):
                        extract_1_file_func(
                            video_path = path_list[i],
                            output_extension = extension,
                            output_folder = output_folder,
                            output_name = output_name,
                            alarm_done=False,
                            overwrite_file=overwrite_file,
                            one_output_per_lang = one_output_per_lang,
                            languages = languages,

                            progress_bar = False

                            )
                    else:
                        extract_1_file_func(
                            video_path = path_list[i],
                            output_extension = extension,
                            output_folder = output_folder,
                            output_name = output_name,
                            alarm_done=False,
                            overwrite_file=overwrite_file,
                            languages = languages,

                            )
                else:

                    extract_1_file_func(
                        video_path = path_list[i],
                        output_extension = extension,
                        output_folder = output_folder,
                        output_name = output_name,
                        alarm_done=False,
                        overwrite_file=overwrite_file)
            except Exception as e:
                print(f"Error occured at file {filename_list[i]}")
            print(f"extracted {output_name} successfully!!!")
        
        # sys.stdout = original_stdout
    if alarm_done:
        try:
            playsound(alarm_done_path)
        except:
            pass
    ts02 = time()
    duration = ts02-ts01
    pw.print_time(duration)
    print()
    return filename_list

@beartype
def get_metadata2(
        media_path: Path | str,
        encoding = "utf-8-sig",
        ):

    """
    Get the index of the first subtitle stream in the video file.
    
    Parameters:
    - video_path: Path to the input video file.
    
    Returns:
    - Index of the first subtitle stream, or None if no subtitle stream is found.
    """

    import subprocess
    import json
    # 80% from GPT4
    command = [
        'ffprobe',
        '-v', 'quiet',
        '-show_streams',
        media_path
    ]
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, text=True,encoding=encoding)
    except UnicodeDecodeError:
        raise UnicodeDecodeError(f"\nError encountered. Please change the encoding parameter to ensure that the function works properly.")
    streams_info_raw = json.loads(result.stdout)
    
    streams_info = [stream for stream  in streams_info_raw['streams']]

    
    return streams_info

@beartype
def get_all_metadata(
        media_path: Path | str,
        encoding:str = "utf-8-sig"):
    import subprocess
    import json    
    import pandas as pd
    #  !!!!!!!!!!!! this is the main get_metadata
    # medium tested
    # 100% from GPT4
    # new and updated version
    

    """
    Get metadata from a media file and return it as a pandas DataFrame.
    
    Parameters:
    - media_path: Path to the input media file.
    
    Returns:
    - DataFrame with columns for 'filetype', 'file_extension', 'language', and 'duration'.
    """
    command = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        '-show_format',
        str(media_path)
    ]
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, text=True,encoding=encoding)
    except UnicodeDecodeError:
        raise UnicodeDecodeError(f"\nError encountered. Please change the encoding parameter to ensure that the function works properly.")

    metadata = json.loads(result.stdout)
    
    # Initialize lists to hold data for each column
    filetypes = []
    file_extensions = []
    languages = []
    durations = []
    
    # Extract stream information
    for stream in metadata.get('streams', []):
        filetypes.append(stream.get('codec_type'))
        file_extensions.append(stream.get('codec_name'))
        # Extract language; note that 'tags' and 'language' might not exist
        language = stream.get('tags', {}).get('language', 'N/A')
        languages.append(language)
    
    # Extract duration from format, if available
    duration = float(metadata.get('format', {}).get('duration', 'N/A')) / 60
    durations = [duration] * len(filetypes)  # Replicate duration for all rows
    
    # Create DataFrame
    info_df = pd.DataFrame({
        'filetype': filetypes,
        'file_extension': file_extensions,
        'language': languages,
        'duration_in_min': durations
    })
    
    return info_df

@beartype
def get_metadata(
        media_path: Path |str
        ,media:Literal["video","audio","subtitle"]
        ,language: None|str = None
        ,file_extension: None|str = None):
    #  not tested
    if language is None:
        language_in = None
    elif not isinstance(language, list):
        language_in = [language]
    else:
        language_in = list(language)
    
    if file_extension is None:
        file_extension_in = None
    elif not isinstance(file_extension, list):
        # remove '.' from the file_extension
        file_extension_in = file_extension.replace('.','')
        file_extension_in = [file_extension_in]
    else:
        file_extension_in = [extension.replace('.','') for extension in file_extension]
    
        
    # requires get_metadata
    media_info = get_all_metadata(media_path)
    
    if language_in:
        if file_extension_in:
            selected_media = media_info.loc[(media_info['filetype'] == media) 
                                            & media_info['language'].isin(language_in)
                                            & media_info['language'].isin(file_extension)
                                            ]
        else:
            selected_media = media_info.loc[(media_info['filetype'] == media) & media_info['language'].isin(language_in)  ]
    else:
        
        if file_extension_in:
            selected_media = media_info.loc[(media_info['filetype'] == media) 
                                            & media_info['language'].isin(file_extension)
                                            ]
        else:
            selected_media = media_info.loc[(media_info['filetype'] == media) ]
            
    return selected_media

@beartype
def _get_media_extension(media_path, media, language = None, file_extension = None
                         ) -> Union[list[int],int, None] :
    # not tested
    # return the unique list of media extension
    # return str if 1 unique extension is found
    selected_media = get_metadata(media_path, media, language = language, file_extension = file_extension)
    # subrip is the same as .srt
    # so I converted to srt
    selected_media.loc[selected_media["file_extension"].isin(["subrip"]),"file_extension"] = "srt"
    unqiue_ext = list(set(selected_media['file_extension'].tolist()))
    
    if len(unqiue_ext) == 0:
        return None
    elif len(unqiue_ext) == 1:
        return unqiue_ext[0]
    else:
        return unqiue_ext

@beartype
def get_video_extension(media_path, file_extension = None):
    return _get_media_extension(media_path,'video')

@beartype
def get_audio_extension(media_path, language = None, file_extension = None):
    return _get_media_extension(media_path,'audio',language)

@beartype
def get_subtitle_extension(media_path, language = None, file_extension = None):
    return _get_media_extension(media_path,'subtitle',language)

@beartype
def _get_media_index(media_path, media, language = None, file_extension = None):
    
    selected_media = get_metadata(media_path, media, language = language, file_extension = file_extension)
    idx_list = selected_media.index.tolist()
    # return None if media is not found
    if len(idx_list) == 0:
        return None
    elif len(idx_list) == 1:
        return idx_list[0]
    else:
        return idx_list

@beartype
def get_video_index(media_path, file_extension = None):
    return _get_media_index(media_path,'video')

@beartype
def get_audio_index(media_path, language = None, file_extension = None):
    return _get_media_index(media_path,'audio',language)

@beartype
def get_subtitle_index(media_path, language = None, file_extension = None):
    return _get_media_index(media_path,'subtitle',language)

@beartype
def extract_subtitle(
        video_folder:     Union[Path,str],
        output_folder:    Union[Path,str],
        video_extension:  Union[list,str] = [".mp4",".mkv"],
        output_extension: Union[list,str] = None,
        overwrite_file:   bool = True,
        n_limit:          int = 150,
        output_prefix:    str = "",
        output_suffix:    str = "",
        languages: List[str] | None = None,
        alarm_done:       bool = True,
):
    input_param = {
        'video_path': 6
    }
    
    _extract_media_setup(
        input_folder = video_folder,
        output_folder = output_folder,
        input_extension = video_extension,
        output_extension = output_extension,
        extract_1_file_func = extract_sub_1_video,
        overwrite_file = overwrite_file,
        n_limit = n_limit,
        output_prefix = output_prefix,
        output_suffix = output_suffix,
        languages=languages,
        alarm_done = alarm_done,
    )

@beartype
def extract_sub_1_video(
    video_path:         Union[str,Path],
    output_folder:      Union[str,Path],
    output_name:        Union[str,Path] = None, 
    output_extension:   Union[str,list] = None,
    alarm_done:         bool = True,
    overwrite_file:     bool = True,
    languages:           Union[str,list, None] = None,
    encoding:str = "utf-8-sig"
                    ):
    # write now language input has to be 3-str letter(BigBang FR)
    # I want to generalize it and work with normal text eg "French" instead of "fre"

    # medium tested
    # ToAdd feature 03: create a suffix for langauge 
    # ToAdd feature 04: generalize it and work with normal text eg "French" instead of "fre"

    # Added 01: extract mutiple subtitles for many languages
    # Added 02: select only some languages to extract
    
    """
    Extract audio from a video file and save it in the specified format.
    
    Parameters:
    -----------
    video_path : str or Path
        The path to the input video file.
        
    output_folder : str or Path
        The folder where the extracted audio file will be saved.
        
    output_name : str
        The name of the output audio file (without extension).
        
    file_extension : str, optional
        The desired file extension for the output audio file (default is ".mp3").
        
    alarm_done : bool, optional
        Whether to play an alarm sound upon successful extraction (default is True).
        
    overwrite_file : bool, optional
        Whether to overwrite the output file if it already exists (default is True).
    
    Returns:
    --------
    bool
        True if audio extraction is successful, False otherwise.
    
    Notes:
    ------
    - Additional feature 1: Output both .wav & .mp3 formats.
    - This function relies on FFmpeg for audio extraction, so make sure FFmpeg is installed.
    - The codec for output format is determined based on the file_extension parameter.
    - An alarm sound is played if alarm_done is set to True upon successful extraction.
    - If the output file already exists and overwrite_file is set to False, the function will return False.
    
    Example:
    --------
    extract_1_audio("input_video.mp4", "output_folder", "output_audio", file_extension=".wav")
    
    """
    import os_toolkit as ost
    from pathlib import Path
    import subprocess
    from playsound import playsound
    import os
    # only input language as str for now
    
    output_folder_in = Path(output_folder)

    video_name = ost.extract_filename(video_path,with_extension=False)
    ori_extension = get_subtitle_extension(video_path,languages)

    if output_extension is None:
        if output_name is None:
            output_name = video_name
        if ori_extension not in output_name:
            if "." not in ori_extension:
                ori_extension = "." + ori_extension
            output_name += ori_extension


    elif isinstance(output_extension, str):

        if output_name is None:
            output_name = video_name

        if output_extension not in output_name:
            
            if "." not in output_extension:
                output_extension = "." + output_extension
            output_name += output_extension
    
    output_path = output_folder_in / output_name
    # if subtitle_stream_index is a list it would create a bug
    subtitle_stream_index = get_subtitle_index(video_path,languages)
    # from extract_1_audio
    # command = [
    #     "ffmpeg",
    #     "-i", str(video_path),
    #     # "-map", "0:a:m:language:por",
    #     "-c:a", codec,
    #     "-q:a", "0",
    #     str(output_path)
    # ]
    subtitle_stream_index_list = list(subtitle_stream_index) if isinstance(subtitle_stream_index, list) else [subtitle_stream_index]

    if output_extension:
        output_ext_no_dot = output_extension.replace('.','')
    else:
        output_ext_no_dot = ori_extension.replace('.','')
    
    for i, sub_index in enumerate(subtitle_stream_index_list):

        curr_output_path = ost.add_suffix_to_name(output_path,i+1)

        command = [
            'ffmpeg',
            '-i', str(video_path),  # Input file
            '-map', f'0:{sub_index}',  # Map the identified subtitle stream
            '-c:s', output_ext_no_dot,  # Subtitle format
            str(curr_output_path)
        ]
        # cmd_line is for debugging
        cmd_line = ' '.join(command)
        
        if os.path.exists(str(curr_output_path)):
            if overwrite_file:
                os.remove(str(curr_output_path))
            else:
                print("The output path is already existed. Please delete the file or set the overwrite parameter to TRUE")
                return False
        try:
            result = subprocess.run(command, text=True, stderr=subprocess.PIPE, encoding=encoding)
        except UnicodeDecodeError:
            raise UnicodeDecodeError(f"\nError encountered. Please change the encoding parameter to ensure that the function works properly.")
    
        if result.returncode != 0:
            print("Error encountered:")
            print(result.stderr)
    
        elif result.returncode == 0:
            # print("Extract audio successfully!!!")
            
            if alarm_done:
                try:
                    playsound(alarm_done_path)
                except:
                    pass

@beartype
def language_name_list():
    import pycountry
    language_names = [lang.name for lang in pycountry.languages if hasattr(lang, 'name')]
    return language_names

@beartype
def closest_language(misspelled_language):
    
    from fuzzywuzzy import process
    import pycountry
    # Get a list of all language names
    language_names = [lang.name for lang in pycountry.languages if hasattr(lang, 'name')]

    # Use fuzzy matching to find the closest match
    closest_match = process.extractOne(misspelled_language, language_names)
    return closest_match[0] if closest_match else None

@beartype
def closest_language_obj(misspelled_language):
    
    """
    Find the closest matching language object for a potentially misspelled language code.
    
    Parameters:
    -----------
    misspelled_language : str
        The potentially misspelled language code.
    
    Returns:
    --------
    langcodes.Language
        A language object representing the closest matching language.
    
    Notes:
    ------
    - This function uses the 'langcodes' library to find the closest matching language object
      for a potentially misspelled language code.
    - It can be useful for language code correction or normalization.
    
    Example:
    --------
    >>> closest_language_obj("englsh")
    <Language('en', 'English')>
    >>> closest_language_obj("español")
    <Language('es', 'Spanish')>
    
    """
    
    
    from langcodes import Language
    correct_language = closest_language(misspelled_language)
    return Language.find(correct_language)

@beartype
def extract_1_audio(video_path:     Union[str,Path],
                    output_folder:  Union[str,Path],
                    output_name:    Union[str,Path], 
                    file_extension: Union[str,list] = ".mp3",
                    alarm_done:     bool = True,
                    overwrite_file: bool = True,
                    encoding='utf-8-sig'
                    ):
    # Additional feature 1: output both .wav & .mp3
    
    
    """
    Extract audio from a video file and save it in the specified format.
    
    Parameters:
    -----------
    video_path : str or Path
        The path to the input video file.
        
    output_folder : str or Path
        The folder where the extracted audio file will be saved.
        
    output_name : str
        The name of the output audio file (without extension).
        
    file_extension : str, optional
        The desired file extension for the output audio file (default is ".mp3").
        
    alarm_done : bool, optional
        Whether to play an alarm sound upon successful extraction (default is True).
        
    overwrite_file : bool, optional
        Whether to overwrite the output file if it already exists (default is True).
    
    Returns:
    --------
    bool
        True if audio extraction is successful, False otherwise.
    
    Notes:
    ------
    - Additional feature 1: Output both .wav & .mp3 formats.
    - This function relies on FFmpeg for audio extraction, so make sure FFmpeg is installed.
    - The codec for output format is determined based on the file_extension parameter.
    - An alarm sound is played if alarm_done is set to True upon successful extraction.
    - If the output file already exists and overwrite_file is set to False, the function will return False.
    
    Example:
    --------
    extract_1_audio("input_video.mp4", "output_folder", "output_audio", file_extension=".wav")
    
    """
    
    from pathlib import Path
    import subprocess
    from playsound import playsound
    import os
    
    
    
    codec = CODEC_DICT[file_extension]
    
    output_folder_in = Path(output_folder)
    
    if isinstance(file_extension, str):
        if file_extension not in output_name:
            
            if "." not in file_extension:
                file_extension = "." + file_extension
            output_name += file_extension
    
    output_path = output_folder_in / output_name
    

    command = [
        "ffmpeg",
        "-i", str(video_path),
        # "-map", "0:a:m:language:por",
        "-c:a", codec,
        "-q:a", "0",
        str(output_path)
    ]
    
    if os.path.exists(str(output_path)):
        if overwrite_file:
            os.remove(str(output_path))
        else:
            print("The output path is already existed. Please delete the file or set the overwrite parameter to TRUE")
            return False
    try:
        result = subprocess.run(command, text=True, stderr=subprocess.PIPE,encoding=encoding)
    except UnicodeDecodeError:
        raise UnicodeDecodeError(f"\nError encountered. Please change the encoding parameter to ensure that the function works properly.")

    if result.returncode != 0:
        print("Error encountered:")
        print(result.stderr)
    
    elif result.returncode == 0:
        print("Extract audio successfully!!!")
        
        if alarm_done:
            playsound(alarm_done_path)



# delete when importing this package
del Union,List,Tuple, Literal, Callable, Dict, Path
del beartype, ost, pkg_resources