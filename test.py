import os
from os import DirEntry, path

import requests

""" Set Environment """

with open(".env") as env_file:
    for line in env_file:
        key, value = line.split("=", 1)
        os.environ[key] = value

""" Test Solutions """


def is_year(entry: DirEntry) -> bool:
    return entry.is_dir() and entry.name[0] == "2"


def set_day(entry: DirEntry):
    _, year, day = entry.path.split("/")

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
        print(f"Downloading Input File for {entry.path}")

        with open(f"{entry.path}/input.txt", "w") as input_file:
            input_file.write(get_input())


def test_day(entry: DirEntry):
    def test_lang(lang: str, command: str):
        print(f"{year.name} :: {day.name} :: {lang}")
        os.system(command)
        print()

    if "python" in os.listdir(entry):
        test_lang(
            "Python", f"cat {entry.path}/input.txt | python {entry.path}/python/main.py"
        )

    if "go" in os.listdir(entry):
        test_lang("Go", f"cat {entry.path}/input.txt | go run {entry.path}/go/main.go")


for f in os.scandir(path.curdir):
    if not is_year(f):
        continue

    year = f
    for day in os.scandir(f):
        set_day(day)
        test_day(day)
