package main

import (
	"bytes"
	"compress/gzip"
	"encoding/binary"
	"io"
	"log"
	"math"
	"net/http"
	"net/url"
	"time"

	"github.com/eiannone/keyboard"
	"github.com/gorilla/websocket"
)

const targetURL = "ws://acds-mazerunner.1nf1n1ty.team/ws"

const MapWidth = 800
const MapHeight = 810

// Upgrade the incoming HTTP request to a WebSocket
var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

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

type FPoint struct {
	x, y float64
}

var serverConn *websocket.Conn
var goal Point
var path []Point
var mapData []byte
var counter uint64
var start = FPoint{0, 0}

func BytesToFloat64(b []byte) float64 {
	bits := binary.BigEndian.Uint64(b)
	return math.Float64frombits(bits)
}

func handleWebSocket(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Failed to upgrade connection:", err)
		return
	}
	defer conn.Close()

	u, err := url.Parse(targetURL)
	if err != nil {
		log.Println("Failed to parse target URL:", err)
		return
	}

	serverConn, _, err = websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		log.Println("Failed to connect to target service:", err)
		return
	}
	defer serverConn.Close()

	go func() {
		for {
			messageType, message, err := serverConn.ReadMessage()
			switch message[0] {

			case 0x2:
				mapData, _ = ungzipData(message[1:])
				mapDataInt := make([]int, MapHeight*MapWidth)

				for i, val := range mapData {
					if val == 8 {
						goal = Point{x: i / MapWidth, y: i % MapWidth}
					}
					mapDataInt[i] = int(val)
				}
				maze := make([][]int, MapHeight)
				start := Point{x: 0, y: 0}
				for i := 0; i < MapHeight; i++ {
					maze[i] = mapDataInt[i*MapWidth : (i+1)*MapWidth]
				}
				path, err = astar(maze, start, goal)
				if err != nil {
					log.Println(err)
				}
				if len(path) != 0 {
					log.Println("Found path for the flag")
				}

			case 1:
				start.x = BytesToFloat64(message[1:9])
				start.y = BytesToFloat64(message[9:17])
				log.Printf("[server]->[client]: (%f, %f)\t(%f, %f)\t(%d, %d)\n", start.x, start.y, start.x/16, start.y/16, int(start.x/16), int(start.y/16))
			case 153:
				log.Println(string(message[1:]))
			default:
				log.Println("UNKNOWN PACKET", message)
			}
			if err != nil {
				log.Println("Error reading from target:", err)
				return
			}

			if err := conn.WriteMessage(messageType, message); err != nil {
				log.Println("Error writing to client:", err)
				return
			}
		}
	}()

	for {
		messageType, message, err := conn.ReadMessage()
		if err != nil {
			log.Println("Error reading from client:", err)
			return
		}
		if message[0] == 1 {
			log.Printf("[client]->[server]: ")
			x := BytesToFloat64(message[2:10])
			y := BytesToFloat64(message[10:18])
			copy(message[18:], Uint64ToBytes(counter)[:])

			if message[1] == 0x1 {
				log.Printf("Up From %f, %f\n", x, y)
			}
			if message[1] == 0x2 {
				log.Printf("Down From %f, %f\n", x, y)
			}
			if message[1] == 0x3 {
				log.Printf("Right From %f, %f\n", x, y)
			}
			if message[1] == 0x4 {
				log.Printf("Left From %f, %f\n", x, y)
			}
			counter++
		} else {
			log.Printf("[client]->[server]: %v\n", message)
		}
		if err := serverConn.WriteMessage(messageType, message); err != nil {
			log.Println("Error writing to target:", err)
			return
		}
	}
}

func main() {
	// Set up the WebSocket proxy handler
	go listenForCheats()
	http.HandleFunc("/ws", handleWebSocket)
	// Start the HTTP server
	log.Println("WebSocket proxy server started on :8585")
	err := http.ListenAndServe(":8585", nil)
	if err != nil {
		log.Fatal("ListenAndServe:", err)
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

// func Teleport(x, y float64) {

// }
func Teleport(conn *websocket.Conn, x, y int) {
	for {
		if int(start.x) == x*16 && int(start.y) == y*16 {
			// log.Println("Got it", x, y, start)
			break
		}
		delX := float64(x*16) - start.x
		delY := float64(y*16) - start.y
		// log.Println("Delta Location: ", delX, delY)
		// log.Println("Player Location: ", start.x/16, start.y/16)
		var direction int
		if delX < 0 {
			direction = 0x4
		} else if delX > 0 {
			direction = 0x3
		} else if delY < 0 {
			direction = 0x1
		} else if delY > 0 {
			direction = 0x2
		}
		var buffer bytes.Buffer
		buffer.Reset()
		buffer.WriteByte(0x1)
		buffer.WriteByte(byte(direction))
		buffer.Write(Float64ToBytes(start.x))
		buffer.Write(Float64ToBytes(start.y))
		buffer.Write(Uint64ToBytes(uint64(counter)))
		err := conn.WriteMessage(websocket.BinaryMessage, buffer.Bytes())
		counter++
		time.Sleep(time.Millisecond * 10)
		if err != nil {
			log.Println("WriteMessage error:", err)
			return
		}
	}
}

func listenForCheats() {
	if err := keyboard.Open(); err != nil {
		log.Fatal(err)
	}
	defer keyboard.Close()
	for {
		char, key, err := keyboard.GetKey()
		if err != nil {
			log.Fatal(err)
		}
		if string(char) == "l" {
			log.Println("Going to flag")
			log.Println(path)
			for i, v := range path {
				log.Println(i)
				log.Println(v)
				Teleport(serverConn, v.y, v.x)
			}
		}

		if key == keyboard.KeyEsc {
			break
		}
	}
	log.Println("cheat code func exited.")

}
