#!/usr/bin/env python
import platform
import shutil
import subprocess
import sys

from os.path import dirname, isdir, join as join_path

file_path = dirname(__file__)
requirements_path = '/'.join(file_path.split('/')[:-1]) + "/requirements"
root_path = file_path.split('/')[:-2]
root_path = '/'.join(root_path)


class VirtualEnvironmentBuilder(object):
    def __init__(self, virt_env_name):
        self.virt_env_name = virt_env_name

    @property
    def virt_env_path(self):
        print(join_path(root_path, self.virt_env_name))
        return join_path(root_path, self.virt_env_name)

    @property
    def virt_env_path(self):
        return root_path + "/" + self.virt_env_name

    def clean_build(self):
        self.delete_env()
        self.build()

    def build(self):
        # Create a fresh virtual environment if it doesn't exist
        self.create_venv()

        try:
            print(requirements_path)
            self.run_in_venv('pip', ['install', '-r', requirements_path])
        except Exception:
            print("Erorrrr")
            self.delete_env()


    def create_venv(self):
        if isdir(self.virt_env_path):
            return
        print(self.virt_env_path)
        try:
            subprocess.check_call([sys.executable, '-m', 'virtualenv', self.virt_env_path, '--no-site-packages'])
        except Exception:
            print("Something is wrong!")
            self.delete_env()
        if isdir(self.virt_env_name):
            print("Environment {} created".format(self.virt_env_path))

    def delete_env(self):
        print("Deleting env!")
        try:
            if isdir(self.virt_env_path):
                shutil.rmtree(self.virt_env_path)
        except Exception:
            print("Could not delete environment!")

    def run_in_venv(self, cmd, args):
        virtual_env_bin_path = self.virt_env_path
        if platform.system() == 'Windows':
            cmd += '.exe'
            virtual_env_bin_path += r'\Scripts'
        else:
            virtual_env_bin_path += r'/bin'
        print("here")
        print(virtual_env_bin_path)
        print(cmd)
        a = join_path[virtual_env_bin_path, cmd]
        print(a)
        subprocess.check_call(join_path[file_path, virtual_env_bin_path, cmd] + args)


if __name__ == '__main__':
    builder = VirtualEnvironmentBuilder('hack33-virtenv')
    builder.build()
