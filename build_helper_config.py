
from typing import Any, Dict
from glob import glob

from distutils.core import Extension


def build(setup_kwargs: Dict[str,Any]) -> None:
    setup_kwargs.update({
        # "ext_modules": [ Extension('klippy.chelper', glob("klippy/chelper/*.c")) ],
        "zip_safe": False
    })
            
