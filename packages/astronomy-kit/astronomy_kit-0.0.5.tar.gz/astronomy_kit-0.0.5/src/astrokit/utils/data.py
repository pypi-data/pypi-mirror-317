from pathlib import Path

import requests
import wget
import zipfile
import shutil

from .utils import get_pwd, get_cwd, get_path_name


def get_astrokit_path():
    return get_pwd(__file__)


def get_astrokit_script(name: str):
    script = get_cwd(__file__).joinpath(f'scripts/{name}')
    if script.exists():
        return script
    raise FileNotFoundError(f'{script} not found!')


def get_astrokit_data(name: str, retry=False):
    data = get_astrokit_path().joinpath(f'data/{name}')
    if data.exists():
        return data
    if not retry:
        check_data()
        get_astrokit_data(name, True)
    else:
        raise FileNotFoundError(f'{data} not found!')


def get_astrokit_example(download_path: str | Path):
    if isinstance(download_path, str):
        download_path = Path(download_path)
    download_file_from_github(r'https://api.github.com/repos/chenzhtbb/astrokit/contents', 'example', download_path)


def check_data():
    download_file_from_github(r'https://api.github.com/repos/chenzhtbb/astrokit/contents', 'data',
                              get_astrokit_path() / 'data', True)


def download_file_from_github(base_url, directory_path, save_path: str | Path, auto_unzip=False):
    if isinstance(save_path, str):
        save_path = Path(save_path)
    save_path.mkdir(parents=True, exist_ok=True)
    url = f'{base_url}/{directory_path}'
    file_list = requests.get(url)
    if file_list.status_code == 200:
        file_list = file_list.json()
    else:
        raise Exception(f'Failed to get astrokit {directory_path} file list from github.')
    print(f'Downloading astrokit data files to {save_path}')
    for file in file_list:
        if file['type'] == 'file':
            file_name = file['name']
            save_file = save_path / file_name
            if save_file.exists():
                print(f'{file_name} already exists, skip download.')
                continue
            file_content = requests.get(file['download_url'])
            if file_content.status_code == 200:
                with open(save_file, 'wb') as f:
                    f.write(file_content.content)
                print(f'Download {file_name} successfully.')
            else:
                raise Exception(f'Failed to download {file_name} from github.')
            if auto_unzip and save_file.suffix == '.zip':
                unzip_file(save_file, save_path, True)
                print(f'Unzip {file_name} successfully.')
    print(f'Download astrokit {directory_path} files to {save_path} successfully.')


def download_file(url: str, path: str | Path):
    if not isinstance(path, Path):
        path = Path(path)
    wget.download(url, get_path_name(path))


def unzip_file(zip_file: str | Path, extract_path: str | Path, smart_extract=False, auto_remove=False):
    if not isinstance(zip_file, Path):
        zip_file = Path(zip_file)
    if not isinstance(extract_path, Path):
        extract_path = Path(extract_path)
    if zip_file.exists():
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        if smart_extract:
            if (extract_path / zip_file.stem).exists():
                for item in (extract_path / zip_file.stem).iterdir():
                    shutil.move(item, extract_path)
                shutil.rmtree(extract_path / zip_file.stem)
