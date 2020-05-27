# Font resources extractor tool
# Helps remixing embedded fonts in HersheyFonts
import argparse
import base64
import os
import re
import tarfile
from io import BytesIO, TextIOWrapper


def decode_bytes_from_file(the_file: TextIOWrapper, search_variable_name: str):
    search_variable_name = search_variable_name.strip()
    search_var_name = re.match(r'^(.*?)(?:_base(\d\d))?$', search_variable_name)
    var_base_name = str(search_var_name[1])
    encode_bases = [str(search_var_name[2])] if search_var_name.lastindex > 1 else ('64', '85', '32', '16')
    saved_file_position = 0
    if the_file.seekable():
        saved_file_position = the_file.tell()
        the_file.seek(0)
    file_content = the_file.read()
    if the_file.seekable():
        the_file.seek(saved_file_position)
    for enc in encode_bases:
        reg_exp = var_base_name + "_base" + str(enc) + r"\s*=\s*[a-zA-Z]{0,2}'''(.*?)'''"
        var_found = re.match(reg_exp, file_content, re.DOTALL)
        if var_found:
            if hasattr(base64, 'b' + enc + 'decode'):
                decoded = getattr(base64, 'b' + enc + 'decode')(var_found[1])
                return var_base_name, bytes(decoded)
            else:
                return None, f'Variable found with unsupported encoding: base{enc}'
    return None, 'Variable not found'


def decode_bytes_from_hershey_fonts_internal():
    try:
        from HersheyFonts import HersheyFonts
    except ImportError:
        return None, 'HersheyFonts package not found'
    font = HersheyFonts()
    for enc in ('64', '85', '32', '16'):
        for attribute_name in ('_HersheyFonts__compressed_fonts_base', '_HersheyFonts_compressed_fonts_base', 'compressed_fonts_base'):
            if hasattr(font, attribute_name + enc):
                if hasattr(base64, 'b' + enc + 'decode'):
                    decoded = getattr(base64, 'b' + enc + 'decode')(getattr(font, attribute_name + enc))
                    return 'default_fonts', bytes(decoded)
                else:
                    return None, f'Variable found with unsupported encoding: base{enc}'
        return None, 'Variable not found in HersheyFonts'


def extract_var(decoded_var):
    extracted = 0
    with BytesIO(decoded_var) as compressed_file_stream:
        with tarfile.open(fileobj=compressed_file_stream, mode='r', ) as tar_file:
            for tar_member in tar_file.getmembers():
                extract_filename = os.path.basename(tar_member.path) + '.jhf'
                print(f'"{tar_member.path}" → "{extract_filename}"', end=' ...')
                with open(extract_filename, 'wb+') as output_file:
                    try:
                        output_file.write(tar_file.extractfile(tar_member).read())
                        print('OK')
                    except IOError:
                        print('Fail')
                    extracted += 1
    return extracted


def main():
    cmdline_parser = argparse.ArgumentParser(description='Extract embedded font resource')
    cmdline_parser.add_argument('-i', '--infile', type=argparse.FileType('r+'), help='Input file to search for the compressed font, when parameter not specified, it extracts from HersheyFont package')
    cmdline_parser.add_argument('-n', '--variable_name', default=None, type=str, help='Variable name in the input file')
    cmdline_parser.add_argument('-sf', '--suppress_fonts', dest='extract_fonts', action='store_false', help='Suppress extracting font files from the archive')
    cmdline_parser.add_argument('-st', '--suppress_tar', dest='save_tar', action='store_false', help='Suppress saving the TAR archive')
    parsed_command_line = cmdline_parser.parse_args()
    search_resource_name = '<HersheyFonts builtin resource>'
    if parsed_command_line.infile:
        if parsed_command_line.variable_name is None:
            parsed_command_line.variable_name = 'compressed_fonts'
            print(f'"-n" command line option not defined, assuming default variable name: "{parsed_command_line.variable_name}"')
        search_resource_name = parsed_command_line.infile.name
        tarfile_base_name, the_bytes = decode_bytes_from_file(parsed_command_line.infile, parsed_command_line.variable_name)
    else:
        if parsed_command_line.variable_name is not None:
            print('Info: "-n" command line option specified, but has no effect when extracting from HersheyFonts package')
        tarfile_base_name, the_bytes = decode_bytes_from_hershey_fonts_internal()
    if tarfile_base_name and the_bytes:
        print(f'Possible font resource found in "{search_resource_name}".')
        if parsed_command_line.save_tar:
            with open(tarfile_base_name+'.tar', 'wb+') as output_file:
                output_file.write(the_bytes)
                print(f'"{tarfile_base_name}.tar" successfully written.')
        if parsed_command_line.extract_fonts:
            num_extracted = extract_var(the_bytes)
            print(f'Number of font files extracted {num_extracted}.')
    elif the_bytes:
        print(f'Extract error: {the_bytes}')
    else:
        print('Unable to extract resource')


if __name__ == '__main__':
    main()
