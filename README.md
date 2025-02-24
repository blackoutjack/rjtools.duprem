# duprem: duplicate file removal utility

Scan a set of directories to identify and potentially remove duplicate files.

## Requirements

* Python 3.12+

The following are installed with the `pip` command under **Installation**.

* [`rjtools.util`](https://github.com/blackoutjack/rjtools.util)
* [`pillow`](https://github.com/python-pillow)

This application has only been tested on Linux. Use on Windows is not
recommended.

## Installation

    python3 -m venv ./venv
    source ./venv/bin/activate
    pip install -r requirements.txt

Then run `./venv/bin/activate` to set up the virtual env in each terminal
session where you'd like to run duprem.

## Example usage

The following command will search through `path/to/my/files` and `another/dir`
for files whose contents are identical. A listing of sets of identical files
is produced.

    python3 -m duprem path/to/my/files another/dir

This command will look through `some/dir` for duplicate files, and will give
the user the option to remove one or more of the duplicates. The image plugin
is used for smarter duplicate detection in image content (non-image files in
the directory will still also be evaluated against each other also).

    python3 -m duprem some/dir -p image --remove

## Plugins

Modules can be added to the `plugin` directory to improve duplicate detection
for particular file types. See the example of `duprem.plugin.image`, which can
detect duplicate image data in files with different encodings.

