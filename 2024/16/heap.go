package main

type Item struct {
	cost int
	item *any
}

type PriorityQueue []Item

func (pq PriorityQueue) Len() int {
	return len(pq)
}

func (pq PriorityQueue) Less(i, j int) bool {
	//High cost => Low priority
	return pq[i].cost > pq[j].cost
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
}

func (pq *PriorityQueue) Push(x Item) {
	*pq = append(*pq, x)
}

func (pq *PriorityQueue) Pop() Item {
	ret := (*pq)[pq.Len()-1]
	*pq = (*pq)[:pq.Len()-1]

	return ret
}
