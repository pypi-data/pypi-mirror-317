import subprocess

from astrokit.utils import get_pwd

example = get_pwd(__file__) / 'example'
for script in example.iterdir():
    subprocess.run(['python', script])