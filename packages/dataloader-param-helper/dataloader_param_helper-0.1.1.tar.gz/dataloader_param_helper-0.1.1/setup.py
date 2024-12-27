from setuptools import setup, find_packages

setup(
    name="dataloader_param_helper",
    version="0.1.1",  #
    author="Soo Hwan Cho",
    author_email="soohwancho@korea.ac.kr",
    description="Finding the optimal parameters for a Dataloader.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/splendidz/dataloader_param_helper", 
    packages=find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
