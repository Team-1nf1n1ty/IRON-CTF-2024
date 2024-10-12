package maze

import (
	"fmt"
	"math/rand"
	"time"
)

const (
	width       = 400
	height      = 400
	Wall        = 3
	WalkingCell = 0
	unvisited   = 2
	FlagTile    = 8
)

type Point struct {
	x, y int
}

var maze [height][width]int

func PrintMaze() {
	for i := 0; i < height; i++ {
		for j := 0; j < width; j++ {
			if maze[i][j] == unvisited {
				fmt.Print("u", " ")
			} else if maze[i][j] == WalkingCell {
				fmt.Print("c", " ")
			} else {
				fmt.Print("w", " ")
			}
		}
		fmt.Println()
	}
	fmt.Println(maze)
}
func FlattenMaze(mapArray []int) *[]byte {
	getRandomMaze()
	rowIndex := 0
	mapArrayBytes := make([]byte, len(mapArray))
	rand.New(rand.NewSource(time.Now().UnixNano()))
	randomIndex := rand.Intn(4000)
	flagIndex := len(mapArray) + randomIndex - 4000

	for i, value := range mapArray {
		if value == 14 {
			currentRow := maze[rowIndex/2]
			doubled := make([]int, len(currentRow)*2)
			for i, val := range currentRow {
				doubled[i*2] = val
				doubled[i*2+1] = val
			}
			copy(mapArray[i:i+width*2+1], doubled[:])
			rowIndex++
			if rowIndex >= height*2 {
				break
			}
		}

	}
	for i, v := range mapArray {
		if v == 8 {
			if i != flagIndex {
				mapArrayBytes[i] = byte(0)
			} else {
				mapArrayBytes[i] = byte(v)
			}
		} else {
			mapArrayBytes[i] = byte(v)
		}
	}

	return &mapArrayBytes
}

func surroundingCells(randWall Point) int {
	sCells := 0
	if maze[randWall.x-1][randWall.y] == WalkingCell {
		sCells++
	}
	if maze[randWall.x+1][randWall.y] == WalkingCell {
		sCells++
	}
	if maze[randWall.x][randWall.y-1] == WalkingCell {
		sCells++
	}
	if maze[randWall.x][randWall.y+1] == WalkingCell {
		sCells++
	}
	return sCells
}

func getRandomMaze() {
	// Seed random number generator
	rand.Seed(time.Now().UnixNano())

	// Initialize the maze with unvisited cells
	for i := range maze {
		for j := range maze[i] {
			maze[i][j] = unvisited
		}
	}

	// Randomize starting point and set it as a WalkingCell
	startX := rand.Intn(height)
	startY := rand.Intn(width)
	if startX == 0 {
		startX++
	}
	if startX == height-1 {
		startX--
	}
	if startY == 0 {
		startY++
	}
	if startY == width-1 {
		startY--
	}
	maze[startX][startY] = WalkingCell

	// List of walls
	var walls []Point
	walls = append(walls, Point{startX - 1, startY})
	walls = append(walls, Point{startX, startY - 1})
	walls = append(walls, Point{startX, startY + 1})
	walls = append(walls, Point{startX + 1, startY})

	// Denote walls in the maze
	maze[startX-1][startY] = Wall
	maze[startX][startY-1] = Wall
	maze[startX][startY+1] = Wall
	maze[startX+1][startY] = Wall

	for len(walls) > 0 {
		// Pick a random wall
		randIndex := rand.Intn(len(walls))
		randWall := walls[randIndex]

		// Check if it is a valid wall
		if randWall.y > 0 && randWall.y < width-1 && randWall.x > 0 && randWall.x < height-1 {
			// Ensure that the wall has only one adjacent WalkingCell
			if maze[randWall.x][randWall.y-1] == unvisited && maze[randWall.x][randWall.y+1] == WalkingCell ||
				maze[randWall.x][randWall.y+1] == unvisited && maze[randWall.x][randWall.y-1] == WalkingCell ||
				maze[randWall.x-1][randWall.y] == unvisited && maze[randWall.x+1][randWall.y] == WalkingCell ||
				maze[randWall.x+1][randWall.y] == unvisited && maze[randWall.x-1][randWall.y] == WalkingCell {

				// Surrounding cells
				sCells := surroundingCells(randWall)

				if sCells < 2 {
					// Convert unvisited WalkingCell to passage
					maze[randWall.x][randWall.y] = WalkingCell

					// Add neighboring walls to the list
					if randWall.x > 1 && maze[randWall.x-1][randWall.y] == unvisited {
						maze[randWall.x-1][randWall.y] = Wall
						walls = append(walls, Point{randWall.x - 1, randWall.y})
					}
					if randWall.x < height-2 && maze[randWall.x+1][randWall.y] == unvisited {
						maze[randWall.x+1][randWall.y] = Wall
						walls = append(walls, Point{randWall.x + 1, randWall.y})
					}
					if randWall.y > 1 && maze[randWall.x][randWall.y-1] == unvisited {
						maze[randWall.x][randWall.y-1] = Wall
						walls = append(walls, Point{randWall.x, randWall.y - 1})
					}
					if randWall.y < width-2 && maze[randWall.x][randWall.y+1] == unvisited {
						maze[randWall.x][randWall.y+1] = Wall
						walls = append(walls, Point{randWall.x, randWall.y + 1})
					}
				}
			}
		}

		// Remove the wall from the list
		walls = append(walls[:randIndex], walls[randIndex+1:]...)
	}

	// Mark the remaining unvisited cells as walls
	for i := 0; i < height; i++ {
		for j := 0; j < width; j++ {
			if maze[i][j] == unvisited {
				maze[i][j] = Wall
			}
		}
	}

	// Set entrance and exit
	for i := 0; i < width; i++ {
		if maze[1][i] == WalkingCell {
			maze[0][i] = WalkingCell
			break
		}
	}

	for i := width - 1; i >= 0; i-- {
		if maze[height-2][i] == WalkingCell {
			maze[height-1][i] = WalkingCell
			break
		}
	}

}
