package main

import (
	"encoding/json"
	"errors"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"sync"
	"time"
)

const (
	bindAddress = "0.0.0.0:5000"
	maxBodySize = 10 * 1024 * 1024 // 10MB limit (NIST SP 800-218 DoS protection)
)

type DataStore struct {
	Attendances []json.RawMessage `json:"attendances"`
	Network     []json.RawMessage `json:"network"`
}

type APIResponse struct {
	OK    bool   `json:"ok"`
	Error string `json:"error,omitempty"`
}

type AppServer struct {
	filePath string
	mu       sync.RWMutex
}

func NewAppServer(dataPath string) *AppServer {
	return &AppServer{
		filePath: dataPath,
	}
}

func (s *AppServer) readData() DataStore {
	s.mu.RLock()
	defer s.mu.RUnlock()

	fallback := DataStore{
		Attendances: make([]json.RawMessage, 0),
		Network:     make([]json.RawMessage, 0),
	}

	rawBytes, err := os.ReadFile(s.filePath)
	if err != nil {
		return fallback
	}

	var data DataStore
	if err := json.Unmarshal(rawBytes, &data); err != nil {
		return fallback
	}

	if data.Attendances == nil {
		data.Attendances = make([]json.RawMessage, 0)
	}
	if data.Network == nil {
		data.Network = make([]json.RawMessage, 0)
	}

	return data
}

func (s *AppServer) writeData(data DataStore) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if data.Attendances == nil {
		data.Attendances = make([]json.RawMessage, 0)
	}
	if data.Network == nil {
		data.Network = make([]json.RawMessage, 0)
	}

	encoded, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		return err
	}

	dir := filepath.Dir(s.filePath)
	tmpFile, err := os.CreateTemp(dir, "integravida_data_*.tmp")
	if err != nil {
		return err
	}
	tmpPath := tmpFile.Name()

	defer func() {
		if tmpPath != "" {
			_ = os.Remove(tmpPath)
		}
	}()

	if _, err := tmpFile.Write(encoded); err != nil {
		_ = tmpFile.Close()
		return err
	}

	if err := tmpFile.Sync(); err != nil {
		_ = tmpFile.Close()
		return err
	}

	if err := tmpFile.Close(); err != nil {
		return err
	}

	if err := os.Rename(tmpPath, s.filePath); err != nil {
		return err
	}

	tmpPath = ""
	return nil
}

func (s *AppServer) setSecurityHeaders(w http.ResponseWriter) {
	w.Header().Set("Cache-Control", "no-cache, no-store, must-revalidate")
	w.Header().Set("Pragma", "no-cache")
	w.Header().Set("Expires", "0")
	w.Header().Set("X-Content-Type-Options", "nosniff")
	w.Header().Set("X-Frame-Options", "DENY")
}

func (s *AppServer) writeJSON(w http.ResponseWriter, status int, payload interface{}) {
	s.setSecurityHeaders(w)
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}

func (s *AppServer) handleAPIData(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		data := s.readData()
		s.writeJSON(w, http.StatusOK, data)

	case http.MethodPut:
		r.Body = http.MaxBytesReader(w, r.Body, maxBodySize)
		bodyBytes, err := io.ReadAll(r.Body)
		if err != nil {
			s.writeJSON(w, http.StatusBadRequest, APIResponse{OK: false, Error: "Payload excessivo ou inválido."})
			return
		}

		var incoming DataStore
		if err := json.Unmarshal(bodyBytes, &incoming); err != nil {
			s.writeJSON(w, http.StatusBadRequest, APIResponse{OK: false, Error: "Não foi possível salvar os dados."})
			return
		}

		if incoming.Attendances == nil {
			s.writeJSON(w, http.StatusBadRequest, APIResponse{OK: false, Error: "Não foi possível salvar os dados."})
			return
		}

		if err := s.writeData(incoming); err != nil {
			s.writeJSON(w, http.StatusInternalServerError, APIResponse{OK: false, Error: "Não foi possível salvar os dados."})
			return
		}

		s.writeJSON(w, http.StatusOK, APIResponse{OK: true})

	default:
		s.writeJSON(w, http.StatusMethodNotAllowed, APIResponse{OK: false, Error: "Método não permitido."})
	}
}

func main() {
	execPath, err := os.Executable()
	if err != nil {
		execPath = "."
	}
	baseDir := filepath.Dir(execPath)
	dataFilePath := filepath.Join(baseDir, "integravida_data.json")

	server := NewAppServer(dataFilePath)
	mux := http.NewServeMux()

	mux.HandleFunc("/api/data", server.handleAPIData)

	fileServer := http.FileServer(http.Dir(baseDir))
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		server.setSecurityHeaders(w)
		fileServer.ServeHTTP(w, r)
	})

	httpServer := &http.Server{
		Addr:              bindAddress,
		Handler:           mux,
		ReadHeaderTimeout: 5 * time.Second,
		ReadTimeout:       15 * time.Second,
		WriteTimeout:      15 * time.Second,
		IdleTimeout:       60 * time.Second,
	}

	log.Printf("Server running at http://%s/\n", bindAddress)
	if err := httpServer.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
		log.Fatalf("HTTP server failed: %v", err)
	}
}