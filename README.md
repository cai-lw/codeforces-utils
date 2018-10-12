# Codeforces command line utilities

Helps you focus on coding in Codeforces contests, by simplifying everything else.

## Usage and Features
```shell
cf new a.cpp            # Create source file, template included
cf run a.cpp            # Compile and run in one command
cf run a.cpp -t 999A    # Automated test with example input/outputs
```
Templates and configurations are located at `~/.cfutils/` (`%USERPROFILE%/.cfutils/` on Windows). You can freely change them according to you preference.

## Installation
Only supports Python 3
```shell
git clone https://github.com/cai-lw/codeforces-utils.git
cd codeforces-utils
python3 setup.py install
```

## TODO
This project is still in an early stage. Many features are planned:
* Login
* Submission
* Standings and other statistics
* Supporting other programming contest sites