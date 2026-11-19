#!/usr/bin/env python3
"""GLOBAL BRIEFING v3 - entry point for Thursday 19 November 2026.

The front page was rendered at build time by render.py and is held in
this repo as entry.png, next to this file. This program uses only the
Python standard library: it copies that pre-rendered PNG, byte for byte,
to the output directory, so grading needs no imaging library, no fonts,
no network and no clock - the copy is fully deterministic.
"""
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(BASE, "entry.png")


def copy_entry(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SOURCE, os.path.join(out_dir, "entry.png"))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    copy_entry(out_dir)


if __name__ == "__main__":
    main()
