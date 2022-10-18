#%%
#AIの記述

import numpy as np
import copy 
import random  
class Node:    #授業の2回目に行った、幅優先探索のノードクラス
    #クラスの初期化。最初のノードは親もない、場所もない。
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.depth = 0

str_path = []

def return_path (node,goal):##授業の2回目に行った、幅優先探索の経路をコマンドで返す
    #　出力経路リストの初期化    
    if (str_path == []):
        path = []
        current = node
        # 現在のノードはスタートまで（親はNone）に迷路の場所(position)を保存
        while current is not None:
            path.append(current.position)
            current = current.parent
        # 作成した経路はゴールノードからスタートノードまでなので逆方向にする

        path = path[::-1]
        for i in range(len(path)-1):#それぞれの移動量に対してコマンドで対応する
            #print(path[i])
            if (path[i][0] > path[i+1][0]):
                str_path.append("w")
            elif(path[i][0] < path[i+1][0]):
                str_path.append("s")
            elif(path[i][1] > path[i+1][1]):
                str_path.append("a")
            else:
                str_path.append("d")
        
        # 戻り値は作成した経路
    if str_path == []:#デバッグ用
        return "w"
    return str_path.pop(0) #["w","d","s","w"]　経路のリストの最後を持ってくる！

        

def breadth_first_search(stageFloor, start, goal):#幅優先探索の関数　スタートとゴールの座標を入力すると,マップを参照してコマンドで帰ってくる
    #　スタートノードとゴールノードを作成（クラスを使用）と深さを初期化
    start_node = Node(None, start)
    start_node.depth = 0
    goal_node = Node(None, goal)
    goal_node.depth = 0

    #print(start,goal)
    
    # まだ訪問されていないノードと既に訪問されたノードを初期化。
    # 既に訪問されたノードは同じノードをもう1回訪問しないためのリスト
    queue = []
    visited_nodes = []
    # スタートノードはまだ訪問されていないので未訪問リストに保存
    queue.append(start_node)
    
    # 2次元の迷路の可能な移動
    move = [[-1, 0],    # 上
            [0, -1],    # 左
            [1, 0],     # 下
            [0, 1]]     # 右

    
    # 迷路の行と列の数を把握（numpyは便利）
    row_no, column_no = np.shape(stageFloor)#------------------------------
    #row_no = len(stageFloor) - 1 
    #column_no = len(stageFloor[0]) - 1 
    
    # ゴールノードを発見するまでのループ（まだ訪問されていないノードがある限る続く）
    while len(queue) > 0:
        #　次に展開するノードは待ち行列の先頭ノードなので待ち行列から取って、待ち行列から削除（popと便利）
        a = 0
        current_node = queue.pop()
        # 次に展開するノードを既に訪問されたノードに追加
        visited_nodes.append(current_node)
        
        # 展開のために選んだノードはゴールノードならば探索終了。その場合、戻り値はスタートからゴールまでの経路（return_path関数で作成）
        if current_node.position == goal_node.position and a == 0:
            #print("Breadth First Search success!!")
            #print("Path cost: ", current_node.depth)
            #print("current posi ",current_node.position)
            return return_path(current_node,goal)
        
        # ノードを展開する。全ての可能な行動を把握。この迷路ゲームの場合、4つ方向は可能（上、左、下、右）
        # 可能な移動先のノードを保存するためのリストを初期化
        
        children = []
        for new_position in move:
            # 次の場所を把握
            node_position = [current_node.position[0] + new_position[0],
                            current_node.position[1] + new_position[1]]
            #　迷路から出ていないことを確認
            if (node_position[0] > (row_no - 1) or
                node_position[0] < 0 or
                node_position[1] > (column_no - 1) or
                node_position[1] < 0):
                continue
            
            # 壁の確認
            
            if stageFloor[node_position[0]][node_position[1]] == WALL :#予想値が壁なら探索の候補に入れない
                #or stageFloor[node_position[0]][node_position[1]] == ENEMY or stageFloor[node_position[0]][node_position[1]] == STEP or stageFloor[node_position[0]][node_position[1]] == HOLE:
                continue
            
            # 可能な移動先。その移動先のノードを作成
            new_node = Node(current_node, node_position)
            #print(new_node.position)
            #print(new_node.position)
            #print(stageFloor[new_node.position[0]][new_node.position[1]])
            
            # 可能な移動先のノードを保存（リストに追加）
            children.append(new_node)

        # 全ての作成された移動先のノードに対して、既に訪問されたかどうか、未訪問ノードの中に既にあるかどうかを確認
        for child_node in children:
            # 子ノードの場所は既に訪問されたら追加しない
            for visited in visited_nodes:
                if child_node.position == visited.position:
                    break
            else:               
                # 子ノードの深さは親ノードの深さ＋１。その情報を保存
                child_node.depth = current_node.depth + 1
                    
                # まだ訪問されていないノードの中に同じ迷路の場所があるならば追加しない
                for node in queue:
                    if child_node.position == node.position:#自身が通る予定のところ　具体的には言って前のノード
                        break
                else:
                    #　未訪問ノードにない場合、未訪問ノードに追加
                    queue.append(child_node)


ADJACENT_LIST = [[0,1],[1,0],[0,-1],[-1,0]]#下,右,上,左

def use_step_response(pmap):#階段を利用するかどうかの判断をする関数
    not_Blank = [] 
    for y in range(10):
            for x in range(10):
                if( (pmap[y][x] != WALL) and (pmap[y][x] != BLANK) ):
                    not_Blank.append([y,x]) #イベントを入れ込む!
    #not_Blank.sort()

    #if ((ENEMY not in not_Blank ) and (BUSH not in not_Blank) and (up_down == True)):#そのフロアで出来る事がなくて、上を目指すとき
    if (up_down == True):#そのフロアで出来る事がなくて、上を目指すとき
        response = "y"
    else:
        response = "n"#それ以外は上がらない
    return response

up_down = False #上へ向かうのか下へ向かうのか決めるグローバル変数　 Falseは下へ向かう

class AI:
    def __init__(self): #全階層のある３次元配列:stageMaps
        pass

    def ai_move(self,stageFloor,playerY,playerX,Life,item_potion_num,item_Sword_num,item_Shield_num,item_key):#ＡＩの移動コマンドを決める関数
        start = [playerY,playerX]#スタートの座標
        pmap_copy = copy.deepcopy(stageFloor)#stageFloorのコピー
        not_Blank = []#イベントを入れ込むリスト
        for y in range(len(stageFloor)-1):
            for x in range(len(stageFloor)-1):
                if( (stageFloor[y][x] != WALL) and (stageFloor[y][x] != BLANK) ):#壁でも空きでもない時
                    not_Blank.append(stageFloor[y][x])#イベントを入れ込む!
               
        not_Blank.sort()#ソートを行う
        #print(not_Blank)

        if(not_Blank == [STEP] or not_Blank == [STEP,GOAL] or not_Blank == [STEP,ENEMY] or not_Blank == [STEP,GOAL,ENEMY]):#最下層に行った時に、
            global up_down
            up_down = True #上に向かうモードにする
        if(not_Blank == [HOLE] or not_Blank == [HOLE,GOAL] or not_Blank == [HOLE,ENEMY] or not_Blank == [HOLE,GOAL,ENEMY]):#最上階に行った時に、
            up_down = False#下に向かうモードにする
        
        #以下はソートされたフロアに配置されたオブジェクトを優先度を変えて並び変える
        sort_not_Blank = []

        for name in (not_Blank):
            if(name == POTION) or (name == SWORD) or (name == SHIELD) or (name == KEY):#回復薬、剣、盾、鍵などのアイテムを第1優先
                sort_not_Blank.append(name)
        for name in (not_Blank):#芝を第２優先
            if (name == BUSH):
                sort_not_Blank.append(name)
        for name in (not_Blank):
            if (name == ENEMY) and (item_Shield_num + item_Sword_num > 2) and (Life > 1):#敵を第3優先、itemとライフを見て倒せる状態の時のみ
                sort_not_Blank.append(name)
        for name in (not_Blank):
            if (name == GOAL) and (item_key == True):#ゴールは第4優先、鍵を持っているときのみ
                sort_not_Blank.append(name)
    
        if(up_down == False):#最下層が目的地の時は
            for name in (not_Blank):
                if (name == HOLE) :
                    sort_not_Blank.append(name)#穴を第５優先
            if not (sort_not_Blank == []):#優先度の関係で何も向かうところがない場合は
                for i in (not_Blank):
                    if (i != BUSH) and (name != POTION) and (name != SWORD) and (name != SHIELD) and (name != KEY) and (name != ENEMY) and (name != GOAL):
                        sort_not_Blank.append(name)#それら以外のオブジェクトを加える!
        else:
            for name in (not_Blank):
                if (name == STEP):#最上階が目的地の時は
                    sort_not_Blank.append(name)
            if not (sort_not_Blank == []):#優先度の関係で何も向かうところがない場合は
                for i in (not_Blank):
                    if (i != BUSH) and (name != POTION) and (name != SWORD) and (name != SHIELD) and (name != KEY) and (name != ENEMY) and (name != GOAL):
                        sort_not_Blank.append(name)#それら以外のオブジェクトを加える!

        if (sort_not_Blank == []) and up_down == True:#優先度の関係で何も向かうところがない、最上階を目指す場合は
            sort_not_Blank = [STEP]#階段を目指す
        elif (sort_not_Blank == []) and up_down == False:#優先度の関係で何も向かうところがない、最下層を目指す場合は
            sort_not_Blank = [HOLE]#穴を目指す

       # print(sort_not_Blank)

       #以下は敵の攻撃範囲をみて入らないようにする
        for y in range(len(stageFloor)-1):
            for x in range(len(stageFloor)-1):
                if((stageFloor[y][x] == ENEMY) and (sort_not_Blank[0] != ENEMY)):#オブジェクトリストに敵がいないならば
                    #print("-------------------------------------------------------------------check-ENEMY-RANGE")
                    for i in range(len(ADJACENT_LIST)):#自身の索敵範囲4マス
                        enemyPredictedY = ADJACENT_LIST[i][0] + y
                        enemyPredictedX = ADJACENT_LIST[i][1] + x
                        if(pmap_copy[enemyPredictedY][enemyPredictedX] == BLANK) :#敵の攻撃範囲を壁にする
                            pmap_copy[enemyPredictedY][enemyPredictedX] = WALL
        goals = []
        for y in range(len(stageFloor)-1):
            for x in range(len(stageFloor)-1):
                if( stageFloor[y][x] == sort_not_Blank[0] ): #sort_not_Blank[0]が多くある場合、全てを記録
                    goals.append([y,x])

        goal = random.choice(goals)#そのリストからランダムでゴールに設定　このようにしないとゴールが敵の周りにある場合、エラーになる
        #print(breadth_first_search(stageFloor, start, goal))
        return breadth_first_search(pmap_copy, start, goal) #w,a,s,d

    def input(self,
    stageFloor,
    
    playerY,
    playerX,

    Life,

    item_potion_num,
    item_Sword_num,
    item_Shield_num,
    item_key):#コマンドを決める関数
        zone_enemy = False#周囲に敵がいるのか
        for i in range(len(ADJACENT_LIST)):#自身の索敵範囲4マス
            enemyPredictedY = ADJACENT_LIST[i][0] + playerY
            enemyPredictedX = ADJACENT_LIST[i][1] + playerX
            #if(stageFloor[enemyPredictedY][enemyPredictedX] == BLANK):#アイテムが範囲内にあるかもしれないので、空白の時のみ
               #stageFloor[enemyPredictedY][enemyPredictedX] == WALL #敵の攻撃範囲をwallという事にする
            
            if(stageFloor[enemyPredictedY][enemyPredictedX] == ENEMY):#自身の周りに敵がいたとき
                zone_enemy = True
                #if((item_Shield_num + item_Sword_num > 1) and (Life > 1)) or (Life > 2):
                if(Life > 1):#自分のライフが2以上ならば
                    return "g"  #攻撃！
        #stageFloor[enemyPredictedY][enemyPredictedX] == BLANK #----------------------------------------------------------------ここで敵の位置によってつまされる事が少なくなる
                                  
        if( (zone_enemy == False) and (Life < 3) and (item_potion_num > 0) ):#敵が周りにいない、ライフが三以下、回復薬が0以上なら
            return "h"  #回復！
       
        stageFloor[playerY][playerX] == BLANK#芝から敵を発見した時にエラーになるので
        return self.ai_move(stageFloor,playerY,playerX,Life,item_potion_num,item_Sword_num,item_Shield_num,item_key) #ここに移動アルゴリズムを返す！　returnは"w","a","s","d"のいずれか
                
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#以下はゲーム本体
import random
import time

#define
#<system>

DEBUGMODE = False

ENDTIME = 40 

IGNOREWAITMODE = True
SEARCH_WAIT_TIME = 1.3
EVENT_WAIT_TIME = 1.1
if(IGNOREWAITMODE == True):
    SEARCH_WAIT_TIME = 0
    EVENT_WAIT_TIME = 0

#</system>

#<MAP>
FLOORSIZE_X = 11 
FLOORSIZE_Y = 11 

NUM_OF_FLOORS = 4 

BLANK = 0 #何もない床
WALL = 1 #壁
HOLE = 2 #穴
STEP = 3 #階段
GOAL = 4 #鍵階段or鍵穴(区別なし)
BUSH = 5 #茂み
POTION = 6 #回復アイテム
SWORD = 7 #剣アイテム
SHIELD = 8 #盾アイテム
KEY = 9 #鍵アイテム
ENEMY = 10 #敵
PLAYER = 11 #主人公

BUSH_AMOUNT = 6 
POTION_AMOUNT = 1 
#</MAP>

#<EVENTLIST>
EVENT_NONE = 0 
EVENT_FINDSWORD = 1 #(剣発見)
EVENT_FINDESHIELD = 2 #(盾発見)
EVENT_FINDPOTION = 3 #(回復薬発見)
EVENT_FINDHOLE = 4 #(穴発見)
EVENT_FINDSTEP = 5 #(階段発見)
EVENT_FINDGOAL = 6 #(鍵付き発見)
EVENT_FINDENEMY = 7 #(敵発見)
EVENT_GOAL = 9 
EVENT_ATTACK_TO_PLAYER = 10 
EVENT_ATTACK_TO_ENEMY = 11 #(素攻撃イベント)
EVENT_STRONG_ATTACK_TO_ENEMY = 13 #(強攻撃イベント)
EVENT_INTO_BUSH = 12 #(茂みに入った)
EVENT_USE_STEP = 15 #階段を使用する
EVENT_FALL_HOLE = 16 #穴を使用する
EVENT_FIND_KEY = 17 
EVENT_DROP_KEY = 18 #敵の鍵ドロップイベント
EVENT_DROP_SWORD = 19 #剣のドロップイベント
EVENT_DROP_SHIELD = 20 #盾のドロップイベント
EVENT_DROP_POTION = 21 #回復薬のドロップイベント


#</EVENTLIST>

#<Player>
#ステータス系
MAN_X = 9 #playerの初期座標の仮置き
MAN_Y = 8 #playerの初期座標の仮置き
PLAYER_DEF_ATK = 1 
PLAYER_DEF_HP = 3 
PLAYER_DEF_MOVE = 1 #1以外にならない想定

NONE_MODIFY_DAMAGE = 1 
SWORD_MODIFY_DAMAGE = 2 
#</Player>

#<Enemy>
ENEMY_HP = 3 
ENEMY_ATK = 1 
#</Enemy>

#//===================================================================================================================//

#global
EventObserver = EVENT_NONE, [MAN_X, MAN_Y] 

class Map:
    def __init__(self, stageMaps, eventList, numOfStage = 0):#(int floorMap[4][11][11], int eventList[4][6]) 
        
        self.stageMaps = stageMaps 
        self.eventList = eventList 
        self.numOfStage = numOfStage #プレイヤーが今居る階層
        
    def generateBush(self, eventListNum: int):
        pass 
        
    def summonEnemy(self):
        pass 
        
    def generateItem(self, eventListNum: int):
        pass 
        
    def generateStep(self, playerX, playerY, numOfStage):#メイン関数でイベントリストを参照してこの生成関数が呼ばれる！よって、呼ばれる関数の判定はメイン関数で行う！
        self.stageMap[numOfStage][playerY][playerX] = 3 
        
    def generateHole(self, playerX, playerY, numOfStage):
        self.stageMap[numOfStage][playerY][playerX] = 2 
        
    def generateItem(self, eventListNum: int):
        pass 
        
    def generateGoal(self, playerX, playerY, numOfStage):
        self.stageMap[numOfStage][playerY][playerX] = 4 
        
    def floorMove(self, destinationFloor: int):#イベントIDから新しいフロアのマップへ行く、関数(要確認)
        pass 
        
    def search_blank(self, fmap):
        blank_list = []
        #floor_num = random.randint(0, 3)
        #search_floor = fmap[floor_num]
        search_floor = fmap
        
        for i in range(len(search_floor[0])):
            for j in range(len(search_floor[1])):
                if search_floor[i][j] == BLANK:
                    blank_list.append([i,j])
        random_choice_blank = random.choice(blank_list)
        return random_choice_blank#y, xが返ってくる？要調査
        
    def printFloor(self, MyX: int, MyY: int):
        #for k in range (len(self.stageMaps)):#階層
        
        k = self.numOfStage 
        if(DEBUGMODE == True):
            print(f"floor={k}") 
        
        for i in range(len(self.stageMaps[k])):#y座標
            
            tempstr = ""
            for j in range(len(self.stageMaps[k][i])):#x座標
                
                #マップ翻訳部分
                if(i == MyY and j == MyX):
                    tempstr += ("{:>1}".format("主")) 
                    
                elif(self.stageMaps[k][i][j] == BLANK):
                    tempstr += ("{:>1}".format("□ ")) #何もないマス
                    
                elif(self.stageMaps[k][i][j] == WALL):
                    tempstr += ("{:>1}".format("■ ")) #壁
                    
                elif(self.stageMaps[k][i][j] == HOLE):
                    tempstr += ("{:>1}".format("穴")) #穴
                    
                elif(self.stageMaps[k][i][j] == STEP):
                    tempstr += ("{:>1}".format("階")) #階段
                    
                elif(self.stageMaps[k][i][j] == GOAL):
                    tempstr += ("{:>1}".format("🔒")) #ゴール
                    
                elif(self.stageMaps[k][i][j] == BUSH):
                    tempstr += ("{:>1}".format("茂")) #茂み
                    
                elif(self.stageMaps[k][i][j] == POTION):
                    tempstr += ("{:>1}".format("♡ ")) #回復薬
                    
                elif(self.stageMaps[k][i][j] == SWORD):
                    tempstr += ("{:>1}".format("⚔ ")) #剣
                    
                elif(self.stageMaps[k][i][j] == SHIELD):
                    tempstr += ("{:>1}".format("🛡 ")) #盾
                    
                elif(self.stageMaps[k][i][j] == KEY):
                    tempstr += ("{:>1}".format("🗝 ")) #鍵
                    
                elif(self.stageMaps[k][i][j] == ENEMY):
                    tempstr += ("{:>1}".format("敵")) #敵
                    
                else:
                    tempstr += ("{:>1}".format("□ ")) #エラー用
            
            print(tempstr) 
        print() #改行用

#//===================================================================================================================//

class Player:
    def __init__(self, playerX, playerY):
        self.playerX = playerX 
        self.playerY = playerY 
        self.past_playerX = 0 
        self.past_playerY = 0 
        self.player_Atk = PLAYER_DEF_ATK 
        self.item_Sword_num = 0 
        self.item_Shield_num = 0 #敵の攻撃時にライフの代わりに消費する
        self.player_Life = PLAYER_DEF_HP 
        self.item_potion_num = 0 
        self.dev = PLAYER_DEF_MOVE
        self.keyboard = None 
        self.item_key = False 
        
    def keyBoardInput(self, inputkey, pmap):#inputkey, int[][] pmap 
        global EventObserver
        ai = AI()
        
        nextX = self.playerX 
        nextY = self.playerY 
        
        if (inputkey == "w"):
            nextY -= 1 
            if (pmap[nextY][nextX] == WALL or pmap[nextY][nextX] == ENEMY):
                
                reinput = ai.input(#AIクラスからキーコマンドを入力
            
            pmap, #現在の階層情報

            self.playerY, #y軸のplayer値
            self.playerX, #x軸のplayer値
         
            self.player_Life, #playerのHP
            
            self.item_potion_num, #playerのHP
            self.item_Sword_num, 
            self.item_Shield_num,
            self.item_key,
        ) #------------------------------------------------------ここのreinputにもai.inputをいれたい。。。けど、参照できない...
                self.keyBoardInput(reinput, pmap) 
            else:
                self.shift(0, -self.dev, pmap) 

        elif (inputkey == "a"):
            nextX -= 1 
            if (pmap[nextY][nextX] == WALL or pmap[nextY][nextX] == ENEMY):
                reinput = ai.input(#AIクラスからキーコマンドを入力
                            pmap, #現在の階層情報

                            self.playerY, #y軸のplayer値
                            self.playerX, #x軸のplayer値
                        
                            self.player_Life, #playerのHP
                            
                            self.item_potion_num, #playerのHP
                            self.item_Sword_num, 
                            self.item_Shield_num,
                            self.item_key,
                            ) 
                self.keyBoardInput(reinput, pmap) 
            else:
                self.shift(-self.dev, 0, pmap) 

        elif (inputkey == "s"):
            nextY += 1 
            if (pmap[nextY][nextX] == WALL or pmap[nextY][nextX] == ENEMY):
                reinput = ai.input(#AIクラスからキーコマンドを入力
                            pmap, #現在の階層情報

                            self.playerY, #y軸のplayer値
                            self.playerX, #x軸のplayer値
                        
                            self.player_Life, #playerのHP
                            
                            self.item_potion_num, #playerのHP
                            self.item_Sword_num, 
                            self.item_Shield_num,
                            self.item_key,
                            ) 
                self.keyBoardInput(reinput, pmap) 
            else:
                self.shift(0, self.dev, pmap) 

        elif (inputkey == "d"):
            nextX += 1 
            if (pmap[nextY][nextX] == WALL or pmap[nextY][nextX] == ENEMY):
                reinput = ai.input(#AIクラスからキーコマンドを入力
                            pmap, #現在の階層情報

                            self.playerY, #y軸のplayer値
                            self.playerX, #x軸のplayer値
                        
                            self.player_Life, #playerのHP
                            
                            self.item_potion_num, #playerのHP
                            self.item_Sword_num, 
                            self.item_Shield_num,
                            self.item_key,
                            ) 
                self.keyBoardInput(reinput, pmap) 
            else:
                self.shift(self.dev, 0, pmap) 

        elif (inputkey == "h"):
            self.potion_use(pmap) 

        elif (inputkey == "y"):
            self.use_step(pmap) 

        elif (inputkey == "g"):
            if(DEBUGMODE == True):
                print(":::::::")
                printListofMap(pmap) 
            breakflag = True 
            for i in range(len(ADJACENT_LIST)):
                if(DEBUGMODE == True):
                    print()
                    #print(f"狙った場所にあるもの:{pmap[ADJACENT_LIST[i][0]+self.playerY][ADJACENT_LIST[i][1]+self.playerX]}")
                    
                enemyPredictedY = ADJACENT_LIST[i][0]+self.playerY
                enemyPredictedX = ADJACENT_LIST[i][1]+self.playerX
                
                if(pmap[enemyPredictedY][enemyPredictedX] == ENEMY):
                    breakflag = False 
                    self.attack(enemyPredictedX ,enemyPredictedY) 
                    if(DEBUGMODE == True):
                        #print("attack()")
                        print()
                    
                    return 
            if(breakflag == True):
                reinput = input("周囲に敵はいません。再入力してください。")
                self.keyBoardInput(reinput, pmap) 
                
        elif(inputkey == "r"):
            self.print_rule() 
            EventObserver = EVENT_NONE, [self.playerX, self.playerY] 
            
            return
            #reinput = input("行動を入力してください。")
            #self.keyBoardInput(reinput, pmap) 
            
        elif(DEBUGMODE == True):
            if(inputkey == "I R Winner"):
                print("************")
                print("チートコード:AOE2 Winner Cheat")
                print("************")
                EventObserver = EVENT_GOAL, [self.playerX, self.playerY] 

        else:
            reinput = ai.input(#AIクラスからキーコマンドを入力
                            pmap, #現在の階層情報

                            self.playerY, #y軸のplayer値
                            self.playerX, #x軸のplayer値
                        
                            self.player_Life, #playerのHP
                            
                            self.item_potion_num, #playerのHP
                            self.item_Sword_num, 
                            self.item_Shield_num,
                            self.item_key,
                            ) 
            self.keyBoardInput(reinput, pmap) 
        
    #//---------------------------------------------------------// 
            
    def shift(self, devx, devy, pmap):
        global EventObserver

        self.past_playerX = self.playerX 
        self.past_playerY = self.playerY 
        
        self.playerX = self.playerX + devx 
        self.playerY = self.playerY + devy 

        if (pmap[self.playerY][self.playerX] == HOLE): # 穴の場合
            self.go_underground() 
            
        elif (pmap[self.playerY][self.playerX] == STEP): # 階段の場合
            self.go_upper(pmap) 
            
        elif (pmap[self.playerY][self.playerX] == GOAL): #鍵付きの穴または階段の場合
            self.keyItemuse() 
            
        elif (pmap[self.playerY][self.playerX] == BUSH): #茂み
            EventObserver = EVENT_INTO_BUSH, [self.playerX, self.playerY] 
            return EVENT_INTO_BUSH, [self.playerX, self.playerY] 
        
        elif (pmap[self.playerY][self.playerX] == POTION or  pmap[self.playerY][self.playerX] == SWORD or  pmap[self.playerY][self.playerX] == SHIELD or  pmap[self.playerY][self.playerX] == KEY): # 移動先にアイテムの時
            self.itemPickedUp(pmap) 
            
        else:
            EventObserver = EVENT_NONE, [self.playerX,self.playerY] 
            return EVENT_NONE, [self.playerX,self.playerY] 
        
    #//---------------------------------------------------------//
    def potion_use(self, pmap):
        global EventObserver
        
        if (self.item_potion_num >= 1 and self.player_Life < PLAYER_DEF_HP):
            print("回復薬を使ってHPを回復した。(回復薬 -1)")
            time.sleep(EVENT_WAIT_TIME)
            self.item_potion_num -= 1 
            self.player_Life += 1 
            
            EventObserver = EVENT_NONE,[self.playerX,self.playerY]
            return EVENT_NONE,[self.playerX,self.playerY]
        else:
            reinput = input("回復薬がないか、ライフが最大です。もう一度、キーを入力してください。")
            self.keyBoardInput(reinput, pmap) 
            
    def attack(self, enemyX, enemyY): #敵のHP操作は行っていない(イベント値を返すだけ)
        global EventObserver
            
        if (self.item_Sword_num >= 1):
            self.item_Sword_num -= 1 
            EventObserver = EVENT_STRONG_ATTACK_TO_ENEMY, [enemyX, enemyY] 
            return EVENT_STRONG_ATTACK_TO_ENEMY, [self.playerX, self.playerY] #有名無実化しているのでそのままに
        
        else:
            EventObserver = EVENT_ATTACK_TO_ENEMY, [enemyX, enemyY] 
            return EVENT_ATTACK_TO_ENEMY, [self.playerX, self.playerY] 
        
    def go_underground(self): # HOLE
        global EventObserver
        
        EventObserver = EVENT_FALL_HOLE, [self.playerX, self.playerY] 
        return EVENT_FALL_HOLE, [self.playerX, self.playerY] 

    def go_upper(self, pmap): # 3
        global EventObserver
        
        inputkey = use_step_response(pmap)#--------------------------------------------------------------------------------------------------------------------------------------------
        if (inputkey == "y"):
            self.use_step(pmap) 
            
        elif (inputkey == "n"):
            EventObserver = EVENT_NONE, [self.playerX, self.playerY] 
            return EVENT_NONE, [self.playerX, self.playerY] 
        
        else:
            if(DEBUGMODE == True):
                print("入力されたキーが対応してないんじゃ、ぼけぇぇぇ！！by Hiratsuka") 
            else:
                print("入力されたキーが対応してません。再入力してください。(y/n)") 
            self.go_upper(pmap) 
            
    def use_step(self, pmap):
        global EventObserver
        
        if (pmap[self.playerY][self.playerX] == STEP): 
            EventObserver = EVENT_USE_STEP, [self.playerX, self.playerY] 
            return EVENT_USE_STEP, [self.playerX, self.playerY] 
        else:
            reinput = input("足元に階段がありません。再入力してください。") 
            self.keyBoardInput(reinput, pmap) 
            
    def keyItemuse(self): # GOAL
        global EventObserver
    
        if (self.item_key == True):
            inputkey = "y" #input("鍵を使ってダンジョンを脱出しますか？(y/n)") 
            if (inputkey == "y"):
                EventObserver = EVENT_GOAL, [self.playerX, self.playerY] 
                return EVENT_GOAL, [self.playerX, self.playerY] 
            
            elif (inputkey == "n"):
                print("あなたはダンジョンの探索を続けます。")
                time.sleep(EVENT_WAIT_TIME)
                EventObserver = EVENT_NONE, [self.playerX, self.playerY] 
                return EVENT_NONE, [self.playerX, self.playerY] 
            else:
                ("入力されたキーが対応してません。再入力してください。(y/n)") 
                self.keyItemuse() 
        else:
            print("鍵がありません。") 
            time.sleep(EVENT_WAIT_TIME)
            EventObserver = EVENT_NONE, [self.playerX, self.playerY] 
            return EVENT_NONE, [self.playerX, self.playerY] 
        
    def itemPickedUp(self, pmap): #アイテム取得
        global EventObserver
        
        eventID = 0 
        if (pmap[self.playerY][self.playerX] == POTION): # 移動先に回復薬があった場合
            eventID = EVENT_FINDPOTION
            #self.item_potion_num += 1 
            
        elif (pmap[self.playerY][self.playerX] == SWORD): # 移動先に剣があった場合
            eventID = EVENT_FINDSWORD
            #self.item_Sword_num += 1 
            
        elif (pmap[self.playerY][self.playerX] == SHIELD): # 移動先に盾があった場合
            eventID = EVENT_FINDESHIELD
            #self.item_Shield_num += 1 
            
        elif (pmap[self.playerY][self.playerX] == KEY): # 移動先に鍵があった場合
            eventID = EVENT_FIND_KEY
            self.item_key = True 

        EventObserver = eventID, [self.playerX,self.playerY] 
        return EVENT_NONE, [self.playerX,self.playerY] 
    
    # Playerクラス　PlayerのHPを減らす関数
    def Player_HP_Reduce(self):
        if(self.item_Shield_num <= 0):
            self.player_Life -= 1 
        else:
            self.item_Shield_num -= 1 
            
    def print_rule(self):
        global EventObserver 
        
        print("")
        print("--------------------------------------------------------------------------")
        print("☆ゲーム説明☆")
        print()
        print("このゲームは全４階層からなるダンジョンをクリアするゲームです。")
        print("ゴールは最上階または最下層にあります。")
        print("ゴールするには鍵が必要です。")
        print("その鍵はどこかの階層にいる敵が所持しています。")
        print("敵を攻略しながらゴールを目指してください。")
        
        print("")
        print("")
        time.sleep(EVENT_WAIT_TIME)
        
        print("☆移動方法 & キー操作説明☆")
        print()
        print("'w'キー入力で上に１マス移動")
        print("'a'キー入力で左に１マス移動")
        print("'s'キー入力で下に１マス移動")
        print("'d'キー入力で右に１マス移動")
        print("")
        print("'h'キー入力で回復薬使用　HPが＋１")
        print("'g'キー入力で上下左右にいる敵に1ダメージの攻撃　剣所持時は２ダメージの攻撃(必ず使われる)")
        print("'y'キー入力で階段の使用。　足元に'階'マスがあるときにも使用可能。")
        print("'n'キー入力で階段の使用を拒否。")
        print("'r'キー入力でこのルール説明を再度開く。")
        
        
        print("")
        print("")
        time.sleep(EVENT_WAIT_TIME)
        
        print("☆フィールドマス説明☆")
        print()
        print("フィールドマスマス一覧　'主' '茂' '□' '■' '穴' '階' '🔒' ' ♡' '⚔' '🛡' '🗝' '敵'")
        
        print("'主'マス　・・・　主人公マス。これを動かす。")
        print("'茂'マス　・・・　イベントマス。踏むと何かが起こる。")
        print("'□'マス　・・・　空マス。移動可能。")
        print("'■'マス　・・・　壁マス。侵入できない。")
        print("'穴'マス　・・・　イベントマス。強制的に下の階に移動。")
        print("'階'マス　・・・　イベントマス。上の階に移動することが出来る。拒否可能。")
        print("'🔒'マス　・・・　ゴールマス。鍵を持ってここに来ればクリア！")
        print("' ♡'マス　・・・　回復薬が手に入る")
        print("'⚔'マス　・・・　剣が手に入る。")
        print("'🛡'マス　・・・　盾が手に入る。")
        print("'🗝'マス　・・・　鍵が手に入る。")
        print("'敵'マス　・・・　敵がいるマス。自分が上下左右のマスに入ると攻撃をうける")
        
        print("")
        print("")
        time.sleep(EVENT_WAIT_TIME)
        
        print("☆アイテム説明☆")
        print()
        print("回復薬　・・・　回復が出来る。使用はhキー")
        print("　盾　　・・・　防御力が上がり、受けるダメージがなくなる。")
        print("　剣　　・・・　攻撃力が上がり、攻撃ダメージが１増える。")
        print("　鍵　　・・・　鍵が手に入る。これをもってゴールへ行こう。")
        print("--------------------------------------------------------------------------")
        print()
        
        return
        
        
#//===================================================================================================================//

class Enemy:
    def __init__(self, enemy_x, enemy_y, enemy_floor):
        self.enemy_x = enemy_x
        self.enemy_y = enemy_y
        self.enemy_floor = enemy_floor 
        self.enemy_Atk = ENEMY_ATK 
        self.enemy_Life = ENEMY_HP 
    
    def Enemy_attack(self, pmap, playerX: int, playerY: int, player_floor: int):
        global EventObserver
    
        around = [[1,0],[0,1],[0,-1],[-1,0]]
        for num in around:
            field_y = self.enemy_y + num[0] #探知マスy
            field_x = self.enemy_x + num[1] #探知マスx
            
            if (field_y == playerY and field_x == playerX and self.enemy_floor == player_floor): 
                if(DEBUGMODE == True):
                    print(f"(・・)/{num}")
                EventObserver = EVENT_ATTACK_TO_PLAYER, [self.enemy_x, self.enemy_y] 
                return EVENT_ATTACK_TO_PLAYER, [self.enemy_x, self.enemy_y] 
            
    def Enemy_HP_Reduce(self, getDamage: int):
        self.enemy_Life -= getDamage 
        return 
        

#//===================================================================================================================//
     
def InitMap(x, y, numOfFloors, bushAmount = BUSH_AMOUNT, potionAmount = POTION_AMOUNT):#x, y はフロアサイズ
    stageMaps = []
    
    midX = x // 2 
    midY = y // 2 
    
    
    for k in range(numOfFloors):
        floorMap = [] 
        randomPathPlaces = []
        randomPathPlaces.append(random.randint(1, midY-2)) 
        randomPathPlaces.append(random.randint(midY+1, y-2)) 
        randomPathPlaces.append(random.randint(1, midX-2)) 
        randomPathPlaces.append(random.randint(midX+1, x-2)) 
        
        #GenRoom
        for i in range(y):
            
            templist = [] 
            for j in range(x):
                if(i == 0 or j == 0 or i == x-1 or j == y-1 or i == midX or j == midY):
                    if((i == midX and j == randomPathPlaces[0]) or (i == midX and j == randomPathPlaces[1])
                    or (i == randomPathPlaces[2] and j == midY) or (i == randomPathPlaces[3] and j == midY)):
                        templist.append(BLANK) 
                    else:
                        templist.append(WALL) 
                
                else:
                    templist.append(BLANK) 
                    
            floorMap.append(templist) 
        
        if(DEBUGMODE == True):
            printListofMap(floorMap)
        
        #GenBUSH
        for j in range(bushAmount):
            tempint1 = 0 
            tempint2 = 0 
            if(DEBUGMODE == True):
                print(f"DEBUG*Bushunm: {j}")
                print(f"DEBUG*floorMap[y:{tempint2}][x:{tempint1}]:{floorMap[tempint2][tempint1]}")
            
            while(True):
                tempint1 = random.randint(2,5) 
                tempint2 = random.randint(2,5) 
                if(tempint1 >= 4):
                    tempint1 += 3 
                if(tempint2 >= 4):
                    tempint2 += 3 
                
                if(floorMap[tempint2][tempint1] == BLANK):
                    floorMap[tempint2][tempint1] = BUSH 
                    break 
                 
        """
        for j in range(potionAmount):
            tempint1 = random.randint(2,8) 
            tempint2 = random.randint(2,8) 
            if(tempint1 >= 5):
                tempint1 += 1 
            if(tempint2 >= 5):
                tempint2 += 1 
                
            if(floorMap[tempint2][tempint1] == BLANK):
                floorMap[tempint2][tempint1] = POTION 
            else:
                j -= 1 
        """
        
        ia = 0 
        while(True):
            if(ia >= potionAmount):
                break 
            else:
                tempint1 = random.randint(2,8) 
                tempint2 = random.randint(2,8) 
                if(tempint1 >= 5):
                    tempint1 += 1 
                if(tempint2 >= 5):
                    tempint2 += 1 
                
                if(floorMap[tempint2][tempint1] == BLANK):
                    if(DEBUGMODE == True):
                        print(f"( > <)/{ia}")
                    floorMap[tempint2][tempint1] = POTION 
                    ia += 1 
                
                
        stageMaps.append(floorMap) 
        
    #改修
    #tempI = random.randint(0,3) 
    #stageMaps[tempI][4][4] = KEY 
        
        #random.randint(1,x-2) 
        
    return stageMaps 

def InitEventList():
    event_list= [[],[],[],[]] # 4 階層分のイベント総リスト
    goal_floor = [0,3] # ゴールマスを生成すべき階層のリスト
    random_item = [EVENT_FINDSWORD ,EVENT_FINDESHIELD, EVENT_FINDPOTION] # ランダムアイテムリスト
    for floor in event_list: # 剣、盾、敵は各階層の茂みに一つずつは最低で生成
        floor.append(EVENT_FINDENEMY)
        floor.append(EVENT_FINDSWORD)
        floor.append(EVENT_FINDESHIELD)
    
    goal_floor_num = random.choice(goal_floor) # ゴールを最上階または最下階に生成する
    event_list[goal_floor_num].append(EVENT_FINDGOAL)
    
    event_list[0].append(EVENT_FINDSTEP) # 最下階には階段のみ
    
    event_list[1].append(EVENT_FINDHOLE) # 下から二番目の階には階段と穴を生成
    event_list[1].append(EVENT_FINDSTEP)
    
    event_list[2].append(EVENT_FINDHOLE) # 上から二番目の階には階段と穴を生成
    event_list[2].append(EVENT_FINDSTEP)
    
    event_list[3].append(EVENT_FINDHOLE) # 最上階にはのみ
    
    for floor in event_list:
        item_choice_1 = random.choice(random_item) # ランダムアイテムリストから一つランダムにアイテムを選び各階層のイベントリストに追加
        floor.append(item_choice_1)
        if len(floor) != 6: # 最上階と最下階はもう１つアイテムを選んで追加
            item_choice_2 = random.choice(random_item)
            floor.append(item_choice_2)
        random.shuffle(floor) # 先頭からpopするようにシャッフルする
        
    enemyCount = 0 
    for i in range(len(event_list)):
        enemyCount += event_list[i].count(EVENT_FINDENEMY) 
    enemy_event_list = [] 
    for i in range(enemyCount):
        if(i <= 0):
            enemy_event_list.append(EVENT_DROP_KEY) 
        else:
            enemy_event_list.append(18 + random.randint(1,3)) 
    random.shuffle(enemy_event_list) 
        
    
    return event_list, enemy_event_list 
        
    
    return event_list, enemy_event_list 

def printListofMap(l):
    output_row = ""
    row_no = 0
    column_no = 0
    
    output_rows = []
    
    for row in l:
        for entry in row:
            output_row += ("{:>3}".format(entry))
            column_no += 1
        #for i in range(len(u)):
        
        output_rows.append(output_row)
        
        #print(output_row)
        output_row = ""
        row_no += 1
        column_no = 0
    for i in range(len(output_rows)):
        print(output_rows[i])
        
def main():
    global EventObserver
    
    GameTime = 0 
    numOfStage = 0 #プレイヤーが今居る階層
    
    numOfStage = random.randint(0,3) 
    if(GameTime == 0):
        startFloor = numOfStage 
    
    templist = InitMap(FLOORSIZE_X, FLOORSIZE_Y, NUM_OF_FLOORS) 
    temp = InitEventList() 
    eventList = temp[0] 
    enemyEventList = temp[1] 
    
    if(DEBUGMODE == True):
        print("INIT_ENEMYEVENTLIST")
        print(enemyEventList)
    
    enemyList = [] 
    
    stage = Map(templist, eventList, numOfStage) #: class Map stage 
    #CheckPlayercouldPlace()
    
    temp = stage.search_blank(stage.stageMaps[numOfStage])
    player = Player(temp[1], temp[0]) # class Player player 
    
    print() 
    print("ダンジョンのどこかにある鍵を取得し、鍵のかかった扉を通って下さい") 
    time.sleep(EVENT_WAIT_TIME)
    print("1文字のキーを入力した後にEnterキーを入力すると行動します。")
    time.sleep(EVENT_WAIT_TIME)
    print()
    
    while(True):
        if(player.player_Life <= 0):
            print("HPが0になりました……") 
            time.sleep(EVENT_WAIT_TIME)
            print() 
            print("Game Over") 
            break 
        
        if(GameTime > ENDTIME and DEBUGMODE == True):#GameTimeになったら強制終了 Debug用
            break 
        
        if(DEBUGMODE == True):
            #stage.stageMaps[numOfStage][8][6] = HOLE 
            """
            #debug
            print(f"(≧∀≦){GameTime}") 
            
            #for i in range(11):#任意の座標を直接書き換えられるかの検証→できた。
            #    stage.stageMaps[0][0][i] = i 
            #stage.stageMaps[0][1][0] = 5
            
            
            #print(stage.stageMaps[0][0][0]) #//任意の座標の情報を直接取得できるかの検証→できた
            """
            
            """
            for i in range(NUM_OF_FLOORS):#全4フロアのマップ生成が出来ているかの確認用
                print(f"***DEBUG*** floorNum-{i}") 
                printListofMap(stage.stageMaps[i]) 
                print() 
            """
            printListofMap(stage.stageMaps[numOfStage]) 
            print(f"イベントリスト:{eventList[numOfStage]}")
            print(player.playerX, player.playerY)
            print("EventObserver's report ( ・・)/")
            print(EventObserver)
        
        tempF = numOfStage - startFloor 
        if(tempF >= 0):
            print(f"{tempF+1}階") 
        else:
            print(f"B{-tempF}階") 
        
        stage.printFloor(player.playerX, player.playerY) #現在のフロアのマップ表示、ゲーム本編で使用する仕様通り
        
        life_heart = ""
        for lp in range(player.player_Life):
            life_heart += "♥ "
        if lp < 3:
            for dp in range(3 - player.player_Life):
                life_heart += "♡ "
        print(f"体力:{life_heart}({player.player_Life}/3), 剣：{player.item_Sword_num}, 盾：{player.item_Shield_num}, 回復薬：{player.item_potion_num}")
        
        if(player.item_key == True):
            print("鍵：取得済み") 
        else:
            print("鍵：未取得") 
        print()
        print("操作説明") 
        print("wasd:移動/h:回復/y:足元の階段を進む/g:敵を攻撃/r:ルールを見る") 
        
        if(DEBUGMODE == True):
            print("##########################")
            print("( >・)/")
            print("DEBUGMODE is Active")
            print("##########################")
        
        #--------------------------------------------------------------------------------------------------------------
        ai = AI()#AIクラス作成

        keyInput = ai.input(#input関数からキーコマンドを入力！
            
            stage.stageMaps[numOfStage], #現在の階層情報

            player.playerY, #y軸のplayer値
            player.playerX, #x軸のplayer値
         
            player.player_Life, #playerのHP
            
            player.item_potion_num, #playerのHP
            player.item_Sword_num, 
            player.item_Shield_num,
            player.item_key,
        ) #ここに文字列が返される 
        
        #keyInput = input("行動を入力して下さい") #----------------------------------------ここでAI
        player.keyBoardInput(keyInput, stage.stageMaps[numOfStage]) #このリターンがreinputの時に処理を追加することで解決できそう！
        #--------------------------------------------------------------------------------------------------------------
        while(EventObserver[0] != EVENT_NONE):
            if(EventObserver[0] == EVENT_FINDSWORD):
                player.item_Sword_num += 1 
                stage.stageMaps[numOfStage][player.playerY][player.playerX] = BLANK 
                print("剣を発見した！ (剣 +1)")
                print()
                time.sleep(EVENT_WAIT_TIME)
                break 
                
            elif(EventObserver[0] == EVENT_FINDESHIELD):
                player.item_Shield_num += 1 
                stage.stageMaps[numOfStage][player.playerY][player.playerX] = BLANK 
                print("盾を発見した！ (盾 +1)")
                print()
                time.sleep(EVENT_WAIT_TIME)
                break 
                
            elif(EventObserver[0] == EVENT_FINDPOTION):
                player.item_potion_num += 1 
                stage.stageMaps[numOfStage][player.playerY][player.playerX] = BLANK 
                print("回復薬を発見した！ (回復薬 +1)")
                print()
                time.sleep(EVENT_WAIT_TIME)
                break 
                
            elif(EventObserver[0] == EVENT_FINDHOLE):
                stage.stageMaps[numOfStage][player.playerY][player.playerX] = HOLE 
                print("落とし穴だ！ (階層 -1F)")
                time.sleep(EVENT_WAIT_TIME)
                tempXY = stage.search_blank(stage.stageMaps[numOfStage-1]) 
                player.playerY = tempXY[0] 
                player.playerX = tempXY[1] 
                numOfStage -= 1 
                stage.numOfStage -= 1 
                print()
                break 
                
            elif(EventObserver[0] == EVENT_FINDSTEP):
                stage.stageMaps[numOfStage][player.playerY][player.playerX] = STEP 
                print("階段を発見した！これで上の階へ行く事ができる。 (使用時に階層 +1)")
                time.sleep(EVENT_WAIT_TIME)
                player.go_upper(stage.stageMaps[numOfStage]) 
                
                if(EventObserver[0] == EVENT_USE_STEP):
                    print("あなたは階段を進んだ") 
                    time.sleep(EVENT_WAIT_TIME)
                    tempXY = stage.search_blank(stage.stageMaps[numOfStage+1]) 
                    player.playerY = tempXY[0] 
                    player.playerX = tempXY[1] 
                    numOfStage += 1 
                    stage.numOfStage += 1 
                    print()
                print()
                break 
                
            elif(EventObserver[0] == EVENT_FINDGOAL):
                stage.stageMaps[numOfStage][player.playerY][player.playerX] = GOAL 
                print("鍵のかかった扉だ！先に進むには鍵が必要だ。 (鍵を使用してゲームクリアが可能)")
                print()
                time.sleep(EVENT_WAIT_TIME)
                
                if(player.item_key == True):
                    player.keyItemuse() 
                break 
                
            elif(EventObserver[0] == EVENT_FINDENEMY):
                stage.stageMaps[numOfStage][player.playerY][player.playerX] = ENEMY 
                tempX = player.playerX 
                tempY = player.playerY 
                player.playerY = player.past_playerY 
                player.playerX = player.past_playerX 
                tempEnemy = Enemy(tempX, tempY, numOfStage) 
                enemyList.append(tempEnemy) 
                print("敵だ！ (直前のマスへ押し戻され、攻撃を受ける)")
                print()
                time.sleep(EVENT_WAIT_TIME)
                
                break 
                
            elif(EventObserver[0] == EVENT_GOAL):
                print("鍵を使って、ダンジョンから脱出した！")
                time.sleep(EVENT_WAIT_TIME)
                print("ゲームクリア")
                print(f"経過したターン数:{GameTime}")
                return 
                
            elif(EventObserver[0] == EVENT_ATTACK_TO_ENEMY):
                if(DEBUGMODE == True):
                    print("Event_ATTACK_TO_ENEMY")
                for i in range(len(enemyList)):
                    
                    if(DEBUGMODE == True):
                        print(enemyList[i].enemy_x, enemyList[i].enemy_y)
                        print(EventObserver[1][0], EventObserver[1][1])
                    
                    if(enemyList[i].enemy_x == EventObserver[1][0] and enemyList[i].enemy_y == EventObserver[1][1]):
                        enemyList[i].Enemy_HP_Reduce(NONE_MODIFY_DAMAGE) 
                        
                        
                        if(DEBUGMODE == True):
                            print(":********:")
                            print(f"{enemyList[i].enemy_Life}") 
                            
                        print("あなたは敵に攻撃した！(敵に1ダメージを与える)") 
                        time.sleep(EVENT_WAIT_TIME)
                        break 
                break 
                
            elif(EventObserver[0] == EVENT_STRONG_ATTACK_TO_ENEMY):
                if(DEBUGMODE == True):
                    print("Event_ATTACK_TO_ENEMY_STRONG")
                for i in range(len(enemyList)):
                    
                    if(DEBUGMODE == True):
                        print(enemyList[i].enemy_x, enemyList[i].enemy_y)
                        print(EventObserver[1][0], EventObserver[1][1])
                    
                    if(enemyList[i].enemy_x == EventObserver[1][0] and enemyList[i].enemy_y == EventObserver[1][1]):
                        enemyList[i].Enemy_HP_Reduce(SWORD_MODIFY_DAMAGE) 
                        
                        if(DEBUGMODE == True):
                            print(":****::****:")
                            print(f"{enemyList[i].enemy_Life}") 
                            
                        print("あなたは剣で敵に攻撃した！(剣 -1)(敵に2ダメージを与える)") 
                        time.sleep(EVENT_WAIT_TIME)
                        break 
                
                break 
                
            elif(EventObserver[0] == EVENT_INTO_BUSH):
                print("あなたは茂みの中を探索した……")
                time.sleep(SEARCH_WAIT_TIME)
                EventObserver = eventList[numOfStage].pop(0), [player.playerX, player.playerY] 
                print()
                #breakしてはいけない
                
                
            elif(EventObserver[0] == EVENT_USE_STEP):
                print("あなたは階段を進んだ。") 
                tempXY = stage.search_blank(stage.stageMaps[numOfStage+1]) 
                player.playerY = tempXY[0] 
                player.playerX = tempXY[1] 
                numOfStage += 1 
                stage.numOfStage += 1 
                print()
                time.sleep(EVENT_WAIT_TIME)
                break 
                
            elif(EventObserver[0] == EVENT_FALL_HOLE):
                print("あなたは落とし穴へ自ら落ちた。") 
                tempXY = stage.search_blank(stage.stageMaps[numOfStage-1]) 
                player.playerY = tempXY[0] 
                player.playerX = tempXY[1] 
                numOfStage -= 1 
                stage.numOfStage -= 1 
                print()
                time.sleep(EVENT_WAIT_TIME)
                break 
                
            elif(EventObserver[0] == EVENT_FIND_KEY):
                player.item_key = True 
                stage.stageMaps[numOfStage][player.playerY][player.playerX] = BLANK 
                print("鍵を発見した！ (鍵を取得)")
                print()
                time.sleep(EVENT_WAIT_TIME)
                break 
                
        
        for i in range(len(enemyList)):
            delflag = False 
            
            #敵のHPチェック
            if(len(enemyList) > 0):
                print(i)
                if(enemyList[i].enemy_Life <= 0):
                    if(len(enemyEventList) > 0):
                        if(DEBUGMODE == True):
                            print(f"enemyEventList:{enemyEventList}")
                            
                        if(enemyEventList[0] == EVENT_DROP_KEY):
                            stage.stageMaps[numOfStage][enemyList[i].enemy_y][enemyList[i].enemy_x] = KEY 
                            
                        elif(enemyEventList[0] == EVENT_DROP_SWORD):
                            stage.stageMaps[numOfStage][enemyList[i].enemy_y][enemyList[i].enemy_x] = SWORD 
                            
                        elif(enemyEventList[0] == EVENT_DROP_SHIELD):
                            stage.stageMaps[numOfStage][enemyList[i].enemy_y][enemyList[i].enemy_x] = SHIELD 
                            
                        elif(enemyEventList[0] == EVENT_DROP_POTION):
                            stage.stageMaps[numOfStage][enemyList[i].enemy_y][enemyList[i].enemy_x] = POTION 
                        
                        del enemyEventList[0]
                        
                        
                    #stage.stageMaps[numOfStage][enemyList[i].enemy_y][enemyList[i].enemy_x] = BLANK 
                    del enemyList[i]
                    delflag = True 
                    
                    #未行動の敵が残っていない場合の確認
                    if(len(enemyList) <= i):
                        break 
                
                #敵のHPが残っていた場合、実行(敵の行動)
                if(delflag == False):
                    enemyList[i].Enemy_attack(stage.stageMaps
                    [numOfStage], player.playerX, player.playerY, numOfStage) 
                    if(EventObserver[0] == EVENT_ATTACK_TO_PLAYER):
                        player.Player_HP_Reduce() 
        
        
        
        GameTime += 1 
    
    return 
    
main()
# %%
