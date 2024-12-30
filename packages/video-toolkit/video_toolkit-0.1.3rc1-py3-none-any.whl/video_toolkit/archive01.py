from typing import Union,List,Tuple, Literal, Callable, Dict
from pathlib import Path

def extract_audio2(
        video_folder:     Union[Path,str],
        output_folder:    Union[Path,str],
        video_extension:  Union[list,str] = [".mp4",".mkv"],
        output_extension: Union[list,str] = ".mp3",
        overwrite_file:   bool = True,
        n_limit:          int = 150,
        output_prefix:    str = "",
        output_suffix:    str = "",
        alarm_done:       bool = True,
):
    """
    the diff between 
    extract_audio1 - use manually code to loop through folder
    extract_audio2 - powered by _extract_media_setup while 
    extract_audio3 - use extract_audio_1file as a base(which is more general than extract_audio1 & extract_audio2), but need more testing to see if it works
    
    # after testing I would then rename extract_audio3 to just extract_audio
    
    """
    input_param = {
        'video_path': 6
    }

    _extract_media_setup(
        input_folder = video_folder,
        output_folder = output_folder,
        input_extension = video_extension,
        output_extension = output_extension,
        extract_1_file_func = extract_1_audio,
        overwrite_file = overwrite_file,
        n_limit = n_limit,
        output_prefix = output_prefix,
        output_suffix = output_suffix,
        alarm_done = alarm_done,
    )


def extract_audio1(video_folder:     Union[Path,str],
                  output_folder:    Union[Path,str],
                  video_extension:  Union[list,str] = [".mp4",".mkv"],
                  output_extension: Union[list,str] = ".mp3",
                  output_prefix:    str = "",
                  output_suffix:    str = "",
                  alarm_done:       bool = True,
                  overwrite_file:   bool = True,
                  n_limit:          int = 150
                  ):
    # TODO 
    # add feature: support multiple languages
    # support multiple output eg [.wav,.mp3,.eac3]
    
    """

    the diff between 
    extract_audio1 - use manually code to loop through folder
    extract_audio2 - powered by _extract_media_setup while 
    extract_audio3 - use extract_audio_1file as a base(which is more general than extract_audio1 & extract_audio2), but need more testing to see if it works

    Extracts audio from video files in the specified `video_folder` and saves them in the `output_folder` in the specified audio format.
    
    Parameters
    ----------
    video_folder : Union[Path, str]
        The path to the folder containing video files.
        
    output_folder : Union[Path, str]
        The path where extracted audio files will be saved.
        
    video_extension : Union[list, str], optional
        List of video file extensions to consider for extraction. Defaults to [".mp4", ".mkv"].
        
    output_extension : Union[list, str], optional
        The audio file extension for the output files. Defaults to ".mp3".
        
    output_prefix : str, optional
        A prefix to be added to the output audio file names. Defaults to an empty string.
        
    output_suffix : str, optional
        A suffix to be added to the output audio file names. Defaults to an empty string.
        
    alarm_done : bool, optional
        Whether to play an alarm sound when the extraction is completed. Defaults to True.
        
    overwrite_file : bool, optional
        Whether to overwrite existing audio files with the same name in the `output_folder`. Defaults to True.
        
    n_limit : int, optional
        The maximum number of video files to process. Defaults to 150.
        
    Returns
    -------
    """
    
    import sys
    from pathlib import Path
    from playsound import playsound
    
    from time import time
    ts01 = time()
    
    
    import os_toolkit as ost
    import python_wizard as pw
    
    codec_dict = {'.mp3': "libmp3lame",
                  'mp3' : "libmp3lame",
                  '.wav': "pcm_s24le",
                  'wav' : "pcm_s24le"
                  }
    
    output_extension = [output_extension]
    output_extension_in = []
    
    # add . to extension in case it doesn't have .
    for extension in output_extension:
        if not "." in extension:
            output_extension_in.append("."+extension)
        else:
            output_extension_in.append(extension)
    
    video_name_list_ext = ost.get_filename(video_folder,video_extension)
    video_path_list = ost.get_full_filename(video_folder,video_extension)
    
    n_file = min(len(video_name_list_ext),n_limit)
    video_name_list_ext = video_name_list_ext[:n_file]
    video_path_list = video_path_list[:n_file]
    
    video_name_list = [filename.split('.')[0] for filename in video_name_list_ext]
    
    for i, video_name in enumerate(video_name_list):
        
            
        output_name = output_prefix + video_name_list[i] + output_suffix
        # original_stdout = sys.stdout
        # sys.stdout = open('nul', 'w') 
        
        for i, extension in enumerate(output_extension_in):
            extract_1_audio(
                video_path = video_path_list[i],
                output_folder = output_folder,
                output_name = output_name,
                file_extension = extension,
                alarm_done=False,
                overwrite_file=overwrite_file)
        
        # sys.stdout = original_stdout
        
    if alarm_done:
        playsound(alarm_done_path)
    ts02 = time()
    duration = ts02-ts01
    pw.print_time(duration)
    
    return video_name_list

del Union,List,Tuple, Literal, Callable, Dict, Path