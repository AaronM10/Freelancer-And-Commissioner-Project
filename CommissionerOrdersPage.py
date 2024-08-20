from customtkinter import *
from UsersDataClass import User
from FreelancerCode.OrdersCode.CommissionerOrdersFrame import CommissionerOrdersFrame
import mysql.connector

class CommissionerOrdersTab():
    
    def __init__(self,root,UserData: User) -> None:
        self.UserData = UserData
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="##########",
            database = "ProjectDatabaseNew"
        )
        #Making Frames
        self.RecommendedJobsFrame = CTkFrame(root,corner_radius=10)
        self.FoundJobsFrame = CTkFrame(root, corner_radius= 10)
        self.CurrentOrdersFrame = CTkFrame(root, corner_radius= 10)
        self.PreviousOrdersFrame = CTkFrame(root, corner_radius= 10)
        
        self.cursor = self.db.cursor()
        self.CommissionerOrderFrame = CTkFrame(root,corner_radius= 10)
        self.TagNumberIntotags = ["Art","Coding","Reviewing Work","Photography", "Other"]
        self.CommissionerOrdersobject = CommissionerOrdersFrame(root,self.db,UserData)
        
        
        
    def GeneratingFindingJobsFrame(self):
        RecommendedJobNumber = self.GettingRecommendedJobsTag()
        self.RecommendedJobsFrame = self.CommissionerOrdersobject.GeneratingCommissionerJobsFrames("RecommendedJobs",RecommendedJobNumber,[])
        TitleInputted = StringVar()
        TagSelected = StringVar()
        FindingJobsInputBox = CTkEntry(self.RecommendedJobsFrame,textvariable= TitleInputted,width = 300, height = 30, corner_radius= 10).grid(column = 0,row = 0,pady = (30,0),sticky = "ne",padx = 20)
        TagDropDownBox = CTkComboBox(self.RecommendedJobsFrame,
                                     values = ["Art","Coding","Reviewing Work","Photography", "Other"],
                                     variable= TagSelected)
        TagDropDownBox.grid(column = 0, row = 0, pady = 10, sticky = "e", padx = 20)
        FindJobsButton = CTkButton(self.RecommendedJobsFrame, text = "Find Job",command= lambda:self.GeneratingFoundJobsFrame(TitleInputted.get(),TagDropDownBox.get())).grid(column = 0, row = 0,sticky = "es",padx = 20,pady = 10)
        return self.RecommendedJobsFrame
    
    def GeneratingFoundJobsFrame(self,Title,Tag):
        self.FoundJobsFrame = self.CommissionerOrdersobject.GeneratingCommissionerJobsFrames("FindingJobs",0,[Title,Tag])
        self.LoadingFrames(self.FoundJobsFrame)
        TitleInputted = StringVar()
        TagSelected = StringVar()
        FindingJobsInputBox = CTkEntry(self.FoundJobsFrame,textvariable= TitleInputted,width = 300, height = 30, corner_radius= 10).grid(column = 0,row = 0,pady = (30,0),sticky = "ne",padx = 20)
        TagDropDownBox = CTkComboBox(self.FoundJobsFrame,
                                     values = ["Art","Coding","Reviewing Work","Photography", "Other"],
                                     variable= TagSelected)
        TagDropDownBox.grid(column = 0, row = 0, pady = 10, sticky = "e", padx = 20)
        FindJobsButton = CTkButton(self.FoundJobsFrame, text = "Find Job",command= lambda:self.GeneratingFoundJobsFrame(TitleInputted.get(),TagDropDownBox.get())).grid(column = 0, row = 0,sticky = "es",padx = 20,pady = 10)
        
    
    def GettingRecommendedJobsTag(self):
        #fetching Tag data
        self.cursor.execute(f"SELECT Clicks_Orders_Tag,Orders_Tag FROM ProjectDatabaseNew.UserTable WHERE UserID = {self.UserData.UserID}")
        TagData = self.cursor.fetchall()
        Clicks_Orders_Tag = TagData[0][0]
        Actual_Orders_Tag = TagData[0][1]
        #Will be the list that stores all of the weights of the tags and the tag with the highest weight will be the tag used for recommendation
        weightOfEachTag = [0,0,0,0,0]
        #Just making string from array into a list so data can be manipulated just like an array
        Clicks_Orders_Tag = Clicks_Orders_Tag.split(",")
        Actual_Orders_Tag = Actual_Orders_Tag.split(",")
        #Finds out the weight of each tag then changes the weightOfEachTag array/list
        for TagPointer in range(len(weightOfEachTag)):
            print(int(Clicks_Orders_Tag[TagPointer]) * 1.5)
            weight = (int(Clicks_Orders_Tag[TagPointer]) * 1.5) + (int(Actual_Orders_Tag[TagPointer]) * 3.25)
            weightOfEachTag[TagPointer] = weight
        RecommendedTagNumber = weightOfEachTag.index(max(weightOfEachTag))
        RecommendedTag = self.TagNumberIntotags[RecommendedTagNumber]
        return RecommendedTagNumber
        
    def GeneratingCommissionerCurrentOrdersFrame(self):
        self.CommissionerOrderFrame = self.CommissionerOrdersobject.GeneratingCommissionerOrderFrame("Current_Orders")
        return self.CommissionerOrderFrame
    
    def GeneratingCommissionerPreviousOrdersFrame(self):
        self.CommissionerOrderFrame = self.CommissionerOrdersobject.GeneratingCommissionerOrderFrame("Previous_Orders")
        return self.CommissionerOrderFrame
        
    def ForgettingFrames(self):
        self.RecommendedJobsFrame.grid_forget()
        self.FoundJobsFrame.grid_forget()
        self.CurrentOrdersFrame.grid_forget()
        self.PreviousOrdersFrame.grid_forget()
        self.CommissionerOrdersobject.CommissionerJobsinDetailFrame.grid_forget()
        
    def LoadingFrames(self,FrameBeingLoaded : CTkFrame):
        self.ForgettingFrames()
        FrameBeingLoaded.grid(row = 0, column = 1, padx = 30, pady = 30, sticky= "nsew")
    
