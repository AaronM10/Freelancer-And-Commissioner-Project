import customtkinter as ctk
from customtkinter import *
from tkinter import * 
from tkmacosx import * 
import mysql.connector
import customtkinter
from UsersDataClass import User
from Calendarpage import CalendarPage
from FreelancerCode.OrdersCode.OrdersFramePractise import GetingOrdersAandputtingItIntoAFrame
#Have to set this at the start for it to work
class OrdersTab():
    
    def __init__(self,root, UserValuesObject: User):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="#########",
            database = "ProjectDatabaseNew"
        )
        self.cursor = self.db.cursor()
        self.UserValues = UserValuesObject
        self.MakingJobsFrameObject = GetingOrdersAandputtingItIntoAFrame(root, UserValuesObject, self.db)
        self.CalendarObject = CalendarPage(root, UserValuesObject)
        self.OrdersFrame = CTkFrame(root, corner_radius= 10)
        self.CreatingJobs = CTkFrame(root, corner_radius= 10)

    def ForgettingFrames(self):
        self.CreatingJobs.grid_forget()
        self.OrdersFrame.grid_forget()
        self.MakingJobsFrameObject.OrdersInDetailFrame.grid_forget()
        self.CalendarObject.CalendarScreen.grid_forget()
        
    def LoadingFrames(self,FrameBeingLoaded : CTkFrame):
        self.ForgettingFrames()
        FrameBeingLoaded.grid(row = 0, column = 1, padx = 30, pady = 30, sticky= "nsew")
    
    def DeletingWidgetsOffFrame(self,frameGiven : CTkFrame):
        for widget in frameGiven.winfo_children():
            widget.destroy()
            
    def MakingCurrentOrdersFrame(self):
        self.MakingJobsFrameObject.StartPointer = 0
        CurrentOrdersFrame = self.MakingJobsFrameObject.GeneratingFrameWithAllJobs("Current_Orders")
        self.OrdersFrame = CurrentOrdersFrame
        return self.OrdersFrame
    
    
    def MakingRequestedOrdersFrame(self):
        self.MakingJobsFrameObject.StartPointer = 0
        RequestedOrdersFrame = self.MakingJobsFrameObject.GeneratingFrameWithAllJobs("Requested_Orders")
        self.OrdersFrame = RequestedOrdersFrame
        return self.OrdersFrame
            
    
    def MakingPastCompletedOrdersFrame(self):
        self.MakingJobsFrameObject.StartPointer = 0
        CompletedOrdersFrame = self.MakingJobsFrameObject.GeneratingFrameWithAllJobs("Completed_Orders")
        self.OrdersFrame = CompletedOrdersFrame
        return self.OrdersFrame
    
    def MakingCurrentJobsMadeFrame(self):
        self.MakingJobsFrameObject.StartPointer = 0
        CurrentJobsMade = self.MakingJobsFrameObject.GeneratingFrameWithAllJobs("Jobs_Made")
        self.OrdersFrame = CurrentJobsMade
        return self.OrdersFrame
      
    def InsertingTheJobIntoDatabase(self,NameOfJob,Description,TagNumber):
        self.cursor.execute(f"INSERT INTO JobTable(JobTitle,FreelancerID,Description,Tag, Private) VALUES ('{NameOfJob}',{self.UserValues.UserID},'{Description}','{TagNumber}',0)")
        self.db.commit()
        self.LoadingFrames(self.MakingJobFrame())
        InfoLabel = CTkLabel(self.CreatingJobs, text = "Job has been created", font = CTkFont(size= 20)).grid(row = 5, column = 1,pady = (0,20))
        
    #When the job has been created it should take them to anotehr fram which shows the current jobs a freelacner has made and also be able to modify the data such as teh title and the tag
    # Find a way to use this frame for modification and teh creation of jobs
    def MakingJobFrame(self):  
        
        #Defining a variable for our entry widget so that it can be used when needed
        NameOfJob = StringVar()
        
        #Deleteing widgets on frame first which acts as a refresh
        self.DeletingWidgetsOffFrame(self.CreatingJobs)
        
        #Sorting out grid so that the widgets in the frame look good
        self.CreatingJobs.grid_columnconfigure((0,2), weight = 1)
        self.CreatingJobs.grid_columnconfigure((1), weight = 2)
        self.CreatingJobs.grid_rowconfigure((0,1), weight = 1)
        self.CreatingJobs.grid_rowconfigure((2,3), weight = 1)
        #All my wigets except send button
        CreatingJobTitle = CTkLabel(self.CreatingJobs, text = "Making a Job",font=CTkFont(size=60)).grid(row = 0, column = 1,pady = (20, 10))
        NameOfJobLabel = CTkLabel(self.CreatingJobs, text = "Name of the job:", font=CTkFont(size=15, weight="bold")).grid(row = 1, column = 1, pady = (50,10),sticky = "nw")
        EntryValueForJob = CTkEntry(self.CreatingJobs, textvariable= NameOfJob).grid(row = 1, column = 1, sticky = "ew")
        DescriptionLabel = CTkLabel(self.CreatingJobs, text = "Description:", font=CTkFont(size=15, weight="bold")).grid(row = 1, column = 1, sticky = "sw", pady = 10)
        DescriptionEntry = CTkTextbox(self.CreatingJobs)
        DescriptionEntry.grid(row = 2, column = 1, sticky = "nsew")# For some reason grid or pack has to be on a seperate line as if it's on the same line then the get function doesn't work
        #Radio Frame with radio buttons in it        
        GroupOfRadioButtons = CTkFrame(self.CreatingJobs, corner_radius= 10)
        GroupOfRadioButtons.grid(row = 1, column = 3, rowspan = 3,sticky = "nsew", padx = (10,40), pady = (30, 10))# Need this on a separate line as it the widgets don't go into the box if you don't do it this way
        ChoiceOfTagLabel = CTkLabel(GroupOfRadioButtons, text = "Tag:", font=CTkFont(size=15, weight="bold"), corner_radius= 10).grid(row = 1, column = 0, sticky = "ew")
        SelectedValue = IntVar(value = 0)
        ArtRadioButton = CTkRadioButton(GroupOfRadioButtons, text="Art", variable=SelectedValue,value = 0).grid(row = 2, column = 0,padx = 10, pady = 10,sticky = "ew")
        CodingRadioButton = CTkRadioButton(GroupOfRadioButtons,text="Coding",variable=SelectedValue,value = 1).grid(row = 3, column = 0,padx = 10, pady = 10,sticky = "ew")
        ReviewingWorkRadioButton = CTkRadioButton(GroupOfRadioButtons,text="Reviewing Work",variable=SelectedValue,value = 2).grid(row = 4,padx = 10, column = 0, pady = 10,sticky = "ew")
        PhotographyRadioButton = CTkRadioButton(GroupOfRadioButtons, text = "Photography",variable=SelectedValue,value = 3).grid(row = 5, padx = 10, column = 0, pady = 10,sticky = "ew")
        OtherRadioRadioButton = CTkRadioButton(GroupOfRadioButtons,text = "Other",variable=SelectedValue,value = 4).grid(row = 6, column = 0,padx = 10, pady = 10,sticky = "ew")
        #Send button which calls a function to insert the data into the database
        SendButton = CTkButton(self.CreatingJobs, text = "Send", command=lambda:self.InsertingTheJobIntoDatabase(NameOfJob.get(),DescriptionEntry.get("1.0", "end-1c"), SelectedValue.get())).grid(row = 3, column = 1)
        return self.CreatingJobs
        
        


        