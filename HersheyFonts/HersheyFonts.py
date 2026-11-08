import base64
import json
import tarfile
from io import BytesIO
from itertools import chain

try:
    from statistics import multimode as statistics_multimode
    from statistics import median as statistics_median
except ImportError:
    # Python 2.7 mockup for statistics
    def statistics_multimode(data):
        return data


    def statistics_median(lst):
        n = len(lst)
        s = sorted(lst)
        return (sum(s[n // 2 - 1:n // 2 + 1]) / 2.0, s[n // 2])[n % 2] if n else None

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

try:
    from string import split
except ImportError:
    split = str.split


class HersheyFonts(object):
    '''The Hershey Fonts:
        - are a set of more than 2000 glyph (symbol) descriptions in vector
                ( <x,y> point-to-point ) format
        - can be grouped as almost 20 'occidental' (english, greek,
                cyrillic) fonts, 3 or more 'oriental' (Kanji, Hiragana,
                and Katakana) fonts, and a few hundred miscellaneous
                symbols (mathematical, musical, cartographic, etc etc)
        - are suitable for typographic quality output on a vector device
                (such as a plotter) when used at an appropriate scale.
        - were digitized by Dr. A. V. Hershey while working for the U.S.
                Government National Bureau of Standards (NBS).
        - are in the public domain, with a few caveats:
                - They are available from NTIS (National Technical Info.
                        Service) in a computer-readable from which is *not*
                        in the public domain. This format is described in
                        a hardcopy publication "Tables of Coordinates for
                        Hershey's Repertory of Occidental Type Fonts and
                        Graphic Symbols" available from NTIS for less than
                        $20 US (phone number +1 703 487 4763).
                - NTIS does not care about and doesn't want to know about
                        what happens to Hershey Font data that is not
                        distributed in their exact format.
                - This distribution is not in the NTIS format, and thus is
                        only subject to the simple restriction described
                        at the top of this file.

Hard Copy samples of the Hershey Fonts are best obtained by purchasing the
book described above from NTIS. It contains a sample of all of the Occidental
symbols (but none of the Oriental symbols).

This distribution:
        - contains
                * a complete copy of the Font data using the original
                        glyph-numbering sequence
                * a set of translation tables that could be used to generate
                        ASCII-sequence fonts in various typestyles
                * a couple of sample programs in C and Fortran that are
                        capable of parsing the font data and displaying it
                        on a graphic device (we recommend that if you
                        wish to write programs using the fonts, you should
                        hack up one of these until it works on your system)

        - consists of the following files...
                hershey.doc - details of the font data format, typestyles and
                                symbols included, etc.
                hersh.oc[1-4] - The Occidental font data (these files can
                                        be catenated into one large database)
                hersh.or[1-4] - The Oriental font data (likewise here)
                *.hmp - Occidental font map files. Each file is a translation
                                table from Hershey glyph numbers to ASCII
                                sequence for a particular typestyle.
                hershey.f77 - A fortran program that reads and displays all
                                of the glyphs in a Hershey font file.
                hershey.c   - The same, in C, using GKS, for MS-DOS and the
                                PC-Color Graphics Adaptor.

Additional Work To Be Done (volunteers welcome!):

        - Integrate this complete set of data with the hershey font typesetting
                program recently distributed to mod.sources
        - Come up with an integrated data structure and supporting routines
                that make use of the ASCII translation tables
        - Digitize additional characters for the few places where non-ideal
                symbol substitutions were made in the ASCII translation tables.
        - Make a version of the demo program (hershey.c or hershey.f77) that
                uses the standard Un*x plot routines.
        - Write a banner-style program using Hershey Fonts for input and
                non-graphic terminals or printers for output.
        - Anything else you'd like!

This file provides a brief description of the contents of the Occidental
Hershey Font Files. For a complete listing of the fonts in hard copy, order
NBS Special Publication 424, "A contribution to computer typesetting
techniques: Tables of Coordinates for Hershey's Repertory of Occidental
Type Fonts and Graphic Symbols". You can get it from NTIS (phone number is
+1 703 487 4763) for less than twenty dollars US.

Basic Glyph (symbol) data:

        hersh.oc1       - numbers 1 to 1199
        hersh.oc2       - numbers 1200 to 2499
        hersh.oc3       - numbers 2500 to 3199
        hersh.oc4       - numbers 3200 to 3999

        These four files contain approximately 19 different fonts in
the A-Z alphabet plus greek and cyrillic, along with hundreds of special
symbols, described generically below.

        There are also four files of Oriental fonts (hersh.or[1-4]). These
files contain symbols from three Japanese alphabets (Kanji, Hiragana, and
Katakana). It is unknown what other symbols may be contained therein, nor
is it known what order the symbols are in (I don't know Japanese!).

        Back to the Occidental files:

Fonts:
        Roman: Plain, Simplex, Duplex, Complex Small, Complex, Triplex
        Italic: Complex Small, Complex, Triplex
        Script: Simplex, Complex
        Gothic: German, English, Italian
        Greek: Plain, Simplex, Complex Small, Complex
        Cyrillic: Complex

Symbols:
        Mathematical (227-229,232,727-779,732,737-740,1227-1270,2227-2270,
                        1294-1412,2294-2295,2401-2412)
        Daggers (for footnotes, etc) (1276-1279, 2276-2279)
        Astronomical (1281-1293,2281-2293)
        Astrological (2301-2312)
        Musical (2317-2382)
        Typesetting (ffl,fl,fi sorts of things) (miscellaneous places)
        Miscellaneous (mostly in 741-909, but also elsewhere):
                - Playing card suits
                - Meteorology
                - Graphics (lines, curves)
                - Electrical
                - Geometric (shapes)
                - Cartographic
                - Naval
                - Agricultural
                - Highways
                - Etc...

ASCII sequence translation files:

        The Hershey glyphs, while in a particular order, are not in an
        ASCII sequence. I have provided translation files that give the
        sequence of glyph numbers that will most closely approximate the
        ASCII printing sequence (from space through ~, with the degree
        circle tacked on at the end) for each of the above fonts:

        File names are made up of fffffftt.hmp,

                where ffffff is the font style, one of:
                        roman   Roman
                        greek   Greek
                        italic  Italic
                        script  Script
                        cyril   Cyrillic (some characters not placed in
                                           the ASCII sequence)
                        gothgr  Gothic German
                        gothgb  Gothic English
                        gothit  Gothic Italian

                and tt is the font type, one of:
                    p       Plain (very small, no lower case)
                    s       Simplex (plain, normal size, no serifs)
                    d       Duplex (normal size, no serifs, doubled lines)
                    c       Complex (normal size, serifs, doubled lines)
                    t       Triplex (normal size, serifs, tripled lines)
                    cs      Complex Small (Complex, smaller than normal size)

The three sizes are coded with particular base line (bottom of a capital
        letter) and cap line (top of a capital letter) values for 'y':

        Size            Base Line       Cap Line

        Very Small         -5              +4
        Small              -6              +7
        Normal             -9              +12

        (Note: some glyphs in the 'Very Small' fonts are actually 'Small')

The top line and bottom line, which are normally used to define vertical
        spacing, are not given. Maybe somebody can determine appropriate
        values for these!

The left line and right line, which are used to define horizontal spacing,
        are provided with each character in the database.

Format of Hershey glyphs:

5 bytes - glyphnumber
3 bytes - length of data  length in 16-bit words including left&right numbers
1 byte  - x value of left margin
1 byte  - x value of right margin
(length*2)-2 bytes      - stroke data

left&right margins and stroke data are biased by the value of the letter 'R'
Subtract the letter 'R' to get the data.

e.g. if the data byte is 'R', the data is 0
     if the data byte is 'T', the data is +2
     if the data byte is 'J', the data is -8

and so on...

The coordinate system is x-y, with the origin (0,0) in the center of the
glyph.  X increases to the right and y increases *down*.

The stroke data is pairs of bytes, one byte for x followed by one byte for y.

A ' R' in the stroke data indicates a 'lift pen and move' instruction.'''
    __compressed_fonts_base64 = B'''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'''

    class _objdict(dict):
        def __getattr__(self, name):
            if name in self:
                return self[name]
            else:
                raise AttributeError('No such attribute: ' + name)

        def __setattr__(self, name, value):
            if name in self:
                self[name] = value
            else:
                raise AttributeError('No such attribute: ' + name)

    class _rednderopts(_objdict):
        @property
        def cap_line(self):
            return self['cap_line'] * self.scaley

        @property
        def bottom_line(self):
            return self['bottom_line'] * self.scaley

        @property
        def base_line(self):
            return self['base_line'] * self.scaley

    class _HersheyRenderIterator(object):
        def __init__(self, glyphs, text=None):
            self.__text = text or ''
            if not isinstance(glyphs, dict):
                raise TypeError('glyphs parameter has to be a dictionary')
            self.__glyphs = glyphs

        def text_glyphs(self, text=None):
            text = text or self.__text or ''
            for current_char in text:
                if current_char in self.__glyphs:
                    the_glyph = self.__glyphs[current_char]
                    if isinstance(the_glyph, _HersheyGlyph):
                        yield the_glyph

        def text_strokes(self, text=None, xofs=0, yofs=0, scalex=1, scaley=1, spacing=0, **kwargs):
            for glyph in self.text_glyphs(text=text):
                for stroke in glyph.strokes:
                    yield [(xofs + (x - glyph.left_offset) * scalex, yofs + y * scaley) for x, y in stroke]
                xofs += spacing + scalex * glyph.char_width

    def __init__(self, load_from_data_iterator='', load_default_font=None):
        self.__glyphs = {}
        self.__default_font_names_list = None
        self.__font_params = self._rednderopts({'xofs': 0, 'yofs': 0, 'scalex': 1, 'scaley': 1, 'spacing': 0, 'cap_line': -12, 'base_line': 9, 'bottom_line': 16})
        if load_default_font is not None:
            self.load_default_font(load_default_font)
        else:
            self.read_from_string_lines(data_iterator=load_from_data_iterator)

    @property
    def render_options(self):
        '''xofs=0, yofs=0,
scalex=1, scaley=1,
spacing=0,
cap_line=-12, base_line= 9, bottom_line= 16'''
        return self.__font_params

    @property
    def all_glyphs(self):
        '''Get all Glyphs stored for currently loaded font. ={} if no font loaded'''
        return dict(self.__glyphs)

    @render_options.setter
    def render_options(self, newdim):
        '''xofs=0, yofs=0,
scalex=1, scaley=1,
spacing=0,
cap_line=-12, base_line= 9, bottom_line= 16'''
        if newdim.issubset(self.render_options.keys()):
            self.render_options.update(newdim)
        else:
            raise AttributeError('Unable to set unknown parameters')

    @property
    def default_font_names(self):
        '''Get the list of built-in fonts'''
        if not self.__default_font_names_list:
            with BytesIO(self.__get_compressed_font_bytes()) as compressed_file_stream:
                with tarfile.open(fileobj=compressed_file_stream, mode='r', ) as ftar:
                    self.__default_font_names_list = list(map(lambda tar_member: tar_member.name, ftar.getmembers()))
            del ftar
            del compressed_file_stream
        return list(self.__default_font_names_list)

    def __get_compressed_font_bytes(self):
        for enc in ('64', '85', '32', '16'):
            if hasattr(self, '_HersheyFonts__compressed_fonts_base' + enc):
                if hasattr(base64, 'b' + enc + 'decode'):
                    decoded = getattr(base64, 'b' + enc + 'decode')(getattr(self, '_HersheyFonts__compressed_fonts_base' + enc))
                    return bytes(decoded)
        raise NotImplementedError('base' + enc + ' encoding not supported on this platform.')

    def normalize_rendering(self, factor=1.0):
        '''Set rendering options to output text lines in upright direction, size set to "factor"'''
        scale_factor = float(factor) / (self.render_options['bottom_line'] - self.render_options['cap_line'])
        self.render_options.scaley = -scale_factor
        self.render_options.scalex = scale_factor
        self.render_options.yofs = self.render_options['bottom_line'] * scale_factor
        self.render_options.xofs = 0

    def load_default_font(self, default_font_name=''):
        '''load built-in font by name. If default_font_name not specified, selects the predefined default font. The routine is returning the name of the loaded font.'''
        if not default_font_name:
            default_font_name = self.default_font_names[0]
        if default_font_name in self.default_font_names:
            with BytesIO(self.__get_compressed_font_bytes()) as compressed_file_stream:
                with tarfile.open(fileobj=compressed_file_stream, mode='r', ) as ftar:
                    tarmember = ftar.extractfile(default_font_name)
                    self.read_from_string_lines(tarmember)
                    return default_font_name
        raise ValueError('"{0}" font not found.'.format(default_font_name))

    def load_font_file(self, file_name):
        '''load font from external file'''
        with open(file_name, 'r') as fin:
            self.read_from_string_lines(fin)

    def read_from_string_lines(self, data_iterator=None, first_glyph_ascii_code=32, use_charcode=False, merge_existing=False):
        '''Read font from iterable list of strings
Parameters:
    - data_iterator : string list or empty to clear current font data
    - use_charcode : if True use the font embedded charcode parameter for glyph storage
    - first_glyph_ascii_code : if use_charcode is False, use this ASCII code for the first character in font line
    - merge_existing : if True merge the glyphs from data_iterator to the current font
    '''
        glyph_ascii_code = first_glyph_ascii_code
        cap = []
        base = []
        bottom = []
        cap_line = None
        base_line = None
        bottom_line = None
        aglyph = None
        if not merge_existing:
            self.__glyphs = {}
        if data_iterator:
            for line in data_iterator or '':
                if isinstance(line, str) and hasattr(line, 'decode'):
                    line = line.decode()
                elif isinstance(line, bytes) and hasattr(line, 'decode'):
                    line = line.decode('utf-8')
                if line[0] == '#':
                    extraparams = json.loads(line[1:])
                    if 'define_cap_line' in extraparams:
                        cap_line = extraparams['define_cap_line']
                    if 'define_base_line' in extraparams:
                        base_line = extraparams['define_base_line']
                    if 'define_bottom_line' in extraparams:
                        bottom_line = extraparams['define_bottom_line']
                if aglyph:
                    aglyph.parse_string_line(line)
                else:
                    aglyph = _HersheyGlyph(data_line=line, default_base_line=base_line, default_bottom_line=bottom_line, default_cap_line=cap_line)
                if line[0] != '#':
                    glyph_key = chr(aglyph.font_charcode if use_charcode else glyph_ascii_code)
                    self.__glyphs[glyph_key] = aglyph
                    cap.append(aglyph.cap_line)
                    base.append(aglyph.base_line)
                    bottom.append(aglyph.bottom_line)
                    aglyph = None
                    glyph_ascii_code += 1
            caps = statistics_multimode(cap)
            bases = statistics_multimode(base)
            bottoms = statistics_multimode(bottom)
            self.render_options.cap_line = statistics_median(caps) if cap_line is None else cap_line
            self.render_options.base_line = statistics_median(bases) if base_line is None else base_line
            self.render_options.bottom_line = statistics_median(bottoms) if bottom_line is None else bottom_line

    def glyphs_for_text(self, text):
        '''Return iterable list of glyphs for the given text'''
        return self._HersheyRenderIterator(self.__glyphs).text_glyphs(text=text)

    def strokes_for_text(self, text):
        '''Return iterable list of continuous strokes (polygons) for all characters with pre calculated offsets for the given text.
Strokes (polygons) are list of (x,y) coordinates.
        '''
        return self._HersheyRenderIterator(self.__glyphs).text_strokes(text=text, **self.__font_params)

    def lines_for_text(self, text):
        '''Return iterable list of individual lines for all characters with pre calculated offsets for the given text.
Lines are a list of ((x0,y0),(x1,y1)) coordinates.
        '''
        return chain.from_iterable(zip(stroke[::], stroke[1::]) for stroke in self._HersheyRenderIterator(self.__glyphs).text_strokes(text=text, **self.__font_params))


class _HersheyGlyph(object):
    def __init__(self, data_line='', default_cap_line=None, default_base_line=None, default_bottom_line=None):
        self.__capline = default_cap_line
        self.__baseline = default_base_line
        self.__bottomline = default_bottom_line
        self.__charcode = -1
        self.__left_side = 0
        self.__right_side = 0
        self.__strokes = []
        self.__xmin = self.__xmax = self.__ymin = self.__ymax = 0
        self.parse_string_line(data_line=data_line)

    @property
    def base_line(self):
        '''Return the base line of the glyph. e.g. Horizontal leg of letter L.
The parameter might be in or outside of the bounding box for the glyph
        '''
        return 9 if self.__baseline is None else self.__baseline

    @property
    def cap_line(self):
        '''Return the cap line of the glyph. e.g. Horizontal hat of letter T.
The parameter might be in or outside of the bounding box for the glyph
        '''
        return -12 if self.__capline is None else self.__capline

    @property
    def bottom_line(self):
        '''Return the bottom line of the glyph. e.g. Lowest point of letter j.
The parameter might be in or outside of the bounding box for the glyph
        '''
        return 16 if self.__bottomline is None else self.__bottomline

    @property
    def font_charcode(self):
        '''Get the Hershey charcode of this glyph.'''
        return self.__charcode

    @property
    def left_offset(self):
        '''Get left side of the glyph. Can be different to bounding box.'''
        return self.__left_side

    @property
    def strokes(self):
        '''Return iterable list of continuous strokes (polygons) for this glyph.
Strokes (polygons) are list of (x,y) coordinates.
        '''
        return self.__strokes

    @property
    def char_width(self):
        '''Return the width of this glyph. May be different to bounding box.'''
        return self.__right_side - self.__left_side

    @property
    def draw_box(self):
        '''Return the graphical bounding box for this Glyph in format ((xmin,ymin),(xmax,ymax))'''
        return (self.__xmin, self.__ymin), (self.__xmax, self.__ymax)

    @property
    def char_box(self):
        '''Return the typographical bounding box for this Glyph in format ((xmin,ymin),(xmax,ymax)).
Can be different to bounding box.
See draw_box property for rendering bounding box
        '''
        return (self.__left_side, self.__bottomline), (self.__right_side, self.__capline)

    def __char2val(self, c):  # data is stored as signed bytes relative to ASCII R
        return ord(c) - ord('R')

    @property
    def lines(self):
        '''Return iterable list of individual lines for this Glyph.
Lines are a list of ((x0,y0),(x1,y1)) coordinates.
        '''
        return chain.from_iterable(zip(stroke[::], stroke[1::]) for stroke in self.__strokes)

    def parse_string_line(self, data_line):
        """Interprets a line of Hershey font text """
        if data_line:
            data_line = data_line.rstrip()
            if data_line:
                if data_line[0] == '#':
                    extraparams = json.loads(data_line[1:])
                    if 'glyph_cap_line' in extraparams:
                        self.__capline = extraparams['glyph_cap_line']
                    if 'glyph_base_line' in extraparams:
                        self.__baseline = extraparams['glyph_base_line']
                    if 'glyph_bottom_line' in extraparams:
                        self.__bottomline = extraparams['glyph_bottom_line']
                elif len(data_line) > 9:
                    strokes = []
                    xmin = xmax = ymin = ymax = None
                    # individual strokes are stored separated by <space>+R
                    # starting at col 11
                    for s in split(data_line[10:], ' R'):
                        if len(s):
                            stroke = list(zip(map(self.__char2val, s[::2]), map(self.__char2val, s[1::2])))
                            xmin = min(stroke + ([xmin] if xmin else []), key=lambda t: t[0])
                            ymin = min(stroke + ([ymin] if ymin else []), key=lambda t: t[1])
                            xmax = max(stroke + ([xmax] if xmax else []), key=lambda t: t[0])
                            ymax = max(stroke + ([ymax] if ymax else []), key=lambda t: t[1])
                            strokes.append(stroke)
                    self.__charcode = int(data_line[0:5])
                    self.__left_side = self.__char2val(data_line[8])
                    self.__right_side = self.__char2val(data_line[9])
                    self.__strokes = strokes
                    self.__xmin, self.__ymin, self.__xmax, self.__ymax = (xmin[0], ymin[1], xmax[0], ymax[1]) if strokes else (0, 0, 0, 0)
                    return True
        return False


def main():
    thefont = HersheyFonts()
    main_script(thefont)
    main_gui(thefont)


def main_script(thefont=HersheyFonts()):
    print('Built in fonts:')
    default_font_names = sorted(thefont.default_font_names)
    for fontname1, fontname2 in zip_longest(default_font_names[::2], default_font_names[1::2]):
        fontname2 = '' if fontname2 is None else '- "' + fontname2 + '"'
        fontname1 = '' if fontname1 is None else '"' + fontname1 + '"'
        print(' - {0:<25} {1}'.format(fontname1, fontname2))
    print('Default font: "{0}"'.format(thefont.load_default_font()))
    print('')
    print('Rendering options:')
    for optname, defval in thefont.render_options.items():
        print(' render_options.{0} = {1}'.format(optname, defval))


def main_gui(thefont=HersheyFonts()):
    import turtle
    thefont.load_default_font()
    thefont.normalize_rendering(30)
    thefont.render_options.xofs = -367
    turtle.mode('logo')
    turtle.tracer(2, delay=3)
    for coord in range(4):
        turtle.forward(200)
        if coord < 2:
            turtle.stamp()
        turtle.back(200)
        turtle.right(90)
    turtle.color('blue')
    lineslist = thefont.lines_for_text('Pack my box with five dozen liquor jugs.')
    for pt1, pt2 in lineslist:
        turtle.penup()
        turtle.goto(pt1)
        turtle.setheading(turtle.towards(pt2))
        turtle.pendown()
        turtle.goto(pt2)
    turtle.penup()
    turtle.color('red')
    turtle.goto(0, 100)
    turtle.setheading(180)
    turtle.update()
    turtle.exitonclick()


if __name__ == '__main__':
    main()
