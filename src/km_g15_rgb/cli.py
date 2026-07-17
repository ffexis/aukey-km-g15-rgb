"""Command-Line Interface for AUKEY KM-G15 RGB Control"""
import click
import sys
import time
from .device import KM_G15_Device
from .protocol import KM_G15_Protocol, RGBColor, Zone, LightingMode
from .effects import list_modes, get_mode_name, MODE_NAMES


def read_current_profile(device) -> int:
    """Read the current active profile from device.

    Args:
        device: Open KM_G15_Device instance

    Returns:
        int: Current profile index (0, 1, or 2)
    """
    cmd = KM_G15_Protocol.build_read_packet()
    device.send_report(cmd)

    time.sleep(0.1)
    response = device.read(timeout_ms=500)

    if response and len(response) >= 19:
        return response[18]
    return 0


@click.group()
@click.version_option(version="0.3.0", prog_name="km-g15-rgb")
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
@click.option("--profile", "-p", type=int, default=None, help="Profile slot (0, 1, or 2). If not specified, uses current active profile.")
def mode(mode_id, profile):
    """Set lighting mode by ID.

    Available modes: 1-18, 20 (use 'list-modes' to see all)

    If --profile is not specified, the command targets the currently active profile.
    """
    if mode_id not in MODE_NAMES:
        valid = ', '.join(str(m) for m in sorted(MODE_NAMES.keys()))
        click.echo(f"Invalid mode {mode_id}. Valid modes: {valid}", err=True)
        sys.exit(1)

    cn, en = get_mode_name(mode_id)

    try:
        with KM_G15_Device() as device:
            # Auto-detect profile if not specified
            if profile is None:
                profile = read_current_profile(device)
                click.echo(f"Auto-detected active profile: {profile}")

            if profile not in (0, 1, 2):
                click.echo("Profile must be 0, 1, or 2", err=True)
                sys.exit(1)

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
@click.option("--speed", "-s", type=int, default=3, help="Speed value (1-5)")
@click.option("--profile", "-p", type=int, default=None, help="Profile slot (0, 1, or 2). If not specified, uses current active profile.")
def speed(speed, profile):
    """Set animation speed (1=slow, 5=fast)."""
    if speed < 1 or speed > 5:
        click.echo("Speed must be 1-5", err=True)
        sys.exit(1)

    try:
        with KM_G15_Device() as device:
            if profile is None:
                profile = read_current_profile(device)
                click.echo(f"Auto-detected active profile: {profile}")

            if profile not in (0, 1, 2):
                click.echo("Profile must be 0, 1, or 2", err=True)
                sys.exit(1)

            click.echo(f"Setting speed to {speed} on profile {profile}")

            start = KM_G15_Protocol.build_start_flag()
            device.send_report(start)

            cmd = KM_G15_Protocol.build_speed_packet(speed, profile)
            device.send_report(cmd)

            end = KM_G15_Protocol.build_end_flag()
            device.send_report(end)

            click.echo("Done!")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--brightness", "-b", type=int, default=4, help="Brightness value (0-4)")
@click.option("--profile", "-p", type=int, default=None, help="Profile slot (0, 1, or 2). If not specified, uses current active profile.")
def brightness(brightness, profile):
    """Set brightness level (0=min, 4=max)."""
    if brightness < 0 or brightness > 4:
        click.echo("Brightness must be 0-4", err=True)
        sys.exit(1)

    try:
        with KM_G15_Device() as device:
            if profile is None:
                profile = read_current_profile(device)
                click.echo(f"Auto-detected active profile: {profile}")

            if profile not in (0, 1, 2):
                click.echo("Profile must be 0, 1, or 2", err=True)
                sys.exit(1)

            click.echo(f"Setting brightness to {brightness} on profile {profile}")

            start = KM_G15_Protocol.build_start_flag()
            device.send_report(start)

            cmd = KM_G15_Protocol.build_brightness_packet(brightness, profile)
            device.send_report(cmd)

            end = KM_G15_Protocol.build_end_flag()
            device.send_report(end)

            click.echo("Done!")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--rate", "-r", type=click.Choice(['125', '250', '500', '1000']), default='1000', help="USB polling rate")
@click.option("--profile", "-p", type=int, default=None, help="Profile slot (0, 1, or 2). If not specified, uses current active profile.")
def rate(rate, profile):
    """Set USB polling rate."""
    rate_map = {'125': 0, '250': 1, '500': 2, '1000': 3}
    rate_code = rate_map[rate]

    try:
        with KM_G15_Device() as device:
            # Auto-detect profile if not specified
            if profile is None:
                profile = read_current_profile(device)
                click.echo(f"Auto-detected active profile: {profile}")

            if profile not in (0, 1, 2):
                click.echo("Profile must be 0, 1, or 2", err=True)
                sys.exit(1)

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
    """Read current device status and configuration."""
    try:
        with KM_G15_Device() as device:
            click.echo("Reading device status...")

            # Read current profile
            profile_index = read_current_profile(device)
            click.echo(f"\nDevice Status:")
            click.echo(f"  Current Profile: {profile_index}")

            # Read full configuration
            click.echo(f"\nReading configuration for Profile {profile_index}...")
            cmd = KM_G15_Protocol.build_read_config_packet(profile_index)
            device.send_report(cmd)

            time.sleep(0.3)
            response = device.read(timeout_ms=500)

            if response and len(response) >= 16:
                config = KM_G15_Protocol.parse_config_response(response)

                # Get mode name
                from .effects import get_mode_name
                cn, en = get_mode_name(config['mode'])

                # Read Speed from runtime register 0x0002
                speed_cmd = KM_G15_Protocol.build_read_runtime_packet(0x0002)
                device.send_report(speed_cmd)
                time.sleep(0.2)
                speed_resp = device.read(timeout_ms=500)
                speed = speed_resp[8] if speed_resp and len(speed_resp) > 8 else 0

                # USB Rate from config
                rate_map = {0: 125, 1: 250, 2: 500, 3: 1000}
                rate = rate_map.get(config['usb_rate'], config['usb_rate'])

                click.echo(f"\nProfile {profile_index} Configuration:")
                click.echo(f"  Mode: {config['mode']} ({cn} / {en})")
                click.echo(f"  Brightness: {config['brightness']}")
                click.echo(f"  Speed: {speed}")
                click.echo(f"  Direction: {config['direction']}")
                click.echo(f"  Colorful: {'ON' if config['colorful'] else 'OFF'}")
                click.echo(f"  Color: #{config['color'].to_hex()}")
                click.echo(f"  USB Rate: {rate}Hz (code={config['usb_rate']})")
            else:
                click.echo("Failed to read configuration.")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
