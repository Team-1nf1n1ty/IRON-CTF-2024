package main

import (
	"math"
	gamemaps "server/maps"
	"server/maze"
)

const POSITIONPACKETID = 0x1
const PINGPACKETID = 0x0
const GETRANDOMMAZE = 0x2
const FLAGPACKETID = 0x3
const ERROR = 0x99

const SPEED = 2

var MapTile, _ = gamemaps.NewTileMapJSON("./maps/map.json")

type PositionPacketFromClient struct {
	KeyPressed byte
	PlayerX    float64
	PlayerY    float64
}

type PositionPacketToClient struct {
	PacketType byte
	PlayerX    float64
	PlayerY    float64
}
type FlagPacket struct {
	flag    string
}

type TextPacket struct {
	data string
}

func (p TextPacket) ToBytes(prefix uint64) []byte {
	flag := []byte(p.data)
	packetData := append([]byte{byte(prefix)}, flag...)
	return packetData
}

func (p PositionPacketFromClient) ToBytes() []byte {
	packetData := append([]byte{POSITIONPACKETID, p.KeyPressed}, Float64ToBytes(p.PlayerX)...)
	packetData = append(packetData, Float64ToBytes(p.PlayerY)...)
	return packetData
}
func (p FlagPacket) ToBytes() []byte {
	flag := []byte(p.flag)
	packetData := append([]byte{FLAGPACKETID}, flag...)
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
