package tiles

import (
	"encoding/json"
	"os"
)

type TileMapLayerJSON struct {
	Data   []int `json:"data"`
	Width  int   `json:"width"`
	Height int   `json:"height"`
}

type TitleMapJSON struct {
	Layers []TileMapLayerJSON `json:"layers"`
}

func NewTileMapJSON(filepath string) (TitleMapJSON, error) {
	content, err := os.ReadFile(filepath)
	if err != nil{
		return TitleMapJSON{}, err
	}
	var tileMapJSON TitleMapJSON
	err = json.Unmarshal(content, &tileMapJSON)
	if err != nil{
		return TitleMapJSON{}, err
	}
	return tileMapJSON, nil
}
