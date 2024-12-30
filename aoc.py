import argparse
import os
import subprocess
from typing import NamedTuple

import requests

FAIL_COLOUR = "\033[91m"

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


class EnvVarError(KeyError): ...


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

        input_data = get_input()
        with open(input_path, "w") as input_file:
            input_file.write(input_data)

    return input_path


def aoc_run(code_path: str, year: str, day: str, norun: bool = False):
    with open(code_path):
        print(f"Running: {code_path}")

    input_path = download_input(year, day)

    if not norun:
        command = lang_info.file_lang(code_path).command
        with open(input_path, "r") as input_file:
            subprocess.run([*command, code_path], stdin=input_file)


parser = argparse.ArgumentParser()
parser.add_argument("-y", "--year", help="year of the problem")
parser.add_argument("-d", "--day", help="day of the problem")
parser.add_argument("-l", "--lang", help="language of solution")
parser.add_argument("-p", "--file", help="runs file on given path", type=str)
parser.add_argument(
    "-n", "--norun", help="only downloads input, doesnt run", action="store_true"
)

args = parser.parse_args()

if ".env" in os.listdir(os.curdir):
    with open(".env") as env_file:  # Set Environment
        for line in env_file:
            key, value = line.split("=", 1)
            os.environ[key] = value

try:
    if args.file:
        year, day = parse_year(args.file), parse_day(args.file)

    else:
        if (args.year is None) or (args.day is None) or (args.lang is None):
            raise AssertionError("Requires -y, -d and -l flag to be set")
            # TODO: Better error handling

        else:
            code_path = CODE_PATH_FORMAT.format(
                year=args.year,
                day=args.day,
                lang=args.lang,
                ext=lang_info[args.lang].extension,
            )

            year, day = args.year, args.day

    aoc_run(args.file, year, day, args.norun)

except FileNotFoundError as e:
    print(f"file {e.filename} doesnt exist")

except UnknownExtension as e:
    print(f"format not supported: {e.ext} format")

except KeyError as e:
    if e.args[0] == "AOC_SESSION":
        print(f"{FAIL_COLOUR}Environment variable AOC_SESSION is not properly set")
