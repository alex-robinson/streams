import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="streams", # Replace with your own username
    version="0.0.1",
    author="Alexander Robinson and Fontina Petrakopoulou",
    author_email="robinson@ucm.es",
    description="A package for calculating exergy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/fontina-petrakopoulou/streams",
    #packages=setuptools.find_packages(),
    packages=['streams'],
    package_dir={'streams': 'streams'},
    package_data={'streams': ['data/ReferenceTables.xlsx','gatex_pc_if97_mj.exe']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
