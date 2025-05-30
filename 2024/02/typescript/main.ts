import { throws } from "assert";
import { readFileSync } from "fs";

class PairWise<T> {
    data: Array<T>

    constructor(i: Array<T>) {
        this.data = i
    }

    *[Symbol.iterator]() {
        for (let i = 0; i < this.data.length - 1; i++) {
            yield [this.data[i], this.data[i + 1]]
        }
    }
}

class Report {
    data: Array<number>

    constructor(l: Array<number>) {
        this.data = l
    }

    check(): boolean {
        const slope = this.data[1] > this.data[0] ? +1 : -1

        for (const [p, n] of new PairWise(this.data)) {
            const diff = (n - p)
            const absDiff = Math.abs(diff)

            if (((absDiff > 3) || (absDiff === 0)) || ((diff * slope) < 0)) {
                return false
            }
        }
        return true
    }
}

const data: Array<Report> = []

for (const line of readFileSync(0, { encoding: "utf-8" }).split("\n")) {
    const report = new Report(line.split(" ").map((e) => parseInt(e)))
    data.push(report)
}

data.pop()

console.log(`P1: ${data.map((r) => r.check()).filter((e) => e).length}`)
// console.log(`P2: ${ countSafe() } `)