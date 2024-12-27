from setuptools import setup, find_packages

setup(
    name='syncv',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'pyperclip',
        'keyboard',
        'requests',
        'flask',
        'pynput'
    ],
    entry_points={
        'console_scripts': [
            'syncv=syncv.cli:main',
        ],
    },
    author='wonster',
    author_email='wooonster@outlook.com',
    description='A cross-platform clipboard synchronization tool',
    url='https://github.com/Wooonster/syncv',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)