import { readFileSync } from "fs";

const vectors = [[0, 1], [1, 0], [0, -1], [-1, 0]]
const diagonal_vectors = [[1, 1], [1, -1], [-1, -1], [-1, +1]]

class WordSearch {
    data: Array<Array<string>>

    constructor(d: Array<Array<string>>) {
        this.data = d
    }

    linearSearch(word: string, [row, col]: [number, number]): number {
        let res = 0
        l_vector: for (const [c_row, c_col] of vectors.concat(diagonal_vectors)) {
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

    crossSearch([c1, c2]: [string, string], [row, col]: [number, number]): boolean {
        const corners = diagonal_vectors.map(([c_row, c_col]) =>
            this.data[row + c_row][col + c_col]
        )

        if (
            (
                (corners[0] === corners[1] && corners[2] === corners[3]) ||
                (corners[1] === corners[2] && corners[3] === corners[0])
            ) &&
            (
                (corners[0] === c1 && corners[2] === c2) ||
                (corners[0] === c2 && corners[2] === c1)
            )
        ) {
            return true
        }

        return false

    }
}

const input_data: Array<Array<string>> = []
for (const line of readFileSync(0, { encoding: "utf-8" }).split("\n")) {
    input_data.push([...line])
}

input_data.pop()

const data = new WordSearch(input_data)

let P1: number = 0
for (let row = 0; row < data.data.length; row++) {
    for (let col = 0; col < data.data[row].length; col++) {
        if (data.data[row][col] === "X") {
            P1 += data.linearSearch("XMAS", [row, col])
        }
    }
}

console.log(`P1: ${P1}`)

let P2: number = 0
for (let row = 1; row < data.data.length - 1; row++) {
    for (let col = 1; col < data.data[row].length - 1; col++) {

        if (data.data[row][col] === "A") {
            if (data.crossSearch(["M", "S"], [row, col])) {
                P2++
            }
        }
    }
}

console.log(`P2: ${P2}`)