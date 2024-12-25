import logging
import pathlib
import platform
import shutil


def get_cwd(base_path):
    return pathlib.Path(base_path).parent


def get_pwd(base_path):
    return get_cwd(base_path).parent


def get_data(name: str):
    file = get_cwd(__file__) / 'data' / name
    if file.exists():
        return file
    raise FileNotFoundError(f'{file} not found!')


def get_script(name: str):
    script = get_cwd(__file__) / 'scripts' / name
    if script.exists():
        return script
    raise FileNotFoundError(f'{script} not found!')


def get_file_list(path: pathlib.Path, ext: str = ''):
    return path.glob(ext)


def get_path_name(path: pathlib.Path):
    return f'%s' % path

def is_linux():
    return platform.system() == 'Linux'

def is_windows():
    return not is_linux()

def search_program(name: str):
    return shutil.which(name) is not None

def get_logger():
    logging.basicConfig(level=logging.INFO,
                        format="[%(levelname)s:%(lineno)d] %(message)s")
    return logging.getLogger()