import os
import re
import setuptools
import pathlib


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

with open(os.path.join(here, 'torcheasy', '__init__.py')) as f:
    meta_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if meta_match:
        version = meta_match.group(1)
    else:
        raise RuntimeError("Unable to find __version__ string.")

long_description = (here / 'README.md').read_text(encoding='utf-8')
setuptools.setup(
    name="torcheasy",
    version=version,
    author="En Fu",
    author_email="fuensit@qq.com",
    description="Easily training module for PyTorch.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fuen1590/Torcheasy",
    packages=setuptools.find_packages(),
    install_requires=['torch>=1.5.0', 'numpy>=1.21.2', 'scipy>=1.5.2', 'matplotlib>=3.4.2'],
    python_requires='~=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
