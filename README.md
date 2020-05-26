# Hershey Font
Hershey font is a python library with built in fonts and low level line and stroke iterators.

## What is Hershey Font?
Hershey font is a vector font, designed many years ago.
The main use today if for generating text for CNC engraving.

[Read more on Wikipedia](https://en.wikipedia.org/wiki/Hershey_fonts)

[Font samples](http://soft9000.com/HersheyShowcase/)
## Overview
Hershey font consists of _glyphs_, each _glyph_ is assigned to an ASCII value from 32 (`'space'`) until 32+number of _glyphs_.<br/>Each _glyph_ consits of array of **strokes**.<br/>A **stroke** is an array of zero or more continous lines (points of an openend or closed ploygon).
## The Python module
The Hershey-Font package is providing the `HersheyFonts` class.<br/>
Great care was taken to be compatible with defulat installation of python 2.7 and python 3.<br/>
The `HersheyFonts` instance is handling only one font at a time. If you need to use multiple type faces as the same time, you can load a new typeface anytime (even during rendering) or create another `HersheyFonts` instance.
### Installing
Sources available on [GitHub](https://github.com/apshu/HersheyFonts) 
Installation is available through pip and pip3
```ShellSession
#python 3
pip3 install Hershey-Fonts

#python 2.7
pip install Hershey-Fonts
```
### Demo
After successfully installing the Hershey-Font package, you can run the module for a simple demonstration.
```ShellSession
#python 3
python3 -m HersheyFonts

#python 2.7
python3 -m HersheyFonts
```

### Built-in fonts
The python module 1.0.0 has **32 fonts included in the source code** as a compressed base64 encoded variable.
The module can also load default fonts or from file and iterable string lines. 
When you make your own font and want to include in the package, please contact me.
You can get the list of built-in fonts by looking at 
```Python
from HersheyFonts import HersheyFonts

print(HersheyFonts().default_font_names)
```
The order and elements of the list may totally vary with any package release.
### Loading a font
To access one of the built-in fonts, use the  `.load_default_font()` method. To read custome fonts you can call the `.load_font_file(file_name)` or `.read_from_string_lines(stringlines)` methods. The constructor also gives opportunity to read built-in or external font.
```Python
from HersheyFonts import HersheyFonts
thefont = HersheyFonts()
thefont.load_default_font('gothiceng')
thefont.load_default_font(thefont.default_font_names[0])
thefont.load_default_font() #Use with caution
thefont.load_font_file('cyrillic.jhf')
thefont.read_from_string_lines(arrayofstrings)
```
For more details and all options see doc comments in the sources.
### Renderig the loaded font
There are several options to convert a text to font data. The simplest way is to read endpoints of the lines returned by renderer method `.lines_for_text(sometext)`<br/> 
There are renderer methods returning list of glyps, list of strokes and list of line endpoints.
> The renderers in version 1.0.0 support only single line texts.
> Rendering is also affected by `.render_options` property.<br/>
> There is a `.normalize_rendering()` method to automatically set the scaling and offsets for easy rendering.
```Python
# Minimalistic code for easy start
from HersheyFonts import HersheyFonts
def draw_line(x1, y1, x2, y2):
︙
︙

thefont = HersheyFonts()
thefont.load_default_font()
thefont.normalize_rendering(100)
for (x1, y1), (x2, y2) in thefont.lines_for_text('Hello'):
    draw_line(x1, y1 ,x2 ,y2)
```
## The Hershey-Font API
The API is documented in the source code. 
## Thank you
Big thanks to all people working on maintaining this old format for the modern age.
