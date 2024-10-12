package main

import (
	"bufio"
	"container/heap"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// Priority Queue for A* algorithm
type Item struct {
	point    Point
	priority int
	index    int
}

type PriorityQueue []*Item

func (pq PriorityQueue) Len() int           { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool { return pq[i].priority < pq[j].priority }
func (pq PriorityQueue) Swap(i, j int)      { pq[i], pq[j] = pq[j], pq[i]; pq[i].index = i; pq[j].index = j }

func (pq *PriorityQueue) Push(x interface{}) {
	n := len(*pq)
	item := x.(*Item)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil
	item.index = -1
	*pq = old[0 : n-1]
	return item
}

// Point represents a cell in the maze
type Point struct {
	x, y int
}

// A* algorithm
func astar(maze [][]int, start, goal Point) ([]Point, error) {
	directions := []Point{{-1, 0}, {1, 0}, {0, -1}, {0, 1}} // Up, Down, Left, Right
	openSet := &PriorityQueue{}
	heap.Push(openSet, &Item{
		point:    start,
		priority: 0,
	})
	cameFrom := make(map[Point]Point)
	gScore := make(map[Point]int)
	fScore := make(map[Point]int)
	gScore[start] = 0
	fScore[start] = heuristic(start, goal)

	for openSet.Len() > 0 {
		current := heap.Pop(openSet).(*Item).point

		if current == goal {
			return reconstructPath(cameFrom, current), nil
		}

		for _, dir := range directions {
			neighbor := Point{current.x + dir.x, current.y + dir.y}
			if neighbor.x >= 0 && neighbor.x < len(maze) && neighbor.y >= 0 && neighbor.y < len(maze[0]) && maze[neighbor.x][neighbor.y] != 3 {
				tentativeGScore := gScore[current] + 1
				if _, ok := gScore[neighbor]; !ok || tentativeGScore < gScore[neighbor] {
					cameFrom[neighbor] = current
					gScore[neighbor] = tentativeGScore
					fScore[neighbor] = tentativeGScore + heuristic(neighbor, goal)
					heap.Push(openSet, &Item{
						point:    neighbor,
						priority: fScore[neighbor],
					})
				}
			}
		}
	}

	return nil, fmt.Errorf("no path found")
}

func heuristic(a, b Point) int {
	return abs(a.x-b.x) + abs(a.y-b.y)
}

func reconstructPath(cameFrom map[Point]Point, current Point) []Point {
	var path []Point
	for current != (Point{}) {
		path = append([]Point{current}, path...)
		current = cameFrom[current]
	}
	return append([]Point{{0,0}}, path...)
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func readMaze(filePath string) ([][]int, int, int, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, 0, 0, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Scan()
	line := scanner.Text()
	values := strings.Fields(line)
	maze1D := make([]int, len(values))
	for i, v := range values {
		maze1D[i], err = strconv.Atoi(v)
		if err != nil {
			return nil, 0, 0, err
		}
	}

	scanner.Scan()
	dims := strings.Fields(scanner.Text())
	height, err := strconv.Atoi(dims[0])
	if err != nil {
		return nil, 0, 0, err
	}
	width, err := strconv.Atoi(dims[1])
	if err != nil {
		return nil, 0, 0, err
	}

	maze := make([][]int, height)
	for i := 0; i < height; i++ {
		maze[i] = maze1D[i*width : (i+1)*width]
	}

	return maze, height, width, nil
}

func writeSolutionToFile(path []Point, goal Point, outputFile string) error {
	file, err := os.Create(outputFile)
	if err != nil {
		return err
	}
	defer file.Close()

	writer := bufio.NewWriter(file)
	for _, p := range path {
		_, err := writer.WriteString(fmt.Sprintf("%d,%d\n", p.x, p.y))
		if err != nil {
			return err
		}
	}
	// Write the goal coordinate as the last entry
	_, err = writer.WriteString(fmt.Sprintf("%d,%d\n", goal.x, goal.y))
	if err != nil {
		return err
	}
	return writer.Flush()
}

// func main() {
// 	// inputFilePath := "maze_1d.txt"
// 	outputFilePath := "solution_path.txt"

// 	maze, height, width, err := readMaze(inputFilePath)
// 	if err != nil {
// 		fmt.Println("Error reading maze:", err)
// 		return
// 	}

// 	var start, goal Point
// 	startFound, goalFound := false, false

// 	for i := 0; i < height; i++ {
// 		for j := 0; j < width; j++ {
// 			if maze[i][j] == 0 && !startFound {
// 				start = Point{x: i, y: j}
// 				startFound = true
// 			} else if maze[i][j] == 8 {
// 				goal = Point{x: i, y: j}
// 				goalFound = true
// 			}
// 		}
// 	}

// 	path, err := astar(maze, start, goal)
// 	if err != nil {
// 		fmt.Println(err)
// 		return
// 	}

// 	fmt.Println("Path found. Writing to file...")
// 	err = writeSolutionToFile(path, goal, outputFilePath)
// 	if err != nil {
// 		fmt.Println("Error writing to file:", err)
// 	}
// }
