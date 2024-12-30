# imported from "C:\Users\Heng2020\OneDrive\Python NLP\NLP 06_ffmpeg\ffmpeg_01.py"
from typing import Union,List,Tuple, Literal, Callable
from pathlib import Path
import sys

import python_wizard as pw
import os_toolkit as ost
import dataframe_short as ds

import pandas as pd
import seaborn as sns

# v02 => add extract_audio2, extract_subtitle, _extract_media_setup,extract_sub_1_video
# get_metadata2, get_all_metadata, get_metadata
# get_subtitle_index,get_audio_index,get_video_index,_get_media_index,get_subtitle_extension,
# get_audio_extension,get_video_extension, _get_media_extension


def make_1_season_Excel_unaligned(EN_folder_path: Union[str,Path],
                                  PT_folder_path: Union[str,Path], 
                                  out_excel_name: Union[str,Path],
                                  output_folder = None,
                                  drop_timestamp = True,
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
    
    sys.path.append(r'C:\Users\Heng2020\OneDrive\Python MyLib\Python MyLib 01\02 DataFrame')
    sys.path.append(r'C:\Users\Heng2020\OneDrive\Python MyLib\Python MyLib 01\06 General Python')
    sys.path.append(r'C:\Users\Heng2020\OneDrive\Python MyLib\Python MyLib 01\09 NLP_lib')
    sys.path.append(r'C:\Users\Heng2020\OneDrive\Python MyLib\Python MyLib 01\10 OS')
    
    import lib02_dataframe as ds
    import video_tools as vt
    import python_wizard01 as pw
    import os_01 as ost
    
    en_df = vt.combine_files_1_season(str(EN_folder_path))
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



    pt_df = vt.combine_files_1_season(str(PT_folder_path))
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


    out_df = ds.indexAlignedAppend(en_df_filter,pt_df_filter,"Episode")
    out_df = out_df.reset_index(drop = True)
    out_df.index = out_df.index + 1
    # keep only the first occurrence of each column (Episode is duplicated)
    out_df = out_df.loc[:, ~out_df.columns.duplicated()]
    
    # automatically add .xlsx extension to the file 
    out_excel_name_in = out_excel_name if ".xlsx" in out_excel_name else (out_excel_name + ".xlsx")
    
    ds.pd_move_col_front(out_df, "Episode")
    
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

def read_sentences_from_excel(file_path, sheet_name, portuguese_col, english_col, nrows=None):
    # imported from NLP 09_SenMem Pipeline
    """
    Reads Portuguese and English sentences from an Excel file.
    
    :param file_path: Path to the Excel file.
    :param sheet_name: Name of the sheet containing the sentences.
    :param portuguese_col: Column letter for Portuguese sentences.
    :param english_col: Column letter for English sentences.
    :return: Tuple of two lists containing Portuguese and English sentences.
    """

    df = ds.pd_read_excel(file_path,sheet_name=sheet_name,nrows=nrows,usecols=[portuguese_col,english_col])

    portuguese_sentences = df.iloc[:,0].tolist()
    english_sentences = df.iloc[:,1].tolist()


    return portuguese_sentences, english_sentences

    
def read_movie_script2(file_path, sheet_name = "Sheet1", portuguese_col = 0, english_col = 1):
    # imported from NLP 09_SenMem Pipeline
    # middle tested 
    # dependency: pd_by_column, pd_split_into_dict_df, pd_regex_index
    # work with format that use title to seperate the episode
    import pandas as pd
    import re
    from openpyxl.utils import column_index_from_string
    
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
    
    data_ori = ds.pd_read_excel(file_path, sheet_name=sheet_name)
    # playsound(alarm_path)
    
    data = ds.pd_by_column(data_ori,[portuguese_col_no, english_col_no])
    

    # Function to check if a cell value matches the episode identifier pattern (e.g., S01E01)
    # r'[Ss]\d{2}[Ee]\d{2}' => S01E01
    df_dict = ds.pd_split_into_dict_df(data,r'[Ss]\d{2}[Ee]\d{2}',0)
    # df_dict = pd_split_into_dict_df(data,index_list=episode_start_indices)
    return df_dict


def read_movie_script(file_path, sheet_name, portuguese_col, english_col):
    # the main function that I should use from now on
    # imported from NLP 09_SenMem Pipeline
    from openpyxl.utils import column_index_from_string
    df = ds.pd_read_excel(file_path, sheet_name=sheet_name)
    # df = pd_by_column(df_ori, [portuguese_col,english_col])
    import pandas as pd
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
        content_df = ds.pd_by_column(group, [portuguese_col_no, english_col_no]).reset_index(drop=True)
        
        # Append season, episode, and content DataFrame to the list
        data.append({'season': season, 'episode': episode, 'content': content_df})
    
    # Convert the list to a DataFrame
    new_df = pd.DataFrame(data)
    
    # Set 'season' and 'episode' as the index
    new_df.set_index(['season', 'episode'], inplace=True)
    
    return new_df


def align_1_season(excel_1_season_script,
                   out_excel_name: Union[str,Path],
                   output_folder = None,
                   sheet_name = 'Sheet1',
                   
                   n_episodes: Union[str,int] = "all",
                   portuguese_col = "F",
                   english_col = "D",
                   lang_from="PT",
                   lang_to="EN",
                   alarm = True,
                   alarm_path = r"H:\D_Music\Sound Effect positive-logo-opener.mp3",
                   
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
            episode_aligned = sen_alignment_df(single_episode,lang_from=lang_from,lang_to=lang_to,alarm = False)
    
            episode_aligned.index = episode_aligned.index + 1
            episode_aligned['sentence_' + lang_from  ] = episode_aligned[lang_from]
            episode_aligned['sentence_' + lang_to  ] = episode_aligned[lang_to]
            
            episode_aligned = episode_aligned.drop(columns = [lang_from,lang_to])
            
            episode_aligned['Season'] =  season
            episode_aligned['Episode'] =  episode
            episode_aligned = episode_aligned.drop_duplicates(subset=['sentence_' + lang_from ,'sentence_' + lang_to])
            ds.move_col_front(episode_aligned, ['Season','Episode'])
            # drop rows that are empty
            episode_aligned = episode_aligned.dropna(subset = ['sentence_' + lang_from] )
            
            season_aligned = pd.concat([season_aligned,episode_aligned])
            print(f"{episode_str} Done Aligning !!! ----------------------------------------")
        except:
            print(f"Error at {episode_str} was found !!! ########################")
            error_episode.append(episode_str)
        
        i += 1
            
    out_excel_name_in = out_excel_name if ".xlsx" in out_excel_name else (out_excel_name + ".xlsx")
    
    
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
    if alarm:
        playsound(alarm_path)
    
    return season_aligned


def sen_alignment_df(df, lang_from = None, lang_to = None,
                       alarm = True,
                       alarm_path = r"H:\D_Music\Sound Effect positive-logo-opener.mp3",
                     ):
    # medium tested
    if lang_from is None: lang_from = df.columns[0]
    if lang_to is None: lang_to = df.columns[1]
    
    text_list_from = df.iloc[:, 0].tolist()
    text_list_to = df.iloc[:, 1].tolist()
    # assume that text from is
    result = sentence_alignment(text_list_from,text_list_to,lang_from,lang_to,alarm=alarm,alarm_path=alarm_path)
    
    return result
    

def sentence_alignment(text_from,text_to, lang_from = "pt", lang_to = "en",
                       alarm = True,
                       alarm_path = r"H:\D_Music\Sound Effect positive-logo-opener.mp3",
                       
                       ):
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
    
    if alarm:
        playsound(alarm_path)
    
    return paragraph_result


def combine_files_1_season(folder_path):
    from functools import partial
    import sys
    sys.path.append(r'C:\Users\Heng2020\OneDrive\Python MyLib\Python MyLib 01\02 DataFrame')
    
    import lib02_dataframe as ds
    
    func = partial(ds.combine_files_to_df, 
                   extract_pattern = r'S\d+E\d+',
                   filename_col_name = "Episode",
                   )
    out_df = func(folder_path)
    out_df.columns.values[1] = 'NoSentence'
    return out_df


def get_metadata2(media_path):
    import subprocess
    import json
    # 80% from GPT4
    """
    Get the index of the first subtitle stream in the video file.
    
    Parameters:
    - video_path: Path to the input video file.
    
    Returns:
    - Index of the first subtitle stream, or None if no subtitle stream is found.
    """
    command = [
        'ffprobe',
        '-v', 'quiet',
        '-show_streams',
        media_path
    ]
    
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, text=True)
    streams_info_raw = json.loads(result.stdout)
    
    streams_info = [stream for stream  in streams_info_raw['streams']]

    
    return streams_info

def get_all_metadata(media_path):
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
        media_path
    ]
    
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, text=True)
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

def get_metadata(media_path, media, language = None, file_extension = None):
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

def get_video_extension(media_path, file_extension = None):
    return _get_media_extension(media_path,'video')

def get_audio_extension(media_path, language = None, file_extension = None):
    return _get_media_extension(media_path,'audio',language)

def get_subtitle_extension(media_path, language = None, file_extension = None):
    return _get_media_extension(media_path,'subtitle',language)


def _get_media_index(media_path, media, language = None, file_extension = None):
    
    selected_media = get_metadata(media_path, media, language = None, file_extension = None)
    idx_list = selected_media.index.tolist()
    # return None if media is not found
    if len(idx_list) == 0:
        return None
    elif len(idx_list) == 1:
        return idx_list[0]
    else:
        return idx_list

def get_video_index(media_path, file_extension = None):
    return _get_media_index(media_path,'video')

def get_audio_index(media_path, language = None, file_extension = None):
    return _get_media_index(media_path,'audio',language)

def get_subtitle_index(media_path, language = None, file_extension = None):
    return _get_media_index(media_path,'subtitle',language)



def extract_audio2(
        video_folder:     Union[Path,str],
        output_folder:    Union[Path,str],
        video_extension:  Union[list,str] = [".mp4",".mkv"],
        output_extension: Union[list,str] = ".mp3",
        overwrite_file:   bool = True,
        n_limit:          int = 150,
        output_prefix:    str = "",
        output_suffix:    str = "",
        play_alarm:       bool = True,
        alarm_done_path:str = r"H:\D_Music\Sound Effect positive-logo-opener.mp3"
):
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
        play_alarm = play_alarm,
        alarm_done_path = alarm_done_path,
    )

def extract_subtitle(
        video_folder:     Union[Path,str],
        output_folder:    Union[Path,str],
        video_extension:  Union[list,str] = [".mp4",".mkv"],
        output_extension: Union[list,str] = None,
        overwrite_file:   bool = True,
        n_limit:          int = 150,
        output_prefix:    str = "",
        output_suffix:    str = "",
        play_alarm:       bool = True,
        alarm_done_path:str = r"H:\D_Music\Sound Effect positive-logo-opener.mp3"
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
        play_alarm = play_alarm,
        alarm_done_path = alarm_done_path,
    )

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
        play_alarm: bool = True,
        alarm_done_path:str = r"H:\D_Music\Sound Effect positive-logo-opener.mp3"
):
    """

    helper function to reduce code redundancy
    it would setup which/ how many files should be extracted in inputs
    how many files should be created in output 


    """
    import sys
    from pathlib import Path
    from playsound import playsound
    from time import time, perf_counter
    import inspect_py as inp
    sys.path.append(r'C:\Users\Heng2020\OneDrive\Python MyLib\Python MyLib 01\08 Other')
    import lib08_Other as pw

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

    for i, filename in enumerate(filename_list):
        
            
        output_name = output_prefix + filename_list[i] + output_suffix
        # original_stdout = sys.stdout
        # sys.stdout = open('nul', 'w')
         
        # the problem here is that the input parameter name in extract_1_file_func
        # could be different and 

        for j, extension in enumerate(output_extension_in):
            # input_dict = {
            #     input_param_name[0]:path_list[i],
            #     input_param_name[1]:extension,
            # }
            extract_1_file_func(
                video_path = path_list[i],
                output_extension = extension,
                output_folder = output_folder,
                output_name = output_name,
                play_alarm=False,
                overwrite_file=overwrite_file)
            print(f"extracted {output_name} successfully!!!")
        
        # sys.stdout = original_stdout
    if play_alarm:
        playsound(alarm_done_path)
    ts02 = time()
    duration = ts02-ts01
    pw.print_time(duration)
    print()
    return filename_list

def extract_sub_1_video(
    video_path:         Union[str,Path],
    output_folder:      Union[str,Path],
    output_name:        Union[str,Path] = None, 
    output_extension:   Union[str,list] = None,
    play_alarm:         bool = True,
    overwrite_file:     bool = True,
    language:           Union[str,list, None] = None,
    alarm_done_path:    str = r"H:\D_Music\Sound Effect positive-logo-opener.mp3"
                    ):
    # medium tested
    # ToAdd feature 01: extract mutiple subtitles for many languages
    # ToAdd feature 02: select only some languages to extract
    
    
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
        
    play_alarm : bool, optional
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
    - An alarm sound is played if play_alarm is set to True upon successful extraction.
    - If the output file already exists and overwrite_file is set to False, the function will return False.
    
    Example:
    --------
    extract_1_audio("input_video.mp4", "output_folder", "output_audio", file_extension=".wav")
    
    """
    
    from pathlib import Path
    import subprocess
    from playsound import playsound
    import os
    # only input language as str for now
    
    output_folder_in = Path(output_folder)

    video_name = ost.extract_filename(video_path,with_extension=False)
    ori_extension = get_subtitle_extension(video_path,language)

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
    
    subtitle_stream_index = get_subtitle_index(video_path,language)
    # from extract_1_audio
    # command = [
    #     "ffmpeg",
    #     "-i", str(video_path),
    #     # "-map", "0:a:m:language:por",
    #     "-c:a", codec,
    #     "-q:a", "0",
    #     str(output_path)
    # ]
    if output_extension:
        output_ext_no_dot = output_extension.replace('.','')
    else:
        output_ext_no_dot = ori_extension.replace('.','')
    command = [
        'ffmpeg',
        '-i', str(video_path),  # Input file
        '-map', f'0:{subtitle_stream_index}',  # Map the identified subtitle stream
        '-c:s', output_ext_no_dot,  # Subtitle format
        str(output_path)
    ]
    # cmd_line is for debugging
    cmd_line = ' '.join(command)
    
    if os.path.exists(str(output_path)):
        if overwrite_file:
            os.remove(str(output_path))
        else:
            print("The output path is already existed. Please delete the file or set the overwrite parameter to TRUE")
            return False
    result = subprocess.run(command, text=True, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        print("Error encountered:")
        print(result.stderr)
    
    elif result.returncode == 0:
        # print("Extract audio successfully!!!")
        
        if play_alarm:
            playsound(alarm_done_path)



def crop_video(
        video_path: str, 
        t_start: str, 
        t_end: str, 
        time_slice: List[Tuple[str, str]],
        output_extension: Literal["mp3", ".mp3",".mp4","mp4","mkv",".mkv","wav",".wav"] = None,
        play_alarm = True
        ):
    # tested only input(mkv) => output(mkv)
    import subprocess
    import os
    from playsound import playsound
    
    
    alarm_done_path = r"H:\D_Music\Sound Effect positive-logo-opener.mp3"
    
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
        
        if play_alarm:
            playsound(alarm_done_path)
    
    return output_path  # Return the output file path



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


def closest_language(misspelled_language):
    
    from fuzzywuzzy import process
    import pycountry
    # Get a list of all language names
    language_names = [lang.name for lang in pycountry.languages if hasattr(lang, 'name')]

    # Use fuzzy matching to find the closest match
    closest_match = process.extractOne(misspelled_language, language_names)
    return closest_match[0] if closest_match else None

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
    
def extract_1_audio(video_path:     Union[str,Path],
                    output_folder:  Union[str,Path],
                    output_name:    Union[str,Path], 
                    file_extension: Union[str,list] = ".mp3",
                    play_alarm:     bool = True,
                    overwrite_file: bool = True
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
        
    play_alarm : bool, optional
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
    - An alarm sound is played if play_alarm is set to True upon successful extraction.
    - If the output file already exists and overwrite_file is set to False, the function will return False.
    
    Example:
    --------
    extract_1_audio("input_video.mp4", "output_folder", "output_audio", file_extension=".wav")
    
    """
    
    from pathlib import Path
    import subprocess
    from playsound import playsound
    import os
    
    codec_dict = {'.mp3': "libmp3lame",
                  'mp3' : "libmp3lame",
                  '.wav': "pcm_s24le",
                  'wav' : "pcm_s24le"
                  }
    
    codec = codec_dict[file_extension]
    
    output_folder_in = Path(output_folder)
    
    if isinstance(file_extension, str):
        if file_extension not in output_name:
            
            if "." not in file_extension:
                file_extension = "." + file_extension
            output_name += file_extension
    
    output_path = output_folder / output_name
    
    alarm_done_path = r"H:\D_Music\Sound Effect positive-logo-opener.mp3"
    
    
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
    result = subprocess.run(command, text=True, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        print("Error encountered:")
        print(result.stderr)
    
    elif result.returncode == 0:
        print("Extract audio successfully!!!")
        
        if play_alarm:
            playsound(alarm_done_path)

def extract_audio(video_folder:     Union[Path,str],
                  output_folder:    Union[Path,str],
                  video_extension:  Union[list,str] = [".mp4",".mkv"],
                  output_extension: Union[list,str] = ".mp3",
                  output_prefix:    str = "",
                  output_suffix:    str = "",
                  play_alarm:       bool = True,
                  overwrite_file:   bool = True,
                  n_limit:          int = 150
                  ):
    # TODO 
    # add feature: support multiple languages
    # support multiple output eg [.wav,.mp3,.eac3]
    
    """
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
        
    play_alarm : bool, optional
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
    
    alarm_done_path = r"H:\D_Music\Sound Effect positive-logo-opener.mp3"
    
    sys.path.append(r"C:\Users\Heng2020\OneDrive\Python MyLib")
    import lib08_SrtToCsv as f8
    import lib08_Other as f9
    
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
    
    video_name_list_ext = f8.get_filename(video_folder,video_extension)
    video_path_list = f8.get_full_filename(video_folder,video_extension)
    
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
                play_alarm=False,
                overwrite_file=overwrite_file)
        
        # sys.stdout = original_stdout
        
    if play_alarm:
        playsound(alarm_done_path)
    ts02 = time()
    duration = ts02-ts01
    f9.print_time(duration)
    
    return video_name_list
       

def test_extract_1_audio():
    
    folder = Path(r"E:\Videos\The Big Bang Theory\The Big Bang Theory French Season 06")
    video_name = "The Big Bang Theory French S06E01.mp4"
    video_path = folder / video_name
    output_folder = Path(r"C:\Users\Heng2020\OneDrive\Python NLP\NLP 06_ffmpeg")
    output_name = "The Big Bang Theory French S06E01.mp3"
    output_path = output_folder / output_name
    
    extract_1_audio(video_path,output_folder,output_name)
    extract_1_audio(video_path,output_folder,output_name,overwrite_file = False)

def test_extract_audio():
    
    from pathlib import Path
    French_bigbang = Path(r"E:\Videos\The Big Bang Theory\The Big Bang Theory French Season 06")
    output_folder = Path(r"E:\Videos\The Big Bang Theory\The Big Bang Theory French Season 06\Audio")
    extract_audio(French_bigbang,output_folder,n_limit=10)
    return True

def test_crop_video():
    from pathlib import Path
    video_path = r"C:\Users\Heng2020\OneDrive\Python NLP\InputData\Westworld S04E01 Portuguese.mkv"
    t1 = "0:02:25"
    t2 = "0:06:00"
    
    crop_video(video_path,t1,t2)

def test_create_subtitle():
    import whisper
    from whisper.utils import get_writer
    from playsound import playsound
    from time import time
    
    alarm_done_path = r"H:\D_Music\Sound Effect positive-logo-opener.mp3"
    
    ts01 = time()
    
    input_path = r"C:\Users\Heng2020\OneDrive\Python NLP\InputData\Westworld S04E01 Portuguese_01.mkv"
    
    model = whisper.load_model("base")
    result = model.transcribe(input_path)
    
    output_directory = r"C:\Users\Heng2020\OneDrive\Python NLP\InputData\Westworld S04E01 Portuguese_01.srt"
    
    writer = get_writer("srt", str(output_directory))
    writer(result, output_name)
    ts02 = time()
    
    duration = ts02 - ts01 
    print(duration)


def srt_to_df(srt_path,
              remove_stopwords=True,
              stopwords = ["♪","\n","<i>","</i>","<b>","</b>"]):
# remove_newline will remove '\n' from the extracted text
    import pysrt
    import pandas as pd
    if ".srt" in srt_path:
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
            sentences = [St_replace(sentence,stopwords,"") for sentence in sentences]
        df = pd.DataFrame({
            'sentence': sentences,
            'start': start_times,
            'end': end_times
        })
        return df
    else:
        # many srt's file using folder
        str_file_names = get_full_filename(srt_path,".srt")
        df_list = []
        for str_file_name in str_file_names:
            each_df = srt_to_df(str_file_name)
            df_list.append(each_df)
        return df_list


def srt_to_csv(srt_path,output_path,encoding='utf-8-sig',index=False):
    # output should be total_path
    df_sub = srt_to_df(srt_path)
    # encoding='utf-8-sig' for Portuguese
    df_sub.to_csv(output_path, encoding=encoding,index=index)

def srt_to_Excel(srt_path,output_path,encoding='utf-8-sig',index=True):
    import pandas as pd
    import os
    """ 
    Wrote on Aug 27, 2023
    I already wrote it for 1 file but it took me about 3 additional hrs to 
    make it work with multiple files in folder
    """
    # output should be total_path
    df_sub = srt_to_df(srt_path)
    pd_ver = pw.package_version("pandas")
    
    if isinstance(df_sub,pd.DataFrame):
    # encoding='utf-8-sig' for Portuguese
        if pd_ver < (2,0,0):
            df_sub.to_excel(output_path, encoding=encoding,index=index)
        else:
            df_sub.to_excel(output_path, index=index)
            
    elif isinstance(df_sub,list):
        short_names = get_filename(srt_path,".srt")
        out_full_name = [os.path.join(output_path,short_name).replace(".srt",".xlsx") for short_name in short_names]
        
        if pd_ver < (2,0,0):
            df_sub.to_excel(output_path, encoding=encoding,index=index)
            for i,df in enumerate(df_sub):
                df.to_excel(out_full_name[i], encoding=encoding,index=index)
                
        else:
            for i,df in enumerate(df_sub):
                df.to_excel(out_full_name[i], index=index)

def to_ms(time_obj):
    time_obj_ms = (time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second) * 1000 + time_obj.microsecond // 1000
    return time_obj_ms

def get_filename(folder_path,extension = "all"):
    # also include "folder"  case
# tested small
# new feature1: include subfolders
    import os
    if extension == "all":
        out_list = [ file for file in os.listdir(folder_path) ]

    elif isinstance(extension,str):
        extension_temp = [extension]

        out_list = []

        for file in os.listdir(folder_path):
            if "." in file:
                file_extension = file.split('.')[-1]
                for each_extention in extension_temp:
                    # support when it's ".csv" or only "csv"
                    if file_extension in each_extention:
                        out_list.append(file)
            elif extension == "folder":
                out_list.append(file)


    elif isinstance(extension,list):
        out_list = []
        for file in os.listdir(folder_path):

            if "." in file:
                file_extension = file.split('.')[-1]
                for each_extention in extension:
                    # support when it's ".csv" or only "csv"
                    if file_extension in each_extention:
                        out_list.append(file)

            elif "folder" in extension:
                out_list.append(file)

        return out_list

    else:
        print("Don't support this dataype for extension: please input only string or list")
        return False

    return out_list

def get_full_filename(folder_path,extension = "all"):
    # tested small
    import os 
    short_names = get_filename(folder_path,extension)
    out_list = []
    for short_name in short_names:
        full_name = os.path.join(folder_path,short_name)
        out_list.append(full_name)
    return out_list

def St_replace(text,to_replace,replace_by):
    # unit_tested
    for word in to_replace:
        new_text = text.replace(word, replace_by)
        
    return new_text

# TODO: srt_to_Excel => similar to srt_to_csv but output as excel
# srt_to_Excel(srt_path,sub_output)

# n_file = len(srt_to_df(srt_folder_path))
# srt_to_Excel(srt_folder_path,output_folder)

# print(f"Done converting srt to Excel in Total {n_file} files ")
# playsound(alarm_path)




