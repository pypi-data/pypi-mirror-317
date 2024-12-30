from typing import List, Literal, Dict, Union
from pathlib import Path
from video_toolkit.utils_vt import *
from video_toolkit.sandbox1_vt import *
from whisper.model import Whisper as whisper_model_Whisper
import pkg_resources

# extra import
try:
    import whisper
except ImportError:
    whisper = None

try:
    import faster_whisper
except ImportError:
    faster_whisper = None

 # https://github.com/jianfch/stable-ts
# pip install -U stable-ts
alarm_done_path = pkg_resources.resource_filename(__name__, 'assets/Sound Effect positive-logo-opener.wav')
sound_error_path = pkg_resources.resource_filename(__name__, 'assets/Sound Effect Error.wav')

# based on numba 0.58.0
# whisper 1.1.10
# stable_whisper 2.17.3
# faster-whisper 1.0.3
if whisper is not None:
    def audio_to_sub_1file(
            model:Union[whisper_model_Whisper, faster_whisper.WhisperModel]
            ,audio_path: Union[str,Path]
            ,output_name: Union[str,Path] = ""
            ,output_folder: Union[str,Path] = ""
            ) -> None:
        # medium tested
        # seems to work
        
        # TOADD_01: output subtitle format
        # TOADD_02: (more important but more difficutl) output with maximum of words before spling
        
        """
        signature function that will extract the subtitle from the audio
        """
        # if output_name is "" then default it should use the same name as the audio
        if output_name == "":
            output_name_in = Path(str(audio_path)).stem
        else:
            output_name_in = output_name

        if output_folder == "":
            output_folder_in = Path(str(audio_path)).parent
        else:
            output_folder_in = output_folder

        output_path = Path(str(output_folder_in)) / output_name_in
        
        if isinstance(model, (whisper_model_Whisper)):
            result = model.transcribe(audio_path)
        elif isinstance(model, (faster_whisper.WhisperModel)): 
            result = model.transcribe_stable(audio_path)
        result.to_srt_vtt(str(output_path),word_level =False)

    # NEXT write transcribe_to_subtitle to loop through the audio files and create subtitles
    def audio_to_sub(
        model:Union[whisper_model_Whisper, faster_whisper.WhisperModel]
        ,audio_paths: Union[str,Path]
        ,output_name: Union[str,Path] = ""
        ,output_folder: Union[str,Path] = ""
        ,progress_bar:bool = True
        ,verbose:int = 1
        ,alarm_done:bool = True
        ,alarm_error:bool = True
        ,input_extension:Union[List[str],str] = [".mp3",".wav"]
        ) -> None:
        # list of files is not supported
        """
        audio_path could be folder_path, single_file, or list of files


        """
        import os_toolkit as ost
        from tqdm import tqdm

        # alarm_done_path = r"H:\D_Music\Sound Effect positive-logo-opener.mp3"


        if ost.is_folder_path(audio_paths):
            audio_full_paths = ost.get_full_filename(audio_paths,extension = input_extension)
            audio_name_paths = ost.get_filename(audio_paths,extension = input_extension)
            if progress_bar:
                loop_obj = tqdm( enumerate(audio_full_paths), total = len(audio_full_paths))
            else:
                loop_obj = enumerate(audio_full_paths)

            for i, path in loop_obj:
                audio_to_sub_1file(model,path,output_name = output_name,output_folder = output_folder)
                if verbose >= 1:
                    print(f"{audio_name_paths[i]} done!!")
                
            if alarm_done:
                try:
                    play_audio(alarm_done_path)
                except:
                    pass
        elif isinstance(audio_paths,list):
            for i in range(len(audio_paths)):
                audio_to_sub_1file(model,audio_paths[i],output_name = output_name,output_folder = output_folder)
                if alarm_done:
                    try:
                        play_audio(alarm_done_path)
                    except:
                        pass
            # raise NotImplementedError(f"list of files is not supported")
        elif isinstance(audio_paths,(str,Path)):
            audio_to_sub_1file(model,audio_paths,output_name = output_name,output_folder = output_folder)
            if alarm_done:
                try:
                    play_audio(alarm_done_path)
                except:
                    pass
del pkg_resources