package main

import (
	"encoding/csv"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"time"
)

type imageDownloadResult struct {
	Id   string
	Data []byte
	Err  error
}

var (
	csvPath       string
	outputPath    string
	limit         int
	offset        int
	cached        bool
	sleepInterval time.Duration
)

func init() {
	flag.StringVar(&csvPath, "file", "", "Path to the csv file")
	flag.StringVar(&outputPath, "output", "", "Path to the output directory")
	flag.IntVar(&limit, "limit", 200, "Limit of the number of images to be indexed")
	flag.IntVar(&offset, "offset", 0, "Offset of the images to be indexed")
	flag.BoolVar(&cached, "cached", false, "Whether to use cached files")
	flag.DurationVar(&sleepInterval, "sleep", 100*time.Millisecond, "Sleep interval between image downloads")
	flag.Parse()
}

func main() {
	fileInfo, err := os.Stat(outputPath)
	if err != nil {
		panic(err)
	}

	if !fileInfo.IsDir() {
		panic("Output path is not a directory")
	}

	ch := make(chan imageDownloadResult, limit)

	readCsvFile(csvPath, offset, limit, func(row []string) bool {
		id := row[0]
		url := row[1]

		if id == "" || url == "" || len(url) < 7 {
			return false
		}

		go downloadImage(id, url, outputPath, cached, ch)
		time.Sleep(sleepInterval)

		return true
	})

	for i := 0; i < limit; i++ {
		result := <-ch
		if result.Err != nil {
			fmt.Printf("Error downloading image %s: %v\n", result.Id, result.Err)
			continue
		}

		imagePath := outputPath + "/" + result.Id + ".jpg"

		err = ioutil.WriteFile(imagePath, result.Data, 0644)

		if err != nil {
			fmt.Printf("Error writing image %s to disk: %v\n", result.Id, err)
		}
	}

}

func downloadImage(id, url string, outputDir string, cached bool, ch chan imageDownloadResult) {
	outputPath := outputDir + "/" + id + ".jpg"
	if cached {
		if _, err := os.Stat(outputPath); err == nil {
			// Already downloaded.
			file, err := os.Open(outputPath)
			if err == nil {
				defer file.Close()

				data, err := ioutil.ReadAll(file)
				if err == nil {
					fmt.Printf("Loaded image %s from %s\n", id, outputPath)
					ch <- imageDownloadResult{Id: id, Data: data, Err: nil}
					return
				}
			}

			fmt.Printf("Failed to open file %s from disk: %v\n", outputPath, err)
		}
	}

	// Download from the internet.
	resp, err := http.Get(url)
	if err != nil {
		ch <- imageDownloadResult{Id: id, Err: err}
		return
	}

	defer resp.Body.Close()

	out, err := os.Create(outputDir + "/" + id + ".jpg")
	if err != nil {
		ch <- imageDownloadResult{Id: id, Err: err}
		return
	}
	defer out.Close()

	data, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		ch <- imageDownloadResult{Id: id, Err: err}
		return
	}

	err = ioutil.WriteFile(outputDir+"/"+id+".jpg", data, 0644)
	if err != nil {
		ch <- imageDownloadResult{Id: id, Err: err}
		return
	}

	fmt.Printf("Downloaded image %s\n", id)

	ch <- imageDownloadResult{Id: id, Data: data, Err: nil}
}

func readCsvFile(path string, offset, limit int, iterator func([]string) bool) error {
	csvFile, err := os.Open(path)
	if err != nil {
		return err
	}
	defer csvFile.Close()

	reader := csv.NewReader(csvFile)
	currentIndex := 0

	for {
		if currentIndex < offset {
			currentIndex++
			continue
		} else if limit > 0 && currentIndex >= offset+limit {
			break
		}

		record, err := reader.Read()
		if err == io.EOF {
			break
		}

		if err != nil {
			return err
		}

		if increase := iterator(record); increase {
			currentIndex++
		}
	}

	return nil
}
