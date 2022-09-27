import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from utils import *
from full_shogi_layer import *
import json
import time


 


class ShogiBan():
    def __init__(self):
        self.nrows = ROW_LENGTH
        self.ncols = COL_LENGTH
        self.num_koma_type = len(koma_name_to_type_dict)
        self.num_layer = len(MochigomaLayerIndex)
        self.sente_koma_list = []
        self.gote_koma_list = []
        self.init_all_state()
        self.init_fig()

    def init_all_state(self):
        self.all_state = {}
        self.all_state['ban'] = np.zeros((self.nrows, self.ncols), dtype=np.int16)
        self.all_state['mochigoma'] = {k : 0 for k in mochigoma_type_list}
        self.state = np.zeros((self.num_layer, self.nrows, self.ncols))

        with open(init_spawn_file, "r") as f:
            for line in f.readlines():
                print(line)
                line = line.replace('\n', '')
                line_list = line.split(',')
                koma_type, row, col = [int(l) for l in line_list]

                self.all_state['ban'][row, col] = koma_type
                inv_r, inv_c = self._invert_position(row, col)
                self.all_state['ban'][inv_r, inv_c] = -1 * koma_type    # invert for "gote" player

                self.state[ban_index_to_layer_index[koma_type], row, col] = 1
                self.state[ban_index_to_layer_index[-1 * koma_type], inv_r, inv_c] = 1 # invert for "gote" player
                print(self.state[ban_index_to_layer_index[koma_type],:,:])
                print(self.state[ban_index_to_layer_index[-1*koma_type],:,:])


    def init_fig(self):
        #plt.close()
        self.fig = plt.figure()
        #self.ax = self.fig.add_subplot(1,1,1)
        #self.ax.set_xticks(np.arange(0,11,1))
        #self.ax.set_yticks(np.arange(0,11,1))
        #self.ax.set_xlim(0,self.ncols)
        #self.ax.set_ylim(0,self.nrows)
        #self.ax.grid()
        #self.ax.tick_params(labelbottom=False,
        #                    labelleft=False,
        #                    labelright=False,
        #                    labeltop=False)
        #self.ax.tick_params(bottom=False,
        #                    left=False,
        #                    right=False,
        #                    top=False)
        #self.ax.set_aspect('equal')

    def _get_mochigoma_num_in_jp(self):
        
        sente_mochigoma =  {koma_type_to_jp_label[abs(k)]:v for k, v in self.all_state['mochigoma'].items() if (k >0) & (k <8)}
        gote_mochigoma =  {koma_type_to_jp_label[abs(k)]:v for k, v in self.all_state['mochigoma'].items() if (k >0) & (k <8)}
        return sente_mochigoma, gote_mochigoma
   
    def reset_fig(self):
        #print("reset fig")
        plt.clf()
        self.ax = self.fig.add_subplot(1,1,1)
        self.ax.set_xticks(np.arange(0,self.ncols+2,1))
        self.ax.set_yticks(np.arange(0,self.nrows+2,1))
        self.ax.set_xlim(0,self.ncols)
        self.ax.set_ylim(0,self.nrows)
        self.ax.grid()
        self.ax.tick_params(labelbottom=False,
                            labelleft=False,
                            labelright=False,
                            labeltop=False)
        self.ax.tick_params(bottom=False,
                            left=False,
                            right=False,
                            top=False)
        self.ax.set_aspect('equal')

       

    def render(self, r_color=None, c_color=None):
        offset = 1.7 / self.nrows
        self.reset_fig()
        for r in range(self.nrows):
            for c in range(self.ncols):
                val = self.all_state['ban'][r,c]
                if abs(val) > 0:
                    
                    if (r_color==r) & (c_color==c):
                        facecolor = "gray"
                    else:
                        facecolor = "None"
                    y = self.nrows -1 - r
                    x = c
                    label = koma_type_to_jp_label[abs(val)]
                    self.ax.annotate(label, (x+LABEL_OFFSET_X,y+LABEL_OFFSET_Y), \
                                     size=LABEL_SIZE)
                    points = get_koma_poligon_coord(x+0.5,y+0.5, invert= (val<0))
                    patch = patches.Polygon(xy=points, closed=True, alpha=0.5, edgecolor='k', facecolor=facecolor)
                    self.ax.add_patch(patch)
        sente_mochigoma_jp = {koma_type_to_jp_label[k]:v for k,v in self.all_state['mochigoma'].items() if k > 0}
        gote_mochigoma_jp = {koma_type_to_jp_label[-1*k]:v for k,v in reversed(self.all_state['mochigoma'].items()) if k < 0}
        #plt.text(0,-1, "先手 " + json.dumps(sente_mochigoma_jp, ensure_ascii=False))
        #plt.text(0, 10, "後手" + json.dumps(gote_mochigoma_jp, ensure_ascii=False))
        plt.annotate(text = "先手" + json.dumps(sente_mochigoma_jp, ensure_ascii=False), \
                    xy = SENTE_MOCHIGOMA_PLOT_POS, xycoords ='figure points')
        plt.annotate(text = "後手" + json.dumps(gote_mochigoma_jp, ensure_ascii=False), \
                    xy = GOTE_MOCHIGOMA_PLOT_POS, xycoords ='figure points')
        plt.pause(0.1)

       
    def _invert_position(self, row, col): 
        # change view point from "sente" to "gote" (vice. versa)
        return( self.nrows -1 -row, self.ncols -1 -col)


    def _convert_koma_type(self, koma_type):
        if koma_type in koma_jp_label:
            koma_type = koma_jp_label.index(koma_type)
        elif koma_type in koma_en_label:
            koma_type = koma_en_label.index(koma_type)
        elif type(koma_type) is int:
            pass
        else:
            raise TypeError("Only int or JP/EN label str are accepted")
        return koma_type

    def _is_within_grid(self, row:int, col:int):
        return (row >=0) & (row < self.nrows) &\
                (col>=0) & (col <self.ncols)

    def _is_within_opponents_area(self, player:str, row:int, col:int):
        if Player[player].value > 0: # sente
            return row < OPPONENTS_AREA_ROW_NUM 
        else: # gote
            return row > ROW_LENGTH - OPPONENTS_AREA_ROW_NUM -1


    def _is_valid_koma_index(self, player:str, koma_type:int):
        # check whether player put available koma type
        koma_type *= Player[player].value
        return (koma_type > 0) & (koma_type < self.num_koma_type + 1)

    def _is_koma_on_shogiban(self, koma_type:int):
        # check whether available koma on shogiban for given koma_type
        if np.sum(self.all_state['ban'] == koma_type) > 0:
            return True

    def _has_koma_in_mochigoma(self, koma_type:int):
        return self.all_state['mochigoma'][koma_type] > 0

    def _is_empty_space(self, row, col):
        # check whether given coordinate is empty or not
        return self.all_state['ban'][row, col] == 0

    def _back_cast(self, koma_type:int, row:int, col:int):
        '''
        search space where given koma type can reach given (row, col)
        '''
        tmp_movable_region = movable_region[koma_type] + (row, col)
        within_grid = [self._is_within_grid(r,c) for r,c in tmp_movable_region]
        tmp_movable_region = tmp_movable_region[within_grid]

        movable_map = np.zeros((self.nrows, self.ncols))
        for (r, c) in tmp_movable_region:
          movable_map[r,c] = 1
        return movable_map

    def _find_movable_koma(self, koma_type:int, row:int, col:int):
        '''
        get movable koma on shogiban
        1: search given koma type on shogiban
        2: search space where given koma_type can reach
        return 1 AND 2 condition
        NOTE: obstacle koma check is not done here. 
        '''
        koma_on_shogiban = self.all_state['ban'] == koma_type
        koma_scope = self._back_cast(koma_type, row, col)
        return koma_on_shogiban * koma_scope


    def _erase_koma(self, row:int, col:int):
        '''
        erase koma on shogiban
        '''
        self.all_state['ban'][row, col] = 0
    
    def _write_koma(self, koma_type:int, row:int, col:int):
        '''
        (re-)write koma on shogiban
        '''
        self.all_state['ban'][row, col] = koma_type

    def _get_opponent_koma(self, player:str, koma_type:int):
        '''
        This function is called when player get opponent's koma
        convert opponent's koma type to own koma_type
        then, add own mochigoma dict
        '''
        mochigoma_type = opponent_koma_type_to_mochigoma_type[koma_type]
        self.all_state['mochigoma'][mochigoma_type] += 1

        

    def _koma_on_moving_pos(self, row:int, col:int):
        '''
        Simply return koma_type on given (row, col)
        '''
        return self.all_state['ban'][row, col]

    def _koma_side_on_moving_pos(self, player:str, row:int, col:int):
        ''' 
        Check koma side on moving position
        1: own side
        0: emtpy space
        -1: opponent side
        This function is used when moving koma.
        We can put koma only empty space or opponent side.
        '''
        return np.sign(self._koma_on_moving_pos(row, col) * Player[player].value)

    def _check_obstacle(self, rs, cs, re, ce):
        '''
        Check obstacle from start point to endpoint.
        This function is used for KASHA, KAKU, HISHA, UMA, RYU.
        No need to apply to 1 move koma (HU, KIN, GIN, OU)
        CAUTION: Do not apply this function to KEIMA. Cause Invalid move error.
        '''
        rmin = min(rs, re)
        rmax = max(rs, re)
        cmin = min(cs, ce)
        cmax = max(cs, ce)

        arr = self.all_state['ban']
        
        if rs == re: # move horizontal 
            obstacle = arr[rs, (cmin+1):cmax]
        elif cs == ce: # move vertical
            obstacle = arr[(rmin+1):rmax, cs]
        elif abs(ce - cs) == abs(re - rs): # move diagonal
            if (ce -cs) * (re - rs) > 0:
                obstacle = np.diag(arr[(rmin+1):rmax, (cmin+1):cmax])
            else:
               obstacle = np.diag(np.flipud(arr[(rmin+1):rmax, (cmin+1):cmax]))
        else:
            raise ValueError("Invalid move")
        num_obstacle_koma = np.sum(abs(obstacle))
        return num_obstacle_koma > 0

    def _rule_violation(self, **kwargs):
        #print("rule violation check...")
        nihu_flag = self._nihu(**kwargs)
        return nihu_flag

    def _nihu(self, player:str):
        #print("calling NIHU check")
        if np.any(np.sum(self.all_state['ban'] == Player[player].value, axis=0) > 1):
            print("NIHU violation!!!!!!!!!!!!!!!!!!")
            return True

       
    def move(self, player:str, koma_type:int, row:int, col:int, row_from:int=None, col_from:int=None, render=False):
        koma_promotion_check = False
             
        # Check 1: Player put valid koma type
        if not self._is_valid_koma_index(player, koma_type):
            print(f"Valid koma index, for player {player}")
            return False

        # Check 2: Player set row, col inside or shogiban
        if not self._is_within_grid(row, col):
            print("row, col are outside grid.")
            return False
        
        # Check 3: Player does not put koma on pre-existing own koma.
        koma_side = self._koma_side_on_moving_pos(player, row, col)
        if koma_side == 1:
            print("own koma already exists on moving position")
            return False
        elif koma_side == 0:
            pass
            #print("moving position is empty")
        elif koma_side == -1:
            pass
            #print("opponent koma exists on moving position")

        # Check 4-1: Find movable koma on shogiban for given set (koma_type, row, col)
        movable_koma = self._find_movable_koma(koma_type, row, col)
        # Check 4-2: at least one or more movable koma
        num_movable_koma = np.sum(movable_koma)
        print(f"num_movable_koma: {num_movable_koma}")
        if num_movable_koma ==0:
            # Cehck 4-2: given koma type is after promotion
            if koma_type not in mochigoma_type_list and \
                np.sum(self._find_movable_koma(inverse_promote_koma_type[koma_type], row, col)):
                print("Original (before promotion) koma can be availabel. Koma might be promoted...")
                koma_promotion_check = True
                movable_koma = self._find_movable_koma(inverse_promote_koma_type[koma_type], row, col)
                num_movable_koma = np.sum(movable_koma)
            # Check 4-3: search koma from mochigoma list
            elif self._has_koma_in_mochigoma(koma_type):
                if koma_side == 0: # player can put mochigoma only on empty space
                    self._write_koma(koma_type, row, col)
                    self.all_state['mochigoma'][koma_type] -= 1
                    self._rule_violation(player=player)
                    if render:
                        self.render(row, col)
                    return True
                else: 
                    print("Player can put mochigoma only on empty space")
                    return False
            else:
                print("for all movable komas, obstacle exists. Or you doesn't has mochigoma. No koma can move")
                return False

        movable_koma = np.array(np.where(movable_koma==1)).T

        if num_movable_koma > 1:
            print('#####CAUTION!! Multi koma can move for this action! 1st one is applied!!! #####')
        
        # Check 5: select movable koma on the list.
        # First movable koma are seleteced on the list as long as they are not blocked by obstacles. 
        #### CAUTION: You can modify policy to choose one koma from movable koma plans.
        has_movable_koma_on_shogiban = False
        # try to use row_from, col_from
        # Case 1: multiple movable koma is shogiban. One of them is (row_from, col_from) 
        print((row_from, col_from))
        if np.sum(np.all(movable_koma == [row_from, col_from], axis=1)) == 1:
            print("Supporting info (where koma moves from) is available")
            has_movable_koma_on_shogiban = True
            row_start,col_start = row_from, col_from
        # Case 2: There is movable koma on Shogiban, but player puts koma from mochigoma
        elif (row_from, col_from) == (0,0):
            print("Player explicity tells 'Koma is from mochigoma list'")
            self._write_koma(koma_type, row, col)
            self.all_state['mochigoma'][koma_type] -= 1
            self._rule_violation(player=player)
            if render:
                self.render(row, col)
            return True
        else:
            for row_start, col_start in movable_koma:
                if (abs(koma_type) != 3) and self._check_obstacle(row_start, col_start, row, col): 
                    # This koma are blocked by obstacle. Discard it and go to next movabel koma
                    print("obstacle exists")
                else:
                    # This koma is selected because there are no obstacles on along direction.
                    has_movable_koma_on_shogiban = True
                    print("from movable koma list, koma is selected")
                    break

        # Check 6: after select moving koma, Just Move!
        # Check 6-1: if player get opponent's koma, add it to mochigoma list
        if koma_side == -1:
            self._get_opponent_koma(player = player,
                    koma_type = self._koma_on_moving_pos(row, col)
                    )
        # erase own koma before moving
        self._erase_koma(row_start, col_start)

        # Check 6-3: If moved koma is within opponent's area, then promote.
        if ((self._is_within_opponents_area(player, row, col)) or \
           (self._is_within_opponents_area(player, row_start, col_start))) and \
           koma_promotion_check:
            koma_type = promote_koma_type[koma_type]
            print("Koma promoted!!")

        # write koma on moving position
        self._write_koma(koma_type, row, col)
        self._rule_violation(player=player)
        if render:
            self.render(row, col)
        return True
       
        ### By above health check, player can move koma.

    def _all_state_to_state(self):
        self.state[:,:,:] = 0 
        for row in range(self.nrows):
            for col in range(self.ncols):
                koma_type = self.all_state['ban'][row, col]
                if koma_type != 0:
                    self.state[ban_index_to_layer_index[koma_type], row, col] = 1
        for k,v in shogiban.all_state['mochigoma'].items():
            if v > 0:
                for i in range(v):
                    index = mochigoma_index_to_layer_index[k][i]
                    self.state[index, :, :] = 1
        



                    

##plt.ion()
shogiban = ShogiBan()

with open("kihu_04.txt", "r") as f:
    discard_line = True
    for i ,line in enumerate(f.readlines()):
        if line == "%TORYO\n":
            break
        if not discard_line:
            #time.sleep(3)
            print(i)
            print(f"{i-start_line}手")
            print(line)
            player = line[0]
            player = "sente" if player == "+" else "gote"
            col = 8 - (int(line[3]) -1)
            row = int(line[4]) -1
            col_from = 8 - (int(line[1]) -1) if int(line[1]) != 0 else 0
            row_from = int(line[2]) -1 if int(line[2]) != 0 else 0
            koma_type = line[5:7]
            koma_type = kihu_name_to_type_dict[koma_type]
            koma_type *= Player[player].value
            shogiban.move(player, koma_type, row, col, row_from, col_from, render=True)
            print(shogiban.all_state['ban'])
        if line =="+\n":
            print(f"line match at {i}")
            discard_line = False
            start_line = i




