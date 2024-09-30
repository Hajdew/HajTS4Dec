# TS4Script Decompiler

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Usage
1. Run the script and select a `.ts4script` file via the GUI.
2. Click "Start Decompiling" to decompile the `.pyc` files.
3. The results will be saved to `./modfile_decompiled/` and the process will be logged.

### Requirements
- Python 3.x
- Install dependencies via `pip install uncompyle6 decompyle3 tqdm`

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