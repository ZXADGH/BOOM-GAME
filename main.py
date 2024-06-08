from tkinter import *
import random
from threading import Timer

window = Tk()
score = StringVar()

class mine_game():
    class minebtn(Button):
        def __init__(self, master, xy, **kw):
            Button.__init__(self, master, **kw)
            self.xy = xy
            self.state = 0
    def __init__(self):
        self.width = 10
        self.Height = 10
        self.minecnt = 10
        self.gamemine = self.minecnt
        self.timepuse = False
        self.run_boom_game()
        self.color = {
            0:'#000000',
            1:'#00FF00',
            2:'#0000FF',
            3:'#FF0000',
            4:'#FF0000',
            5:'#28004D',
            6:'#00E3E3',
            7:'#642100',
            8:'#FFD306',
            'B':'#000000'
        }

    def cr_map(self):
        global game_map
        game_map = []
        for i in range(self.width*self.Height):
            game_map.append(0)

    def cr_block(self):
        global window ,game_map
        self.button_list = []
        for i in range(self.width*self.Height):
            self.button_list.append(self.minebtn(window,state='active',width=4,height=2,xy = i))
            self.button_list[i].bind('<ButtonRelease-1>',lambda event:self.open(event.widget))
            self.button_list[i].bind('<ButtonRelease-3>',lambda event:self.make_point(event.widget))
            self.button_list[i].grid(row = i%10 + 1,column = int(i / 10))

    def cr_mine(self):
        global game_map
        self.mineplace = random.sample(range(self.width * self.Height), self.gamemine)
        for i in self.mineplace:
            game_map[i] = 1

    def open(self,widget):
        global game_map
        x = widget.xy % 10
        y = int(widget.xy / 10)
        print(widget.xy)
        if (self.timepuse == 1):
            self.t = Timer(1, self.timer1s)
            self.t.start()
            self.timepuse = 2
        if(widget.xy in self.mineplace):
            self.showmine()
            return
        if(widget.state == 1): return
        widget.config(state="disabled")
        widget.state = 1
        game_map[widget.xy] = 2
        near = [(x - 1, y - 1),
                (x, y - 1),
                (x + 1, y - 1),
                (x - 1, y),
                (x + 1, y),
                (x - 1, y + 1),
                (x, y + 1),
                (x + 1, y + 1)]
        how_many_mine = 0
        around_mine = []
        for a,b in near:
            if(0 <= a <= self.width-1 and 0 <= b <= self.Height-1):
                around_mine.append(a+b*10)
                if(a+b*10 in self.mineplace):
                    how_many_mine += 1
        if(how_many_mine == 0):
            widget['text'] = '0'
            for i in around_mine:
                print(i)
                if(self.button_list[int(i)].state == 0):
                    self.open(self.button_list[i])
        else:
            widget['text'] = how_many_mine


        tmp = 0
        for i in range(self.width*self.Height):
            if(game_map[i] == 2): tmp +=1
        if(tmp == self.width*self.Height - self.minecnt):
                for i in range(self.width * self.Height):
                    if (i in self.mineplace):
                        self.button_list[i].config(text='B')
                    else:
                        self.open(self.button_list[i])
                    self.restarbutton.config(text=":D")
                    self.t.cancel()


    def make_point(self,widget):
        if(widget.state == 0):
            widget.state = 2
            self.gamemine -= 1
            score.set(str(self.gamemine))
            widget['text'] = 'F'
        elif(widget.state == 2):
            widget.state = 3
            self.gamemine += 1
            score.set(str(self.gamemine))
            widget['text'] = '?'
        elif(widget.state == 3):
            widget.state = 0
            widget.config(text = "")

    def showmine(self):
        for i in range(self.width*self.Height):
            if(i in self.mineplace):
                self.button_list[i].config(text='B')
            else:
                self.open(self.button_list[i])
            self.restarbutton.config(text = ":(")
            self.t.cancel()

    def timer1s(self):
        self.time += 1
        self.timer1.config(text= str(self.time))
        self.t = Timer(1, self.timer1s)
        self.t.start()

    def game_restart(self):
        self.time = 0
        self.timepuse = 1
        self.timer1.config(text = str(self.time))
        self.gamemine = self.minecnt
        self.timer1.grid(row=0, column=8, columnspan=2)
        self.cr_map()
        self.cr_mine()
        self.cr_block()
        window.mainloop()

    def restart(self):
        self.time = 0
        self.timepuse = 1
        self.timer1.config(text=str(self.time))
        self.gamemine = self.minecnt
        self.timer1.grid(row=0, column=8, columnspan=2)
        self.restarbutton.config(text=":)")
        score.set(str(self.gamemine))
        self.cr_map()
        self.cr_mine()
        self.cr_block()
        self.t.cancel()

    def run_boom_game(self):
        global window
        window.title("踩地雷!")
        window.geometry("480x540")
        score.set(str(self.gamemine))
        self.boom = Label(window, textvariable=score, font=('黑體',20,'bold'), height=4, width=2).grid(row= 0,column=0)
        self.restarbutton =  Button(window,text = ":)",height = 2 ,width= 2,command= self.restart)
        self.restarbutton.grid(row = 0 ,column = 5)
        self.timer1 = Label(window,text='0', font=('黑體',20,'bold'))
        self.timer1.grid(row = 0 ,column = 8,columnspan=2)
        self.timepuse = 1
        self.cr_map()
        self.cr_mine()
        self.cr_block()
        self.game_restart()

mine_game()