#!/usr/bin/env python3

import re, copy, sys
import AI


#Вместо len лучше было бы вставить hoops_number
class stack_pyramid(list):
    def __init__(self, arr = []):
        self.hoops_number = len(arr)
        list.__init__(self)
        for i in arr:
            self.append(i)
    def push(self, value):
        if not(self.hoops_number) or value <= self[-1]:
            self.hoops_number+=1
            self.append(value)
        else:
            raise Exception("ERROR: YOUR PYRAMID LIKE LEANING TOWER OF PISA")
    def pop(self):
        try:
            elem = self[-1]
            del self[-1]
            self.hoops_number-=1
            return elem
        except:
            raise Exception("ERROR: EMPTY PYRAMID.")
    def get_top(self):
        try:
            return self[-1]
        except:
            raise Exception("ERROR: EMPTY PYRAMID.")
    def get_all(self):
        return self
    def get_len(self):
        return self.hoops_number
        
class Game:

    mov_cmd = re.compile('\d+')
    
    def __init__(self, ai = None, who = "Player", lvl = 5, istream = input, ostream = print, log=0):
        self.status = "Runing"
        self.who = who
        self.istream = istream
        self.ai = ai
        self.lvl = lvl
        self.log = log
        self.count = 0
        arr = list(range(lvl+1))[1:]
        arr.reverse()
        self.pyramids = [
            stack_pyramid( copy.copy(arr) ),
            stack_pyramid(), 
            stack_pyramid()
        ]
        self.win_combination = arr
    
    def process(self):
        #(user_input[0] != "exit"  or user_input[0] != "e") and
        if (self.log==1):
            f= open('log.txt', 'w')
        while( self.status == "Runing"):
            if self.who == "Player":
                moves = self.istream().lower()
                moves = re.findall(Game.mov_cmd, moves)
                if len(moves) < 2: continue
                for i in range(len(moves)): moves[i] = int(moves[i])
            elif self.who == "AI":
                if self.count > 1000:
                    self.status = "Stopped"
                    print ("AI FAILED (TO MANY MOVES)")
                moves = self.ai(self)
            else: break
            if(  moves[0] > 0 and moves[0] < 4 ) and ( moves[1] > 0 and moves[1] < 4 ):
                self.count+=1
                from_ = moves[0]-1
                if (self.log==1):
                    f.write(str(from_))
                to_ = moves[1]-1
                if (self.log==1):
                    f.write(str(to_)+'\n')
            else:
                print("WRONG MOVE")
            try:
                self.pyramids[to_].push( self.pyramids[from_][-1] )
                self.pyramids[from_].pop()
            except:
                if self.who == "AI":
                    self.status = "Stopped"
                    print ("AI FAILED (FORBIDDEN MOVE)")
            self.situation()
    def draw(self):
        print ("COUNT: " + str(self.count) )
        print ("| "*3)
        for g in range(self.lvl):
            for pyramid in self.pyramids:
                try:
                    print( str(pyramid[self.lvl-g-1]), end=" " )
                except IndexError:
                    print("|", end=" ")
            print()
    def situation(self):
        #self.count+=1
        self.draw()
        if self.pyramids[2] == self.win_combination:
            self.status = "Win"
            print ("YOU WIN")
            
    
if __name__ == "__main__":
    game=Game()
    who1="Player"
    ai1=None
    log1=0
    if '--help' in sys.argv:
        print(u"\nПРАВИЛА:")
        print(u"Подробнее тут - https://ru.wikipedia.org/wiki/Ханойская_башня")
        print(u"Если вкратце, то нам даны 3 стержня, на первом из которых расположены N элементов")
        print(u"(В оригинале эти элементы - кольца разного диаметра, в нашем случае это числа) в порядке убывания снизу вверх.")
        print(u"Тоесть наменьшее кольцо расположено на вершине башни, а наибольшее лежит в основании, в самом низу.")
        print(u"Цель - переместить башню с первого стержня на заданный (либо на второй, либо на третий, либо на любой из них)")
        print(u"Причём можно снимать только один, верхний элемент с башни и класть его либо на пустой стержень,")
        print(u"либо на элемент большего размера. Тоесть 1 на 2 положить можно, а вот 2 на 1 - нет.\n")
        print(u"Основная информация:")
        print(u"Используй флаг --ai для того, чтобы играл ваш ИИ (для игры используется файл AI.py)")
        print(u"Чтобы ИИ сделал ход, верните в файле AI.py список из двух элементов - откуда куда соответсвенно")
        print(u"ПРИМЕР:")
        print(u"return [1, 2] - снять элемент из первой пирамиды и положить на вторую\n")
        print(u"Используйте следующие методы:")
        print(u"game.pyramids[N].get_top() - вернуть верхний элемент N-ой пирамиды")
        print(u"game.pyramids[N].get_all() (или просто game.pyramids[N]) - вернуть список всех элементов N-ой пирамиды")
        print(u"game.pyramids[N].get_len() - вернуть количество элементов в N-ой пирамиде\n")
        print(u"ВНИМАНИЕ!\n")
        print(u"N - номер пирамиды МИНУС один. Помните, что вы обращаетесь к списку :)")
        print(u"Если вы хотите получить информацию о первой пирамиде, то N = 0\n")
        print(u"УДАЧИ!\n")
        exit()
    if '--ai' in sys.argv:
        who1="AI"
        ai1=AI.AI
    if '--log' in sys.argv:
        log1=1
    game=Game(who=who1, ai=ai1,log=log1)



    # else: game = Game()
    game.draw()
    game.process()
