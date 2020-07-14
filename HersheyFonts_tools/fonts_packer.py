import argparse
import base64
import importlib
import os
import re
import shutil
import tarfile
from io import BytesIO


def get_encoding():
    encoding_match = re.match(r"base(\d\d)", parsed_command_line.encoding)
    if encoding_match and encoding_match.lastindex:
        encoding_base = encoding_match[1]
        if hasattr(base64, f'b{encoding_base}encode') and hasattr(base64, f'b{encoding_base}decode'):
            return int(encoding_base), getattr(base64, f'b{encoding_base}encode'), getattr(base64, f'b{encoding_base}decode')
    raise ValueError(f'Unimplemented encoding: "{parsed_command_line.encoding}"')


def decode_bytes(data):
    _, _, decoder = get_encoding()
    return decoder(data)


def encode_bytes(data):
    _, encoder, _ = get_encoding()
    return encoder(data)


def get_string_to_inject(bytes_array):
    return f"compressed_fonts_{parsed_command_line.encoding} = B'''{encode_bytes(bytes_array).decode()}'''"


def create_compressed_data():
    compressed_file_stream = BytesIO()
    files_in_folder = sorted(os.listdir())
    ci_files_dict = dict(zip(map(str.casefold, files_in_folder), files_in_folder))
    if len(ci_files_dict) != len(files_in_folder):
        print('###Warning, some files differ only in letter case. Duplicates eliminated!')
    ci_fonts_in_folder = list(filter(lambda file_name: file_name.endswith('.jhf'.casefold()), ci_files_dict.keys()))
    ci_default_font_file = 'futural.jhf'.casefold()
    ci_default_font_file = ci_default_font_file if ci_default_font_file in ci_fonts_in_folder else ci_fonts_in_folder[0]
    if parsed_command_line.default_font:
        parsed_command_line.default_font.close()
        ci_default_font_file = parsed_command_line.default_font.name.casefold()
    ci_fonts_in_folder.remove(ci_default_font_file)
    ci_fonts_in_folder.insert(0, ci_default_font_file)
    with tarfile.open(fileobj=compressed_file_stream, format=tarfile.GNU_FORMAT, mode='w|' + parsed_command_line.compression) as tar:
        print(f'Using default font file: "{ci_files_dict[ci_default_font_file]}"')
        for ci_file_name in ci_fonts_in_folder:
            font_name = os.path.splitext(ci_files_dict[ci_file_name])[0]
            print(f'Adding font: "{ci_files_dict[ci_file_name]}" → "{font_name}" ', end='... ')
            tar.add(ci_file_name, arcname=font_name)
            print('OK')
    return compressed_file_stream.getvalue(), ci_files_dict[ci_default_font_file]


def write_tarfile(compressed_bytes, file_name='hershey_font_resource.tar'):
    with open(file_name, 'wb+') as output_file:
        print(f'# Writing compressed resource: {file_name} ', end='... ')
        output_file.write(compressed_bytes)
        print('OK')


def write_python_resource(compressed_bytes, file_name='hershey_font_resource.py'):
    with open(file_name, 'w+') as output_file:
        print(f'# Writing python resource: {file_name} / compressed_fonts_{parsed_command_line.encoding} ', end='... ')
        print(get_string_to_inject(compressed_bytes), file=output_file)
        print(f'OK. Total Python bytes written: {output_file.tell()}')


def inject_python_resource(compressed_bytes, inject_file):
    print(f'# Injecting to source file: "{inject_file.name}" ', end='... ')
    inject_file.seek(0)
    input_string = inject_file.read()
    regex = r"compressed_fonts(?:_base\d\d)?\s*=\s*[a-zA-Z]{0,2}'''.*?'''"
    subst = get_string_to_inject(compressed_bytes)
    # You can manually specify the number of replacements by changing the 4th argument
    if re.findall(regex, input_string, re.DOTALL):
        result = re.sub(regex, subst, input_string, 1, re.DOTALL)
        print('Pattern found, injecting data ', end='... ')
        inject_file.seek(0)
        inject_file.truncate()
        inject_file.write(result)
        print('OK')
        return True
    print('Pattern not found ... Fail')
    return False


def verify_resources(binary_data):
    all_ok, num_verified = True, 0
    compressed_file_stream = BytesIO(decode_bytes(binary_data))
    with tarfile.open(fileobj=compressed_file_stream, mode='r', ) as tar_file:
        for tar_member in tar_file.getmembers():
            tar_member_name = tar_member.name
            font_file_name = tar_member_name + '.jhf'
            for font_file_name_real in os.listdir():
                if font_file_name_real.casefold() == font_file_name.casefold():
                    font_file_name = font_file_name_real
                    break
            print(f'Comparing "{tar_member_name}" and "{font_file_name}" ', end='... ')
            with open(font_file_name, 'rb') as font_file:
                if font_file.read() == tar_file.extractfile(tar_member_name).read():
                    print('OK')
                    num_verified += 1
                else:
                    all_ok = False
                    print('FAIL!!!')
    return all_ok, num_verified


def do_all(cmdline_params):
    resource_file_name = parsed_command_line.output
    inject_ok = None
    print("# Create compressed data")
    compressed_bytes, default_font_file_name = create_compressed_data()
    print("# Compressed data created")
    write_tarfile(compressed_bytes, resource_file_name + '.tar')
    write_python_resource(compressed_bytes, file_name=resource_file_name + '.py')
    if cmdline_params.inject_to:
        with open(cmdline_params.inject_to.name + '.bak', 'w+') as backup_file:
            print(f"# Creating backup before injecting. Backup is: '{backup_file.name}' ", end='... ')
            cmdline_params.inject_to.seek(0)
            shutil.copyfileobj(cmdline_params.inject_to, backup_file)
            print("OK")
        inject_ok = inject_python_resource(compressed_bytes, cmdline_params.inject_to)
    print("# Verification")
    _locals = {}
    print(f'Loading "{resource_file_name}.py" ', end='... ')
    resource_file_module = importlib.import_module(resource_file_name)
    _locals = dir(resource_file_module)
    print('OK')
    print(f'Checking if variable created: ', end='... ')
    if f'compressed_fonts_{parsed_command_line.encoding}' in _locals:
        print('OK')
        print('# Comparing variable and original resources')
        ver_result, num_verified = verify_resources(getattr(resource_file_module, f'compressed_fonts_{parsed_command_line.encoding}'))
        print("# Verification result: ", 'OK' if ver_result else 'FAIL!!!')
        print(f'''DONE. Summary: 
         - default font file: {default_font_file_name}
         - resource encoding: {parsed_command_line.encoding}
         - compressed file: "{parsed_command_line.output}.tar"
         - python file: "{parsed_command_line.output}.py"
         - variable name: compressed_fonts_{parsed_command_line.encoding}''')
        if inject_ok is not None:
            print(f'         - data {"NOT " if not inject_ok else ""}injected: "{os.path.realpath(cmdline_params.inject_to.name)}"')
    else:
        print('FAIL!!!')


def get_list_of_encodings():
    base64_funcs_list = filter(lambda element: callable(getattr(base64, element)), dir(base64))
    encoders_or_decoders = [re.match(r"^b(\d{1,3})(en|de)code$", func)[1] for func in base64_funcs_list if re.match(r"^b\d{1,3}(en|de)code$", func)]
    encoders_and_decoders = [int(bit_length) for bit_length, occurrences in {bit_size: encoders_or_decoders.count(bit_size) for bit_size in encoders_or_decoders}.items() if occurrences == 2]
    return ['base' + str(bit_length) for bit_length in sorted(encoders_and_decoders)]


def get_compress_methods():
    return tarfile.TarFile.OPEN_METH.keys()


def get_default_compress_method():
    return 'bz2' if 'bz2' in get_compress_methods() else get_compress_methods()[0]


def get_default_encoding():
    return 'base64' if 'base64' in get_list_of_encodings() else get_list_of_encodings()[0]


if __name__ == '__main__':
    cmdline_parser = argparse.ArgumentParser(description='Compress *.jhf fonts in found in the current folder, create .py with inline data and optionally inject the new data into an existing class.')
    cmdline_parser.add_argument('-it', '--inject_to', type=argparse.FileType('r+'), help='Filename to inject compressed data to')
    cmdline_parser.add_argument('-df', '--default_font', type=argparse.FileType('r+'), help="Default font file name (Default: try 'futural')")
    cmdline_parser.add_argument('-e', '--encoding', choices=get_list_of_encodings(), default=get_default_encoding(), help=f'Encoding used for the compressed data (Default:{get_default_encoding()})')
    cmdline_parser.add_argument('-o', '--output_base', dest='output', default='hershey_font_resource', help='Output base name for generated resources (Default: hershey_font_resource)')
    cmdline_parser.add_argument('-c', '--compression', choices=get_compress_methods(), default=get_default_compress_method(), help=f'Output compression type (Default:{get_default_compress_method()})')
    parsed_command_line = cmdline_parser.parse_args()
    do_all(parsed_command_line)
