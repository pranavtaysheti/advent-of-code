import { readFileSync } from "fs";

class Mul {
    data: string

    constructor(m: string) {
        this.data = m
    }

    multiply(): number {
        const [sn1, sn2] = this.data.slice(4, -1).split(",")
        const [n1, n2] = [parseInt(sn1), parseInt(sn2)]
        return n1 * n2
    }
}


class Memory {
    data: string
    re: RegExp

    constructor(d: string) {
        this.data = d
        this.re = /(mul\(\d+\,\d+\))|(do\(\))|(don't\(\))/g

        console.log(this.re.source)
    }

    solve(): Array<[boolean, number]> {
        const matches = this.data.match(this.re)
        let count: boolean = true

        const res: Array<[boolean, number]> = []
        for (const m of matches as RegExpMatchArray) {
            if (m === "do()") {
                count = true
            } else if (m === "don't()") {
                count = false
            } else {
                const val = new Mul(m).multiply()
                res.push([count, val])
            }
        }

        return res
    }
}

const data = new Memory(readFileSync(0, { encoding: "utf-8" }))
const res = data.solve()

let P1: number = 0
for (const [count, val] of res) {
    P1 += val
}

console.log(`P1: ${P1}`)

let P2: number = 0
for (const [count, val] of res) {
    if (count) {
        P2 += val
    }
}

console.log(`P2: ${P2}`)
