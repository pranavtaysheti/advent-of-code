# Advent Of Code

## Code should work on

- Python >= 3.14
- Go >= 1.25
- C (I used clang 21 + musl, defaults)

## Stars Collected

| Year | Stars  |
| ---- | ------ |
| 2025 | 21     |
| 2024 | **50** |
| 2023 | 38     |
| 2022 | 16     |

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

## Credits

This project uses code from following projects:

- https://github.com/tidwall/hashmap.c by Josh Baker

## License

GNU General Public License v3.0 or later

### Notice on AI Usage

Author requests that this repository and its contents not be used for:

- Training machine learning or AI models
- Dataset aggregation
- Embedding or fine-tuning purposes

Explicit written permission is required.
