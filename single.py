from email import message
from glob import glob
from itertools import count
from flask import Flask , render_template , request , redirect , url_for , session
from single import *
from threading import Event

app = Flask(__name__)

import random
import numpy as np


ocean = [['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-']]

opponent_ocean = [['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-'],
['-','-','-','-','-','-','-','-','-','-']]

turn = 0
_y = 0
oppo_add = 0
color = "primary"
visible = "hidden"
rounds = 0
winner = None
fired = None
_x = 0
_count = 0
add = 0
foggy = 0
og_ocean = ocean.copy()
ocean_size = 10
carrier_size = 5
battleship_size = 4
cruiser_size = 3
submarine_size = 3
destroyer_size = 2
all_sunk = 0
t_count = 0

global x_coord, y_coord
row_count = 0
#Question 1
def count_number_of_marker(oc , marker):
  count = 0
  for _m in oc:
    for markers in _m:
      if markers == str(marker):
        count += 1

  return count


def print_ocean():
    line = 1
    print("  A B C D E F G H I J")
    for i in ocean:
        if line < ocean_size:
            print(str(line)+" ", end='')
        else:
            print("0 ", end='')
        line = line + 1
        for j in i:
            print(j+" ", end='')
        print()
        

#Question 2
def fire_coords( oc , x , y):
  targets = ["a" , "b" , "c" , "d" ,"s"]
  
  if oc[int(x)][int(y)] in targets:
    oc[int(x)][int(y)] = "x"

  elif oc[int(x)][int(y)] == ("x" or "o"):
    return oc

  else:
    oc[int(x)][int(y)] = "o"

  return oc

def add_fleet( oc ,  m, size):
    ok = False
    marker = m
    while not ok:
        axis = random.randint(0, 1)
        if axis == 0:   #Row
            r = random.randint(0, 9)
            c = random.randint(0, ocean_size - size)
            count = 0
            for i in range(c, c + size):
                if oc[r][i] == '-':
                    count += 1
            if count == size:
                for i in range(c, c + size):
                    oc[r][i] = marker
                    # fleet_coor.append([r,i])
                ok = True
        else:           #Col
            r = random.randint(0, ocean_size - size)
            c = random.randint(0, 9)
            count = 0
            for i in range(r, r + size): #adjustable ## for i in range(size): 
                                                     ## ocean[r + i][c] = marker
                if oc[i][c] == '-':
                    count += 1
            if count == size:
                for i in range(r, r + size):
                    oc[i][c] = marker
                    # fleet_coor.append([i,c])
                ok = True

def reset_ocean():
  for i in range(10):
    for j in range(10):
      np_ocean[i][j] = "-"
      np_opponent_ocean[i][j] = "-"

def fleets_sunks():
  targets = ["a" , "b" , "c" , "d" ,"s"]
  count = 0
  oppo_count = 0
  for m in targets:
    if count_number_of_marker(np_ocean,m) == 0:
      count += 1
  for m in targets:
    if count_number_of_marker(np_opponent_ocean,m) == 0:
      oppo_count += 1
  if count == 5 or oppo_count == 5:
    return True

  else:
    return False


def sink_fleet():
  count = 0
  for col in range(np_ocean.shape[0]):
    for row in range(np_ocean.shape[1]):
      if fleets_sunks() == False:
        fire_coords(col, row)
        count += 1
  return count


np_ocean = np.array(ocean.copy())

np_opponent_ocean = np.array(opponent_ocean.copy())


@app.route('/sink_fleets/' , methods = ["POST"])
def sink_fleets():
    global all_sunk

    count  = sink_fleet()
    all_sunk = 1
    return redirect(url_for('home' , count = count ))


@app.route('/' )
def index():  
    return redirect(url_for('home', count = _count ))

@app.route('/call_back/' , methods = ['GET' , 'POST'])
def call_back(): 

  global rounds , all_sunk , visible , turn , fired , winner

  if request.method == "POST": 
    data = request.form.get('ship_coords')
    if all_sunk != 1:
        if data != None:
          data = list(data)
          data = [x for x in data if x != " "]
          x_coord = int(data[0])
          y_coord = int(data[2])

          turn = int(data[4])


          if fleets_sunks() == True:
              all_sunk = 1
              if turn == 1: winner = "Player 2"
              else: winner = "Player 1"

          if fired == None:
            if turn == 1:
                fire_coords( np_opponent_ocean, x_coord , y_coord)
                fired = False

            else:
                fire_coords( np_ocean, x_coord , y_coord)
                fired = True
            
            rounds += 1
          else:
            if turn == 0 and fired == False:
                fire_coords( np_ocean, x_coord , y_coord)
                fired = True

            if turn == 1 and fired == True:
                fire_coords( np_opponent_ocean, x_coord , y_coord)
                fired = False


                rounds += 1
      
          return render_template("index.html" , ocean = np_ocean, oppo_ocean = np_opponent_ocean , _counts = 0,  x_c = x_coord ,
          y_c = y_coord , rounds = rounds , _visible = visible,  _turn = turn , winner = winner)
        else:
          return render_template("data.html" , x_c = 0 )

    else:
      visible = "visible"
      return render_template("index.html" , ocean = np_ocean, _turn = turn , oppo_ocean = np_opponent_ocean, _counts = 0,  x_c = None ,
        y_c = None , rounds = rounds ,  _visible = visible , winner = winner)
  else:
    return render_template("index.html" , ocean = np_ocean , oppo_ocean = np_opponent_ocean, _counts = 0,  x_c = None ,
        y_c = None , rounds = rounds ,  _visible = visible, _turn = turn , winner = winner)



@app.route('/home/<count>' )
def home(count):  
    global _count , color , turn
    _c = 0
    _ocean = np_ocean
    _count = count
    return render_template('index.html' , rounds = rounds,
      ocean = _ocean , oppo_ocean = np_opponent_ocean , _counts = _count ,  _visible = visible,
      c = _c , _row_count = list(range(1,10)) , color = color , _turn = turn , winner = winner)

@app.route('/refresh/' , methods = ["POST"])
def refresh():
    global foggy , rounds ,all_sunk , visible , color , fired
    global add
    global _x , _y
    reset_ocean()
    fired = None
    add = 0
    foggy = 0
    visible = "hidden"
    color = "primary"
    all_sunk = 0
    rounds = 0
    _x , _y = 0 , 0
    return redirect(url_for('home', count = 0))



@app.route('/addFleet/' , methods = ["POST"])
def addFleet():
    global add , color
    if add == 0:
        add_fleet( np_ocean, 'a', carrier_size)
        add_fleet(np_ocean,'b', battleship_size)
        add_fleet(np_ocean,'c', cruiser_size)
        add_fleet(np_ocean,'s', submarine_size)
        add_fleet(np_ocean,'d', destroyer_size)

        add_fleet(np_opponent_ocean, 'a', carrier_size)
        add_fleet(np_opponent_ocean,'b', battleship_size)
        add_fleet(np_opponent_ocean,'c', cruiser_size)
        add_fleet(np_opponent_ocean,'s', submarine_size)
        add_fleet(np_opponent_ocean,'d', destroyer_size)
        add = 1
        color = "danger"
    else:
        pass

    return redirect(url_for('home' , count = _count , _turn = turn))




if __name__ == '__main__':
    app.run(debug=True)

