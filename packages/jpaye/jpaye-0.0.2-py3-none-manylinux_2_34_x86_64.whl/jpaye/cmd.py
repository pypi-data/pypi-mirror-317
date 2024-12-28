#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
import os
import sys
import json
import argparse
import importlib


def main():
    parser = argparse.ArgumentParser(description="Jpaye Commandline.")
    parser.add_argument('json_file', type=str, help="Path to the JSON file")
    args = parser.parse_args()
    
    if not os.path.exists(args.json_file):
        sys.exit(f"Error: The file '{args.json_file}' does not exist.")

    with open(args.json_file, 'r') as fh:
        js = json.load(fh)

    pkg_name = js.get("package")
    worker_name = js.get("function")
    args = js.get("args", [])
    kwargs = js.get("kwargs", {})

    try:
        module = importlib.import_module(pkg_name)
        worker = getattr(module, worker_name, None)
        if not callable(worker):
            raise AttributeError(f"'{worker_name}' is not callable.")
        return worker(*args, **kwargs)
    except (ImportError, AttributeError) as e:
        sys.exit(f"Error: {e}")

