from setuptools import setup, find_packages

setup(
    name="fast-whisper-diarizer",
    version="0.1.0",
    author='Salim',
    author_email='salimkt25@gmail.com',
    packages=find_packages(where="."),
    package_dir={"": "."},
    install_requires=[
        'faster-whisper>=1.1.0',
        'ctranslate2==4.4.0',
        'nemo-toolkit[asr]>=2.dev',
        'torch',
        'torchaudio',
        'omegaconf',
        'nltk',
        'wget',
        'deepmultilingualpunctuation'
    ],
    entry_points={
        'console_scripts': [
            'whisper-diarize=main:main',
        ],
    }
)
