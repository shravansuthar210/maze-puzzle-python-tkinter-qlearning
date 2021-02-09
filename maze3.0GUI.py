import random
import tkinter

class maze():
    def __init__(self):
        # self.enviroment=[[1,1,1,1],[1,12,1,1],[1,0,0,1],[1,1,1,1]]
        # self.enviroment=[
        #                 [1,1,1,1,1,1,1],
        #                 [1,12,0,1,0,0,1],
        #                 [1,1,0,1,0,1,1],
        #                 [1,0,0,1,0,1,1],
        #                 [1,0,1,1,0,1,1],
        #                 [1,0,0,0,0,1,1],
        #                 [1,1,1,1,1,1,1],
        #             ]
        self.enviroment=[
                        [1,1,1,1,1,1,1,1,1],
                        [1,12,0,0,1,0,0,0,1],
                        [1,0,1,0,1,1,1,0,1],
                        [1,0,1,1,0,0,0,0,1],
                        [1,0,0,0,1,0,1,1,1],
                        [1,0,1,0,1,0,1,1,1],
                        [1,0,1,1,1,0,0,1,1],
                        [1,0,0,0,0,1,0,1,1],
                        [1,0,1,1,0,0,0,0,1],
                        [1,1,1,1,1,1,1,1,1]
                        ]
        self.start=(1,1)
        self.home=(1,5)#(1,5)#(2,2)
        self.previous_play=[]
        self.q_table={}
        self.alpha=0.5
        self.discout=0.5
        self.discount=0.5
        self.root=tkinter.Tk()

    def game_try_again(self):
        self.previous_play=[]
        self.enviroment=[
                        [1,1,1,1,1,1,1,1,1],
                        [1,12,0,0,1,0,0,0,1],
                        [1,0,1,0,1,1,1,0,1],
                        [1,0,1,1,0,0,0,0,1],
                        [1,0,0,0,1,0,1,1,1],
                        [1,0,1,0,1,0,1,1,1],
                        [1,0,1,1,1,0,0,1,1],
                        [1,0,0,0,0,1,0,1,1],
                        [1,0,1,1,0,0,0,0,1],
                        [1,1,1,1,1,1,1,1,1]
                    ]
    
    
    def update_q_table(self,state,action,next_state,reward,valid_action):
        try:
            value=self.q_table[state][action]
        except Exception as identifier:
            value=0.0
        try:
            v=list(self.q_table[next_state].values())
            next_value=max(v) if v else 0
        except Exception as identifier:
            next_value=0
        value=value+self.alpha*(reward+self.discout*next_value-value)
        try:
            self.q_table[state][action]=value
        except Exception as identifier:
            valid_action_new=valid_action.remove(action)
            q_table_row={}
            for i in valid_action:
                q_table_row[i]=0
            q_table_row[action]=value
            self.q_table[state]=q_table_row
        
    
    def get_max_action(self,state):
        try:
            value=self.q_table[state]
            key=[]
            values=[]
            for i in value:
                key.append(i)
                values.append(value[i])
            max_value=max(values)
            action_key_index=values.index(max_value)
            action_key=key[action_key_index]
            return action_key
        except Exception as identifier:
            return None
        
    
    def learn_game(self,max_number):
        for i in range(max_number):
            while True:
                state=str(self.get_player_position())
                valid_action=self.get_valid_action()
                action=self.get_action(state,valid_action)
                play=self.play(action)
                
                if self.is_game_win()==True:
                    print("win")
                    self.update_q_table(state,str(action),str(self.get_player_position()),100,valid_action)
                    break
                elif self.is_previous_position()==True:
                    print("lost")
                    self.update_q_table(state,str(action),str(self.get_player_position()),-100,valid_action)
                    break
                self.update_q_table(state,str(action),str(self.get_player_position()),0,valid_action)
            self.game_try_again()
        print(self.q_table)
        # print(self.previous_play)
    

    def is_previous_position(self):
        state=self.get_player_position()
        try:
            k=self.previous_play[:len(self.previous_play)-1].index(state)
            return True
        except Exception as e:
            return False

    def get_action(self,state,valid_action):
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
        return get_valid_action 

    def play(self,action):
        row,column=self.get_player_position()
        if action=='up':
            self.previous_play.append((row,column))
            self.enviroment[row][column]=0
            new_row=row-1
            self.enviroment[new_row][column]=12
        elif action=='down':
            self.previous_play.append((row,column))
            self.enviroment[row][column]=0
            new_row=row+1
            self.enviroment[new_row][column]=12
        elif action=='left':
            self.previous_play.append((row,column))
            self.enviroment[row][column]=0
            new_column=column-1
            self.enviroment[row][new_column]=12
        elif action=='right':
            self.previous_play.append((row,column))
            self.enviroment[row][column]=0
            new_column=column+1
            self.enviroment[row][new_column]=12
        return self.is_game_win()
    def display(self,render):
        if render==True:
            road={}
            for i in range(len(self.enviroment)):
                for j in range(len(self.enviroment)-1):
                    if self.enviroment[i][j]==1:
                        wall=tkinter.Button(self.root,bg='black',height=4,width=5)
                        wall.grid(row=i,column=j)
                    elif i==self.home[0] and j==self.home[1]:
                        home=tkinter.Button(self.root,bg='green',height=4,width=5)
                        home.grid(row=i,column=j)
                    elif (i,j)==self.start:
                        home=tkinter.Button(self.root,bg='red',height=4,width=5)
                        home.grid(row=i,column=j)
                        road[str((i,j))]=home
                    elif self.enviroment[i][j]==0:
                        way=tkinter.Button(self.root,height=4,width=5)
                        way.grid(row=i,column=j)
                        road[str((i,j))]=way
            while True:
                state=str(self.get_player_position())
                valid_action=self.get_valid_action()
                action=self.get_action(state,valid_action)
                play=self.play(action)
                road[state].configure(bg='blue')
                if self.is_game_win()==True:
                    print("win")
                    break
                elif self.is_previous_position()==True:
                    print("lost")
                    break

            
        else:
            for i in range(len(self.enviroment)):
                for j in range(len(self.enviroment)):
                    print(self.enviroment[i][j],end=',')
                print('\n')
    def root_mainloop(self):
        self.root.mainloop()

maze=maze()
maze.learn_game(100)
maze.display(True)
maze.root_mainloop()

