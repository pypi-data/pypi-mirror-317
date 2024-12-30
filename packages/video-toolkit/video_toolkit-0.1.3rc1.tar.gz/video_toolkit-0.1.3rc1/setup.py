from setuptools import setup, find_packages
# status: published online
setup(
    author= "Dear Norathee",
    description="package to help you with extraction of video information eg audio, subtitle",
    name="video_toolkit",
    version="0.1.3rc1",
    packages=find_packages(),
    license="MIT",
    install_requires=[
        "os_toolkit>=0.1.1",
        "dataframe_short>=0.1.6",
        "python_wizard>=0.1.2",
        "inspect_py>=0.1.1",
        "py_string_tool>=0.1.3",

        "pandas",
                      
        "seaborn",
        "pysrt",
        "pydub",
        "playsound",
        "tqdm",
        "pycountry",
        "lingtrain_aligner",
        "ffmpeg",
        "fuzzywuzzy",
        "pysubs2",
        "beartype"
                      
                      ],
    python_requires='>=3.10.0',
    extras_require={
        'full': ['torch>=1.0']  # Optional torch dependency
    },
    

)