from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.11'
DESCRIPTION = 'Searching related data by image'
LONG_DESCRIPTION = 'A package that allows to build an image search engine using k-means clustering.'

# Setting up
setup(
    name="vasrch",
    version=VERSION,
    author="Steven Manangu (Varsitymart)",
    author_email="<stevenmanangu360@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'matplotlib', 'scikit-learn', 'tensorflow', 'joblib', 'cloudinary', 'requests'],
    keywords=['python', 'image', 'search', 'image search', 'e-commerce', 'clustering', 'k-means'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)