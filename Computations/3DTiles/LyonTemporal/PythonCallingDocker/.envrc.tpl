#!/usr/bin/env bash

# Template file (.tpl extension) for direnv ".envrc" file
# Usage:
#   echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
#   ln -s .envrc.tpl .envrc
#   direnv allow
#   pip install -r requirements.txt
# If you wish your shell cursor to reflect your active virtual environment
# refer to this method https://github.com/direnv/direnv/wiki/Python#bash
#
# Further references:
#  - https://github.com/direnv/direnv
#  - https://www.stackabuse.com/managing-python-environments-with-direnv-and-pyenv/

layout python3
