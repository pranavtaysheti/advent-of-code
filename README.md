# Advent Of Code

## Code should work on

Python >= 3.13
Go >= 1.23

## Usage

1. Install `requirements.txt` python packages.

2. Create a `.env` file in this folder with following content:

    ```env
    AOC_SESSION=<your "session" cookie from AoC website after you login>
    ```

    Or alternively set environment variable using `.zshrc`, `direnv`, etc.

3. Then run following command in terminal.

    ```bash
    python aoc.py -y <year> -d <day> -l <language>
    ```

It will automatically download the input file.
