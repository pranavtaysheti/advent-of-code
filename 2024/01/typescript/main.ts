import { readFileSync } from "node:fs"

let data: [Array<number>, Array<number>] = [[], []]
for (const line of readFileSync(0, { "encoding": "utf-8" }).split("\n")) {
    const [l0, l1] = line.split("   ")
    data[0].push(parseInt(l0))
    data[1].push(parseInt(l1))
}


// for some reason readFileSync adds an empty line at end, this removes it.
data[0].pop()
data[1].pop()

function solve(): number {
    data[0].sort((a, b) => a - b)
    data[1].sort((a, b) => a - b)

    let res = 0;
    for (let i = 0; i < data[0].length; i++) {
        res += Math.abs(data[0][i] - data[1][i])
    }

    return res
}

function similarityScore(): number {
    const counts = new Map<number, number>

    for (const i of data[1]) {
        const val = counts.get(i)
        if (!val) {
            counts.set(i, 1)
        } else {
            counts.set(i, val + 1)
        }
    }

    let res = 0
    for (const i of data[0]) {
        const qty = counts.get(i)
        if (qty) {
            res += qty * i
        }
    }

    return res
}

console.log(`P1: ${solve()}`)
console.log(`P2: ${similarityScore()}`)