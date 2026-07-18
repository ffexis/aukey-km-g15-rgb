# AUKEY KM-G15 RGB 控制工具

[English](README.md)

用于通过 USB HID 控制 AUKEY KM-G15 机械键盘 RGB 灯效的命令行工具。

## 功能

- 切换 3 个配置文件槽位
- 设置灯效模式（19 种效果）
- 调整亮度、速度、方向
- 开启/关闭多彩模式（Multi-color cycling）
- 配置 USB 回报率（125-1000 Hz）
- 自动检测当前激活的配置文件
- 读取当前设备状态

## 支持的键盘

- **AUKEY KM-G15**（Sonix MCU）
- VID: `0x0C45`，PID: `0x7666`

## 安装

### 下载 Release

从 [Releases](https://github.com/ffexis/aukey-km-g15-rgb/releases) 下载对应平台的二进制文件。

### 从源码编译

需要 Go 1.21+ 和 C 编译器（用于 CGO/hidapi）。

```bash
cd go
make build
```

二进制文件将输出为 `km-g15-rgb.exe`（Windows）或 `km-g15-rgb`（Linux/macOS）。

## 使用方法

```bash
km-g15-rgb <command> [flags]

全局参数：
  --device <path>    指定设备路径（多键盘时使用）
  -p, --profile <n>  目标配置文件槽位（0-2，默认：自动检测）
```

### 命令列表

| 命令 | 说明 |
|------|------|
| `info` | 显示连接的设备信息 |
| `status` | 读取当前设备配置 |
| `mode <id>` | 设置灯效模式（0-18, 20） |
| `brightness <0-4>` | 设置亮度等级 |
| `speed <0-4>` | 设置动画速度（0=最慢, 4=最快） |
| `rate <hz>` | 设置 USB 回报率（125, 250, 500, 1000） |
| `profile <0-2>` | 切换配置文件槽位 |
| `colorful <on\|off>` | 开启/关闭多彩模式 |
| `list-modes` | 列出可用的灯效模式 |

### 示例

```bash
# 显示设备信息
km-g15-rgb info

# 读取当前状态
km-g15-rgb status

# 在当前配置文件上设置常亮模式
km-g15-rgb mode 6

# 在配置文件 1 上设置呼吸模式
km-g15-rgb mode 5 -p 1

# 设置最大亮度
km-g15-rgb brightness 4

# 设置最快速度
km-g15-rgb speed 4

# 设置 1000Hz 回报率
km-g15-rgb rate 1000

# 开启多彩模式
km-g15-rgb colorful on

# 切换到配置文件 2
km-g15-rgb profile 2
```

## 灯效模式

| ID | 中文名 | 英文名 |
|----|--------|--------|
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

## 参数范围

| 参数 | 范围 | 说明 |
|------|------|------|
| 亮度 | 0-4 | 0=最小, 4=最大 |
| 速度 | 0-4 | 0=最慢, 4=最快 |
| 回报率 | 125/250/500/1000 | Hz |

## 协议文档

详见 [docs/PROTOCOL.md](docs/PROTOCOL.md) 了解详细协议文档。

## 许可证

MIT License

## 贡献者

- **MiMo-V2.5** — 分析、代码、测试
- **Google Gemini 3.5 Flash** — 分析

## 致谢

本项目使用了以下开源项目：

- [go-hid](https://github.com/sstallion/go-hid) — libhidapi 的 Go 语言绑定（USB HID 通信）
- [cobra](https://github.com/spf13/cobra) — Go 语言 CLI 框架
- [libhidapi](https://github.com/libusb/hidapi) — 跨平台 HID API 库

协议通过 [Wireshark](https://www.wireshark.org/) 和 [USBPcap](https://usbpcap.org/) 进行 USB 抓包分析逆向工程得到。
