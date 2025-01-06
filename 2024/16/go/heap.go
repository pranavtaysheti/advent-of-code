package main

type Item[T any] struct {
	cost int
	item *T
}

type PriorityQueue[T any] []Item[T]

func (pq PriorityQueue[T]) Len() int {
	return len(pq)
}

func (pq PriorityQueue[T]) Less(i, j int) bool {
	//High cost => Low priority
	return pq[i].cost > pq[j].cost
}

func (pq PriorityQueue[T]) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
}

func (pq *PriorityQueue[T]) Push(x any) {
	*pq = append(*pq, x.(Item[T]))
}

func (pq *PriorityQueue[T]) Pop() any {
	ret := (*pq)[pq.Len()-1]
	*pq = (*pq)[:pq.Len()-1]

	return ret
}
