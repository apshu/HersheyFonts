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
        if load_default_font:
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

    def load_default_font(self, default_font_name='futural'):
        '''load built-in font by name'''
        if default_font_name in self.default_font_names:
            with BytesIO(self.__get_compressed_font_bytes()) as compressed_file_stream:
                with tarfile.open(fileobj=compressed_file_stream, mode='r', ) as ftar:
                    tarmember = ftar.extractfile(default_font_name)
                    self.read_from_string_lines(tarmember)
                    return
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
    thefont.load_default_font()
    print('Built in fonts:')
    for fontname1, fontname2 in zip_longest(thefont.default_font_names[::2], thefont.default_font_names[1::2]):
        fontname2 = '' if fontname2 is None else '- "' + fontname2 + '"'
        fontname1 = '' if fontname1 is None else '"' + fontname1 + '"'
        print(' - {0:<25} {1}'.format(fontname1, fontname2))
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
