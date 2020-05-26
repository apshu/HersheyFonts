# Hershey Font
Hershey font library with built in fonts and low level line and stroke iterators

## What is Hershey Font
Hershey font is a vector font, designed many years ago.
The main use today if for generating text for CNC engraving.
[Read more on Wikipedia](https://en.wikipedia.org/wiki/Hershey_fonts)
[Font samples](http://soft9000.com/HersheyShowcase/)
## How to use
### Python module
Great care was taken to be compatible with defulat installation of python 2.7 and python 3.
### Installing
Sources available on GitHub 
Installation is available through pip and pip3
```ShellSession
%python 3
pip3 install Hershey-Fonts

%python 2.7
pip install Hershey-Fonts
```
### Included fonts
The python module 1.0.0 has 32 fonts included in a compressed base64 encoded format.
The module can load default fonts or from file and iterable string lines. 
When you make your own font and want to include in the package, please contact me.
You can get the list of built-in fonts by looking at 
```Python
import HersheyFonts

print(HersheyFonts().default_font_names)
```
## Thank you
Big thanks to all people working on maintaining this old format for the modern age.
