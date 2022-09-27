from enum import Enum
import numpy as np
#from full_shogi import *
from doubutsu_shogi import *

movable_region = {
    # NOTE should be inversed direction
    1 : np.array([[1,0]]), # 'HU'
    2 : np.array([[i,0] for i in range(1,ROW_LENGTH)]), # 'KASHA'
    3 : np.array([[2,1], [2,-1]]), # 'KEIMA'
    4 : np.array([[1,0],[1,1],[1,-1],[-1,1],[-1,-1]]), # 'GIN'
    5 : np.array([[1,0],[1,1],[1,-1],[0,1],[0,-1],[-1,0]]), # 'KIN'
    6 : np.concatenate([ # 'KAKU'
            [[i,i] for i in range(1,MIN_ROW_COL_LENGTH)],
            [[i,-i] for i in range(1,MIN_ROW_COL_LENGTH)],
            [[-i,i] for i in range(1,MIN_ROW_COL_LENGTH)],
            [[-i,-i] for i in range(1,MIN_ROW_COL_LENGTH)],
            ], axis=0),
    7 : np.concatenate([ # 'HISHA'
            [[i,0] for i in range(1,ROW_LENGTH)],
            [[-i,0] for i in range(1,ROW_LENGTH)],
            [[0,i] for i in range(1,COL_LENGTH)],
            [[0,-i] for i in range(1,COL_LENGTH)],
            ], axis=0),
    8 : np.array([[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]), # 'OU'
    9 :np.array([[1,0],[1,1],[1,-1],[0,1],[0,-1],[-1,0]]), # 'HU_KIN'
    10 :np.array([[1,0],[1,1],[1,-1],[0,1],[0,-1],[-1,0]]), # 'KASHA_KIN'
    11 :np.array([[1,0],[1,1],[1,-1],[0,1],[0,-1],[-1,0]]), # 'KEIMA_KIN'
    12 :np.array([[1,0],[1,1],[1,-1],[0,1],[0,-1],[-1,0]]), # 'GIN_KIN'
    13 : np.concatenate([  # 'KAKU_UMA'
                    [[i,i] for i in range(1,MIN_ROW_COL_LENGTH)],
                    [[i,-i] for i in range(1,MIN_ROW_COL_LENGTH)],
                    [[-i,i] for i in range(1,MIN_ROW_COL_LENGTH)],
                    [[-i,-i] for i in range(1,MIN_ROW_COL_LENGTH)],
                    [[1,0],[-1,0],[0,1],[0,-1]]
                    ], axis=0),
    14 : np.concatenate([ # 'HISHA_RYU'
                    [[i,0] for i in range(1,ROW_LENGTH)],
                    [[-i,0] for i in range(1,ROW_LENGTH)],
                    [[0,i] for i in range(1,COL_LENGTH)],
                    [[0,-i] for i in range(1,COL_LENGTH)],
                    [[1,1],[-1,1],[1,-1],[-1,-1]]
                    ], axis=0),
    -1 : -1*np.array([[1,0]]), # 'HU'
    -2 : -1*np.array([[i,0] for i in range(1,ROW_LENGTH)]), # 'KASHA'
    -3 : -1*np.array([[2,1], [2,-1]]), # 'KEIMA'
    -4 : -1*np.array([[1,0],[1,1],[1,-1],[-1,1],[-1,-1]]), # 'GIN'
    -5 : -1*np.array([[1,0],[1,1],[1,-1],[0,1],[0,-1],[-1,0]]), # 'KIN'
    -6 : -1*np.concatenate([ # 'KAKU'
            [[i,i] for i in range(1,MIN_ROW_COL_LENGTH)],
            [[i,-i] for i in range(1,MIN_ROW_COL_LENGTH)],
            [[-i,i] for i in range(1,MIN_ROW_COL_LENGTH)],
            [[-i,-i] for i in range(1,MIN_ROW_COL_LENGTH)],
            ], axis=0),
    -7 : -1*np.concatenate([ # 'HISHA'
            [[i,0] for i in range(1,ROW_LENGTH)],
            [[-i,0] for i in range(1,ROW_LENGTH)],
            [[0,i] for i in range(1,COL_LENGTH)],
            [[0,-i] for i in range(1,COL_LENGTH)],
            ], axis=0),
    -8 : -1*np.array([[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]), # 'OU'
    -9 : -1*np.array([[1,0],[1,1],[1,-1],[0,1],[0,-1],[-1,0]]), # 'HU_KIN'
    -10 : -1*np.array([[1,0],[1,1],[1,-1],[0,1],[0,-1],[-1,0]]), # 'KASHA_KIN'
    -11 : -1*np.array([[1,0],[1,1],[1,-1],[0,1],[0,-1],[-1,0]]), # 'KEIMA_KIN'
    -12 : -1*np.array([[1,0],[1,1],[1,-1],[0,1],[0,-1],[-1,0]]), # 'GIN_KIN'
    -13 : -1*np.concatenate([  # 'KAKU_UMA'
                    [[i,i] for i in range(1,MIN_ROW_COL_LENGTH)],
                    [[i,-i] for i in range(1,MIN_ROW_COL_LENGTH)],
                    [[-i,i] for i in range(1,MIN_ROW_COL_LENGTH)],
                    [[-i,-i] for i in range(1,MIN_ROW_COL_LENGTH)],
                    [[1,0],[-1,0],[0,1],[0,-1]]
                    ], axis=0),
    -14 : -1*np.concatenate([ # 'HISHA_RYU'
                    [[i,0] for i in range(1,ROW_LENGTH)],
                    [[-i,0] for i in range(1,ROW_LENGTH)],
                    [[0,i] for i in range(1,COL_LENGTH)],
                    [[0,-i] for i in range(1,COL_LENGTH)],
                    [[1,1],[-1,1],[1,-1],[-1,-1]]
                    ], axis=0),
}   


class KomaType(Enum):
    SENTE_HU = 1
    SENTE_KASHA = 2
    SENTE_KEIMA = 3
    SENTE_GIN = 4
    SENTE_KIN = 5
    SENTE_KAKU = 6
    SENTE_HISHA = 7
    SENTE_OU = 8
    SENTE_HU_KIN = 9
    SENTE_KASHA_KIN = 10
    SENTE_KEIMA_KIN = 11
    SENTE_GIN_KIN = 12
    SENTE_KAKU_UMA = 13
    SENTE_HISHA_RYU = 14
    GOTE_HU = -1
    GOTE_KASHA = -2
    GOTE_KEIMA = -3
    GOTE_GIN = -4
    GOTE_KIN = -5
    GOTE_KAKU = -6
    GOTE_HISHA = -7
    GOTE_OU = -8
    GOTE_HU_KIN = -9
    GOTE_KASHA_KIN = -10
    GOTE_KEIMA_KIN = -11
    GOTE_GIN_KIN = -12
    GOTE_KAKU_UMA = -13
    GOTE_HISHA_RYU = -14

koma_name_to_type_dict = {
    'SENTE_HU': 1,
    'SENTE_KASHA': 2,
    'SENTE_KEIMA': 3,
    'SENTE_GIN': 4,
    'SENTE_KIN': 5,
    'SENTE_KAKU': 6,
    'SENTE_HISHA': 7,
    'SENTE_OU': 8,
    'SENTE_HU_KIN': 9,
    'SENTE_KASHA_KIN': 10,
    'SENTE_KEIMA_KIN': 11,
    'SENTE_GIN_KIN': 12,
    'SENTE_KAKU_UMA': 13,
    'SENTE_HISHA_RYU': 14,
    'GOTE_HU': -1,
    'GOTE_KASHA': -2,
    'GOTE_KEIMA': -3,
    'GOTE_GIN': -4,
    'GOTE_KIN': -5,
    'GOTE_KAKU': -6,
    'GOTE_HISHA': -7,
    'GOTE_OU': -8,
    'GOTE_HU_KIN': -9,
    'GOTE_KASHA_KIN': -10,
    'GOTE_KEIMA_KIN': -11,
    'GOTE_GIN_KIN': -12,
    'GOTE_KAKU_UMA': -13,
    'GOTE_HISHA_RYU': -14,
}

koma_type_to_name_dict = {v:k for k,v in koma_name_to_type_dict.items()}

kihu_name_to_type_dict = {
    'FU': 1,
    'KY': 2,
    'KE': 3,
    'GI': 4,
    'KI': 5,
    'KA': 6,
    'HI': 7,
    'OU': 8, 
    'TO': 9,
    'NY': 10,
    'NK': 11,
    'NG': 12,
    'UM': 13,
    'RY': 14,
} 


promote_koma_type = {
    1:9, 2:10, 3:11, 4:12, 5:5, 6:13, 7:14, 8:8, 9:9, 10:10, 11:11, 12:12, 13:13, 14:14,
    -1:-9, -2:-10, -3:-11, -4:-12, -5:-5, -6:-13, -7:-14, -8:-8, -9:-9, -10:-10, -11:-11, -12:-12, -13:-13, -14:-14,
}

inverse_promote_koma_type = {
    1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:1, 10:2, 11:3, 12:4, 13:6, 14:7,
    -1:-1, -2:-2, -3:-3, -4:-4, -5:-5, -6:-6, -7:-7, -8:-8, -9:-1, -10:-2, -11:-3, -12:-4, -13:-6, -14:-7,
}

opponent_koma_type_to_mochigoma_type = {
  1:-1,
  2:-2,
  3:-3,
  4:-4,
  5:-5,
  6:-6,
  7:-7,
  9:-1,
  10:-2,
  11:-3,
  12:-4,
  13:-6,
  14:-7,
  -1:1,
  -2:2,
  -3:3,
  -4:4,
  -5:5,
  -6:6,
  -7:7,
  -9:1,
  -10:2,
  -11:3,
  -12:4,
  -13:6,
  -14:7,
}



class Player(Enum):
    sente = 1
    gote = -1

def get_koma_poligon_coord(x, y, invert=False, A=25.3, B=29.3, alpha=83.5, beta=115.5, scale=0.18):
    points = np.array([[0.2,0.],
                       [0.8,3.7],
                       [2.5,4.5],
                       [4.2,3.7],
                       [4.8, 0.]])
    if invert:
        points[:,1] *= -1
    cog = np.mean(points, axis=0)
    out = points - cog
    out *= scale
    out += np.array([x,y])
    return out
 
koma_type_to_jp_label = {
    1:'歩',2:'香',3:'桂',
    4:'銀',5:'金',6:'角',
    7:'飛',8:'王',9:'と',
    10:'香金',11:'桂金',12:'全',
    13:'馬',14:'龍'
    }

koma_type_to_en_label = {
    1:'HU',2:'KASHA',3:'KEIMA',
    4:'GIN',5:'KIN',6:'KAKU',
    7:'HISHA',8:'OU',9:'HU_KIN',
    10:'KASHA_KIN',11:'KEIMA_KIN',12:'GIN_KIN',
    13:'KAKU_UMA',14:'HISHA_RYU'
}


#koma_jp_en_label_dict = {koma_type_to_jp_label[i]:koma_type_to_en_label[i] for i in range(len(koma_type_to_jp_label))}
#
#koma_en_jp_label_dict = {koma_type_to_en_label[i]:koma_type_to_jp_label[i] for i in range(len(koma_type_to_jp_label))}
#
#
