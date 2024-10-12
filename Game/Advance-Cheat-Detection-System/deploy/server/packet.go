package main

import (
	"errors"
	"fmt"
	"log"
	"math"
	gamemaps "server/maps"
	"server/maze"
	"sort"
)

const POSITIONPACKETID = 0x1
const PINGPACKETID = 0x0
const GETRANDOMMAZE = 0x2
const FLAGPACKETID = 0x3
const ERROR = 0x99

const SPEED = 8

var MapTile, _ = gamemaps.NewTileMapJSON("./maps/map.json")

type PositionPacketFromClient struct {
	KeyPressed byte
	PlayerX    float64
	PlayerY    float64
	Index      uint64
}

type PositionPacketToClient struct {
	PacketType byte
	PlayerX    float64
	PlayerY    float64
}
type TextPacket struct {
	data string
}

func (p PositionPacketFromClient) ToBytes() []byte {
	packetData := append([]byte{POSITIONPACKETID, p.KeyPressed}, Float64ToBytes(p.PlayerX)...)
	packetData = append(packetData, Float64ToBytes(p.PlayerY)...)
	return packetData
}
func (p TextPacket) ToBytes(prefix uint64) []byte {
	flag := []byte(p.data)
	packetData := append([]byte{byte(prefix)}, flag...)
	return packetData
}
func (p PositionPacketToClient) ToBytes() []byte {
	packetData := append([]byte{p.PacketType}, Float64ToBytes(p.PlayerX)...)
	packetData = append(packetData, Float64ToBytes(p.PlayerY)...)
	return packetData
}

func (p PositionPacketFromClient) Respond(clientConn *Connection) (PositionPacketToClient, bool) {
	newX := p.PlayerX
	newY := p.PlayerY
	switch p.KeyPressed {
	case 0x01:
		newY = p.PlayerY - SPEED
	case 0x02:
		newY = p.PlayerY + SPEED
	case 0x03:
		newX = p.PlayerX + SPEED
	case 0x04:
		newX = p.PlayerX - SPEED
	}
	log.Println(newX, newY)
	walkAble, reachedFlag := p.tileValue(newX, newY, clientConn)

	if walkAble {
		return PositionPacketToClient{POSITIONPACKETID, newX, newY}, reachedFlag
	} else {
		return PositionPacketToClient{POSITIONPACKETID, p.PlayerX, p.PlayerY}, reachedFlag
	}
}

func (p PositionPacketFromClient) tileValue(x, y float64, clientConn *Connection) (bool, bool) {
	if x < 0 || y < 0 {
		return false, false
	}

	tileIndexCheck := []int{
		int(math.Ceil(y/16))*MapTile.Layers[0].Width + int(math.Ceil(x/16)),
		int(math.Floor(y/16))*MapTile.Layers[0].Width + int(math.Floor(x/16)),
		int(math.Ceil(y/16))*MapTile.Layers[0].Width + int(math.Floor(x/16)),
		int(math.Floor(y/16))*MapTile.Layers[0].Width + int(math.Ceil(x/16)),
	}
	for _, val := range tileIndexCheck {
		if val < 0 {
			return false, false
		}
		if val >= len(clientConn.gamemap) {
			return false, false
		}
		if clientConn.gamemap[val] == maze.Wall {
			return false, false
		}
		if clientConn.gamemap[val] == maze.FlagTile {
			return true, true
		}
	}
	return true, false
}

type StateQueue struct {
	items []Cordinate
	size  int
}

type Cordinate struct {
	X float64
	Y float64
	id uint64
}

func (c *Cordinate) Distance(x2 Cordinate) float64 {
	return math.Sqrt(math.Pow(c.X-x2.X, 2) + math.Pow(c.Y-x2.Y, 2))
}

func NewStateQueue(size int) *StateQueue {
	return &StateQueue{
		items: make([]Cordinate, 0, size),
		size:  size,
	}
}

func (q *StateQueue) Enqueue(item Cordinate) {
	if len(q.items) == q.size {
		q.items = q.items[1:]
	}
	q.items = append(q.items, item)
	sort.Slice(q.items, func(i, j int) bool {
		return q.items[i].id < q.items[j].id
	})
}

func (q *StateQueue) Dequeue() (Cordinate, error) {
	if len(q.items) == 0 {
		return Cordinate{}, errors.New("queue is empty")
	}

	item := q.items[0]
	q.items = q.items[1:]
	return item, nil
}

func (q *StateQueue) IsEmpty() bool {
	return len(q.items) == 0
}
func (q *StateQueue) IsValid() bool {
	queueSize := q.Size()
	if queueSize == 1 {
		return q.items[0].X == 0 && q.items[0].Y == 0
	}
	distanceTraved := q.items[queueSize-2].Distance(q.items[queueSize-1])
	if distanceTraved == SPEED || distanceTraved == 0 {
		return distanceTraved == SPEED || distanceTraved == 0
	} else {
		fmt.Printf("Error distanceTraved: %f\n", distanceTraved)
		return false
	}
}

func (q *StateQueue) Size() int {
	return len(q.items)
}
