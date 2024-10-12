package main

import (
	"log"
	"net/http"
	"os"
	tiles "server/maps"
	"server/maze"
	"time"
	"github.com/gorilla/websocket"
)

type Connection struct {
	conn    *websocket.Conn
	gamemap []byte
}

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

var Total int = 0
var CloseErrorCode = []int{1000, 1001, 1002, 1003, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1015}

func websocketHandler(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Fatal(err)
		return
	}
	Total++
	defer func() { conn.Close(); Total-- }()
	log.Printf("connetion opened from: %v and users: %d", conn.RemoteAddr(), Total)
	connection := &Connection{
		conn: conn,
	}
	for {
		_, data, err := conn.ReadMessage()
		if err != nil {
			if websocket.IsCloseError(err, CloseErrorCode...) {
				log.Printf("%s from: %s", err, conn.RemoteAddr())
				break
			}
			log.Printf("error dealing with reading msg: %s", err)
			break
		}
		parseMessage(data, connection)
	}

}

// 0x99 response means unable to parse the packet
// 0x01 response means unable to parse the packet
// 0x00 response means unable to parse the packet
func parseMessage(data []byte, connection *Connection) {
	switch data[0] {
	case POSITIONPACKETID:
		if len(data) != 26 {
			connection.conn.WriteMessage(websocket.BinaryMessage, []byte{ERROR})
			return
		}
		presentPlayerPosition := PositionPacketFromClient{data[1], BytesToFloat64(data[2:10]), BytesToFloat64(data[10:18])}
		nextMove, reachedFlag := presentPlayerPosition.Respond(connection)
		if reachedFlag {
			var FLAG = os.Getenv("FLAG")
			if FLAG == "" {
				FLAG = "ironCTF{TESTING}"
			}
			flagData := FlagPacket{flag: FLAG}.ToBytes()
			connection.conn.WriteMessage(websocket.BinaryMessage, flagData)
		}
		nextMoveData := nextMove.ToBytes()
		connection.conn.WriteMessage(websocket.BinaryMessage, nextMoveData)
	case PINGPACKETID:
		connection.conn.WriteMessage(websocket.BinaryMessage, data)
	case GETRANDOMMAZE:
		if connection.gamemap == nil {
			var MapTile, err = tiles.NewTileMapJSON("./maps/map.json")
			if err != nil {
				log.Fatalf("Map file not present")
			}
			mazeData := maze.FlattenMaze(MapTile.Layers[0].Data)
			connection.gamemap = *mazeData
			encoded_map, _ := gzipData(connection.gamemap)
			dataFinal := append([]byte{GETRANDOMMAZE}, encoded_map...)
			connection.conn.WriteMessage(websocket.BinaryMessage, dataFinal)
		} else {
			errorData := TextPacket{data: "Map Already sent"}.ToBytes(ERROR)
			connection.conn.WriteMessage(websocket.BinaryMessage, errorData)
		}
	default:
		connection.conn.WriteMessage(websocket.BinaryMessage, []byte{ERROR})
	}
}

func GetUsersCount() {
	for {
		time.Sleep(time.Second * 2)
		log.Printf("Users: %d", Total)
	}
}

func main() {
	go GetUsersCount()
	http.HandleFunc("/ws", websocketHandler)
	log.Printf("Deployment Is Ready For Maze Runner Challenge")
	http.ListenAndServe(":8000", nil)
}
