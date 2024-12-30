from setuptools import setup, find_packages

setup(
    name="sertistssim",
    version="0.1",
    author="Kornpob Bhirombhakdi",
    author_email="kbhir@sertiscorp.com",
    description="Time-Series Simulator by Sertis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/your_project",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
