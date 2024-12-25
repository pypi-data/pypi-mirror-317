from setuptools import setup, find_packages

setup(
    name='pyreelmaker',
    version='1.0.0',
    description='A Python package for creating short video reels.',
    author='Jaswanth Krishna Perla',
    author_email='perlajaswanthkrishna@gmail.com',
    packages=find_packages(),
    install_requires=[
        'moviepy',
        'ffmpeg-python',
    ],
    python_requires='>=3.7',
)
