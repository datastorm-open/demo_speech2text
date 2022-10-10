import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="speech2text",
    version='0.1',
    author="Kaicheng Li",
    author_email="kaicheng.li@datastorm.fr",
    description="This package allows speech cutting of large files in English and French, speech recognition of large files, and the ability to add punctuation to text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/datastorm_projects/r-d/speech2text",
    packages=setuptools.find_packages(),
    include_package_data=True,
    envdir=".env",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10'
)

