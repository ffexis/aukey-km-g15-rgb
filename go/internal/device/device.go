// Package device provides USB HID device communication for the AUKEY KM-G15 keyboard.
package device

import (
	"fmt"
	"time"

	hid "github.com/sstallion/go-hid"
)

const (
	VendorID  = 0x0C45
	ProductID = 0x7666

	UsagePageVendor = 0xFF1C
	UsageVendorRGB  = 0x0092

	PacketSize = 64
)

// DeviceInfo holds information about a discovered HID device.
type DeviceInfo struct {
	VendorID          uint16
	ProductID         uint16
	Path              string
	ProductString     string
	ManufacturerString string
	UsagePage         uint16
	Usage             uint16
	InterfaceNumber   int
}

// Device wraps a hid.Device for KM-G15 RGB communication.
type Device struct {
	handle *hid.Device
}

// EnumerateDevices finds all KM-G15 HID interfaces.
func EnumerateDevices() ([]DeviceInfo, error) {
	var devices []DeviceInfo

	err := hid.Enumerate(VendorID, ProductID, func(info *hid.DeviceInfo) error {
		devices = append(devices, DeviceInfo{
			VendorID:          info.VendorID,
			ProductID:         info.ProductID,
			Path:              info.Path,
			ProductString:     info.ProductStr,
			ManufacturerString: info.MfrStr,
			UsagePage:         info.UsagePage,
			Usage:             info.Usage,
			InterfaceNumber:   info.InterfaceNbr,
		})
		return nil
	})
	if err != nil {
		return nil, fmt.Errorf("hid enumerate: %w", err)
	}
	return devices, nil
}

// FindRGBInterface finds the vendor-specific RGB control interface.
func FindRGBInterface() (*DeviceInfo, error) {
	devices, err := EnumerateDevices()
	if err != nil {
		return nil, err
	}

	for i := range devices {
		if devices[i].UsagePage == UsagePageVendor && devices[i].Usage == UsageVendorRGB {
			return &devices[i], nil
		}
	}
	return nil, fmt.Errorf("RGB control interface not found (usage page 0x%04X, usage 0x%04X) - is the keyboard connected?",
		UsagePageVendor, UsageVendorRGB)
}

// Open opens the RGB control interface by device path.
func Open(path string) (*Device, error) {
	handle, err := hid.OpenPath(path)
	if err != nil {
		return nil, fmt.Errorf("open device: %w", err)
	}
	return &Device{handle: handle}, nil
}

// OpenDefault finds and opens the first RGB interface.
func OpenDefault() (*Device, error) {
	info, err := FindRGBInterface()
	if err != nil {
		return nil, err
	}
	return Open(info.Path)
}

// Write sends raw data to the device.
func (d *Device) Write(data []byte) (int, error) {
	if d.handle == nil {
		return 0, fmt.Errorf("device not open")
	}
	n, err := d.handle.Write(data)
	if err != nil {
		return 0, fmt.Errorf("write: %w", err)
	}
	return n, nil
}

// SendReport sends a 64-byte RGB control packet.
func (d *Device) SendReport(packet []byte) error {
	if len(packet) != PacketSize {
		return fmt.Errorf("packet must be %d bytes, got %d", PacketSize, len(packet))
	}
	n, err := d.Write(packet)
	if err != nil {
		return err
	}
	if n != PacketSize {
		return fmt.Errorf("wrote %d bytes, expected %d", n, PacketSize)
	}
	return nil
}

// Read reads data from the device with a timeout.
func (d *Device) Read(timeoutMs int) ([]byte, error) {
	if d.handle == nil {
		return nil, fmt.Errorf("device not open")
	}
	buf := make([]byte, PacketSize)
	n, err := d.handle.ReadWithTimeout(buf, time.Duration(timeoutMs)*time.Millisecond)
	if err != nil {
		return nil, nil // Timeout or error treated as no data
	}
	if n == 0 {
		return nil, nil
	}
	return buf[:n], nil
}

// GetManufacturerString returns the manufacturer string.
func (d *Device) GetManufacturerString() string {
	if d.handle == nil {
		return ""
	}
	s, err := d.handle.GetMfrStr()
	if err != nil {
		return ""
	}
	return s
}

// GetProductString returns the product string.
func (d *Device) GetProductString() string {
	if d.handle == nil {
		return ""
	}
	s, err := d.handle.GetProductStr()
	if err != nil {
		return ""
	}
	return s
}

// Close closes the device connection.
func (d *Device) Close() error {
	if d.handle != nil {
		err := d.handle.Close()
		d.handle = nil
		return err
	}
	return nil
}
