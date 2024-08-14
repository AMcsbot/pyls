
# pyls - A Python-based File Listing Utility

## Overview
`pyls` is a simple Python utility that mimics the basic functionality of the Unix `ls` command. It lists files and directories in the specified directory, with options to display additional details such as file size, modification time, and file type indicators.

## Features
- List files in the current or specified directory.
- Display detailed information with the `-l` or `--long-format` option.
- Append file type indicators with the `-F` or `--filetype` option.

## Usage

```bash
python pyls.py [directory] [-l] [-F]
```

### Examples
- List files in the current directory:
  ```bash
  python pyls.py
  ```
- List files in a specific directory with long format:
  ```bash
  python pyls.py /path/to/directory -l
  ```
- List files with file type indicators:
  ```bash
  python pyls.py /path/to/directory -F
  ```

## Testing
To run the tests, use `pytest`:
```bash
pytest test_pyls.py
```

## Requirements
- Python 3.6+
- pytest for testing

## License
This project is licensed under the MIT License.
