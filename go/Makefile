VERSION ?= $(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")
LDFLAGS := -ldflags "-s -w -X github.com/ffexis/aukey-km-g15-rgb/cmd.Version=$(VERSION)"

.PHONY: build build-all clean

build:
	CGO_ENABLED=1 go build $(LDFLAGS) -o km-g15-rgb.exe .

build-all: build-linux build-windows build-macos

build-linux:
	CGO_ENABLED=1 GOOS=linux GOARCH=amd64 go build $(LDFLAGS) -o km-g15-rgb-linux-amd64 .

build-windows:
	CGO_ENABLED=1 GOOS=windows GOARCH=amd64 go build $(LDFLAGS) -o km-g15-rgb-windows-amd64.exe .

build-macos:
	CGO_ENABLED=1 GOOS=darwin GOARCH=amd64 go build $(LDFLAGS) -o km-g15-rgb-darwin-amd64 .

clean:
	rm -f km-g15-rgb km-g15-rgb.exe km-g15-rgb-linux-amd64 km-g15-rgb-windows-amd64.exe km-g15-rgb-darwin-amd64
