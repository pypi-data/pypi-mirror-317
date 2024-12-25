import os
import pathlib
import subprocess

from ..utils import is_linux, get_path_name, search_program, get_logger


class Oskar(object):
    applications = [
        'oskar',
        'oskar_binary_file_query',
        'oskar_fit_element_data',
        'oskar_fits_image_to_sky_model',
        'oskar_imager',
        'oskar_sim_beam_pattern',
        'oskar_sim_interferometer',
        'oskar_system_info',
        'oskar_vis_add',
        'oskar_vis_add_noise',
        'oskar_vis_summary',
        'oskar_vis_to_ms'
    ]

    def __init__(self, run_path: str | pathlib.Path, use_singularity=True):
        self.sif = None
        self.ini = None
        self.use = None
        self.logger = get_logger()

        if type(run_path) == str:
            run_path = pathlib.Path(run_path)
        self.run_path = run_path
        self.use_singularity = use_singularity
        self.envs = os.environ.copy()
        if is_linux() and use_singularity:
            self.sif = self.envs['OSKAR_SIF']

    def singularity_command(self, command):
        return ['singularity', 'exec', '--nv', self.sif] + command

    def run_oskar(self, command, **kwargs):
        if self.use_singularity:
            command = self.singularity_command(command)
        result = subprocess.run(command, env=self.envs, cwd=self.run_path,
                                capture_output=kwargs.get('capture_output', False),
                                text=kwargs.get('capture_output', False))
        return result

    def use_task(self, task_name='oskar_sim_interferometer', ini=None, check=True):
        if task_name not in self.applications:
            raise ValueError(f'oskar application {task_name} task not found!')
        if not search_program(task_name) and not self.use_singularity:
            raise FileNotFoundError(f'program {task_name} not found!')
        if ini is None:
            raise FileNotFoundError(f'{ini} not found!')
        self.use = task_name
        if type(ini) == str:
            ini = pathlib.Path(ini)
        self.ini = get_path_name(ini.relative_to(self.run_path))
        if check:
            self.check_task(self.use)

    def check_task(self, task_name):
        checkpoint = {
            'oskar_sim_interferometer': ['sky/oskar_sky_model/file', 'telescope/input_directory'],
        }
        if task_name in checkpoint:
            for key in checkpoint[task_name]:
                val = self.get(key, capture_output=True).stdout
                if val.strip() == '':
                    raise ValueError(f'{key} not found in {self.ini}')

    def set(self, key: str, value: str, **kwargs):
        return self.run_oskar([self.use, self.ini, '--set', key, value], **kwargs)

    def update(self, **kwargs):
        return self.set(**kwargs)

    def get(self, key: str, **kwargs):
        return self.run_oskar([self.use, self.ini, '--get', key], **kwargs)

    def run(self, **kwargs):
        return self.run_oskar([self.use, self.ini], **kwargs)

    def output_log(self, result):
        self.logger.info(f'command: {result.args}')
        self.logger.info(f'stdout: {result.stdout}')
        self.logger.info(f'stderr: {result.stderr}')
        self.logger.info(f'returncode: {result.returncode}')
