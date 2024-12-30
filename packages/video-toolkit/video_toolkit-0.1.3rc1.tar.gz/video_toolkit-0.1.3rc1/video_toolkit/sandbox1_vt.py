from typing import Literal,Union,List, Tuple
from pathlib import Path

def play_audio(audio_path:Union[Path,str],
               engine:Literal["auto","simpleaudio","pydub","playsound"] = "auto") -> None:
    """
    
    provided user with multiple option of packages for playing audio

    Parameters
    ----------
    audio_path : Union[Path,str]
        DESCRIPTION.
    engine : Literal["auto","simpleaudio","pydub","playsound"], optional
        DESCRIPTION. The default is "auto".

    Returns
    -------
    None.

    """
    
    from playsound import playsound
    import simpleaudio as sa
    from pydub import AudioSegment
    from pydub.playback import play
    
    try:
        audio = AudioSegment.from_mp3(str(audio_path))
    except:
        pass

    try:
        wave_obj = sa.WaveObject.from_wave_file(str(audio_path))
    except:
        pass
    
    
    if engine in ["auto"]:
        try:
            # playsound
            playsound(str(audio_path))
        except:
            try:
                # simpleaudio
                play_obj = wave_obj.play()
            except:
                # pydub
                play(audio)
                
    elif engine in ["simpleaudio"]:
        play_obj = wave_obj.play()
    elif engine in ["pydub"]:
        play(audio)
    elif engine in ["playsound"]:
        playsound(str(audio_path))

del Literal,Union,List, Tuple