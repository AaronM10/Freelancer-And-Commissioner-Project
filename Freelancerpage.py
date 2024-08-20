import customtkinter as ctk
from tkinter import messagebox
from customtkinter import * 
import PIL
from UsersDataClass import User
from OrdersPage import OrdersTab
from HomePage import HomePage
from ChallengesTab import ChallengesPage
from Calendarpage import CalendarPage
from MilestonePage import Milestones
from CommissionerGUI import CommissionerPage
class FreelancerPage():
    
    #Setting the widgets on the frame as well as definoing the grid structure first
    def __init__(self,root : CTk,UsersValuesObject: User) -> None:
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=39)
        root.grid_columnconfigure(0, weight = 1)
        self.AppearanceMode = StringVar()
        # defining classes
        self.ordersObject = OrdersTab(root, UsersValuesObject)
        self.ChallengesObject = ChallengesPage(root, UsersValuesObject)
        self.HomeObject = HomePage(root, UsersValuesObject)
        self.Calendar = CalendarPage(root, UsersValuesObject)
        self.MilestonesPages = Milestones(root, UsersValuesObject)
        self.CommissionerObject = CommissionerPage(root, UsersValuesObject)
        #Defining sidebars
        self.MainSideBar = CTkFrame(root, corner_radius=0)
        self.HomePageSideBar = CTkFrame(root, corner_radius=0)
        self.SettingsSideBar = CTkFrame(root, corner_radius=0)
        self.OrdersSideBar = CTkFrame(root, corner_radius=0)
        self.ChallengesSideBar = CTkFrame(root, corner_radius=0)
        self.MilestoneSideBar = CTkFrame(root, corner_radius=0)
        self.LoadingNewSideBar(self.GeneratingMainSideBarFrame())
        
        
    def GeneratingMainSideBarFrame(self) -> CTkFrame:
        #Making sidebar
        self.MainSideBar.grid_rowconfigure(6, weight=1)
        self.DeletingWidgetsOfAFrame(self.MainSideBar)
        sidebar_frame_label = CTkLabel(self.MainSideBar, text="Freelancer page",
                                                             compound="left", font=CTkFont(size=15, weight="bold"))
        sidebar_frame_label.grid(row=0, column=0, padx=20, pady=20)


        OrdersOptionMenu = CTkButton(self.MainSideBar, corner_radius=0, height=40, border_spacing=10, text="Orders",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                       anchor="nesw" ,command= lambda:self.LoadingNewSideBar(self.GeneratingOrdersSideBar()))
        OrdersOptionMenu.grid(row=1, column=0, sticky="ew")

        ChallengesButton = CTkButton(self.MainSideBar, corner_radius=0, height=40, border_spacing=10, text="Challenges",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nsew",command = lambda:self.LoadingNewSideBar(self.GeneratingChallengesSideBar()))
        ChallengesButton.grid(row=2, column=0, sticky="ew")
        
        MilestonesButton = CTkButton(self.MainSideBar, corner_radius=0, height=40, border_spacing=10, text="Milestones",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nsew",command = lambda: self.LoadingNewSideBar(self.GeneratingMilestoneSidebar()))
        MilestonesButton.grid(row=3, column=0, sticky="ew")
        
        CalendarButton = CTkButton(self.MainSideBar, corner_radius=0, height=40, border_spacing=10, text="Calendar Page",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nsew",command = lambda:self.Calendar.GeneratingCalendarPage())
        CalendarButton.grid(row = 4, column = 0,sticky = "ew")
        
        SettingsButton = CTkButton(self.MainSideBar, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nsew",command = lambda:self.LoadingNewSideBar(self.GeneratingSettingsSidebar()))
        SettingsButton.grid(row=5, column=0, sticky="ew")
        
        #Changes apperance based on a switch off = light on = dark
        ChangingAppearanceSwitch = CTkSwitch(self.MainSideBar, text = "Dark Mode", command=self.change_appearance_mode_event,variable = self.AppearanceMode, onvalue= "Dark", offvalue = "Light").grid(row = 7, column = 0, padx = 10, pady = 10)
        return self.MainSideBar
    
    def GeneratingHomePageSideBar(self):
        self.HomePageSideBar.grid(row = 0, column = 0, sticky = "nsw")
        self.HomePageSideBar.grid_rowconfigure(6, weight=1)
        sidebar_frame_label = CTkLabel(self.HomePageSideBar, text="Home:",
                                                             compound="left", font=CTkFont(size=30))
        sidebar_frame_label.grid(row=0, column=0, padx=20, pady=20)

        SettingsButton = CTkButton(self.HomePageSideBar, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                                   fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30")
                                                    ,anchor = "w",command= lambda: print("Should take user to the settings page"))
        
        SettingsButton.grid(row=1, column=0, sticky="ew")
        
        SwitchingToCommissionerButton = CTkButton(self.HomePageSideBar, corner_radius=0, height=40, border_spacing=10, text="Switching to Commissioner  ",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                      anchor = "w",command= lambda: print("Should switch the freelancer to a commissioner"))
        
        SwitchingToCommissionerButton.grid(row = 2, column = 0)
        
        CalenderButton = CTkButton(self.HomePageSideBar, corner_radius=0, height=40, border_spacing=10, text="Calender",
                                                   fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30")
                                                    ,anchor = "w",command= lambda: print("Should take user to the settings page"))
        
        CalenderButton.grid(row = 3, column = 0)
        
        ExitingProgramButton = CTkButton(self.HomePageSideBar, corner_radius=0, height=40, border_spacing=10, text="Quit",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                      anchor = "w",command= lambda: print("Should switch the freelancer to a commissioner"))
        
        ExitingProgramButton.grid(row = 4, column = 0)
        

        
        BackButton = CTkButton(self.HomePageSideBar, corner_radius=0, height=40, border_spacing=10, text="Back"                                                          ,
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nsew",command= lambda:[self.LoadingNewSideBar(self.GeneratingMainSideBarFrame()), self.ForgettingCurrentFrame()])
        BackButton.grid(row = 7, column = 0)
        #Changes apperance based on a switch off = light on = dark
        ChangingAppearanceSwitch = CTkSwitch(self.HomePageSideBar, text = "Dark Mode", command=self.change_appearance_mode_event,variable = self.AppearanceMode, onvalue= "Dark", offvalue = "Light").grid(row = 8, column = 0, padx = 10, pady = (0,10))
        #Just testing how option menu works.
        return self.HomePageSideBar
    
    #Generates sidebar for the orders tab with all the buttons needed
    def GeneratingOrdersSideBar(self):
        self.OrdersSideBar.grid(row=0, column=0,padx = (100,100), sticky="nsew")
        self.OrdersSideBar.grid_rowconfigure(6, weight=1)
        sidebar_frame_label = CTkLabel(self.OrdersSideBar, text="Orders Tab",
                                                             compound="left", font=CTkFont(size=15, weight="bold"))
        sidebar_frame_label.grid(row=0, column=0, padx=20, pady=20)

        CurrentordersButton = CTkButton(self.OrdersSideBar, corner_radius=0, height=40, border_spacing=10, text="Current Orders",
                                                   fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                    anchor="nsew",command= lambda:self.ordersObject.LoadingFrames(self.ordersObject.MakingCurrentOrdersFrame()))
        
        CurrentordersButton.grid(row=1, column=0, sticky="ew")

        RequestedOrdersbutton = CTkButton(self.OrdersSideBar, corner_radius=0, height=40, border_spacing=10, text="Requested Orders",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                       anchor="nsew" ,command= lambda:self.ordersObject.LoadingFrames(self.ordersObject.MakingRequestedOrdersFrame()))
        RequestedOrdersbutton.grid(row=2, column=0, sticky="ew")

        CompletedOrders = CTkButton(self.OrdersSideBar, corner_radius=0, height=40, border_spacing=10, text="Completed Orders",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nsew",command= lambda:self.ordersObject.LoadingFrames(self.ordersObject.MakingPastCompletedOrdersFrame()))
        CompletedOrders.grid(row=3, column=0, sticky="ew")
        
        ViewingCurrentJobsMade = CTkButton(self.OrdersSideBar, corner_radius=0, height=40, border_spacing=10, text="Current Jobs Made",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nesw",command= lambda:self.ordersObject.LoadingFrames(self.ordersObject.MakingCurrentJobsMadeFrame()))
        
        ViewingCurrentJobsMade.grid(row = 4, column = 0, sticky = "nesw")
        
        MakingJobsButton = CTkButton(self.OrdersSideBar, corner_radius=0, height=40, border_spacing=10, text="Making Jobs",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nesw",command= lambda: self.ordersObject.LoadingFrames(self.ordersObject.MakingJobFrame()))
        
        MakingJobsButton.grid(row = 5, column = 0)
        
        BackButton = CTkButton(self.OrdersSideBar, corner_radius=0, height=40, border_spacing=10, text="Back",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nsew",command= lambda:[self.LoadingNewSideBar(self.GeneratingMainSideBarFrame()), self.ForgettingCurrentFrame()])
        BackButton.grid(row = 7, column = 0)
        #Changes apperance based on a switch off = light on = dark
        ChangingAppearanceSwitch = CTkSwitch(self.OrdersSideBar, text = "Dark Mode", command=self.change_appearance_mode_event,variable = self.AppearanceMode, onvalue= "Dark", offvalue = "Light").grid(row = 8, column = 0, padx = 10, pady = (0,10))
        #Just testing how option menu works.
        return self.OrdersSideBar
        
    def GeneratingChallengesSideBar(self) -> CTkFrame:
        self.ChallengesSideBar.grid(row=0, column=0,padx = (100,100), sticky="nsew")
        self.ChallengesSideBar.grid_rowconfigure(6, weight=1)
        sidebar_frame_label = CTkLabel(self.ChallengesSideBar, text="Challenges",
                                                             compound="left", font=CTkFont(size=15, weight="bold"))
        sidebar_frame_label.grid(row=0, column=0, padx=20, pady=20)

        FindChallengesButton = CTkButton(self.ChallengesSideBar, corner_radius=0, height=40, border_spacing=10, text="Find Challenges",
                                                   fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                    anchor="nsew", command = lambda:self.ChallengesObject.LoadingChallengesFrame(self.ChallengesObject.FindingChallengesFrame()))
        
        FindChallengesButton.grid(row=1, column=0, sticky="ew")

        ChallengesCurrentlyInbutton = CTkButton(self.ChallengesSideBar, corner_radius=0, height=40, border_spacing=10, text="Challenges Currently In",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                       anchor="nsew", command= lambda: self.ChallengesObject.LoadingChallengesFrame(self.ChallengesObject.CurrentChallengesInFrame()))
        ChallengesCurrentlyInbutton.grid(row=2, column=0, sticky="ew")
        
        PreviousChallengesButton = CTkButton(self.ChallengesSideBar, corner_radius=0, height=40, border_spacing=10, text="Previous Challenges In",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nesw", command = lambda: self.ChallengesObject.LoadingChallengesFrame(self.ChallengesObject.MakingPreviousChallengesInFrame()))
        
        PreviousChallengesButton.grid(row = 4, column = 0, sticky = "nesw")

        BackButton = CTkButton(self.ChallengesSideBar, corner_radius=0, height=40, border_spacing=10, text="Back",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nsew",command= lambda:[self.LoadingNewSideBar(self.GeneratingMainSideBarFrame()), self.ForgettingCurrentFrame()])
        BackButton.grid(row = 7, column = 0)
        #Changes apperance based on a switch off = light on = dark
        ChangingAppearanceSwitch = CTkSwitch(self.ChallengesSideBar, text = "Dark Mode", command=self.change_appearance_mode_event,variable = self.AppearanceMode, onvalue= "Dark", offvalue = "Light").grid(row = 8, column = 0, padx = 10, pady = (0,10))
        #Just testing how option menu works.
        return self.ChallengesSideBar
    
    def GeneratingMilestoneSidebar(self):
        self.MilestoneSideBar.grid(row=0, column=0,padx = (100,100), sticky="nsew")
        self.MilestoneSideBar.grid_rowconfigure(6, weight=1)
        sidebar_frame_label = CTkLabel(self.MilestoneSideBar, text="Milestones Tab",
                                                             compound="left", font=CTkFont(size=15, weight="bold"))
        sidebar_frame_label.grid(row=0, column=0, padx=20, pady=20)

        AcceptedOrdersMilestoneButton = CTkButton(self.MilestoneSideBar, corner_radius=0, height=40, border_spacing=10, text="Accepted orders milestones",
                                                   fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                    anchor="nsew", command = lambda:self.MilestonesPages.LoadingMilestone(self.MilestonesPages.GeneratingAcceptedOrdersMilestone()))
        
        AcceptedOrdersMilestoneButton.grid(row=1, column=0, sticky="ew")
        
        CompletedOrdersMilestoneButton = CTkButton(self.MilestoneSideBar, corner_radius=0, height=40, border_spacing=10, text="Completed orders milestones",
                                                   fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                    anchor="nsew",command = lambda:self.MilestonesPages.LoadingMilestone(self.MilestonesPages.GeneratingCompletedOrdersMilestone()))
        
        CompletedOrdersMilestoneButton.grid(row=2, column=0, sticky="ew")
        
        BackButton = CTkButton(self.MilestoneSideBar, corner_radius=0, height=40, border_spacing=10, text="Back",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nsew",command= lambda:[self.LoadingNewSideBar(self.GeneratingMainSideBarFrame()), self.ForgettingCurrentFrame()])
        BackButton.grid(row = 7, column = 0)
        #Changes apperance based on a switch off = light on = dark
        ChangingAppearanceSwitch = CTkSwitch(self.MilestoneSideBar, text = "Dark Mode", command=self.change_appearance_mode_event,variable = self.AppearanceMode, onvalue= "Dark", offvalue = "Light").grid(row = 8, column = 0, padx = 10, pady = (0,10))
        return self.MilestoneSideBar
    
    def GeneratingSettingsSidebar(self):
        self.SettingsSideBar.grid(row = 0, column = 0, padx = (100,100), sticky = "nsew")
        self.SettingsSideBar.grid_rowconfigure(6,weight = 1)
        sidebar_frame_label = CTkLabel(self.SettingsSideBar, text="Settings",
                                                             compound="left", font=CTkFont(size=15, weight="bold"))
        sidebar_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        SwitchToCommissionerButton = CTkButton(self.SettingsSideBar, corner_radius=0, height=40, border_spacing=10, text="Switch to commissioner",
                                                   fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                    anchor="nsew", command = lambda:[self.CommissionerObject.LoadingNewSideBar(self.CommissionerObject.GeneratingMainSideBar()),self.ForgettingCurrentFrame(),self.ForgettingSidebars()])
        
        SwitchToCommissionerButton.grid(row = 1, column = 0, sticky = "ew")
        
        QuitingButton = CTkButton(self.SettingsSideBar, corner_radius= 0, height = 40, border_spacing= 10, text = "Quit", fg_color="transparent",
                                             text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="nsew", command = lambda: [messagebox.showinfo("Thanks", "Thank you for using this software"), quit()])
        
        QuitingButton.grid(row = 2, column = 0, sticky= "ew")
        BackButton = CTkButton(self.SettingsSideBar, corner_radius=0, height=40, border_spacing=10, text="Back",
                                                      fg_color="transparent", text_color=("gray30","gray80"), hover_color=("gray70", "gray30"),
                                                     anchor="nsew",command= lambda:[self.LoadingNewSideBar(self.GeneratingMainSideBarFrame()), self.ForgettingCurrentFrame()])
        BackButton.grid(row = 7, column = 0)
        
        ChangingAppearanceSwitch = CTkSwitch(self.SettingsSideBar, text = "Dark Mode", command=self.change_appearance_mode_event,variable = self.AppearanceMode, onvalue= "Dark", offvalue = "Light").grid(row = 8, column = 0, padx = 10, pady = (0,10))
        
        return self.SettingsSideBar
    
    def ForgettingSidebars(self):
        self.MainSideBar.grid_forget()
        self.SettingsSideBar.grid_forget()
        self.HomePageSideBar.grid_forget()
        self.OrdersSideBar.grid_forget()
        self.ChallengesSideBar.grid_forget()
        self.MilestoneSideBar.grid_forget()
        

    def LoadingNewSideBar(self,Frame: CTkFrame):
        self.ForgettingSidebars()
        Frame.grid(row = 0, column = 0,sticky="nsew")
    
    def DeletingWidgetsOfAFrame(self,Frame: CTkFrame):
        for widget in Frame.winfo_children():
            widget.destroy()
    
        
    def change_appearance_mode_event(self):
        ctk.set_appearance_mode(self.AppearanceMode.get())

    def ForgettingCurrentFrame(self):
        self.ordersObject.ForgettingFrames()
        self.ChallengesObject.ForgettingFramesInChallenges()
        self.Calendar.CalendarScreen.grid_forget()
        

root = CTk()
MyUser = User(11,"Aaron Mojica","originalcoffee20184@gmail.com")
myObject = FreelancerPage(root,MyUser)
root.mainloop()

