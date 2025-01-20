package main

type Item[T any] struct {
	cost int
	item *T
}

type priorityQueue[T any] []Item[T]

func (pq priorityQueue[T]) Len() int {
	return len(pq)
}

func (pq priorityQueue[T]) Less(i, j int) bool {
	//High cost => Low priority
	return pq[i].cost > pq[j].cost
}

func (pq priorityQueue[T]) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
}

func (pq *priorityQueue[T]) Push(x any) {
	*pq = append(*pq, x.(Item[T]))
}

func (pq *priorityQueue[T]) pushItem(i Item[T]) {
	pq.pushItem(i)
}

func (pq *priorityQueue[T]) Pop() any {
	ret := (*pq)[pq.Len()-1]
	*pq = (*pq)[:pq.Len()-1]

	return ret
}

func (pq *priorityQueue[T]) popItem() Item[T] {
	return pq.Pop().(Item[T])
}
