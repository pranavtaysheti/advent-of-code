"use strict"

import { readFileSync } from "fs";

const data: Array<Array<number>> = []

for (const line of readFileSync(0, { encoding: "utf-8" }).split("\n")) {
    const nums = line.split(" ").map((e) => parseInt(e))
    data.push(nums)
}

data.pop()

function countSafe(): number {
    const check = (l: Array<number>): boolean => {
        let prev = l[0]
        let ascend = l[1] > l[0] ? +1 : -1
        for (const n of l.slice(1)) {
            const diff = (n - prev)
            const absDiff = Math.abs(diff)
            if (((absDiff > 3) || (absDiff < 1)) || diff * ascend < 0) {
                return false
            }

            prev = n
        }

        return true
    }

    let res = 0
    for (const nums of data) {
        res += Number(check(nums))
    }

    return res
}

console.log(`P1: ${countSafe()}`)