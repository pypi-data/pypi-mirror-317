from setuptools import setup, find_packages

setup(
    name="StableCox",  
    version="0.3",  
    packages=find_packages(),
    dependencies = [
        "lifelines>=0.27.8",
        "numpy>=1.20.3",
        "pandas>=2.0.3",
        "scikit-learn>=1.3.0",
    ],
    author="Shaohua Fan",
    author_email="shaohuafan@tsinghua.edu.cn",  
    description="The official implement of Stable Cox",  
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/googlebaba/StableCox",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
