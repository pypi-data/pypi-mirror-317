# AutoJS Python Project

## Overview
This project provides a set of Python functions to automate GUI interactions using `pyautogui` and perform OCR (Optical Character Recognition) using `pytesseract`.

## Project Structure
```commandline
autojs_python_project/
├── .gitignore
├── README.md
├── pyproject.toml
├── poetry.lock
├── src/
│   └── autojs_py/
│       ├── __init__.py
│       ├── opearation.py
│       ├── ocr.py
│       └── ...
├── tests/
│   ├── __init__.py
│   ├── test_opearation.py
│   └── ...
└── docs/
    └── ...
```

## Installation 

1. **Install Tesseract OCR**

- **Windows**:
  Download the installer from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) and follow the installation instructions.

- **Linux**:
    ```sh
    sudo apt-get update
    sudo apt-get install tesseract-ocr
    ```

- **macOS**:
    ```sh
    brew install tesseract
    ```
2 **Install use pip**:
```sh
pip install autojs-py
```
## Development
**Clone the repository**:
```sh
git clone https://github.com/angleyanalbedo/your-repo-name.git
cd your-repo-name
```

**Install dependencies using Poetry:**
    ```sh
    poetry install
    ```


## Usage
### GUI Automation
The `opearation.py` file contains functions to perform various mouse and keyboard actions:
- `Click(x, y)`
- `LClick(x, y)`
- `RClick(x, y)`
- `DClick(x, y)`
- `Send(text)`
- `Press(key)`
- `LongClick(s)`
- `tclick(template)`
- `tlclick(template)`
- `trcick(template)`
- `dclick(template)`
- `Swap(pos, pos2)`
- `tswap(template, direct)`
- `clicktext(text)`

### OCR
The `ocr.py` file contains functions to perform OCR on images:
- `ocr2str(image_path)`
- `ocr2box(img)`

## Example
Here is an example of how to use the `clicktext` function:
```python
from autojs_py.opearation import clicktext

clicktext("example text")