from setuptools import setup, find_packages

setup(
    name='JynPopMod',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'requests',
        'pyperclip',
        'pyttsx3',
        'speechrecognition',
        'psutil',
        'pyautogui'
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
