import tkinter as tk
import tkinter.messagebox
import calendar
import datetime
import os
import random
from typing import NamedTuple
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from PIL import ImageTk, Image

# --------- top level tk window ---------

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        #self.master.geometry("500x500")
        self.frame = tk.Frame(self.master)
        self.grid()
        self.create_widgets()
        self.frame.grid(row=0, column=0)
    

    # Allows user to easily create buttons for new windows
    
    def butnew(self, text, number, _class):
        tk.Button(self.master, text=text, height=2,
                  command=lambda:self.new_window(number, _class)).grid(sticky=tk.E+tk.W, row=number-2, pady=10, padx=10)

    def new_window(self, number, _class):
        self.new = tk.Toplevel(self.master)
        _class(self.new, number)


    # set up basic widgets on home screen
    def create_widgets(self):
        self.quit = tk.Button(self.master, text="QUIT", fg="red", width=20,
                                  command=self.master.destroy) 
        self.quit.grid(row=0, column=1, rowspan=3, padx = 30)

        self.butnew("Click to open Scheduler", 2, Win_Sched)
        self.butnew("Click to open Flash Cards", 3, Win_Flash_Cards)
        self.butnew("Click to open Integral Calculator", 4, Win_Integral)



# Full control for schedule window within this class

class Win_Sched:
    def __init__(self, master, number):
        
        self.master = master
        self.master.geometry("800x500")
        self.frame_control = tk.Frame(self.master, width=300, height=600)
        self.frame_control.grid(row=0, column=0)
        self.frame_display = tk.Frame(self.master, width=700, height=600, relief=tk.RAISED)
        self.frame_display.grid(row=0, column=1, padx=30)

        self.butt_quit = tk.Button(self.frame_control, text="QUIT", width=10,
                                   fg="red", command = self.close_window)
        self.label = tk.Label(self.frame_control, text=f"this is window num {number}")
        self.butt_quit.grid(row=1, column=0)
        self.label.grid(row=0, column=0)
        
        self.display_calendar_man()
        
        self.butt_add_event = tk.Button(self.frame_control, text="ADD EVENT",
                                        command=self.add_event)
        self.butt_add_event.grid(row=10, column=0, columnspan=3)
        
        self.create_widgets()
        
        # self.display_calendar()
        # #print(self.Nov_Events.events[5])

    
    # create widgets in one area for ease of access
    def create_widgets(self):

        self.butt_month_view = tk.Button(self.frame_control, text="MONTH VIEW")
        self.butt_month_view.grid(row=2, column=0)

        self.butt_day_view = tk.Button(self.frame_control, text="DAY VIEW")
        self.butt_day_view.grid(row=3, column=0)

        self.label_break = tk.Label(self.frame_control, text=" "*8+"-"*39)
        self.label_break.grid(row=4, column=0, columnspan=3)

        self.label_title = tk.Label(self.frame_control, text="Event Title:")
        self.label_title.grid(row=5, column=0)
        self.entry_title = tk.Entry(self.frame_control)
        self.entry_title.grid(row=5, column=1, columnspan=2)        

        self.label_loc = tk.Label(self.frame_control, text="Event Location:")
        self.label_loc.grid(row=6, column=0)
        self.entry_loc = tk.Entry(self.frame_control)
        self.entry_loc.grid(row=6, column=1, columnspan=2)

    # --------- -------------------- ---------
        self.label_select_day = tk.Label(self.frame_control, text="DAY:")
        self.label_select_day.grid(row=7, column=0)

        self.DayList = [i+1 for i in range(self.num_days_in_month)]

        self.add_event_to_day = tk.StringVar(self.master)
        self.add_event_to_day.set(self.DayList[0])

        self.drop_event_day = tk.OptionMenu(self.frame_control, self.add_event_to_day, *self.DayList)
        self.drop_event_day.grid(row=7, column=1, columnspan=2)

    # --------- -------------------- ---------
        self.HourList = [i for i in range(24)]
        self.MinList = [i*15 for i in range(4)]
        
    # --------- start time selection ---------
        self.label_start_time = tk.Label(self.frame_control, text="Start:")
        self.label_start_time.grid(row=8, column=0)

        self.start_hour = tk.StringVar(self.master)
        self.start_hour.set(self.HourList[0])
        self.start_min = tk.StringVar(self.master)
        self.start_min.set(self.MinList[0])
        
        self.drop_start_time_hour = tk.OptionMenu(self.frame_control, self.start_hour, *self.HourList)
        self.drop_start_time_hour.grid(row=8, column=1)

        self.drop_start_time_min = tk.OptionMenu(self.frame_control, self.start_min, *self.MinList)
        self.drop_start_time_min.grid(row=8, column=2)

    # ---------  end time selection  ---------

        self.label_end_time = tk.Label(self.frame_control, text="End:")
        self.label_end_time.grid(row=9, column=0)

        self.end_hour = tk.StringVar(self.master)
        self.end_hour.set(self.HourList[0])
        self.end_min = tk.StringVar(self.master)
        self.end_min.set(self.HourList[0])

        self.drop_end_hour = tk.OptionMenu(self.frame_control, self.end_hour, *self.HourList)
        self.drop_end_hour.grid(row=9, column=1)

        self.drop_end_min = tk.OptionMenu(self.frame_control, self.end_min, *self.MinList)
        self.drop_end_min.grid(row=9, column=2)

    # --------- -------------------- ---------

        # self.month = datetime.datetime.now().month
        self.Nov_Events = self.month_events(self.month)
        #print(self.Nov_Events)
        

    # create event and store it in month class to be able to view later
    def add_event(self):
        if(self.entry_title.get() != ""):
            # #print("before: ", self.Nov_Events.get_num_events())
            self.Nov_Events.add_event( self.entry_title.get(),
                                       self.entry_loc.get(),
                                       int(self.add_event_to_day.get()),
                                       int(self.start_hour.get()),
                                       int(self.start_min.get()),
                                       int(self.end_hour.get()),
                                       int(self.end_min.get())
                                       )

            self.butt_all_days[int(self.add_event_to_day.get())-1].configure(bg="#737ade")

            self.entry_title.delete(0, len(self.entry_title.get()))
            self.entry_loc.delete(0, len(self.entry_loc.get()))
            self.add_event_to_day.set(self.DayList[0])
            self.start_hour.set(self.HourList[0])
            self.start_min.set(self.MinList[0])
            self.end_hour.set(self.HourList[0])
            self.end_min.set(self.MinList[0])
            
        #tkinter.messagebox.showinfo("pls work", "this is some info")            

    # displays calendar from calendar library, does not have buttons, not used in gui
    def display_calendar(self):
        calendar_content = calendar.month(2020,11)
        cal_disp = tk.Label(self.frame_control, text = calendar_content,
                         font="Consolas 30 bold", justify="left")
        cal_disp.grid(row=1, column=2, rowspan=6, padx=100)
        

    # manually generates calendar with buttons corresponding to each day
    def display_calendar_man(self):

        # access info about current day, month, year
        self.day = datetime.datetime.now().day
        self.month = datetime.datetime.now().month
        self.month_name = calendar.month_name[self.month]
        self.year = datetime.datetime.now().year

        
        self.butt_all_days = [tk.Button(self.frame_display) for i in range(31)] # max 31 days in a month
        days_list = calendar.weekheader(3).split(" ")
        self.first_day, self.num_days_in_month = calendar.monthrange(2020,self.month)
        #print(self.first_day, self.num_days_in_month)
        #print(days_list[self.first_day])

        # displays month and year at top          
        #print(self.day, self.month, self.year, calendar.month_name[self.month])
        self.label_month_year_title = tk.Label(self.frame_display, text=self.month_name+", "+str(self.year),
                                               font="Consolas 25 bold")
        self.label_month_year_title.grid(row=0, column=0, columnspan=7, pady=10)

        # displays header of days of week
        for i in range(len(days_list)):
            self.label_day = tk.Label(self.frame_display, text=days_list[i],
                                      font="Consolas 18 bold")
            self.label_day.grid(row=1, column=i, pady=10, padx=10)


        # generates and draws buttons for each day 
        row=2

        for i in range(self.first_day, self.num_days_in_month + self.first_day):

            # i goes from 6 to 35 - will help with gridding
            # i-self.first_day goes 0 to 29 and provides day of month
            # i%7 indicates num between 0 and 6 for day of week - helps with column
            # for rows, we need to know everytime i%7 == 0

            if(i%7==0):
                row += 1
            
            self.butt_all_days[i-self.first_day].config(width=7, height=2, bg="#5ec98a",
                                                   text=i-self.first_day+1)
            self.butt_all_days[i-self.first_day].grid(row=row, column=(i%7))
         
            self.butt_all_days[i-self.first_day].config(command= lambda i=i: self.display_day_events(i-self.first_day+1))
            

    # view events for day by selecting a day from monthly calendar view
    def display_day_events(self, day):
        # #print(self.Nov_Events.get_num_events())
        #to_disp = self.Nov_Events.check_day_events(day+1)
        self.Nov_Events.check_days_events(day)
     
        

    def close_window(self):
        self.master.destroy()


    # class to store and access all events belonging to one month
    class month_events:
        def __init__(self, month):
            self.month = month
            self.events = []


        def add_event(self, title, location, day, start_hour, start_min, end_hour, end_min):
            self.events.append(self.event(title, location, day, start_hour, start_min, end_hour, end_min))


        def check_days_events(self, day):
            disp_string = ""
            for ev in self.events:
                if (ev.day == day):
                
                    disp_string += ("You have an event on this day entitled: "+ ev.title+
                                    "\ntaking place at: "+ ev.location+
                                    "\nfrom "+ str(ev.start_hr)+":"+str(ev.start_min)+
                                    " to "+ str(ev.end_hr)+":"+str(ev.end_min)+"\n\n")
                    '''
                    print("You have an event on this day entitled", ev.title,
                                    "\n taking place at", ev.location,
                                    "\nfrom", str(ev.start_hr)+":"+str(ev.start_min),
                                    "to", str(ev.end_hr)+":"+str(ev.end_min))
'''
            tkinter.messagebox.showinfo("pls work", disp_string)

        def get_num_events(self):
            return len(self.events)

        def get_num_events_in_day(self, day):
            count = 0
            for ev in self.events:
                if (ev.day == day):
                    count += 1
            return count

        class event(NamedTuple):
            title: str
            location: str
            day: int
            start_hr: int
            start_min: int
            end_hr: int
            end_min: int
            

# Full control for flash cards window within this class

class Win_Flash_Cards:    
    def __init__(self, master, number):
        self.master = master
        frame_width = 500
        frame_height = 500
        #self.master.geometry(f"{frame_width}x{frame_height}")
        self.frame = tk.Frame(self.master)
        self.frame.grid()

        # TODO: CREATE WIDGET SET UP FN AND ANY OTHER SET UP FN

        self.file_name = "flash_cards.txt"
        self.flash_qa = {
            "Who sucks at basketball?": "Ali Salman"
        }
        self.set_up_file()
        self.create_widgets()

    # widgets created here
    def create_widgets(self):

        self.label_welc = tk.Label(self.frame, text="welc")
        self.label_welc.grid(padx=100)

        self.currentlyOnDisplay = self.dict_get_key("Ali Salman")
        
        self.butt_Card = tk.Button(self.frame, text=self.currentlyOnDisplay,
                                   width=30, height=10,
                                   command = self.toggle_ques_ans,
                                   wraplength=180)
        self.butt_Card.grid(row=0, column=2, rowspan=6, padx = 10, pady = 10)

        self.label_Q = tk.Label(self.frame, text="Enter question (to be displayed):")
        self.label_Q.grid(row=1, column=0)
        self.entry_Q = tk.Entry(self.frame)
        self.entry_Q.grid(row=1, column=1)

        self.label_A = tk.Label(self.frame, text="Enter answer (to be revealed):")
        self.label_A.grid(row=2, column=0)
        self.entry_A = tk.Entry(self.frame)
        self.entry_A.grid(row=2, column=1)

        self.butt_submit = tk.Button(self.frame, text="submit",
                                     command=self.submit_qa)
        self.butt_submit.grid(row=3, column=0, columnspan=2)

        self.butt_load = tk.Button(self.frame, text="load",
                                   command = self.load_flash_cards)
        self.butt_load.grid(row=4, column=0, columnspan=2)

        self.butt_next = tk.Button(self.frame, text="next",
                                   command=self.next_card)
        self.butt_next.grid(row=5, column=0, columnspan=2)    



    # saves ques/ans and writes it to file
    def submit_qa(self):
        ques = self.entry_Q.get()
        ans = self.entry_A.get()
        if(ques != "" and ans != ""):
            self.flash_qa[ques] = ans
            flash_card_file = open(self.file_name, 'a')
            flash_card_file.write(f"\nQ={ques}, A={ans}\n")
            flash_card_file.close()
            self.entry_Q.delete(0, len(ques))
            self.entry_A.delete(0, len(ans))

    def set_up_file(self):
        open(self.file_name, 'a').close()
        
    # loads flash card from pre-determined file
    # future idea: tweak to allow different files to supple Q/A
    def load_flash_cards(self):
        flash_card_file = open(self.file_name, "r+")
        #print(flash_card_file)
        #print(os.stat(self.file_name).st_size==0)
        if(os.stat(self.file_name).st_size != 0):
            for line in flash_card_file.readlines():
                if(line.strip() != ""):
                    #print(line.strip())
                    first, sec = line.strip().split(',')
                    #print("first, sec: ", first, sec)
                    q = first.split("Q=")[1].strip()
                    a = sec.split("A=")[1].strip()
                    #print("Before adding: ", self.flash_qa.keys())
                    self.flash_qa[q] = a
                    #print("After adding: ", self.flash_qa.keys())
        flash_card_file.close()


    # upon press of button, will toggle between ques and ans
    def toggle_ques_ans(self):
        current = self.butt_Card['text']
        if(current in self.flash_qa.keys()):
            self.butt_Card['text'] = self.flash_qa[current]
        elif(current in self.flash_qa.values()):
            self.butt_Card['text'] = self.dict_get_key(current)


    # randomly chooses next flash card and displays question
    def next_card(self):
        ques, ans = random.choice(list(self.flash_qa.items()))
        self.butt_Card['text'] = ques
        

    def dict_get_key(self, value):
        for key, val in (self.flash_qa).items():
            if value == val:
                return key
        return "error"
        
    def close_window(self):
        self.master.destroy()

# Full control for integral window within this class

class Win_Integral:
    def __init__(self, master, number):
        self.master = master
        self.master.geometry("300x300")
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=0, column=0)
        self.butt_quit = tk.Button(self.frame, text="QUIT", 
                                  command = self.close_window)
        self.label = tk.Label(self.frame, text=f"this is window num {number}")
        self.label.grid(row=0, column=0)
        self.butt_quit.grid(row=1, column=0)

        self.set_up_widgets()


    # widgets created and placed here
    def set_up_widgets(self):
        
        self.label_fn = tk.Label(self.frame, text="Enter function:")
        self.label_fn.grid(row=2, column=0)
        self.entry_fn = tk.Entry(self.frame)
        self.entry_fn.grid(row=2, column=1, columnspan=2)        

        self.label_ub = tk.Label(self.frame, text="Upper Bound:")
        self.label_ub.grid(row=3, column=0)
        self.entry_ub = tk.Entry(self.frame)
        self.entry_ub.grid(row=3, column=1, columnspan=2)

        self.label_lb = tk.Label(self.frame, text="Lower Bound:")
        self.label_lb.grid(row=4, column=0)
        self.entry_lb = tk.Entry(self.frame)
        self.entry_lb.grid(row=4, column=1, columnspan=2)

        # button to calculate integral
        self.butt_calc = tk.Button(self.frame, text="Calculate",
                                   command=self.calculate_integral)
        self.butt_calc.grid(row=5, column=1)
        

    def close_window(self):
        self.master.destroy()

    # utilizes python libraries to provide integral of fn
    def calculate_integral(self):
        self.Upper_Bound = int(self.entry_ub.get())
        self.Lower_Bound = int(self.entry_lb.get())
        x = np.linspace(self.Lower_Bound, self.Upper_Bound, 100)
        y = self.entry_fn.get()

        x = sp.Symbol('x')
        num_ans = sp.integrate(y, (x, self.Lower_Bound, self.Upper_Bound))
        equ = sp.integrate(y)
        
        #print("Numerical answer is: ", num_ans)
        #print("Integral is: ", equ)

        tkinter.messagebox.showinfo("pls work", "Numerical answer is: " + str(num_ans) + "\n Integral is: " + str(equ))

# running application until program exited    
root = tk.Tk()
app = Application(master=root)
app.mainloop()
