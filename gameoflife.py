import tkinter

win = tkinter.Tk()
WIDTH = 900
HEIGHT = 600

temp = 1

canvas = tkinter.Canvas(width=WIDTH,height=HEIGHT,bg="white")
canvas.grid(columnspan=3,rowspan=1)

fr = open("input.txt","r",encoding="UTF-8")

def drawgrid(ws=15):
    count = HEIGHT // ws
    for i in range(count):
        canvas.create_line(0,i*ws,WIDTH,i*ws)
    count = WIDTH // ws
    for i in range(count):
        canvas.create_line(i*ws,0,i*ws,HEIGHT)

def create2Dmatrix(width,height):
    matrix = []
    for y in range(height):
        temp = []
        for x in range(width):
            temp.append(0)
        matrix.append(temp)
    return matrix

def processfile(matrix):
    x = 0
    y = 0
    for row in fr:
        x = 0
        for char in row:
            if char =='1':
                matrix[y][x]=1
            x+=1
        y+=1

def returnFriends(x,y,matrix):
    global count
    count = 0

    if x<width-1 and matrix[y][x+1]==1:
        count+=1
    if x<width-1 and y < height-1 and matrix[y+1][x+1]==1:
        count+=1
    if y > 0 and matrix[y-1][x] == 1:
        count+=1
    if x < width-1 and y > 0 and matrix[y-1][x+1]==1:
        count+=1
    if y < height-1 and matrix[y+1][x]==1:
        count+=1
    if x >0 and y<height-1 and matrix[y+1][x-1]==1:
        count+=1
    if x>0 and matrix[y][x-1]==1:
        count+=1
    if x>0 and y>0 and matrix[y-1][x-1]==1:
        count+=1

    return count

def rewrite(oldfield,newfield):
    #cyklus v cykle v tom if s returnFriends
    for x in range(width):
        for y in range(height):
            if oldfield[y][x]==0:
                    friends = returnFriends(x,y,oldfield)
                    if friends == 3:
                        newfield[y][x]=1
            elif oldfield[y][x]==1:
                    friends = returnFriends(x, y, oldfield)
                    if friends == 2 or friends == 3:
                        newfield[y][x] = 1
                    elif friends < 2:
                        newfield[y][x] = 0
                    elif friends > 3:
                        newfield[y][x] = 0
    return newfield

width,height = fr.readline().split(" ")
width = int(width)
height = int(height)

#vytvorí 2rozmerny zoznam plny nul
oldfield = create2Dmatrix(width,height)
#vytvorí iny 2rozmerny zoznam plny nul
newfield = create2Dmatrix(width,height)
# do prveho zoznamu nahodime jednotky zo suboru
processfile(oldfield)

# print(returnFriends(1,0,oldfield))
# print(rewrite(oldfield,newfield))

def drawcells(oldfield,ws=15):
    canvas.delete("all")
    drawgrid()
    # for item in cellist:
    #     canvas.delete(item)
    # canvas.update()
    cellist = []
    for y in range(height):
        for x in range(width):
            if oldfield[y][x]==1:
                cellist.append(canvas.create_oval(x*ws,y*ws,(x+1)*ws,(y+1)*ws,fill="turquoise"))

def generations():
    if temp % 2 == 1:
        global oldfield,newfield,cellist
        print(oldfield)
        drawcells(oldfield)
        #vypocitas novy matrix
        #novy hodis do stareho -> pomocou cyklov
        for y in range(height):
            for x in range(width):
                newfield[y][x] = oldfield[y][x]
        #novy musis vynulovať
        rewrite(oldfield, newfield)
        oldfield = newfield.copy()
        newfield = create2Dmatrix(width,height)
        canvas.after(100,generations)
        #input()

def generacia_postupne():
    global oldfield,newfield,cellist
    print(oldfield)
    drawcells(oldfield)
    for y in range(height):
        for x in range(width):
            newfield[y][x] = oldfield[y][x]
    rewrite(oldfield, newfield)
    oldfield = newfield.copy()
    newfield = create2Dmatrix(width,height)

def stopauto():
    global temp
    temp += 1


drawcells(oldfield)
drawgrid()
button_auto = tkinter.Button(win,bg="grey",fg="white" ,text="Automatika", font="Arial 20",command=generations)
button_auto.grid(row=1,column=0)
button_auto = tkinter.Button(win,bg="grey",fg="white",text="Generácia", font="Arial 20",command=generacia_postupne)
button_auto.grid(row=1,column=2)
button_auto = tkinter.Button(win,bg="red",fg="white",text="Stop auto", font="Arial 10",command=stopauto)
button_auto.grid(row=1,column=1)
win.mainloop()
