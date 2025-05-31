import { readFileSync } from "fs";

const vectors = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]

class WordSearch {
    data: Array<Array<string>>

    constructor(d: Array<Array<string>>) {
        this.data = d
    }

    linearSearch(word: string, pos: [number, number]): number {
        const [row, col] = pos

        let res = 0
        l_vector: for (const [c_row, c_col] of vectors) {
            for (let i = 0; i < word.length; i++) {
                const c = word[i]
                const [n_row, n_col] = [row + i * c_row, col + i * c_col]
                if ((n_row >= this.data.length || n_row < 0) || (n_col >= this.data[n_row].length || n_col < 0)) {
                    continue l_vector
                }

                if (this.data[n_row][n_col] === c) {
                    continue
                }

                continue l_vector
            }

            res++
        }

        return res
    }
}

const input_data: Array<Array<string>> = []
for (const line of readFileSync(0, { encoding: "utf-8" }).split("\n")) {
    input_data.push([...line])
}

input_data.pop()

const data = new WordSearch(input_data)

let P1: number = 0
for (const row in data.data) {
    for (const col in data.data[row]) {
        if (data.data[row][col] === "X") {
            P1 += data.linearSearch("XMAS", [Number(row), Number(col)])
        }
    }
}

console.log(`P1: ${P1}`)