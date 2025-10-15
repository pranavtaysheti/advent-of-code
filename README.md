# Advent Of Code

## Code should work on

- Python >= 3.14
- Go >= 1.25

## Usage

1. Install `requirements.txt` python packages.

2. Set environment variable as follows using `.zshrc`, `direnv`, etc

    ```env
    AOC_SESSION=<your "session" cookie from AoC website after you login>
    ```

3. Then run following command in terminal.

    ```bash
    python aoc.py -y <year> -d <day> -l <language>
    ```

It will automatically download the input file.
