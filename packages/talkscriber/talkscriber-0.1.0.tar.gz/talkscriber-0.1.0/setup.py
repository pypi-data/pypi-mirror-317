from setuptools import setup, find_packages

setup(
    name="talkscriber",
    version="0.1.0",
    author="Talkscriber",
    author_email="info@talkscriber.com",
    description="A short description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Talkscriber/ts-client",
    packages=find_packages(),  # Automatically find sub-packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.22.3,<1.23.0",
        #"numpy>1.23.0",
        "ffmpeg-python==0.2.0",
        "future==0.18.3",
        "mkl-fft==1.3.1",
        "mkl-random==1.2.2",
        "mkl-service==2.4.0",
        "numpy==1.26.4",
        "PyAudio==0.2.11",
        "scipy==1.12.0",
        "websocket-client==1.6.0",    
        ],
)
