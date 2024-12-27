# Kelian

Kelian is a Python library that provides a collection of useful and commonly used code snippets to speed up development and avoid reinventing the wheel. It includes utility functions, common algorithms, data manipulations, and more, designed to simplify your workflow and increase productivity.

## Installation

You can install the Kelian library via pip:

```bash
pip install kelian
```

## Examples

- [Encryption](./examples/encryption.md)
- [Loading Bar](./examples/loading_bar.md)
- [System](./examples/system.md)
- [Utilities](./examples/utilities.md)

## Functions

### Encryption

Simple functions to encrypt and decrypt data using predefined mappings or lists.

- `alpha2dict`: Maps alphabets to a dictionary for encryption.
- `list2dict`: Converts a list to a dictionary.
- `encrypt`: Encrypts a given text using predefined mappings.
- `decrypt`: Decrypts a given encrypted text.
- `encrypt_by_list`: Encrypts text based on a custom list.
- `decrypt_by_list`: Decrypts text based on a custom list.

### Loading Bar

- `ProgressBar`: Class
    - `format`: Change pattern of progress bar
    - `display`: Return the progress bar updated or not, depending on the given parameter
    - `__str__` or print class: Return the progress bar updated

### System

Retrieve detailed information about your computer's hardware, including processor, motherboard, GPU, RAM, and more.

- `get_processor_details`: Returns details about the CPU.
- `get_motherboard_details`: Returns details about the motherboard.
- `get_gpu_details`: Returns details about the GPU.
- `get_monitor_details`: Returns details about the monitor.
- `get_cd_drive_details`: Returns details about the CD drive.
- `get_mouse_details`: Returns details about the mouse.
- `get_speaker_details`: Returns details about the speakers.
- `get_keyboard_details`: Returns details about the keyboard.
- `get_hard_disk_details`: Returns details about the hard disk.
- `get_ram_details`: Returns details about the RAM.

### Utility

Helper functions like hashing utilities for common tasks.

- `string2hash`: Converts a string to its sha256 hashed value.

## License

This project is licensed under the MIT License. See the <a href="./LICENSE.txt">LICENSE</a> file for more details.
