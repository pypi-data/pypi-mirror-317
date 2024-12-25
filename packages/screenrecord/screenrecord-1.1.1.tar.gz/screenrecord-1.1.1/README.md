# screenrecord

[![PyPI](https://img.shields.io/pypi/v/screenrecord.svg)](https://pypi.org/project/screenrecord/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/screenrecord?include_prereleases&label=changelog)](https://github.com/sukhbinder/screenrecord/releases)
[![Tests](https://github.com/sukhbinder/screenrecord/actions/workflows/test.yml/badge.svg)](https://github.com/sukhbinder/screenrecord/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/screenrecord/blob/master/LICENSE)

Record screen with python

## Installation

Install this tool using `pip`:
```bash
pip install screenrecord
```
## Usage

For help, run:
```bash
record --help
```
You can also use:
```bash
python -m record --help
```

Shows 

```bash
usage: record [-h] [-i INITDELAY] [-d DELAY] [-dur DURATION]
              [--bbox BBOX [BBOX ...]] [-f] [-aw]
              filename

Screen Recording with python

positional arguments:
  filename              filename can be mp4 or gif or mov

optional arguments:
  -h, --help            show this help message and exit
  -i INITDELAY, --initdelay INITDELAY
                        Initial delay in seconds, default 5 s
  -d DELAY, --delay DELAY
                        Delay between frames in seconds, default 0.5 s
  -dur DURATION, --duration DURATION
                        Duration of capture, default 20 s
  --bbox BBOX [BBOX ...]
                        Bounding box, default (0, 0, 50, 50)
  -f, --fullscreen
  -aw, --activewindow

```

![demo usage of screenrecord](https://raw.githubusercontent.com/sukhbinder/screenrecord/main/usage.gif)

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd screenrecord
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
