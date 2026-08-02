# AUKEY KM-G15 USB HID Protocol

This document describes the reverse-engineered USB HID protocol for controlling RGB lighting on the AUKEY KM-G15 mechanical keyboard (Sonix MCU).

## 1. Device Information / 设备信息

| Property | Value |
|----------|-------|
| Vendor ID | `0x0C45` (Sonix) |
| Product ID | `0x7666` |
| Interface Class | `0x03` (HID) |
| RGB Interface | Usage Page `0xFF1C`, Usage `0x0092` |

## 2. Transport Layer / 传输层

Commands are sent via **USB HID SET_REPORT** (Control Transfer):

| Field | Value |
|-------|-------|
| bmRequestType | `0x21` (Host→Device, Class, Interface) |
| bRequest | `0x09` (SET_REPORT) |
| wValue | `0x0204` (ReportType=Output, ReportID=4) |
| wIndex | `1` (Interface 1) |
| Data Length | 64 bytes |

## 3. Packet Structure / 报文结构

Each command is a fixed **64-byte** packet:

| Offset | Field | Type | Description |
|--------|-------|------|-------------|
| 0 | ReportID | uint8 | Fixed: `0x04` |
| 1 | Checksum | uint8 | Sum of bytes[2..63] mod 256 |
| 2 | Reserved | uint8 | Fixed: `0x00` |
| 3 | CmdType | uint8 | Command type (see §4) |
| 4 | DataLen | uint8 | Payload length |
| 5 | Addr_LSB | uint8 | Target address low byte |
| 6 | Addr_MSB | uint8 | Target address high byte |
| 7 | Reserved | uint8 | Fixed: `0x00` |
| 8..N | Data | uint8[] | Payload (length = DataLen) |
| N+1..63 | Padding | uint8[] | Zero-filled |

### Checksum Algorithm / 校验和算法

```
checksum = sum(packet[2:64]) & 0xFF
```

## 4. Command Types / 命令类型

| Value | Name | Description |
|-------|------|-------------|
| `0x01` | START | Begin write transaction |
| `0x02` | END | Commit write transaction to Flash |
| `0x03` | READ | Read configuration from device |
| `0x04` | PROFILE | Switch profile slot |
| `0x05` | LED_BUF | Reset LED render buffer |
| `0x06` | RUNTIME | Write runtime parameter |
| `0x11` | RGB_STATIC | Write static per-key RGB data |

## 5. Transaction Flow / 事务流程

All write operations must follow the **three-step sequence**:

```
1. START  →  2. Command(s)  →  3. END
```

Example (set light mode to Breathing on Profile 0):

```
→ START:   04 01 00 01 00 00 00 00 ... (64 bytes)
→ CMD:     04 0C 00 06 01 00 00 00 05 00 ... (mode=5)
→ END:     04 04 00 02 00 02 00 00 ... (64 bytes)
```

## 6. Profile Memory Map / 配置文件内存映射

The keyboard has **3 profiles** (0, 1, 2), each with its own address space.

### Runtime Parameters (CmdType=0x06)

Each profile has an offset of `0x002A` from the base address:

| Parameter | Profile 0 | Profile 1 | Profile 2 | DataLen |
|-----------|-----------|-----------|-----------|---------|
| Light Mode | `0x0000` | `0x002A` | `0x0054` | 1 |
| Speed | `0x0002` | `0x002C` | `0x0056` | 1 |
| Brightness | `0x0001` | `0x002B` | `0x0055` | 1 |
| Direction | `0x0003` | `0x002D` | `0x0057` | 1 |
| Colorful | `0x0004` | `0x002E` | `0x0058` | 1 |
| Static Color R | `0x0005` | `0x002F` | `0x0059` | 1 |
| Static Color G | `0x0006` | `0x0030` | `0x005A` | 1 |
| Static Color B | `0x0007` | `0x0031` | `0x005B` | 1 |
| USB Polling Rate | `0x000F` | `0x0039` | `0x0063` | 1 |

**Static color write**: R/G/B are written as three separate single-byte RUNTIME
commands, each wrapped in its own `START → CMD → END` transaction. The registers
mirror the config-response layout (Color at response bytes 5-7).
**Verified on real hardware (2026-08-02)** via the WebHID web UI; the write
mechanism was not previously implemented in the CLI.

### Reading Configuration (CmdType=0x05)

Configuration data (including speed) is read using **CmdType=0x05** at the profile base address. The response contains 42 bytes of config data starting at byte 8:

| Byte Offset | Field | Description |
|-------------|-------|-------------|
| 0 | Mode | Lighting mode (1-18, 20) |
| 1 | Brightness | Brightness level (0-4) |
| 2 | Speed | Hardware speed value (0-4; user value = 4 - hw) |
| 3 | Direction | 0x00=Right, 0xFF=Left |
| 4 | Colorful | 0=OFF, 1=ON |
| 5-7 | Color | RGB color data |

**Note**: Speed is stored in flash config and read directly from the config response. No separate runtime register read is needed.

### Static RGB Data (CmdType=0x11)

Each profile has an offset of `0x0200` from the base address:

| Profile | Start Address | End Address |
|---------|---------------|-------------|
| Profile 0 | `0x0200` | `0x03FF` |
| Profile 1 | `0x0400` | `0x05FF` |
| Profile 2 | `0x0600` | `0x07FF` |

## 7. Speed Value Mapping / 速度值映射

**Important**: Hardware stores speed **inverted** (counter-intuitive).

| User Value (UI) | Hardware Value | Meaning |
|-----------------|----------------|---------|
| 0 (Slowest) | 4 | Min speed |
| 1 | 3 | |
| 2 | 2 | |
| 3 | 1 | |
| 4 (Fastest) | 0 | Max speed |

Formula: `Hardware Value = 4 - User Value`

The CLI automatically handles this conversion. When reading from hardware, the value is inverted back to user-facing value (0-4).

## 8. Light Mode Values / 灯效模式值

19 lighting modes available (note: mode 19 does not exist):

| Value | Name (CN) | Name (EN) |
|-------|-----------|-----------|
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

## 8. USB Polling Rate Values / USB 回报率值

| Value | Rate |
|-------|------|
| 0 | 125 Hz |
| 1 | 250 Hz |
| 2 | 500 Hz |
| 3 | 1000 Hz |

## 9. Profile Switch / 配置文件切换

Profile switch uses a special **magic signature** in the data payload:

```
Magic (16 bytes): 55 AA FF 02 45 0C 66 76 03 01 [profile_index] 18 00 00 00 00
Fill (28 bytes):  01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 11 10 12 14 + 9 zeros
```

- `profile_index`: 0, 1, or 2
- CmdType: `0x04`
- DataLen: `0x2C` (44 bytes)

## 10. Read Command / 读取命令

Send CmdType `0x03` with a 44-byte zero payload (`DataLen=0x2C`). Device responds with:

```
[Header] [44 bytes of configuration data including magic signature]
```

The current profile index is at **byte 18 of the response** (payload offset 10, inside the echoed magic signature).

## 11. Implementation Notes / 实现注意事项

1. **Open device with `open_path()`**, not `open(VID, PID)` - must select the correct RGB interface
2. **Data starts at Byte 8** (8-byte header, not 7)
3. **LED Buffer Reset** requires sending 3 packets to addresses `0x0000`, `0x002A`, `0x0054`
4. **Profile switch is sent once** (verified working in the Go implementation; a single packet suffices)

## References / 参考

- [AUKEY KM-G15 Official Software](https://www.aukey.com/)
- [USB HID Specification](https://usb.org/document-class/hid)
- Wireshark USB capture analysis
