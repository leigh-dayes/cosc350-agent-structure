""" 
    Agent Environment: simple agent demonstration with Tkinter.
    COSC350/550 Workshop 2
"""

import time
from threading import Thread
from tkinter import *
import numpy as np
import random
import os
import sys
from agent import Agent

# Start global variables #
quit = False
width = 500
height = 500
iterations = 1000000
num_bots = 50
dot_size = 10
delay = 0.05
# End global variables #

def create_circle(x, y, r, canvasName,colour,obj_tag): 
    "Create dot with fill colour: (x,y): center coordinates, r: radius "
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1,fill=colour,tag=obj_tag)

def collision_detection(x, y, bot_locs):
    " Detection based on radius and bot locations "
    global num_bots
    global dot_size
    rad = dot_size*0.9
    for i in range(num_bots):
        if (x > (bot_locs[i][0]-rad) and x < (bot_locs[i][0]+rad)) and (y > (bot_locs[i][1]-rad) and y < (bot_locs[i][1]+rad)):
            return i
        
    return -1
    
def create_environment(agent,bot_locs,myCanvas):
    " Create initial environment with enemy bots and agent  "
    global num_bots
    global dot_size
    for i in range(num_bots):
        bot_locs.append([random.randint(10,490),random.randint(10,490)])
        create_circle(bot_locs[i][0], bot_locs[i][1], dot_size, myCanvas,"red", "bot"+str(i))
    create_circle(agent.get_x(), agent.get_y(), dot_size, myCanvas,agent.get_colour(), agent.get_tag())
    #print(bot_locs)
    
    return bot_locs
        
    

def run_environment(agent,delay,iterations,bot_locs,myCanvas):
    " Main feed-back loop for agent "
    global width
    global height
    global quit
    global dot_size
     
    for i in range(iterations):
        if quit:
            return
        
		# New location to move to - agent decides action based on new location
        new_x = agent.get_x() + random.randint(-agent.get_speed(),agent.get_speed())
        new_y = agent.get_y() + random.randint(-agent.get_speed(),agent.get_speed())		
		
        # check boudaries and move to other if cross
        if new_x > width - dot_size:
            new_x = dot_size * 0.5
        elif new_x < dot_size:
            new_x = width - dot_size;
        if new_y > height - dot_size:
            new_y = dot_size * 0.5
        elif new_y < dot_size:
            new_y = height - dot_size;

        # Get status and then get action from agent
        detection = collision_detection(new_x,new_y, bot_locs)
        status = "unspecified"
        if detection >= 0:
            if detection % 2 == 0:
                status = "even"
            else:
                status = "odd"
        else:
            status = "free"
        
        action = agent.program(status,[new_x,new_y])
        
        if action == "move":
            time.sleep(delay)
            agent.set_x(new_x)
            agent.set_y(new_y)

        elif action == "eat":
            time.sleep(delay*2)
            myCanvas.delete("bot"+str(detection))
            bot_locs[detection][0] = -1
            bot_locs[detection][1] = -1
            agent.set_x(new_x)
            agent.set_y(new_y)
			
        elif action == "interact":
            time.sleep(delay*2)
            myCanvas.delete("bot"+str(detection))
            create_circle(bot_locs[detection][0], bot_locs[detection][1], dot_size, myCanvas,"green", "bot"+str(detection))
            bot_locs[detection][0] = -1
            bot_locs[detection][1] = -1
            agent.set_x(new_x)
            agent.set_y(new_y)
        elif action == "stop":
            print("Agent stopped")
            time.sleep(delay*10)
        
        # Update to stored location - delete current location
        if action != "wait":        		
            myCanvas.delete(agent.get_tag())
            create_circle(agent.get_x(), agent.get_y(), dot_size, myCanvas,agent.get_colour(), agent.get_tag())
    print("Max iterations of environment reached")  
    agent.print_model()
        
    quit = True

def start_thread(thread):
    thread.start()

def close_properly(root,thread):
    global quit
    if quit==False:
        quit = True
        thread.join(timeout=0.05)
    else:
        root.destroy()
    
def on_closing():
    print("Use Quit Button - Hit twice")
 

def main():
    " Main function: call and report... "
    global width
    global height
    global iterations
    global num_bots
    global delay
    global dot_size
    
    random.seed(os.urandom(128))
    root = Tk()
    root.title("Agent Environment")
    
    myCanvas = Canvas(root, width=width, height=height, borderwidth=0, highlightthickness=0, bg="white")
    myCanvas.pack()
    bot_locs = []
    
    agent = Agent("agent","blue",10,width/2,height/2,width,height,dot_size)
    agent.print_details()
    bot_locs = create_environment(agent,bot_locs,myCanvas)
    
    thread = Thread(target = run_environment, args = (agent,delay,iterations,bot_locs,myCanvas, ))
    thread.start()
    Button(root, text="Quit", command = lambda: close_properly(root,thread)).pack()
    
    

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    
if __name__ == "__main__":
    main()
