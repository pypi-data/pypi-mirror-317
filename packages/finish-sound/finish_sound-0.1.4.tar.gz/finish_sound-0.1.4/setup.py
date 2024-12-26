from setuptools import setup, find_packages

setup(
    name="finish-sound",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[ 
        "playsound>=1.2.2", 
        "pygame>=2.0.1",     
        "pydub>=0.25.1",     
        "IPython>=7.0",      
    ],
    description="A simple package that plays a sound when code finishes running",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/kentjliu/finish-sound",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    package_data={
        "finish_sound": ["sounds/*.mp3"], 
    },
)
