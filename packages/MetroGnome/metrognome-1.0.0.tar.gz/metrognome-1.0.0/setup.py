import os
import subprocess
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py
from distutils.cmd import Command


class GenerateSoundsCommand(Command):
    """Custom command to generate .wav files by running a shell script."""

    description = "Generate wave files at build time using generate_sounds.sh"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        script_path = os.path.join(os.path.dirname(__file__), "generate_sounds.sh")
        print(f"Running {script_path} to generate .wav files...")
        subprocess.check_call(["bash", script_path])
        print("WAV file generation complete!")


class CustomBuildPy(_build_py):
    """Custom build_py that runs the generate_sounds step first."""

    def run(self):
        self.run_command("generate_sounds")
        super().run()


setup(
    package_data={"metrognome": ["resources/*.wav", "resources/*.svg"]},
    cmdclass={
        "generate_sounds": GenerateSoundsCommand,
        "build_py": CustomBuildPy,
    },
)
