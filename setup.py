import setuptools
import io

with io.open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Hershey Fonts",
    version="1.1.0",
    author="Attila",
    author_email="attila.kolinger@gmail.com",
    description="Vector font package with built-in fonts and font rendering iterators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apshu/HersheyFonts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "Topic :: Text Processing :: Fonts",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "HersheyFonts_demo=HersheyFonts.HersheyFonts:main_script",
        ],
        "gui_scripts": [
            "HersheyFonts_demo=HersheyFonts.HersheyFonts:main",
        ]
    },
    python_requires='>=2.7',
)