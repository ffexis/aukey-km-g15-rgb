"""Command-Line Interface for AUKEY KM-G15 RGB Control"""
import click
import sys
from .device import KM_G15_Device
from .protocol import KM_G15_Protocol, RGBColor, Zone, LightingMode
from .effects import list_modes, get_mode_name, MODE_NAMES


@click.group()
@click.version_option(version="0.2.0", prog_name="km-g15-rgb")
def cli():
    """AUKEY KM-G15 RGB Keyboard Control CLI"""
    pass


@cli.command()
def info():
    """Show device information."""
    devices = KM_G15_Device.enumerate_devices()
    
    if not devices:
        click.echo("No AUKEY KM-G15 device found.", err=True)
        sys.exit(1)
    
    click.echo(f"Found {len(devices)} interface(s):\n")
    
    for i, d in enumerate(devices):
        click.echo(f"Interface {i}:")
        click.echo(f"  VID: 0x{d['vendor_id']:04x}")
        click.echo(f"  PID: 0x{d['product_id']:04x}")
        click.echo(f"  Product: {d.get('product_string', 'N/A')}")
        click.echo(f"  Manufacturer: {d.get('manufacturer_string', 'N/A')}")
        click.echo(f"  Usage Page: 0x{d.get('usage_page', 0):04x}")
        click.echo(f"  Usage: 0x{d.get('usage', 0):04x}")
        click.echo()


@cli.command("list-modes")
def list_modes_cmd():
    """List available lighting modes."""
    click.echo("Available lighting modes:\n")
    click.echo("ID | 中文名         | 英文名")
    click.echo("-" * 55)

    for mode_id in list_modes():
        cn, en = get_mode_name(mode_id)
        click.echo(f"{mode_id:2d} | {cn:<12} | {en}")


@cli.command()
@click.argument("mode_id", type=int)
@click.option("--profile", "-p", type=int, default=0, help="Profile slot (0, 1, or 2)")
def mode(mode_id, profile):
    """Set lighting mode by ID.

    Available modes: 1-18, 20 (use 'list-modes' to see all)
    """
    if mode_id not in MODE_NAMES:
        valid = ', '.join(str(m) for m in sorted(MODE_NAMES.keys()))
        click.echo(f"Invalid mode {mode_id}. Valid modes: {valid}", err=True)
        sys.exit(1)

    if profile not in (0, 1, 2):
        click.echo("Profile must be 0, 1, or 2", err=True)
        sys.exit(1)

    cn, en = get_mode_name(mode_id)

    try:
        with KM_G15_Device() as device:
            click.echo(f"Setting mode to {mode_id}: {cn} ({en}) on profile {profile}")

            # Three-step command sequence
            start = KM_G15_Protocol.build_start_flag()
            device.send_report(start)

            cmd = KM_G15_Protocol.build_mode_packet(LightingMode(mode_id), profile)
            device.send_report(cmd)

            end = KM_G15_Protocol.build_end_flag()
            device.send_report(end)

            click.echo("Done!")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--speed", "-s", type=int, default=1, help="Speed/brightness value (1-255)")
@click.option("--profile", "-p", type=int, default=0, help="Profile slot (0, 1, or 2)")
def speed(speed, profile):
    """Set lighting speed/brightness."""
    if profile not in (0, 1, 2):
        click.echo("Profile must be 0, 1, or 2", err=True)
        sys.exit(1)

    try:
        with KM_G15_Device() as device:
            click.echo(f"Setting speed to {speed} on profile {profile}")

            # Three-step command sequence
            start = KM_G15_Protocol.build_start_flag()
            device.send_report(start)

            cmd = KM_G15_Protocol.build_brightness_packet(speed, profile)
            device.send_report(cmd)

            end = KM_G15_Protocol.build_end_flag()
            device.send_report(end)

            click.echo("Done!")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--rate", "-r", type=click.Choice(['125', '250', '500', '1000']), default='1000', help="USB polling rate")
@click.option("--profile", "-p", type=int, default=0, help="Profile slot (0, 1, or 2)")
def rate(rate, profile):
    """Set USB polling rate."""
    rate_map = {'125': 0, '250': 1, '500': 2, '1000': 3}
    rate_code = rate_map[rate]

    if profile not in (0, 1, 2):
        click.echo("Profile must be 0, 1, or 2", err=True)
        sys.exit(1)

    try:
        with KM_G15_Device() as device:
            click.echo(f"Setting USB rate to {rate}Hz on profile {profile}")

            # Three-step command sequence
            start = KM_G15_Protocol.build_start_flag()
            device.send_report(start)

            cmd = KM_G15_Protocol.build_rate_packet(rate_code, profile)
            device.send_report(cmd)

            end = KM_G15_Protocol.build_end_flag()
            device.send_report(end)

            click.echo("Done!")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("profile", type=int)
def profile(profile):
    """Switch to profile slot (0, 1, or 2)."""
    if profile not in (0, 1, 2):
        click.echo("Profile must be 0, 1, or 2", err=True)
        sys.exit(1)

    try:
        with KM_G15_Device() as device:
            click.echo(f"Switching to profile {profile}")

            # Three-step command sequence
            start = KM_G15_Protocol.build_start_flag()
            device.send_report(start)

            cmd = KM_G15_Protocol.build_profile_switch_packet(profile)
            device.send_report(cmd)

            end = KM_G15_Protocol.build_end_flag()
            device.send_report(end)

            click.echo("Done!")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command("light-on")
def light_on():
    """Enable RGB lighting (master switch)."""
    try:
        with KM_G15_Device() as device:
            click.echo("Enabling RGB lighting...")

            # Three-step command sequence
            start = KM_G15_Protocol.build_start_flag()
            device.send_report(start)

            cmd = KM_G15_Protocol.build_light_on_packet()
            device.send_report(cmd)

            end = KM_G15_Protocol.build_end_flag()
            device.send_report(end)

            click.echo("Done!")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def status():
    """Read current device status."""
    try:
        with KM_G15_Device() as device:
            click.echo("Reading device status...")

            # Send READ command
            cmd = KM_G15_Protocol.build_read_packet()
            device.send_report(cmd)

            # Try to read response
            import time
            time.sleep(0.1)
            response = device.read(timeout_ms=500)

            if response and len(response) >= 18:
                # Parse response
                # Header: 04 [checksum] 00 03 [datalen] [addr_lsb] [addr_msb] 00
                # Data starts at Byte 8: 55 aa ff 02 45 0c 66 76 03 01 [profile_index] 18 ...
                cmd_type = response[3]
                data_len = response[4]
                profile_index = response[18] if len(response) > 18 else 0

                click.echo(f"\nDevice Status:")
                click.echo(f"  Current Profile: {profile_index}")
                click.echo(f"  CmdType: 0x{cmd_type:02x}")
                click.echo(f"  DataLen: {data_len}")
            else:
                click.echo("No valid response received.")
                if response:
                    click.echo(f"Raw: {response.hex()}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
