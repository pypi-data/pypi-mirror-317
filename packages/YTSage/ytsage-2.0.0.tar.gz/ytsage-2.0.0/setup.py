from setuptools import setup

setup(
    name='YTSage',
    version='2.0.0',
    author='oop7',
    author_email='oop7_support@proton.me', # Replace with your email
    description='A simple GUI for yt-dlp',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/oop7/YTSage',
    packages=['YTSage'],  # Explicitly list the package directory
    package_data={'YTSage': ['YTSage.py']}, # Include the Python file within the package
    install_requires=[
        'yt-dlp',
        'PyQt6',
        'requests',
        'Pillow',
        'packaging'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'YTSage=YTSage.YTSage:main', # Correct entry point
        ],
    },
)