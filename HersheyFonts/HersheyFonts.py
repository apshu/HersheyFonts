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
    __compressed_fonts_base64=B'''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'''

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
    - first_glyph_ascii_code : if use_charcode is Talse, use this ASCII code for the first character in font line
    - merge_existing : if True merge the glyphs from data_iterator to the current font
    '''
        glyph_ascii_code = first_glyph_ascii_code
        cap = []
        base = []
        bottom = []
        cap_line = None
        base_line = None
        bottom_line = None
        if not merge_existing:
            self.__glyphs = {}
        if data_iterator:
            for line in data_iterator or '':
                line = line.decode()
                if line[0] == '#':
                    extraparams = json.loads(line[1:])
                    if 'define_cap_line' in extraparams:
                        cap_line = extraparams['define_cap_line']
                    if 'define_base_line' in extraparams:
                        base_line = extraparams['define_base_line']
                    if 'define_bottom_line' in extraparams:
                        bottom_line = extraparams['define_bottom_line']
                aglyph = _HersheyGlyph(data_line=line, default_base_line=base_line, default_bottom_line=bottom_line, default_cap_line=cap_line)
                if line[0] != '#':
                    glyph_key = chr(aglyph.font_charcode if use_charcode else glyph_ascii_code)
                    self.__glyphs[glyph_key] = aglyph
                    cap.append(aglyph.cap_line)
                    base.append(aglyph.base_line)
                    bottom.append(aglyph.bottom_line)
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
