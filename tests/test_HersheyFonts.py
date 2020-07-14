import binascii
import tarfile
from io import BytesIO
from unittest import TestCase

from HersheyFonts import HersheyFonts


class TestHersheyFonts(TestCase):
    def setUp(self) -> None:
        self.font = HersheyFonts()

    def get_compressed_data(self):
        return self.font._HersheyFonts__get_compressed_font_bytes()


class TestDefaultFonts(TestHersheyFonts):
    def test_return_font_name(self):
        def_load_font_name = self.font.load_default_font()
        self.assertIsNotNone(def_load_font_name, msg='load_default_font did not return loaded font name')

    def test_invalid_font_raises_exception(self):
        nonexisting_font_name = '|*|' * 1000
        with self.assertRaises(ValueError, msg='Loading invalid default font did not raise proper exception'):
            self.font.load_default_font(nonexisting_font_name)

    def test_is_default_font_first(self):
        def_font_name = self.font.default_font_names[0]
        def_load_font_name = self.font.load_default_font()
        self.assertEqual(def_font_name, def_load_font_name, msg='Default font is not reported as first font')

    def test_load_all(self):
        all_font_names = self.font.default_font_names
        failed_fonts = {}
        for font_name in all_font_names:
            try:
                self.assertEqual(font_name, self.font.load_default_font(font_name), msg='Did not load the requested font')
            except Exception as e:
                failed_fonts[font_name] = e
        self.assertFalse(failed_fonts, msg=f'Failed loading font{["", "s in list"][len(failed_fonts) > 1]}')

    def test_coding(self):
        compressed = self.get_compressed_data()
        self.assertIsInstance(compressed, bytes, msg='Decoded stream should be binary string')

    def test_invalid_font_resource(self):
        font_resource_data_name = None
        for enc in ('64', '85', '32', '16'):
            font_resource_data_name_test = '_HersheyFonts__compressed_fonts_base' + enc
            if hasattr(self.font, font_resource_data_name_test):
                font_resource_data_name = font_resource_data_name_test
                break
        self.assertIsNotNone(font_resource_data_name, msg='Couldn\'t find font data resource in class')
        original_data = getattr(self.font, font_resource_data_name)

        # Ruin data
        ruined_data = []
        setattr(self.font, font_resource_data_name, bytes(ruined_data))
        self.test_coding()
        with self.assertRaises(tarfile.ReadError, msg='tarfile corruption handled incorrectly'):
            self.test_compression()

        # Ruin encoding
        ruined_data = list(original_data)
        ruined_data[0] = 254
        setattr(self.font, font_resource_data_name, bytes(ruined_data))
        with self.assertRaises(binascii.Error, msg='font resource encoding handeled incorrectly'):
            self.test_coding()
        with self.assertRaises((binascii.Error, tarfile.ReadError), msg='tarfile corruption handled incorrectly'):
            self.test_compression()

        # Ruin compression
        ruined_data = list(original_data)
        ruined_data[0] = 0x32 if original_data[0] == 0x33 else 0x33
        setattr(self.font, font_resource_data_name, bytes(ruined_data))
        self.test_coding()
        with self.assertRaises(tarfile.ReadError, msg='tarfile corruption handled incorrectly'):
            self.test_compression()

    def test_compression(self):
        with BytesIO(self.get_compressed_data()) as compressed_file_stream:
            with tarfile.open(fileobj=compressed_file_stream, mode='r', ) as ftar:
                for tar_member in ftar.getmembers():
                    self.assertIsNotNone(tar_member, 'tar_member does not exist')
                    font_file = ftar.extractfile(tar_member)
                    data = font_file.read()
                    self.assertGreater(len(data), 0, 'Empty font file wasting space in module')
