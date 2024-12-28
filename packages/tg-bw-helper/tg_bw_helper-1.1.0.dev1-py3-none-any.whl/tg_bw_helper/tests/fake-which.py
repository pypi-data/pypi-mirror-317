#!/usr/bin/env python
import pathlib
import sys


if sys.argv[1] != "bw":
    sys.stdout.write(str((pathlib.Path(__file__).parent / sys.argv[1]).absolute()))
sys.stdout.write("\n")

if sys.argv[1] == "bw":
    exit(1)
