import argparse
import os
import subprocess
from os import DirEntry, path

import requests

""" Set Environment """

with open(".env") as env_file:
    for line in env_file:
        key, value = line.split("=", 1)
        os.environ[key] = value

""" Test Solutions """


def set_day(entry: str):
    _, year, day = entry.split("/")

    def get_input() -> str:
        aoc_day = day
        if aoc_day[0] == "0":
            aoc_day = aoc_day[1:]

        response = requests.get(
            url=f"https://adventofcode.com/{year}/day/{aoc_day}/input",
            cookies={
                "session": os.environ["AOC_SESSION"],
            },
        )

        return str(response.content, encoding="utf8")

    if "input.txt" not in os.listdir(entry):
        print(f"Downloading Input File for {entry}")

        with open(f"{entry}/input.txt", "w") as input_file:
            input_file.write(get_input())


def test_day(entry: str):
    def test_lang(args: list[str], file: str):
        if not path.exists(f"{entry}/{file}"):
            print(f"File {entry}/{file} is Missing")
            return

        print(f"{args[0].title()} Solution:")
        print("-----------------------------")

        with open(f"{entry}/input.txt") as input_file:
            subprocess.run([*args, f"{entry}/{file}"], stdin=input_file)

        print()

    lang_matrix = {
        "python": (["python"], "/python/main.py"),
        "go": (["go", "run"], "/go/main.go"),
    }

    for k, v in lang_matrix.items():
        if k in os.listdir(entry):
            test_lang(*v)


""" Argument Parsing """

parser = argparse.ArgumentParser()
parser.add_argument("year", help="year of the problem")
parser.add_argument("day", help="day of the problem")

args = parser.parse_args()

if args.year not in os.listdir(path.curdir):
    print(f"Solution for {args.year} is not available")
    exit()

if args.day not in os.listdir(f"{path.curdir}/{args.year}"):
    print(f"Solution for {args.year}/{args.day} is not available")
    exit()

set_day(f"{path.curdir}/{args.year}/{args.day}")
test_day(f"{path.curdir}/{args.year}/{args.day}")
