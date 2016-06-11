# Panda Answer Checker

## Overview
Python script to generate answer checkers for P&amp;A Magazine.

This script will log into pandamagazine.com, then generate an answer checker for each issue of P&A Magazine you have. The answer checker is a barebones html page that functions much like the actual answer checker.

**NOTE:** This script uses your "progress" page to get the answers, meaning that it will only get answers to puzzles you've solved already. I would have to parse the answer .pdf to get all the answers and I don't want to do that. Sorry.

## Usage
python panda.py USERNAME PASSWORD

The script will generate an HTML file for each issue you have.

## Requirements
[requests](http://docs.python-requests.org/en/master/)

[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
