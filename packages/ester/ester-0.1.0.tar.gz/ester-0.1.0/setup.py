from setuptools import setup, find_packages

setup(
    name="ester",
    version="0.1.0",
    author="Your Name",
    author_email="your_email@example.com",
    description="A voice assistant package similar to Jarvis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ester",
    packages=find_packages(),
    install_requires=[
        "speechrecognition",
        "pyttsx3",
        "requests",
        "pyaudio",
        # Add other dependencies
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)