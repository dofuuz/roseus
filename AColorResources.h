const unsigned char specColormap[256][3] = {
   {  0,   0,   0},
   {  0,   0,   0},
   {  0,   0,   0},
   {  0,   1,   0},
   {  0,   1,   1},
   {  1,   1,   1},
   {  1,   2,   2},
   {  1,   2,   2},
   {  1,   3,   3},
   {  1,   4,   4},
   {  2,   5,   4},
   {  2,   6,   5},
   {  2,   7,   6},
   {  2,   8,   8},
   {  2,   9,   9},
   {  2,  10,  10},
   {  2,  11,  12},
   {  2,  13,  13},
   {  2,  14,  15},
   {  2,  15,  16},
   {  2,  16,  18},
   {  2,  18,  19},
   {  2,  19,  21},
   {  2,  20,  22},
   {  1,  21,  24},
   {  1,  22,  26},
   {  1,  23,  27},
   {  1,  25,  29},
   {  0,  26,  31},
   {  0,  27,  33},
   {  0,  28,  34},
   {  0,  29,  36},
   {  0,  30,  38},
   {  0,  31,  40},
   {  0,  32,  42},
   {  0,  33,  44},
   {  0,  34,  46},
   {  0,  35,  48},
   {  0,  36,  50},
   {  0,  37,  52},
   {  0,  38,  55},
   {  0,  39,  57},
   {  0,  40,  59},
   {  0,  41,  61},
   {  0,  42,  64},
   {  0,  42,  66},
   {  0,  43,  69},
   {  0,  44,  71},
   {  0,  45,  73},
   {  0,  46,  76},
   {  0,  46,  79},
   {  0,  47,  81},
   {  0,  48,  84},
   {  0,  48,  86},
   {  1,  49,  89},
   {  3,  49,  92},
   {  5,  50,  94},
   {  7,  50,  97},
   { 10,  51, 100},
   { 13,  51, 102},
   { 16,  51, 105},
   { 19,  52, 108},
   { 22,  52, 111},
   { 25,  52, 113},
   { 27,  53, 116},
   { 30,  53, 119},
   { 33,  53, 121},
   { 35,  53, 124},
   { 38,  53, 127},
   { 41,  53, 129},
   { 43,  53, 132},
   { 46,  53, 134},
   { 49,  53, 137},
   { 52,  53, 139},
   { 54,  52, 142},
   { 57,  52, 144},
   { 60,  52, 146},
   { 62,  52, 148},
   { 65,  51, 151},
   { 68,  51, 153},
   { 70,  51, 155},
   { 73,  50, 157},
   { 76,  50, 159},
   { 78,  49, 161},
   { 81,  49, 162},
   { 84,  48, 164},
   { 86,  48, 166},
   { 89,  47, 167},
   { 92,  46, 169},
   { 94,  46, 170},
   { 97,  45, 171},
   { 99,  45, 172},
   {102,  44, 173},
   {105,  44, 174},
   {107,  43, 175},
   {110,  42, 176},
   {112,  42, 177},
   {115,  41, 178},
   {117,  41, 178},
   {120,  40, 179},
   {122,  40, 179},
   {124,  39, 179},
   {127,  39, 180},
   {129,  38, 180},
   {132,  38, 180},
   {134,  37, 180},
   {136,  37, 180},
   {139,  37, 179},
   {141,  37, 179},
   {143,  36, 179},
   {146,  36, 178},
   {148,  36, 178},
   {150,  36, 177},
   {152,  36, 176},
   {155,  36, 176},
   {157,  36, 175},
   {159,  36, 174},
   {161,  36, 173},
   {163,  37, 172},
   {165,  37, 171},
   {167,  37, 170},
   {170,  38, 169},
   {172,  38, 167},
   {174,  39, 166},
   {176,  39, 165},
   {178,  40, 163},
   {180,  41, 162},
   {182,  41, 160},
   {183,  42, 159},
   {185,  43, 157},
   {187,  44, 155},
   {189,  45, 154},
   {191,  45, 152},
   {193,  46, 150},
   {195,  47, 149},
   {196,  48, 147},
   {198,  49, 145},
   {200,  50, 143},
   {202,  51, 141},
   {203,  53, 139},
   {205,  54, 138},
   {207,  55, 136},
   {208,  56, 134},
   {210,  57, 132},
   {211,  59, 130},
   {213,  60, 128},
   {214,  61, 126},
   {216,  63, 124},
   {217,  64, 122},
   {219,  65, 120},
   {220,  67, 118},
   {222,  68, 116},
   {223,  70, 114},
   {224,  71, 112},
   {226,  72, 110},
   {227,  74, 108},
   {228,  75, 106},
   {230,  77, 104},
   {231,  78, 102},
   {232,  80, 100},
   {233,  81,  98},
   {234,  83,  96},
   {236,  84,  94},
   {237,  86,  92},
   {238,  87,  91},
   {239,  89,  89},
   {240,  91,  87},
   {241,  92,  85},
   {242,  94,  83},
   {243,  96,  81},
   {244,  97,  79},
   {245,  99,  77},
   {246, 101,  75},
   {247, 102,  73},
   {248, 104,  71},
   {249, 106,  69},
   {249, 108,  67},
   {250, 110,  65},
   {251, 111,  63},
   {251, 113,  61},
   {252, 115,  59},
   {253, 117,  57},
   {253, 119,  55},
   {254, 121,  53},
   {254, 123,  51},
   {254, 125,  49},
   {255, 127,  48},
   {255, 129,  46},
   {255, 131,  44},
   {255, 134,  43},
   {255, 136,  41},
   {255, 138,  40},
   {255, 140,  39},
   {255, 142,  38},
   {255, 145,  37},
   {255, 147,  36},
   {255, 149,  35},
   {255, 151,  35},
   {254, 154,  35},
   {254, 156,  36},
   {253, 158,  36},
   {253, 161,  37},
   {252, 163,  38},
   {252, 166,  40},
   {251, 168,  41},
   {250, 170,  43},
   {249, 173,  45},
   {248, 175,  48},
   {248, 177,  50},
   {247, 180,  53},
   {246, 182,  56},
   {245, 185,  59},
   {244, 187,  63},
   {242, 189,  66},
   {241, 192,  70},
   {240, 194,  73},
   {239, 196,  77},
   {238, 198,  81},
   {237, 200,  85},
   {236, 203,  90},
   {234, 205,  94},
   {233, 207,  99},
   {232, 209, 103},
   {231, 211, 108},
   {230, 213, 112},
   {229, 215, 117},
   {228, 217, 122},
   {227, 219, 127},
   {227, 220, 132},
   {226, 222, 137},
   {226, 224, 142},
   {225, 225, 147},
   {225, 227, 152},
   {225, 228, 157},
   {225, 230, 163},
   {225, 231, 168},
   {225, 233, 173},
   {226, 234, 178},
   {226, 235, 183},
   {227, 236, 188},
   {228, 237, 192},
   {229, 238, 197},
   {230, 239, 202},
   {232, 240, 206},
   {233, 241, 211},
   {235, 242, 215},
   {236, 243, 219},
   {238, 244, 223},
   {240, 245, 227},
   {242, 245, 231},
   {244, 246, 235},
   {247, 247, 238},
   {249, 248, 241},
   {251, 248, 245},
   {253, 249, 247},
   {255, 250, 250},
};

const unsigned char selColormap[256][3] = {   { 77,  77,  77},
   { 77,  77,  77},
   { 77,  77,  77},
   { 77,  77,  77},
   { 77,  77,  77},
   { 77,  78,  77},
   { 77,  78,  78},
   { 77,  78,  78},
   { 77,  79,  79},
   { 78,  80,  79},
   { 78,  80,  80},
   { 78,  81,  81},
   { 78,  82,  82},
   { 78,  83,  83},
   { 78,  84,  84},
   { 78,  85,  85},
   { 78,  86,  86},
   { 78,  87,  87},
   { 78,  88,  88},
   { 78,  89,  89},
   { 78,  90,  91},
   { 78,  91,  92},
   { 78,  91,  93},
   { 78,  92,  94},
   { 78,  93,  96},
   { 77,  94,  97},
   { 77,  95,  98},
   { 77,  96, 100},
   { 77,  97, 101},
   { 76,  98, 103},
   { 76,  99, 104},
   { 76, 100, 105},
   { 75, 100, 107},
   { 75, 101, 109},
   { 75, 102, 110},
   { 74, 103, 112},
   { 74, 104, 113},
   { 74, 105, 115},
   { 73, 105, 117},
   { 73, 106, 118},
   { 72, 107, 120},
   { 72, 108, 122},
   { 72, 108, 124},
   { 72, 109, 126},
   { 72, 110, 127},
   { 72, 110, 129},
   { 72, 111, 131},
   { 72, 112, 133},
   { 72, 112, 135},
   { 72, 113, 137},
   { 73, 113, 139},
   { 74, 114, 141},
   { 75, 115, 143},
   { 76, 115, 146},
   { 77, 116, 148},
   { 79, 116, 150},
   { 80, 116, 152},
   { 82, 117, 154},
   { 85, 117, 156},
   { 87, 117, 158},
   { 90, 118, 161},
   { 92, 118, 163},
   { 94, 118, 165},
   { 96, 118, 167},
   { 98, 119, 169},
   {101, 119, 171},
   {103, 119, 173},
   {105, 119, 176},
   {107, 119, 178},
   {109, 119, 180},
   {111, 119, 182},
   {113, 119, 184},
   {116, 119, 186},
   {118, 119, 188},
   {120, 118, 190},
   {122, 118, 192},
   {124, 118, 193},
   {126, 118, 195},
   {128, 118, 197},
   {131, 117, 199},
   {133, 117, 200},
   {135, 117, 202},
   {137, 116, 203},
   {139, 116, 205},
   {141, 115, 206},
   {143, 115, 208},
   {146, 115, 209},
   {148, 114, 210},
   {150, 114, 211},
   {152, 113, 212},
   {154, 113, 213},
   {156, 112, 214},
   {158, 112, 215},
   {160, 111, 216},
   {162, 111, 217},
   {164, 110, 217},
   {166, 110, 218},
   {168, 110, 219},
   {170, 109, 219},
   {172, 109, 219},
   {174, 108, 220},
   {176, 108, 220},
   {178, 107, 220},
   {180, 107, 220},
   {182, 107, 220},
   {184, 106, 220},
   {186, 106, 220},
   {187, 106, 220},
   {189, 106, 220},
   {191, 106, 219},
   {193, 105, 219},
   {195, 105, 219},
   {197, 105, 218},
   {198, 105, 218},
   {200, 105, 217},
   {202, 105, 216},
   {204, 105, 216},
   {205, 106, 215},
   {207, 106, 214},
   {209, 106, 213},
   {210, 106, 212},
   {212, 107, 211},
   {214, 107, 210},
   {215, 108, 209},
   {217, 108, 208},
   {219, 108, 207},
   {220, 109, 206},
   {222, 110, 205},
   {223, 110, 203},
   {225, 111, 202},
   {226, 111, 201},
   {228, 112, 200},
   {229, 113, 198},
   {231, 114, 197},
   {232, 114, 195},
   {234, 115, 194},
   {235, 116, 193},
   {236, 117, 191},
   {238, 118, 190},
   {239, 119, 188},
   {240, 120, 187},
   {242, 120, 185},
   {243, 121, 183},
   {244, 122, 182},
   {246, 123, 180},
   {247, 124, 179},
   {248, 126, 177},
   {249, 127, 176},
   {250, 128, 174},
   {252, 129, 173},
   {253, 130, 171},
   {254, 131, 169},
   {255, 132, 168},
   {255, 133, 166},
   {255, 134, 165},
   {255, 136, 163},
   {255, 137, 162},
   {255, 138, 160},
   {255, 139, 158},
   {255, 140, 157},
   {255, 142, 155},
   {255, 143, 154},
   {255, 144, 152},
   {255, 145, 150},
   {255, 146, 149},
   {255, 148, 147},
   {255, 149, 146},
   {255, 150, 144},
   {255, 152, 143},
   {255, 153, 141},
   {255, 154, 139},
   {255, 156, 138},
   {255, 157, 136},
   {255, 158, 135},
   {255, 160, 133},
   {255, 161, 131},
   {255, 163, 130},
   {255, 164, 128},
   {255, 166, 127},
   {255, 167, 125},
   {255, 169, 124},
   {255, 170, 122},
   {255, 172, 120},
   {255, 173, 119},
   {255, 175, 117},
   {255, 177, 116},
   {255, 178, 115},
   {255, 180, 113},
   {255, 182, 112},
   {255, 183, 111},
   {255, 185, 109},
   {255, 187, 108},
   {255, 189, 107},
   {255, 190, 107},
   {255, 192, 106},
   {255, 194, 105},
   {255, 196, 105},
   {255, 198, 105},
   {255, 200, 105},
   {255, 201, 105},
   {255, 203, 105},
   {255, 205, 106},
   {255, 207, 107},
   {255, 209, 108},
   {255, 211, 109},
   {255, 213, 111},
   {255, 215, 113},
   {255, 217, 115},
   {255, 218, 117},
   {255, 220, 119},
   {255, 222, 121},
   {255, 224, 124},
   {255, 226, 127},
   {255, 228, 129},
   {255, 230, 132},
   {255, 232, 135},
   {255, 233, 138},
   {255, 235, 142},
   {255, 237, 145},
   {255, 239, 148},
   {255, 240, 152},
   {255, 242, 155},
   {255, 244, 159},
   {255, 245, 163},
   {255, 247, 166},
   {255, 248, 170},
   {255, 250, 174},
   {255, 251, 178},
   {255, 253, 182},
   {255, 254, 186},
   {255, 255, 190},
   {255, 255, 194},
   {255, 255, 198},
   {255, 255, 202},
   {255, 255, 207},
   {255, 255, 211},
   {255, 255, 215},
   {255, 255, 219},
   {255, 255, 223},
   {255, 255, 227},
   {255, 255, 230},
   {255, 255, 234},
   {255, 255, 238},
   {255, 255, 242},
   {255, 255, 245},
   {255, 255, 249},
   {255, 255, 252},
   {255, 255, 255},
   {255, 255, 255},
   {255, 255, 255},
   {255, 255, 255},
   {255, 255, 255},
   {255, 255, 255},
   {255, 255, 255},
   {255, 255, 255},
   {255, 255, 255},
};

const unsigned char freqSelColormap[256][3] = {   { 62,  65,  89},
   { 63,  65,  91},
   { 64,  66,  92},
   { 65,  66,  94},
   { 66,  66,  95},
   { 67,  67,  97},
   { 68,  67,  98},
   { 70,  67, 100},
   { 71,  68, 101},
   { 72,  68, 103},
   { 74,  68, 104},
   { 75,  69, 106},
   { 76,  69, 107},
   { 78,  69, 109},
   { 79,  69, 110},
   { 81,  69, 112},
   { 82,  70, 113},
   { 84,  70, 115},
   { 86,  70, 116},
   { 87,  70, 118},
   { 89,  70, 119},
   { 91,  70, 120},
   { 92,  70, 122},
   { 94,  70, 123},
   { 96,  70, 124},
   { 98,  70, 126},
   {100,  70, 127},
   {102,  70, 128},
   {104,  70, 129},
   {106,  69, 130},
   {108,  69, 132},
   {110,  69, 133},
   {112,  69, 134},
   {114,  69, 135},
   {116,  68, 136},
   {118,  68, 137},
   {120,  68, 138},
   {122,  67, 138},
   {124,  67, 139},
   {126,  66, 140},
   {129,  66, 141},
   {131,  65, 141},
   {133,  65, 142},
   {135,  64, 142},
   {138,  64, 142},
   {140,  63, 143},
   {142,  63, 143},
   {144,  62, 143},
   {147,  61, 143},
   {149,  61, 143},
   {151,  60, 143},
   {153,  59, 143},
   {156,  59, 142},
   {158,  58, 142},
   {160,  57, 141},
   {162,  57, 141},
   {165,  56, 140},
   {167,  55, 139},
   {169,  55, 138},
   {171,  54, 137},
   {173,  53, 136},
   {176,  53, 135},
   {178,  52, 134},
   {180,  51, 133},
   {182,  51, 131},
   {184,  50, 130},
   {186,  50, 128},
   {188,  49, 127},
   {190,  49, 125},
   {192,  49, 123},
   {194,  48, 121},
   {196,  48, 119},
   {198,  48, 117},
   {200,  48, 115},
   {202,  48, 113},
   {203,  47, 110},
   {205,  47, 108},
   {207,  48, 106},
   {209,  48, 103},
   {210,  48, 101},
   {212,  48,  98},
   {214,  48,  96},
   {215,  49,  93},
   {217,  49,  91},
   {218,  50,  88},
   {220,  50,  85},
   {221,  51,  83},
   {223,  52,  80},
   {224,  53,  77},
   {225,  54,  74},
   {226,  55,  71},
   {228,  56,  68},
   {229,  57,  65},
   {230,  58,  62},
   {231,  59,  59},
   {232,  60,  56},
   {233,  62,  53},
   {234,  63,  49},
   {235,  64,  46},
   {236,  66,  42},
   {237,  67,  38},
   {238,  69,  35},
   {239,  71,  30},
   {239,  72,  26},
   {240,  74,  20},
   {241,  76,  14},
   {241,  77,   5},
   {242,  79,   0},
   {243,  81,   0},
   {243,  83,   0},
   {244,  85,   0},
   {244,  87,   0},
   {244,  89,   0},
   {245,  91,   0},
   {245,  93,   0},
   {245,  95,   0},
   {245,  97,   0},
   {245,  99,   0},
   {245, 101,   0},
   {245, 103,   0},
   {245, 105,   0},
   {245, 108,   0},
   {245, 110,   0},
   {245, 112,   0},
   {245, 114,   0},
   {244, 116,   0},
   {244, 119,   0},
   {243, 121,   0},
   {243, 123,   0},
   {242, 126,   0},
   {242, 128,   0},
   {241, 130,   0},
   {241, 132,   0},
   {240, 135,   0},
   {239, 137,   0},
   {238, 139,   0},
   {237, 142,   0},
   {236, 144,   0},
   {235, 146,   0},
   {234, 149,   0},
   {233, 151,   0},
   {232, 154,   0},
   {230, 156,   0},
   {229, 158,   0},
   {227, 161,   0},
   {226, 163,   0},
   {224, 165,   0},
   {223, 168,   0},
   {221, 170,   0},
   {219, 173,   0},
   {217, 175,   0},
   {215, 177,   0},
   {213, 180,   0},
   {211, 182,   0},
   {209, 184,   0},
   {207, 187,   0},
   {205, 189,   0},
   {202, 191,   0},
   {200, 193,   0},
   {197, 196,   0},
   {195, 198,   0},
   {192, 200,   0},
   {189, 203,   0},
   {186, 205,   0},
   {183, 207,   0},
   {180, 209,   0},
   {177, 211,   0},
   {174, 214,   0},
   {170, 216,   0},
   {167, 218,   0},
   {163, 220,   0},
   {159, 222,   0},
   {155, 225,   0},
   {151, 227,   0},
   {147, 229,   0},
   {142, 231,   0},
   {137, 233,  10},
   {132, 235,  24},
   {127, 237,  34},
   {121, 239,  42},
   {116, 241,  50},
   {109, 243,  56},
   {103, 245,  63},
   { 95, 247,  69},
   { 88, 249,  75},
   { 79, 251,  80},
   { 69, 253,  86},
   { 57, 255,  91},
   { 42, 255,  97},
   { 18, 255, 102},
   {  0, 255, 107},
   {  0, 255, 113},
   {  0, 255, 118},
   {  0, 255, 123},
   {  0, 255, 129},
   {  0, 255, 134},
   {  0, 255, 139},
   {  0, 255, 144},
   {  0, 255, 149},
   {  0, 255, 155},
   {  0, 255, 160},
   {  0, 255, 165},
   {  0, 255, 170},
   {  0, 255, 175},
   {  0, 255, 180},
   {  0, 255, 185},
   {  0, 255, 190},
   {  0, 255, 195},
   {  0, 255, 200},
   {  0, 255, 205},
   {  0, 255, 210},
   {  0, 255, 214},
   {  0, 255, 219},
   {  0, 255, 223},
   {  0, 255, 228},
   {  0, 255, 232},
   {  0, 255, 237},
   {  0, 255, 241},
   {  0, 255, 245},
   {  0, 255, 249},
   {  0, 255, 253},
   {  0, 255, 255},
   {  0, 255, 255},
   { 21, 255, 255},
   { 50, 255, 255},
   { 68, 255, 255},
   { 82, 255, 255},
   { 95, 255, 255},
   {106, 255, 255},
   {116, 255, 255},
   {126, 255, 255},
   {135, 255, 255},
   {143, 255, 255},
   {151, 255, 255},
   {159, 255, 255},
   {166, 255, 255},
   {173, 255, 255},
   {180, 255, 255},
   {187, 255, 255},
   {193, 255, 255},
   {199, 255, 255},
   {205, 255, 255},
   {211, 255, 255},
   {216, 255, 255},
   {222, 255, 255},
   {227, 255, 255},
   {232, 255, 255},
   {237, 255, 255},
   {241, 255, 255},
   {246, 255, 255},
   {250, 255, 255},
   {254, 255, 255},
   {255, 255, 255},
   {255, 255, 255},
   {255, 255, 255},
   {255, 255, 253},
};

