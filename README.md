# TS4Script Decompiler
This is Decompiler for .ts4script file formats, this format is used for The Sims 4 Mods with Scripts.
You can use it if you found bug and want to fix it or just you are curious what is under the engine, Remember Mods can have Licences!


## Table of Contents

- [Usage](#usage)
- [Installation](#installation)
- [License](#license)

## Usage
1. Run the script and select a `.ts4script` file via the GUI.
2. Click "Start Decompiling" to decompile the `.pyc` files.
3. The results will be saved to `./modfile_decompiled/` and the process will be logged.

### Requirements
- Python 3.x
- Install dependencies via `pip install uncompyle6 decompyle3 tqdm` or `pip install -r requirements.txt` when cloned repo

### Features
- Decompiles `.pyc` files using `uncompyle6` with a fallback to `decompyle3`.
- Logs errors and `.pyc` file metadata.
- Graphical User Interface for selecting `.ts4script` files.
 

## Installation

Instructions on how to install and set up the project locally.

```bash
# Clone the repository
git clone git clone https://github.com/hajdew/HajTS4Dec

# Change into the project directory
cd HajTS4Dec

# Install any dependencies
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
