from setuptools import setup
from yasiu_math import VERSION


project_urls = {
    "1. Native Package": "https://pypi.org/project/yasiu-native/",
    "2. Math Package": "https://pypi.org/project/yasiu-math/",
    "3. Image Package": "https://pypi.org/project/yasiu-image/",
    "4. Visualisation Package": "https://pypi.org/project/yasiu-vis/",

    "5. Source repo": "https://github.com/GrzegorzKrug/yasiu-math",
}

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: Implementation :: CPython",

    "Topic :: Scientific/Engineering :: Mathematics",

    "Intended Audience :: Education",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",

    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

keywords = [
    "numpy", "scipy", "math",
]

author = "Grzegorz Krug"
author_email = "kruggrzegorz@gmail.com"

description = "High level functions that are missing in numpy / scipy"
readme_path = "README.md"

with open(readme_path, "rt") as file:
    long_description = file.read()

python_requires = '>=3.7'
install_requires = [
    "numpy", "scipy",
]

setup(
    name='yasiu-math',
    version=".".join([str(num) for num in VERSION]),
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,

    license='MIT',

    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls=project_urls,

    keywords=keywords,
    classifiers=classifiers,

    python_requires=python_requires,
    install_requires=install_requires,
    # setup_requires=install_requires,

    package_dir={
        "yasiu_math": "yasiu_math",
    }

)
