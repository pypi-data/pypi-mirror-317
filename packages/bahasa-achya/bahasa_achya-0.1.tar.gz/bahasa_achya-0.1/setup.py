from setuptools import setup, find_packages

setup(
    name="bahasa-achya",
    version="0.1",
    packages=find_packages(),
    install_requires=[], 
    entry_points={
        'console_scripts': [
            'achya = achya:main',
            'achya-install = achya_install:main',
        ],
    },
    author="Muhammad Achya",
    author_email="muhachya@gmail.com",
    description="Achya Language adalah bahasa pemrograman berbasis Python dengan sintaks menggunakan bahasa Indonesia.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/cholilfayyadl/bahasa-achya", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
