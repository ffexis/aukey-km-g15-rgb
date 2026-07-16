# AUKEY KM-G15 RGB Control / AUKEY KM-G15 RGB 控制工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Python CLI tool for controlling RGB lighting on the AUKEY KM-G15 mechanical keyboard via USB HID.

用于通过 USB HID 控制 AUKEY KM-G15 机械键盘 RGB 灯效的 Python CLI 工具。

## Features / 功能

- Switch between 3 profile slots / 切换 3 个配置文件槽位
- Set lighting modes (19 effects) / 设置灯效模式（19 种效果）
- Adjust speed/brightness / 调整速度/亮度
- Configure USB polling rate (125-1000 Hz) / 配置 USB 回报率
- Read current device status / 读取当前设备状态

## Supported Keyboard / 支持的键盘

- **AUKEY KM-G15** (Sonix MCU)
- VID: `0x0C45`, PID: `0x7666`

## Installation / 安装

```bash
git clone https://github.com/your-username/aukey-km-g15-rgb.git
cd aukey-km-g15-rgb
pip install -e .
```

## Usage / 使用

### Show device info / 显示设备信息

```bash
km-g15-rgb info
```

### List available modes / 列出可用模式

```bash
km-g15-rgb list-modes
```

### Switch profile / 切换配置文件

```bash
km-g15-rgb profile 0    # Profile 0
km-g15-rgb profile 1    # Profile 1
km-g15-rgb profile 2    # Profile 2
```

### Set lighting mode / 设置灯效模式

```bash
km-g15-rgb mode 6 -p 0     # Profile 0, 常亮 (Static)
km-g15-rgb mode 5 -p 1     # Profile 1, 呼吸 (Breathing)
km-g15-rgb mode 1 -p 2     # Profile 2, 随波逐流 (Stream)
```

### Set speed / 设置速度

```bash
km-g15-rgb speed -s 1 -p 0   # Speed 1 on Profile 0
```

### Set USB polling rate / 设置 USB 回报率

```bash
km-g15-rgb rate -r 1000 -p 0   # 1000Hz on Profile 0
km-g15-rgb rate -r 125 -p 1    # 125Hz on Profile 1
```

### Enable RGB lighting / 启用 RGB 灯效

```bash
km-g15-rgb light-on
```

### Read device status / 读取设备状态

```bash
km-g15-rgb status
```

## Lighting Modes / 灯效模式

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

## USB Polling Rate / USB 回报率

| Rate | Code |
|------|------|
| 125 Hz | 0 |
| 250 Hz | 1 |
| 500 Hz | 2 |
| 1000 Hz | 3 |

## Protocol Documentation / 协议文档

See [PROTOCOL.md](docs/PROTOCOL.md) for detailed protocol documentation.

详见 [PROTOCOL.md](docs/PROTOCOL.md) 了解详细协议文档。

## Project Structure / 项目结构

```
aukey-km-g15-rgb/
├── src/km_g15_rgb/
│   ├── __init__.py
│   ├── device.py          # USB HID device communication
│   ├── protocol.py        # Protocol definitions
│   ├── effects.py         # Lighting mode definitions
│   └── cli.py             # Command-line interface
├── docs/
│   └── PROTOCOL.md        # Protocol documentation
├── tests/
│   └── test_protocol.py
├── setup.py
├── requirements.txt
└── README.md
```

## Requirements / 依赖

- Python 3.8+
- hidapi

## License / 许可

MIT License

## Acknowledgments / 致谢

- Protocol reverse-engineered via USB packet capture analysis
- Original software by AUKEY
