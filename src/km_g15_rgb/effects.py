"""Lighting Effect Modes for AUKEY KM-G15

From Main.ini [Mode] section - 19 lighting modes (no mode 19).
"""
from enum import IntEnum
from typing import Tuple, List


class LightingMode(IntEnum):
    """Lighting Effect Modes."""
    STREAM = 1           # 随波逐流 / Go with the stream
    CLOUDS = 2           # 彩云纷飞 / Clouds fly
    WINDING = 3          # 峰回路转 / Winding paths
    TRIAL = 4            # 光之审判 / The trial of light
    BREATHING = 5        # 呼吸 / Breathing
    STATIC = 6           # 常亮 / Normally on
    SNOW = 7             # 踏雪无痕 / Pass without trace
    RIPPLE = 8           # 泛起涟漪 / Ripple graff
    FAST = 9             # 奔逸绝尘 / Fast run without trace
    STARS = 10           # 繁星点点 / Snow winter jasmine
    FLOWERS = 11         # 百花争艳 / Flowers blooming
    METEOR = 12          # 流星赶月 / Swift action
    HURRICANE = 13       # 大鹏展翅 / Hurricane
    ACCUMULATE = 14      # 厚积薄发 / Accumulate
    DIGITAL = 15         # 落雨纷纷 / Digital Times
    BOTHWAYS = 16        # 左右逢缘 / Both ways
    SURMOUNT = 17        # 众志成城 / Surmount
    FASTFURIOUS = 18     # 速度激情 / Fast and the Furious
    COASTAL = 20         # 指点江山 / Coastal


# Mode name mappings for display
MODE_NAMES = {
    1:  ("随波逐流", "Go with the stream"),
    2:  ("彩云纷飞", "Clouds fly"),
    3:  ("峰回路转", "Winding paths"),
    4:  ("光之审判", "The trial of light"),
    5:  ("呼吸", "Breathing"),
    6:  ("常亮", "Normally on"),
    7:  ("踏雪无痕", "Pass without trace"),
    8:  ("泛起涟漪", "Ripple graff"),
    9:  ("奔逸绝尘", "Fast run without trace"),
    10: ("繁星点点", "Snow winter jasmine"),
    11: ("百花争艳", "Flowers blooming"),
    12: ("流星赶月", "Swift action"),
    13: ("大鹏展翅", "Hurricane"),
    14: ("厚积薄发", "Accumulate"),
    15: ("落雨纷纷", "Digital Times"),
    16: ("左右逢缘", "Both ways"),
    17: ("众志成城", "Surmount"),
    18: ("速度激情", "Fast and the Furious"),
    20: ("指点江山", "Coastal"),
}


def get_mode_name(mode_id: int) -> Tuple[str, str]:
    """Get mode name in Chinese and English.

    Args:
        mode_id: Mode ID (1-18, 20)

    Returns:
        Tuple of (Chinese name, English name)
    """
    return MODE_NAMES.get(mode_id, ("Unknown", "Unknown"))


def list_modes() -> List[int]:
    """List all available mode IDs."""
    return sorted(MODE_NAMES.keys())
