# __init__.py

"""
kelian: A Python library of useful code snippets
------------------------------------------------
Description:
    This library speeds up Python development by avoiding reinventing the wheel.
    It is made up of many commonly used code snippets, such as utility functions,
    classic algorithms, data manipulations and much more, to simplify development
    and improve productivity.

Auteur:
    Kelian

Licence:
    MIT License (voir LICENSE pour plus de détails)

Version:
    0.1.0
"""

__version__ = "0.1.6"
__author__ = "Kelian"
__license__ = "MIT"

from .encryption import alpha2dict, list2dict, encrypt, decrypt, encrypt_by_list, decrypt_by_list, encrypt_by_character_manga, decrypt_by_character_manga
from .loading_bar import ProgressBar
from .system import get_processor_details, get_motherboard_details, get_gpu_details, get_monitor_details, get_cd_drive_details, get_mouse_details, get_speaker_details, get_keyboard_details, get_hard_disk_details, get_ram_details
from .utils import string2hash, fix_encoding, multi_replace, while_replace

# Définir ce qui sera importé lors d'un 'from package import *'
__all__ = [
    "alpha2dict", 
    "list2dict", 
    "encrypt", 
    "decrypt", 
    "encrypt_by_list", 
    "decrypt_by_list", 
    "encrypt_by_character_manga", 
    "decrypt_by_character_manga", 
    "ProgressBar", 
    "get_processor_details", 
    "get_motherboard_details", 
    "get_gpu_details", 
    "get_monitor_details", 
    "get_cd_drive_details", 
    "get_mouse_details", 
    "get_speaker_details", 
    "get_keyboard_details", 
    "get_hard_disk_details", 
    "get_ram_details", 
    "string2hash",
    "fix_encoding", 
    "multi_replace", 
    "while_replace"
]
