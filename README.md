# AUKEY KM-G15 RGB Control

[中文版](README_CN.md)

A CLI tool for controlling RGB lighting on the AUKEY KM-G15 mechanical keyboard via USB HID.

## Features

- Switch between 3 profile slots
- Set lighting modes (19 effects)
- Adjust brightness, speed, direction
- Toggle Colorful mode (multi-color cycling)
- Configure USB polling rate (125-1000 Hz)
- Auto-detect active profile
- Read current device status

## Supported Keyboard

- **AUKEY KM-G15** (Sonix MCU)
- VID: `0x0C45`, PID: `0x7666`

## Installation

### Download Release

Download the latest binary for your platform from [Releases](https://github.com/ffexis/aukey-km-g15-rgb/releases).

### Build from Source

Requires Go 1.21+ and a C compiler (for CGO/hidapi).

```bash
cd go
make build
```

The binary will be output as `km-g15-rgb.exe` (Windows) or `km-g15-rgb` (Linux/macOS).

## Usage

```bash
km-g15-rgb <command> [flags]

Global Flags:
  --device <path>    Specific device path (if multiple keyboards)
  -p, --profile <n>  Target profile slot (0-2, default: auto-detect)
```

### Commands

| Command | Description |
|---------|-------------|
| `info` | Show connected device information |
| `status` | Read current device configuration |
| `mode <id>` | Set lighting effect mode (0-18, 20) |
| `brightness <0-4>` | Set brightness level |
| `speed <0-4>` | Set animation speed (0=slowest, 4=fastest) |
| `rate <hz>` | Set USB polling rate (125, 250, 500, 1000) |
| `profile <0-2>` | Switch active profile slot |
| `colorful <on\|off>` | Enable/disable Colorful mode |
| `list-modes` | List available lighting modes |

### Examples

```bash
# Show device info
km-g15-rgb info

# Read current status
km-g15-rgb status

# Set static mode on current profile
km-g15-rgb mode 6

# Set breathing mode on profile 1
km-g15-rgb mode 5 -p 1

# Set max brightness
km-g15-rgb brightness 4

# Set fastest speed
km-g15-rgb speed 4

# Set 1000Hz polling rate
km-g15-rgb rate 1000

# Enable Colorful mode
km-g15-rgb colorful on

# Switch to profile 2
km-g15-rgb profile 2
```

## Lighting Modes

| ID | Name (CN) | Name (EN) |
|----|-----------|-----------|
| 1 | 随波逐流 | Go with the stream |
| 2 | 彩云纷飞 | Clouds fly |
| 3 | 峰回路转 | Winding paths |
| 4 | 光之审判 | The trial of light |
| 5 | 呼吸 | Breathing |
| 6 | 常亮 | Normally on |
| 7 | 踏雪无痕 | Pass without trace |
| 8 | 泛起涟漪 | Ripple graff |
| 9 | 奔逸绝尘 | Fast run without trace |
| 10 | 繁星点点 | Snow winter jasmine |
| 11 | 百花争艳 | Flowers blooming |
| 12 | 流星赶月 | Swift action |
| 13 | 大鹏展翅 | Hurricane |
| 14 | 厚积薄发 | Accumulate |
| 15 | 落雨纷纷 | Digital Times |
| 16 | 左右逢缘 | Both ways |
| 17 | 众志成城 | Surmount |
| 18 | 速度激情 | Fast and the Furious |
| 20 | 指点江山 | Coastal |

## Parameter Ranges

| Parameter | Range | Description |
|-----------|-------|-------------|
| Brightness | 0-4 | 0=Min, 4=Max |
| Speed | 0-4 | 0=Slowest, 4=Fastest |
| USB Rate | 125/250/500/1000 | Hz |

## Protocol Documentation

See [docs/PROTOCOL.md](docs/PROTOCOL.md) for detailed protocol documentation.

## License

MIT License
