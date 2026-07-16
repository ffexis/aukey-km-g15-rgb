# USB 抓包分析指南

## 前置准备

### 1. 安装 USBPcap

USBPcap 是 Windows 上的 USB 抓包工具，需要与 Wireshark 配合使用。

**下载地址**: https://usbpcap.org/download

**安装步骤**:
1. 下载最新版本的 USBPcap Installer
2. 以管理员身份运行安装程序
3. 安装时勾选 "USBPcapCMD" 和 "USBPcapDLL"
4. 安装完成后重启电脑

### 2. Wireshark 配置

如果还没有安装 Wireshark：
- 下载地址: https://www.wireshark.org/download.html
- 安装时勾选 USBPcap 支持

## 抓包步骤

### 步骤 1: 启动 Wireshark

1. 打开 Wireshark
2. 在接口列表中，你应该能看到 `USBPcap1`, `USBPcap2` 等接口
3. 找到与你的键盘相关的 USBPcap 接口（通常是第一个或第二个）

### 步骤 2: 开始抓包

1. 双击对应的 USBPcap 接口开始抓包
2. 确保在抓包状态下保持运行

### 步骤 3: 操作官方软件

1. 打开 AUKEY 官方 RGB 控制软件
2. 进行以下操作（每次操作间隔 2-3 秒）：
   - 切换不同的灯效模式
   - 调整颜色
   - 调整亮度
   - 调整速度
3. 每个操作后等待几秒，确保数据被捕获

### 步骤 4: 停止抓包并保存

1. 停止 Wireshark 抓包
2. 保存捕获的数据为 `.pcapng` 格式
3. 保存到项目目录: `F:\Dev Project\km-g15-kb-reverse-eng\captures\`

## 分析抓包数据

### 过滤 USB HID 数据

在 Wireshark 中使用以下过滤器：

```
# 过滤 USB HID Output Reports (设备 -> 主机)
usb.transfer_type == 0x01 && usb.endpoint_address.direction == 0x00

# 过滤 USB HID Input Reports (主机 -> 设备)
usb.transfer_type == 0x01 && usb.endpoint_address.direction == 0x01

# 过滤特定 VID:PID 的数据
usb.idVendor == 0x0c45 && usb.idProduct == 0x7666

# 组合过滤器：特定设备的 HID 数据
(usb.idVendor == 0x0c45) && (usb.transfer_type == 0x01)
```

### 识别 RGB 控制数据

RGB 控制数据通常具有以下特征：
1. **固定的数据长度**: 通常是 32 或 64 字节
2. **重复的模式**: 相同的命令结构，只是参数不同
3. **时间戳规律**: 在你操作官方软件时会出现

### 常见的 RGB 控制协议模式

```
Byte 0: Report ID (通常为 0x01-0x0F)
Byte 1: Command (命令类型)
  - 0x01: 设置颜色
  - 0x02: 设置模式
  - 0x03: 设置亮度
  - 0x04: 设置速度
Byte 2-N: 参数数据
  - RGB 颜色: R, G, B (各 1 字节)
  - 模式 ID: 单字节
  - 亮度值: 0-100 或 0-255
```

## 预期产出

完成抓包分析后，你应该能够：

1. **识别出 RGB 控制的 Report ID**
2. **解析出命令格式**
3. **理解颜色编码方式**
4. **列出所有支持的灯效模式**

## 下一步

将抓包数据保存后，我们可以：
1. 分析数据包结构
2. 编写协议文档
3. 开始实现 Python CLI 工具

## 故障排除

### 问题: 看不到 USBPcap 接口
- 确保 USBPcap 已正确安装
- 重启 Wireshark
- 检查设备管理器中是否有 USBPcap 设备

### 问题: 抓不到数据
- 确保 USBPcap 正在监听正确的设备
- 尝试不同的 USBPcap 接口
- 检查是否有其他程序占用了设备

### 问题: 数据太多难以分析
- 使用 Wireshark 过滤器
- 只在操作官方软件时才开始抓包
- 操作之间留出足够的间隔
