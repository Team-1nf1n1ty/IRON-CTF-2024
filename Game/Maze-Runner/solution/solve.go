package main

import (
	"bytes"
	"compress/gzip"
	"encoding/binary"
	"fmt"
	"github.com/gorilla/websocket"
	"io"
	"log"
	"math"
)

const MapWidth = 800
const MapHeight = 810

func ungzipData(compressedData []byte) ([]byte, error) {
	buf := bytes.NewBuffer(compressedData)
	reader, err := gzip.NewReader(buf)
	if err != nil {
		return nil, err
	}
	defer reader.Close()

	var result bytes.Buffer
	_, err = io.Copy(&result, reader)
	if err != nil {
		return nil, err
	}

	return result.Bytes(), nil
}

func readMessages(conn *websocket.Conn, done chan struct{}) {
	defer close(done)
	for {
		_, state, err := conn.ReadMessage()
		if err != nil {
			log.Println("ReadMessage error:", err)
			return
		}
		parse(state, conn, done)
	}
}

func parse(state []byte, conn *websocket.Conn, done chan struct{}) {
	switch state[0] {
	case 0x2:
		mapData, _ := ungzipData(state[1:])
		for i, val := range mapData {
			if val == 8 {
				flagX := (i % MapWidth) * 16
				flagY := (i / MapWidth) * 16
				fmt.Println(flagX, flagY)
				Teleport(conn, flagX, flagY)
			}
		}
	case 0x3:
		fmt.Println(string(state[1:]))
		close(done)
	default:
		fmt.Println(state)
	}
}

func Float64ToBytes(f float64) []byte {
	bits := math.Float64bits(f)
	bytesBuf := make([]byte, 8)
	binary.BigEndian.PutUint64(bytesBuf, bits)
	return bytesBuf
}

func Uint64ToBytes(u uint64) []byte {
	bytes := make([]byte, 8)
	binary.BigEndian.PutUint64(bytes, u)
	return bytes
}
func Teleport(conn *websocket.Conn, x, y int) {
	var buffer bytes.Buffer
	for i := 0; i < 10; i++ {
		buffer.Reset()
		buffer.WriteByte(0x1)
		buffer.WriteByte(0x2)
		buffer.Write(Float64ToBytes(float64(x)))
		buffer.Write(Float64ToBytes(float64(y - i)))
		buffer.Write(Uint64ToBytes(uint64(i)))
		err := conn.WriteMessage(websocket.BinaryMessage, buffer.Bytes())
		if err != nil {
			log.Println("WriteMessage error:", err)
			return
		}
	}
}

func main() {
	serverURL := "ws://mazerunner.1nf1n1ty.team/ws"
	done := make(chan struct{})
	conn, _, err := websocket.DefaultDialer.Dial(serverURL, nil)
	if err != nil {
		log.Fatal("Dial error:", err)
	}
	defer conn.Close()

	go readMessages(conn, done)

	err = conn.WriteMessage(websocket.BinaryMessage, []byte{0x2})
	if err != nil {
		log.Println("WriteMessage error:", err)
	}
	
	<-done
}
