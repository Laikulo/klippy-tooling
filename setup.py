from setuptools import setup
import subprocess, sys, os, logging
from setuptools.command.build import build, SubCommand
from setuptools import Command
from wheel.bdist_wheel import bdist_wheel
from glob import glob
import setuptools.command.install as orig_install


## Handling for klipper's building of the C helper and hubctl

class BuildCHelperSubCommand(build):
    def run(self):
        build_env = dict(os.environ)
        build_env['OVERRIDE_CHELPER_OUTPUT'] = os.path.join(os.getcwd(),f"{self.build_lib}/klippy/chelper/c_helper.so")
        build_env['OVERRIDE_HUBCTRL_OUTPUT'] = os.path.join(os.getcwd(),f"{self.build_lib}/klippy/chelper/hub-ctrl")
        build_dir=os.path.join(os.getcwd(), self.build_lib)
        subprocess.run([sys.executable, os.path.join(os.getcwd(),"compile.py")], cwd=build_dir, check=True, env=build_env)
    
    def get_source_files(self):
        source_list = []
        source_list += glob("klippy/chelper/*.[ch]")
        source_list += glob("hub-ctrl/*.[ch]")
        source_list.append("compile.py")
        return source_list

    def get_outputs(self):
        return [
                f"{self.build_lib}/klippy/chelper/c_helper.so",
                f"{self.build_lib}/klippy/chelper/hub-ctrl"
        ]


class BuildKlipperCommand(build):
    def __init__(self,dist):
        super().__init__(dist)
        self.sub_commands.append(('build_klipper_chelper', None))

## Because the above doesn't trigger bdist_wheel to treat this as non pure-python

class ImpureBdistWheel(bdist_wheel):
    description = "create an explicitly nonportable wheel"

    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False

## Similar case with install

class ImpureInstall(orig_install.install):
    description = "Install, but always into platlib"

    def finalize_options(self):
        super().finalize_options()
        self.install_lib = self.install_platlib
        

setup(
    cmdclass={
        'build': BuildKlipperCommand,
        'build_klipper_chelper': BuildCHelperSubCommand,
        'bdist_wheel': ImpureBdistWheel,
        'install': ImpureInstall
    }
)
