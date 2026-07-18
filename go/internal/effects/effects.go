package effects

// LightingMode represents a keyboard lighting effect mode.
type LightingMode int

const (
	Stream      LightingMode = 1
	Clouds      LightingMode = 2
	Winding     LightingMode = 3
	Trial       LightingMode = 4
	Breathing   LightingMode = 5
	Static      LightingMode = 6
	Snow        LightingMode = 7
	Ripple      LightingMode = 8
	Fast        LightingMode = 9
	Stars       LightingMode = 10
	Flowers     LightingMode = 11
	Meteor      LightingMode = 12
	Hurricane   LightingMode = 13
	Accumulate  LightingMode = 14
	Digital     LightingMode = 15
	BothWays    LightingMode = 16
	Surmount    LightingMode = 17
	FastFurious LightingMode = 18
	Coastal     LightingMode = 20
)

// ModeInfo holds display names for a lighting mode.
type ModeInfo struct {
	ID     int
	NameCN string
	NameEN string
}

var registry = map[LightingMode]ModeInfo{
	Stream:      {1, "随波逐流", "Go with the stream"},
	Clouds:      {2, "彩云纷飞", "Clouds fly"},
	Winding:     {3, "峰回路转", "Winding paths"},
	Trial:       {4, "光之审判", "The trial of light"},
	Breathing:   {5, "呼吸", "Breathing"},
	Static:      {6, "常亮", "Normally on"},
	Snow:        {7, "踏雪无痕", "Pass without trace"},
	Ripple:      {8, "泛起涟漪", "Ripple graff"},
	Fast:        {9, "奔逸绝尘", "Fast run without trace"},
	Stars:       {10, "繁星点点", "Snow winter jasmine"},
	Flowers:     {11, "百花争艳", "Flowers blooming"},
	Meteor:      {12, "流星赶月", "Swift action"},
	Hurricane:   {13, "大鹏展翅", "Hurricane"},
	Accumulate:  {14, "厚积薄发", "Accumulate"},
	Digital:     {15, "落雨纷纷", "Digital Times"},
	BothWays:    {16, "左右逢缘", "Both ways"},
	Surmount:    {17, "众志成城", "Surmount"},
	FastFurious: {18, "速度激情", "Fast and the Furious"},
	Coastal:     {20, "指点江山", "Coastal"},
}

// GetModeName returns (cn, en, ok) for the given mode ID.
func GetModeName(id int) (string, string, bool) {
	info, ok := registry[LightingMode(id)]
	if !ok {
		return "", "", false
	}
	return info.NameCN, info.NameEN, true
}

// ListModes returns all available modes sorted by ID.
func ListModes() []ModeInfo {
	ids := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20}
	result := make([]ModeInfo, len(ids))
	for i, id := range ids {
		result[i] = registry[LightingMode(id)]
	}
	return result
}

// IsValidMode returns true if the given mode ID is valid.
func IsValidMode(id int) bool {
	_, ok := registry[LightingMode(id)]
	return ok
}
