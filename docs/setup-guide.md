# USB 抓包环境安装指南

## 需要安装的工具

### 1. Wireshark
- **下载**: https://www.wireshark.org/download.html
- **安装**: 选择默认选项，确保勾选 USBPcap 支持

### 2. USBPcap
- **下载**: https://usbpcap.org/download
- **安装**: 
  1. 以管理员身份运行安装程序
  2. 勾选所有组件
  3. 安装后重启电脑

## 快速安装命令 (PowerShell)

```powershell
# 使用 winget 安装 Wireshark (如果可用)
winget install WiresharkFoundation.Wireshark

# USBPcap 需要手动下载安装
# 访问 https://usbpcap.org/download 下载最新版本
```

## 验证安装

安装完成后，打开 Wireshark 应该能看到 USBPcap 接口：

```
USBPcap1
USBPcap2
...
```

## 抓包步骤

1. **打开 Wireshark**
   - 选择一个 USBPcap 接口开始抓包

2. **打开 AUKEY 官方软件**
   - 进行 RGB 设置操作

3. **操作列表** (按顺序执行，每个操作间隔 2-3 秒):
   - [ ] 切换到静态模式
   - [ ] 设置红色
   - [ ] 设置绿色
   - [ ] 设置蓝色
   - [ ] 切换到呼吸模式
   - [ ] 切换到波浪模式
   - [ ] 调整亮度 (低 -> 高)
   - [ ] 调整速度 (慢 -> 快)

4. **停止抓包并保存**
   - File -> Save As
   - 保存到: `F:\Dev Project\km-g15-kb-reverse-eng\captures\capture.pcapng`

5. **导出 HID 数据**
   - 应用过滤器: `(usb.idVendor == 0x0c45) && (usb.transfer_type == 0x01)`
   - File -> Export Packet Dissections -> As Plain Text
   - 保存到: `F:\Dev Project\km-g15-kb-reverse-eng\captures\hid_data.txt`

## 下一步

完成抓包后，运行分析脚本：

```bash
python scripts/analyze_capture.py captures/hid_data.txt
```

然后我们可以根据分析结果编写协议文档。
