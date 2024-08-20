from customtkinter import *
from UsersDataClass import User
from tkinter import messagebox
import customtkinter as ctk
from CommissionerOrdersPage import CommissionerOrdersTab
from CommissionerCalendarPage import CommissionerCalendarPage

class CommissionerPage():
    
    def __init__(self,root,UserData: User) -> None:
        #Defining root window and user data attribute so can be used throughout the class
        self.root = root
        self.UserData = UserData
        self.AppearanceMode = StringVar()
        #Defining Sidebars
        self.MainCommissionerSideBar = CTkFrame(root, corner_radius= 0)
        self.CommissionerOrdersSideBar = CTkFrame(root, corner_radius= 0)
        self.CommissionerSettingsSideBar = CTkFrame(root, corner_radius= 0)
        #Defining Objects for making frames
        self.CommissionerOrderObjects = CommissionerOrdersTab(root,UserData)
        self.CommissionerCalenderObject = CommissionerCalendarPage(root, UserData)
        
    def GeneratingMainSideBar(self):
        #Making sidebar
        self.MainCommissionerSideBar.grid_rowconfigure(6, weight=1)
        self.DeletingWidgetsOfAFrame(self.MainCommissionerSideBar)
        sidebar_frame_label = CTkLabel(self.MainCommissionerSideBar, text="Commissioner page",
                                                             compound="left", font=CTkFont(size=15, weight="bold"))
        sidebar_frame_label.grid(row=0, column=0, padx=20, pady=20)


        OrdersOptionMenu = CTkButton(self.MainCommissionerSideBar, corner_radius=0, height=40, border_spacing=10, text="Orders",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                       anchor="nesw" ,command= lambda:self.LoadingNewSideBar(self.GeneratingCommissionerOrdersSideBar()))
        OrdersOptionMenu.grid(row=1, column=0, sticky="ew")
        
        CalendarButton = CTkButton(self.MainCommissionerSideBar, corner_radius=0, height=40, border_spacing=10, text="Calendar Page",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nsew",command = lambda:self.CommissionerCalenderObject.LoadingCalendarFrame(self.CommissionerCalenderObject.GeneratingCalendarPage()))
        CalendarButton.grid(row = 2, column = 0,sticky = "ew")
        
        SettingsButton = CTkButton(self.MainCommissionerSideBar, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nsew",command = lambda:self.LoadingNewSideBar(self.GeneratingCommissionerSettingsSideBar()))
        SettingsButton.grid(row=3, column=0, sticky="ew")
        
        #Changes apperance based on a switch off = light on = dark
        ChangingAppearanceSwitch = CTkSwitch(self.MainCommissionerSideBar, text = "Dark Mode", command=self.change_appearance_mode_event,variable = self.AppearanceMode, onvalue= "Dark", offvalue = "Light").grid(row = 7, column = 0, padx = 10, pady = 10)
        return self.MainCommissionerSideBar
    
    def GeneratingCommissionerOrdersSideBar(self):
        self.CommissionerOrdersSideBar.grid(row=0, column=0,padx = (100,100), sticky="nsew")
        self.CommissionerOrdersSideBar.grid_rowconfigure(6, weight=1)
        sidebar_frame_label = CTkLabel(self.CommissionerOrdersSideBar, text="Orders Tab",
                                                             compound="left", font=CTkFont(size=15, weight="bold"))
        sidebar_frame_label.grid(row=0, column=0, padx=20, pady=20)

        FindingJobsButton = CTkButton(self.CommissionerOrdersSideBar, corner_radius=0, height=40, border_spacing=10, text="Finding Jobs",
                                                   fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                    anchor="nsew",command= lambda:self.CommissionerOrderObjects.LoadingFrames(self.CommissionerOrderObjects.GeneratingFindingJobsFrame()))
        
        FindingJobsButton.grid(row=1, column=0, sticky="ew")

        CurrentOrdersbutton = CTkButton(self.CommissionerOrdersSideBar, corner_radius=0, height=40, border_spacing=10, text="Current Orders",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                       anchor="nsew" ,command = lambda: self.CommissionerOrderObjects.LoadingFrames(self.CommissionerOrderObjects.GeneratingCommissionerCurrentOrdersFrame()))
        CurrentOrdersbutton.grid(row=2, column=0, sticky="ew")

        CompletedOrders = CTkButton(self.CommissionerOrdersSideBar, corner_radius=0, height=40, border_spacing=10, text="Previous Orders",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nsew",command= lambda:self.CommissionerOrderObjects.LoadingFrames(self.CommissionerOrderObjects.GeneratingCommissionerPreviousOrdersFrame()))
        CompletedOrders.grid(row=3, column=0, sticky="ew")
        
        
        BackButton = CTkButton(self.CommissionerOrdersSideBar, corner_radius=0, height=40, border_spacing=10, text="Back",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nsew",command= lambda:[self.LoadingNewSideBar(self.GeneratingMainSideBar()), self.ForgettingCurrentFrame()])
        BackButton.grid(row = 7, column = 0)
        #Changes apperance based on a switch off = light on = dark
        ChangingAppearanceSwitch = CTkSwitch(self.CommissionerOrdersSideBar, text = "Dark Mode", command=self.change_appearance_mode_event,variable = self.AppearanceMode, onvalue= "Dark", offvalue = "Light").grid(row = 8, column = 0, padx = 10, pady = (0,10))
        #Just testing how option menu works.
        return self.CommissionerOrdersSideBar
    
    
    def GeneratingCommissionerSettingsSideBar(self):
        self.CommissionerSettingsSideBar.grid(row = 0, column = 0, padx = (100,100), sticky = "nsew")
        self.CommissionerSettingsSideBar.grid_rowconfigure(6,weight = 1)
        sidebar_frame_label = CTkLabel(self.CommissionerSettingsSideBar, text="Settings",
                                                             compound="left", font=CTkFont(size=15, weight="bold"))
        sidebar_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        SwitchToCommissionerButton = CTkButton(self.CommissionerSettingsSideBar, corner_radius=0, height=40, border_spacing=10, text="Switch to Freelancer",
                                                   fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                    anchor="nsew", command = lambda: print("Should switch to freelancer GUI"))
        
        SwitchToCommissionerButton.grid(row = 1, column = 0, sticky = "ew")
        
        QuitingButton = CTkButton(self.CommissionerSettingsSideBar, corner_radius= 0, height = 40, border_spacing= 10, text = "Quit", fg_color="transparent",
                                             text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="nsew", command = lambda: [messagebox.showinfo("Thanks", "Thank you for using this software"), quit()])
        
        QuitingButton.grid(row = 2, column = 0, sticky= "ew")
        BackButton = CTkButton(self.CommissionerSettingsSideBar, corner_radius=0, height=40, border_spacing=10, text="Back",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nsew",command= lambda:[self.LoadingNewSideBar(self.GeneratingMainSideBarFrame()), self.ForgettingCurrentFrame()])
        BackButton.grid(row = 7, column = 0)
        
        ChangingAppearanceSwitch = CTkSwitch(self.CommissionerSettingsSideBar, text = "Dark Mode", command=self.change_appearance_mode_event,variable = self.AppearanceMode, onvalue= "Dark", offvalue = "Light").grid(row = 8, column = 0, padx = 10, pady = (0,10))
        
        return self.CommissionerSettingsSideBar
        
        
    def ForgettingSidebars(self):
        self.MainCommissionerSideBar.grid_forget()
        self.CommissionerOrdersSideBar.grid_forget()
        self.CommissionerSettingsSideBar.grid_forget()
        

    def LoadingNewSideBar(self,Frame: CTkFrame):
        self.ForgettingSidebars()
        Frame.grid(row = 0, column = 0,sticky="nsew")
    
    def DeletingWidgetsOfAFrame(self,Frame: CTkFrame):
        for widget in Frame.winfo_children():
            widget.destroy()
    
        
    def change_appearance_mode_event(self):
        ctk.set_appearance_mode(self.AppearanceMode.get())

