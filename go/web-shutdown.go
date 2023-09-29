package main

import (
	"log"
	"net/http"
	"os/exec"
	"runtime"
)

func main() {
	http.HandleFunc("/", homeHandler)
	http.HandleFunc("/shutdown", shutdownHandler)

	addr := "localhost:8080" // Replace with your desired address

	log.Printf("Server started at http://%s\n", addr)
	log.Fatal(http.ListenAndServe(addr, nil))
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
	message := "Make a POST request to /shutdown to shutdown the PC"
	_, _ = w.Write([]byte(message))
}

func shutdownHandler(w http.ResponseWriter, r *http.Request) {
	switch runtime.GOOS {
	case "windows":
		exec.Command("shutdown", "/s", "/t", "0").Run()
	case "darwin", "linux":
		exec.Command("shutdown", "-h", "now").Run()
	default:
		message := "Shutdown not supported on this operating system."
		http.Error(w, message, http.StatusInternalServerError)
		return
	}

	message := "Shutdown request received. The PC will shut down shortly."
	_, _ = w.Write([]byte(message))
}
