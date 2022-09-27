from enum import Enum

class MochigomaLayerIndex(Enum):
    HU1 = 15
    HU2 = 16
    HU3 = 17
    HU4 = 18
    HU5 = 19
    HU6 = 20
    HU7 = 21
    HU8 = 22
    KASHA1 = 23
    KASHA2 = 24
    KASHA3 = 25
    KASHA4 = 26
    KEIMA1 = 27
    KEIMA2 = 28
    KEIMA3 = 29
    KEIMA4 = 30
    GIN1 = 31
    GIN2 = 32
    GIN3 = 33
    GIN4 = 34
    KIN1 = 35
    KIN2 = 36
    KIN3 = 37
    KIN4 = 38
    KAKU1 = 39
    KAKU2 = 40
    HISHA1 = 41
    HISHA2 = 42

ban_index_to_layer_index = {1:0, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 
            -1:42, -2:43, -3:44, -4:45, -5:46, -6:47, -7:48, -8:49,}


