import argparse
import os
import subprocess
from typing import NamedTuple

import requests

CODE_PATH_FORMAT = "{year}/{day}/{lang}/main.{ext}"
INPUT_PATH_FORMAT = "{year}/{day}/"


def parse_year(p: str) -> str:
    return p.split("/")[-4]


def parse_day(p: str) -> str:
    return p.split("/")[-3]


class UnknownExtension(ValueError):
    def __init__(self, ext: str):
        self.ext = ext
        super().__init__()


class LangValue(NamedTuple):
    command: list[str]
    extension: str


class LangInfo(dict[str, LangValue]):
    def file_lang(self, file_name: str) -> LangValue:
        *_, ext = file_name.split(".")

        for v in lang_info.values():
            if ext == v.extension:
                return v

        raise UnknownExtension(ext)


lang_info = LangInfo(
    {
        "python": LangValue(["python"], "py"),
        "go": LangValue(["go", "run"], "go"),
    }
)


def download_input(year: str, day: str) -> str:
    def get_input() -> str:
        response = requests.get(
            url=f"https://adventofcode.com/{year}/day/{day.lstrip("0")}/input",
            cookies={
                "session": os.environ["AOC_SESSION"],
            },
        )

        return str(response.content, encoding="utf8")

    input_dir = f"{os.curdir}/{INPUT_PATH_FORMAT.format(year=year, day=day)}"
    input_path = f"{input_dir}/input.txt"

    if "input.txt" not in os.listdir(input_dir):
        print(f"Downloading Input file at {input_dir}")

        with open(input_path, "w") as input_file:
            input_file.write(get_input())

    return input_path


def aoc_run(code_path: str, year: str, day: str):
    with open(code_path):
        print(f"Running: {code_path}")

    command = lang_info.file_lang(code_path).command
    with open(download_input(year, day), "r") as input_file:
        subprocess.run([*command, code_path], stdin=input_file)


parser = argparse.ArgumentParser()
parser.add_argument("-y", "--year", help="year of the problem")
parser.add_argument("-d", "--day", help="day of the problem")
parser.add_argument("-l", "--lang", help="language of solution")
parser.add_argument("-p", "--file", help="runs file on given path", type=str)

args = parser.parse_args()

with open(".env") as env_file:  # Set Environment
    for line in env_file:
        key, value = line.split("=", 1)
        os.environ[key] = value

try:
    if args.file:
        year = parse_year(args.file)
        day = parse_day(args.file)

        aoc_run(args.file, year, day)

    else:
        if (args.year is None) or (args.day is None) or (args.lang is None):
            print("Requires -y, -d and -l flag to be set")

        else:
            code_path = CODE_PATH_FORMAT.format(
                year=args.year,
                day=args.day,
                lang=args.lang,
                ext=lang_info[args.lang].extension,
            )

            aoc_run(code_path, args.year, args.day)

except FileNotFoundError as e:
    print(f"file {e.filename} doesnt exist")

except UnknownExtension as e:
    print(f"format not supported: {e.ext} format")
