from collections import defaultdict
import random
# import tkinter

class maze():
    def __init__(self,render=False):
        # self.enviroment=[[1,1,1,1],[1,12,1,1],[1,0,0,1],[1,1,1,1]]
        self.enviroment=[
                        [1,1,1,1,1,1,1],
                        [1,12,0,1,0,0,1],
                        [1,1,0,1,0,1,1],
                        [1,0,0,1,0,1,1],
                        [1,0,1,1,0,1,1],
                        [1,0,0,0,0,1,1],
                        [1,1,1,1,1,1,1],
                    ]
        self.start=(1,1)
        self.home=(1,5)#(2,2)#
        self.previous_play=[]
        self.q_table=defaultdict(lambda :defaultdict(lambda:0.0))
        self.alpha=0.5
        self.discout=0.5
        self.discount=0.5
        self.eps=1
        self.eps_action=2
        self.render=render
    
    def game_try_again(self):
        self.previous_play=[]
        self.enviroment=[
                        [1,1,1,1,1,1,1],
                        [1,12,0,1,0,0,1],
                        [1,1,0,1,0,1,1],
                        [1,0,0,1,0,1,1],
                        [1,0,1,1,0,1,1],
                        [1,0,0,0,0,1,1],
                        [1,1,1,1,1,1,1],
                    ]
        print(self.enviroment)
    
    
    def update_q_table(self,state,action,next_state,reward):
        value=self.q_table[state][action]
        v=list(self.q_table[next_state].values())
        next_value=max(v) if v else 0
        value=value+self.alpha*(reward+self.discount*next_value-value)
        self.q_table[state][action]=value
        # try:
        #     value=self.q_table[state][action]
        # except Exception as identifier:
        #     value=0.0
        # try:
        #     v=list(self.q_table[next_state].values())
        #     next_value=max(v) if v else 0
        # except Exception as identifier:
        #     next_value=0
        # print("next_value",next_value)
        # value=value+self.alpha*(reward+self.discout*next_value-value)
        # try:
        #     self.q_table[state][action]=value
        # except Exception as identifier:
        #     self.q_table[state]={action:value}
        
    
    def get_max_action(self,state):
        keys = list(self.q_table[state].keys())
        if not keys:
            return None
        return max(keys, key=lambda x: self.q_table[state][x])
        # value=self.q_table[state]
        # return max(value)
    
    def learn_game(self,max_number):
        for i in range(max_number):
            while True:
                state=str(self.get_player_position())
                valid_action=self.get_valid_action()
                action=self.get_action(state,valid_action)
                print(valid_action)
                print(state,action)
                play=self.play(action)
                
                if self.is_game_win()==True:
                    print("win")
                    self.update_q_table(state,str(action),str(self.get_player_position()),100)
                    break
                elif self.is_previous_position()==True:
                    print("lost")
                    self.update_q_table(state,str(action),str(self.get_player_position()),-100)
                    break
                self.update_q_table(state,str(action),str(self.get_player_position()),0)
            self.game_try_again()
            self.eps=self.eps+1
        print(self.q_table)
        # print(self.previous_play)
    

    def is_previous_position(self):
        state=self.get_player_position()
        try:
            k=self.previous_play[:len(self.previous_play)-1].index(state)
            print(k)
            return True
        except Exception as e:
            return False

    def get_action(self,state,valid_action):
        if self.eps<self.eps_action:
            return random.choice(valid_action)
        action=self.get_max_action(state)
        if action==None:
            return random.choice(valid_action)
        return action
        

    def is_game_win(self):
        row,column=self.get_player_position()
        if row==self.home[0] and column==self.home[1]:
            return True
        else:
            return False

    def get_player_position(self):
        for i in range(len(self.enviroment)):
            try:
                index1=self.enviroment[i].index(12)
                return i,index1
            except Exception as e:
                pass
    def get_aroung_position(self):
        row,column=self.get_player_position()
        start_row,start_column=row-1,column-1
        end_row,end_column=row+1,column+1
        first_row_matirix=self.enviroment[start_row][column:end_column]
        second_row_matirix=self.enviroment[row][start_column:end_column+1]
        third_row_matirix=self.enviroment[end_row][column:end_column]
        around_matix=[first_row_matirix,second_row_matirix,third_row_matirix]
        return around_matix
    def get_valid_action_position_def(self):
        get_valid_action_position=[]
        around_matix=self.get_aroung_position()
        for i in range(len(around_matix)):
            for j in range(len(around_matix[i])):
                if around_matix[i][j]==0:
                    get_valid_action_position.append((i,j))
        return get_valid_action_position

    def get_valid_action(self):
        get_valid_action=[]
        get_valid_action_position_def=self.get_valid_action_position_def()
        for i in get_valid_action_position_def:
            if i==(0,0):
                get_valid_action.append('up')
            elif i==(1,0):
                get_valid_action.append('left')
            elif i==(1,2):
                get_valid_action.append('right')
            elif i==(2,0):
                get_valid_action.append('down')
        return get_valid_action   #get_vlid_action

    def play(self,action):#up,down,left,right        
        row,column=self.get_player_position()
        if action=='up':#==True:
            self.previous_play.append((row,column))
            self.enviroment[row][column]=0
            new_row=row-1
            self.enviroment[new_row][column]=12
        elif action=='down':#==True:
            self.previous_play.append((row,column))
            self.enviroment[row][column]=0
            new_row=row+1
            self.enviroment[new_row][column]=12
        elif action=='left':#==True:
            self.previous_play.append((row,column))
            self.enviroment[row][column]=0
            new_column=column-1
            self.enviroment[row][new_column]=12
        elif action=='right':#==True:
            self.previous_play.append((row,column))
            self.enviroment[row][column]=0
            new_column=column+1
            self.enviroment[row][new_column]=12
        return self.is_game_win()
    def display(self):
        if render==True:
            pass
        else:
            for i in range(len(self.enviroment)):
                for j in range(len(self.enviroment)):
                    print(self.enviroment[i][j],end=',')
                print('\n')
            # print(self.enviroment)

maze=maze()
maze.learn_game(200)
# print(maze.is_game_win())
# maze.display()
# print(maze.get_player_position())
# print(maze.get_aroung_position())
# # print(maze.get_valid_action_position_def())
# print(maze.get_valid_action())
# maze.play(True,False,False,False)
