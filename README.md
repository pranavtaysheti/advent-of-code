# Advent Of Code

## Requirements

- OS: Any Linux 🐧 / Mac / WSL
- Python (>= 3.13)
- Go (>= 1.23)
- [requests](https://pypi.org/project/requests/)

## Usage

Create a `.env` file in this folder with following content:

```
AOC_SESSION=<your "session" cookie from AoC website after you login>
```

Then run following command in terminal.

```bash
python aoc.py -y <year> -d <day>
```

It will automatically download the input file and run.
