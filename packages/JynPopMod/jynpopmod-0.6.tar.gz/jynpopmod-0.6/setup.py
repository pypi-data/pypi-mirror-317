from setuptools import setup, find_packages

setup(
    name='JynPopMod',
    version='0.6',
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyperclip",
        "pyttsx3",
        "SpeechRecognition",  # Matches the package name for speech_recognition
        "psutil",
        "mouse",
        "pyautogui",
        "better_profanity",
    ],
    author='Jynoqtra',
    author_email='Jynoqtra@gmail.com',
    description='JynPopMod Python Module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Jynoqtra/JynPopMod',
    classifiers=[  
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Intended Audience :: Developers',
    ],
)
