#!/usr/bin/env python3

import os
import sys
from setuptools import setup, Extension
from subprocess import check_output, CalledProcessError

def get_compile_flags():

    path, _ = os.path.split(__file__)
    path = os.path.join(path, "detect_rpi.py")
    try:
        flags = check_output([path])
    except CalledProcessError:
        print("Cannot determine RPi version. Is this running on an RPi?")
        sys.exit(-1)

    compile_flags = str(flags, "utf-8").split(" ")
    try:
        nchans = os.environ["LED_NCHANS"]
        try:
            nchans = int(nchans)
            if nchans not in [8, 16]:
                raise ValueError
        except ValueError:
            print("LED_NCHANS env var must be either 8 or 16.")
            sys.exit(-1)
    except KeyError:
        nchans = 8

    print("Building smi_leds extension for %d channels" % nchans)
    compile_flags.append("-O2 -DLED_NCHANS=%d" % nchans)

    return compile_flags

if sys.argv[1] == "sdist":
    compile_flags = []
else:
    compile_flags = get_compile_flags()

path, _ = os.path.split(__file__)
readme = os.path.join(path, "README.md")
with open(readme, "r") as f:
    long_description=f.read()

setup(name = "smileds",
      version = "2024.12.29.1",
      ext_modules = [Extension("smileds",
                               ["python/module.c",
                               "python/libsmi_leds.c",
                               "smi_leds/rpi_dma_utils.c",
                               "smi_leds/rpi_pixleds_lib.c"],
                               extra_compile_args=compile_flags,
                               include_dirs=["include"])],
      install_requires=[ "wheel" ],
      py_modules=["detect_rpi"],
      author="Jeremy P Bentham, Robert Kaye",
      classifiers=[
          "Programming Language :: Python :: 3",
          "Development Status :: 4 - Beta",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: POSIX :: Linux"
      ],
      description="A Python3 extension to drive 8 or 16 WS2812 LED Strips with a single Raspberry Pi",
      url="https://github.com/mayhem/smi_leds",
      long_description=long_description,
      long_description_content_type="text/markdown"
)
