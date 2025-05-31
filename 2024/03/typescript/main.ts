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
        this.re = /mul\(\d+\,\d+\)/g
    }

    match() {
        return this.data.match(this.re)
    }
}

const data = new Memory(readFileSync(0, { encoding: "utf-8" }))

let P1: number = 0
for (const m of data.match() as RegExpExecArray) {
    P1 += new Mul(m).multiply()
}

console.log(P1)
