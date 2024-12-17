import argparse
import os
import subprocess
from os import path

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


def test_day(entry: str, lang: str | None = None):
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

    if lang == None:
        for k, v in lang_matrix.items():
            if k in os.listdir(entry):
                test_lang(*v)

    else:
        test_lang(*lang_matrix[lang])


""" Argument Parsing """


def run(year: str, day: str, no_run: bool, lang: str | None = None):
    if year not in os.listdir(path.curdir):
        print(f"Solution for {year} is not available")
        return

    if day not in os.listdir(f"{path.curdir}/{year}"):
        print(f"Solution for {year}/{day} is not available")
        return

    set_day(f"{path.curdir}/{year}/{day}")

    if not no_run:
        test_day(f"{path.curdir}/{year}/{day}", lang)
        


parser = argparse.ArgumentParser()
parser.add_argument("-y", "--year", help="year of the problem")
parser.add_argument("-d", "--day", help="day of the problem")

parser.add_argument(
    "-n", "--norun", help="only downloads the input.txt", action="store_true"
)
parser.add_argument("-p", "--file", help="runs file on given path", type=str)

args = parser.parse_args()

if not args.file:
    run(args.year, args.day, args.norun)

else:
    path_list = args.file.split("/")
    year, day, lang = path_list[-4], path_list[-3], path_list[-2]
    run(year, day, args.norun, lang)
