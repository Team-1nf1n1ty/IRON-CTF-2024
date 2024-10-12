package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	tiles "server/maps"
	"server/maze"
	// "time"
	"github.com/gorilla/websocket"
)

type Connection struct {
	conn        *websocket.Conn
	gamemap     []byte
	playerState *StateQueue
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
		log.Printf("error: %s", err)
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
			errorData := TextPacket{data: "Invalid Packet..."}.ToBytes(ERROR)
			connection.conn.WriteMessage(websocket.BinaryMessage, errorData)
			return
		}
		if connection.playerState == nil {
			connection.playerState = NewStateQueue(10)
		}
		presentPlayerPosition := PositionPacketFromClient{data[1], BytesToFloat64(data[2:10]), BytesToFloat64(data[10:18]), BytesToUint64(data[18:26])}
		connection.playerState.Enqueue(Cordinate{presentPlayerPosition.PlayerX, presentPlayerPosition.PlayerY, presentPlayerPosition.Index})
		// fmt.Printf("%v\n", connection.playerState.items)
		stateValidity := connection.playerState.IsValid()
		if !stateValidity {
			// fmt.Println(connection.playerState.items)
			errorData := TextPacket{data: "Invalid state cheating detected restart the game..."}.ToBytes(ERROR)
			connection.conn.WriteMessage(websocket.BinaryMessage, errorData)
			connection.conn.Close()
			return
		}
		nextMove, reachedFlag := presentPlayerPosition.Respond(connection)
		if reachedFlag {
			var FLAG = os.Getenv("FLAG")
			if FLAG == "" {
				FLAG = "ironCTF{TESTING}"
			}
			flagData := TextPacket{data: FLAG}.ToBytes(FLAGPACKETID)
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
			data, _ = gzipData(connection.gamemap)
			if err != nil {
				fmt.Printf("error: %v", err)
			}
			dataFinal := append([]byte{GETRANDOMMAZE}, data...)
			connection.conn.WriteMessage(websocket.BinaryMessage, dataFinal)
		} else {
			errorData := TextPacket{data: "Map Already sent"}.ToBytes(ERROR)
			connection.conn.WriteMessage(websocket.BinaryMessage, errorData)
		}
	default:
		errorData := TextPacket{data: "Something went wrong restart the game"}.ToBytes(ERROR)
		connection.conn.WriteMessage(websocket.BinaryMessage, errorData)
	}
}

// func GetUsersCount() {
// 	for {
// 		time.Sleep(time.Second * 2)
// 		log.Printf("Users: %d", Total)
// 	}
// }

func main() {
	// go GetUsersCount()
	http.HandleFunc("/ws", websocketHandler)
	log.Printf("Deployment Is Ready For Maze Runner V2 Challenge, SPEED %d", SPEED)
	err := http.ListenAndServe(":8000", nil)
	if err != nil {
		fmt.Errorf("%s", err)
	}
}
