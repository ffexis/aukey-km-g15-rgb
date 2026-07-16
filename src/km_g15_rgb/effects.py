"""Predefined Lighting Effects for AUKEY KM-G15

These are the actual lighting modes from Main.ini [Mode] section.
"""
from dataclasses import dataclass
from typing import List, Dict
from .protocol import RGBColor, Zone


@dataclass
class LightingEffect:
    """A lighting effect."""
    id: int
    name_cn: str
    name_en: str
    description: str = ""
    
    def __str__(self):
        return f"{self.id}: {self.name_cn} ({self.name_en})"


# Actual lighting modes from Main.ini [Mode] section
LIGHTING_MODES = {
    1: LightingEffect(1, "随波逐流", "Go with the stream", "Wave-like effect"),
    2: LightingEffect(2, "彩云纷飞", "Clouds fly", "Colorful cloud effect"),
    3: LightingEffect(3, "峰回路转", "Winding paths", "Winding path effect"),
    4: LightingEffect(4, "光之审判", "The trial of light", "Light trial effect"),
    5: LightingEffect(5, "呼吸", "Breathing", "Breathing effect"),
    6: LightingEffect(6, "常亮", "Normally on", "Static color"),
    7: LightingEffect(7, "踏雪无痕", "Pass without trace", "Snow trace effect"),
    8: LightingEffect(8, "泛起涟漪", "Ripple graff", "Ripple effect"),
    9: LightingEffect(9, "奔逸绝尘", "Fast run without trace", "Fast run effect"),
    10: LightingEffect(10, "繁星点点", "Snow winter jasmine", "Stars effect"),
    11: LightingEffect(11, "百花争艳", "Flowers blooming", "Flowers effect"),
    12: LightingEffect(12, "流星赶月", "Swift action", "Meteor effect"),
    13: LightingEffect(13, "大鹏展翅", "Hurricane", "Hurricane effect"),
    14: LightingEffect(14, "厚积薄发", "Accumulate", "Accumulate effect"),
    15: LightingEffect(15, "落雨纷纷", "Digital Times", "Rain effect"),
    16: LightingEffect(16, "左右逢缘", "Both ways", "Both ways effect"),
    17: LightingEffect(17, "众志成城", "Surmount", "Unity effect"),
    18: LightingEffect(18, "速度激情", "Fast and the Furious", "Fast and Furious effect"),
    20: LightingEffect(20, "指点江山", "Coastal", "Coastal effect"),
}


def list_modes() -> List[int]:
    """List all available mode IDs."""
    return sorted(LIGHTING_MODES.keys())


def get_mode(mode_id: int) -> LightingEffect:
    """Get a mode by ID.
    
    Args:
        mode_id: Mode ID (1-18, 20)
    
    Returns:
        LightingEffect: The mode information
    
    Raises:
        KeyError: If mode not found
    """
    if mode_id not in LIGHTING_MODES:
        available = ", ".join(str(m) for m in list_modes())
        raise KeyError(f"Mode {mode_id} not found. Available: {available}")
    return LIGHTING_MODES[mode_id]


def list_modes_table() -> str:
    """Get a formatted table of all modes."""
    lines = ["ID | 中文名 | 英文名", "- " * 20]
    for mode_id in list_modes():
        mode = LIGHTING_MODES[mode_id]
        lines.append(f"{mode_id:2d} | {mode.name_cn:<10} | {mode.name_en}")
    return "\n".join(lines)
