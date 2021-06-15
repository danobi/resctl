#!/bin/env python3

import argparse
import pathlib
import os
from os import path
import subprocess
import sys
import time

# Paths to crates relative to repository root
# NB: Order the list based on dependencies: least deps first, most deps last
PACKAGES = [
    "resctl/common/cgroupfs",
    "resctl/common/procfs",
    "resctl/below/common",
    "resctl/below/below_derive",
    "resctl/below/model",
    "resctl/below/render",
    "resctl/below/store",
    "resctl/below/view",
    "resctl/below/dump",
    "resctl/below",
]


def is_logged_in():
    return path.exists(path.expanduser("~/.cargo/credentials"))


def get_repository_root():
    return pathlib.Path(__file__).parent.parent.absolute()


def publish_crate(crate_root, dry_run):
    args = []
    args.append("cargo")
    args.append("publish")
    if dry_run:
        args.append("--dry-run")
    args.append("--manifest-path")
    args.append(f"{crate_root}/Cargo.toml")

    subprocess.run(args, check=True)


def main(args):
    if not args.dry_run and not is_logged_in():
        print("Please run `cargo login` first and then retry")
        return 1

    repo_root = get_repository_root()
    for package in PACKAGES:
        crate_root = f"{repo_root}/{package}"
        print(f"++ Publishing {crate_root}")
        publish_crate(crate_root, args.dry_run)

        # HACK: wait for crates.io to stabilize previously uploaded deps
        print("++ Waiting for crates.io to stabilize")
        time.sleep(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish to crates.io")
    parser.add_argument("--dry-run", action="store_true")
    sys.exit(main(parser.parse_args()))
