from typing import Any
from customtkinter import *
import mysql.connector
from UsersDataClass import User

class Milestones():
    
    def __init__(self,root, UserData: User) -> None:
        self.UserData = UserData
        #The frames for this class
        self.AcceptedOrdersPage = CTkFrame(root, corner_radius= 10)
        self.CompletedOrdersPage = CTkFrame(root, corner_radius= 10)
        #Connectign to database
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="######",
            database = "ProjectDatabaseNew"
        )
        self.cursor = self.mydb.cursor()
        
        
    def FetchingUserOrdersData(self,type):
        if type == 0:
            self.cursor.execute(f"SELECT Accepted_Orders,CompletedAcceptedMilestone1,CompletedAcceptedMilestone2,CompletedAcceptedMilestone3 FROM UserTable WHERE UserID = {self.UserData.UserID}")
            AcceptedOrdersData = self.cursor.fetchone()
            return AcceptedOrdersData
        if type == 1:
            self.cursor.execute(f"SELECT Completed_Orders,CompletedOrderMilestone1,CompletedOrderMilestone2,CompletedOrderMilestone3 FROM UserTable WHERE UserID = {self.UserData.UserID}")
            CompletedOrdersData = self.cursor.fetchone()
            return CompletedOrdersData
    
    #Where all accepted milestoens are shown
    def GeneratingAcceptedOrdersMilestone(self):
        self.DeletignWidgetsOfFrame(self.AcceptedOrdersPage)
        self.AcceptedOrdersPage.rowconfigure((0,1,2,3), weight = 1)
        self.AcceptedOrdersPage.columnconfigure(0, weight = 1)
        AcceptedOrdersData = self.FetchingUserOrdersData(0)
        print(AcceptedOrdersData)
        titleOfFirstAcceptedOrderMilestone = CTkLabel(self.AcceptedOrdersPage, text = "Accepted Orders Milestone:", font = CTkFont(size = 30)).grid(row = 0, column = 0)
        self.GeneratingASingleAcceptedOrdersMilestone(AcceptedOrdersData[0],AcceptedOrdersData[1], 10,0).grid(row = 1, column = 0,sticky = "nsew",pady = 10, padx = 10)
        self.GeneratingASingleAcceptedOrdersMilestone(AcceptedOrdersData[0],AcceptedOrdersData[2], 50,1).grid(row = 2, column = 0,sticky = "nsew",pady = 10, padx = 10)
        self.GeneratingASingleAcceptedOrdersMilestone(AcceptedOrdersData[0],AcceptedOrdersData[3], 250,2).grid(row = 3, column = 0,sticky = "nsew",pady = 10, padx = 10)     
        return self.AcceptedOrdersPage

    #Generates a single accepted mielstone frame that is going to be placed on a bigger frame where all milestones are shown
    def GeneratingASingleAcceptedOrdersMilestone(self,NumberOfAcceptedOrders,CollectedCoinsOrNot,MilestoneMaxValue,Level):
        SingleMilestoneFrame = CTkFrame(self.AcceptedOrdersPage)
        SingleMilestoneFrame.columnconfigure(0,weight = 1)
        SingleMilestoneFrame.rowconfigure((0,1,2), weight = 1)
        MilestonLabel = CTkLabel(SingleMilestoneFrame, text = f"Orders accepted: {NumberOfAcceptedOrders} out of {MilestoneMaxValue}").grid(row = 1, column = 0,sticky = "n")
        MilestoneProgressBar = CTkProgressBar(SingleMilestoneFrame,orientation= "horizontal")
        MilestoneProgressBar.grid(row = 1, column = 0)
        MilestoneProgressBar.set(NumberOfAcceptedOrders / MilestoneMaxValue)
        if CollectedCoinsOrNot == 1:
            InfoLabel = CTkLabel(SingleMilestoneFrame,text = "Already collected milestone reward").grid(row = 2, column = 0)
        elif NumberOfAcceptedOrders < MilestoneMaxValue:
            InfoLabel = CTkLabel(SingleMilestoneFrame, text = "Not met requirment to collect reward").grid(row = 2, column = 0)
        else:
            CollectRewardsButton = CTkButton(SingleMilestoneFrame, text = "Collect Milestone Reward!!",command = lambda:self.CollectingRewardForMilestone(0,Level)).grid(row = 2, column = 0)
        return SingleMilestoneFrame

        
    #Where all completed orders milestones are shown
    def GeneratingCompletedOrdersMilestone(self):
        self.DeletignWidgetsOfFrame(self.CompletedOrdersPage)
        self.CompletedOrdersPage.rowconfigure((0,1,2,3), weight = 1)
        self.CompletedOrdersPage.columnconfigure(0, weight = 1)
        self.DeletignWidgetsOfFrame(self.CompletedOrdersPage)
        CompletedOrdersData = self.FetchingUserOrdersData(1)
        TitleOfScreen = CTkLabel(self.CompletedOrdersPage, text = "Completed Orders Milestones:", font=CTkFont(size=30)).grid(row = 0, column = 0, pady = 10, padx = 10)
        self.GeneratingASingleCompletedOrdersMilestone(CompletedOrdersData[0],CompletedOrdersData[1],10,0).grid(row = 1, column = 0, sticky = "nsew", pady = 10, padx = 10)
        self.GeneratingASingleCompletedOrdersMilestone(CompletedOrdersData[0],CompletedOrdersData[2],50,1).grid(row = 2, column = 0, sticky = "nsew", pady = 10, padx = 10)
        self.GeneratingASingleCompletedOrdersMilestone(CompletedOrdersData[0],CompletedOrdersData[3],250,2).grid(row = 3, column = 0, sticky = "nsew", pady = 10, padx = 10)
        return self.CompletedOrdersPage    
            
    def GeneratingASingleCompletedOrdersMilestone(self,NumberOfCompletedOrders,CollectedMilestoneOrNot,MilestoneMaxValue,Level):
        SingleCompletedOrderMilestoneFrame = CTkFrame(self.CompletedOrdersPage)
        SingleCompletedOrderMilestoneFrame.columnconfigure(0,weight = 1)
        SingleCompletedOrderMilestoneFrame.rowconfigure((0,1,2), weight = 1)
        MilestonLabel = CTkLabel(SingleCompletedOrderMilestoneFrame, text = f"Orders accepted: {NumberOfCompletedOrders} out of {MilestoneMaxValue}").grid(row = 1, column = 0,sticky = "n")
        MilestoneProgressBar = CTkProgressBar(SingleCompletedOrderMilestoneFrame,orientation= "horizontal")
        MilestoneProgressBar.grid(row = 1, column = 0)
        MilestoneProgressBar.set(NumberOfCompletedOrders / MilestoneMaxValue)
        if CollectedMilestoneOrNot == 1:
            InfoLabel = CTkLabel(SingleCompletedOrderMilestoneFrame,text = "Already collected milestone reward").grid(row = 2, column = 0)
        elif NumberOfCompletedOrders < MilestoneMaxValue:
            InfoLabel = CTkLabel(SingleCompletedOrderMilestoneFrame, text = "Not met requirment to collect reward").grid(row = 2, column = 0)
        else:
            CollectRewardsButton = CTkButton(SingleCompletedOrderMilestoneFrame, text = "Collect Milestone Reward!!",command = lambda:self.CollectingRewardForMilestone(1,Level)).grid(row = 2, column = 0)
        return SingleCompletedOrderMilestoneFrame
    #type helps to differentiate between completed and accepted but level helsp to differentiate from something like 10 accepted orders and 250 accepted orders. Higher the better when it comes to level
    def CollectingRewardForMilestone(self,type,level):
        EarnedMicroBucks = 0
        if type == 0:
            if level == 0:
                EarnedMicroBucks = 100
            elif level == 1:
                EarnedMicroBucks = 500
            elif level == 2:
                EarnedMicroBucks = 2500
            self.cursor.execute(f"UPDATE UserTable SET MicroBucks = MicroBucks + {EarnedMicroBucks}, CompletedAcceptedMilestone{level + 1} = 1 WHERE UserID = {self.UserData.UserID}")
        elif type == 1:
            if level == 0:
                EarnedMicroBucks = 500
            elif level == 1:
                EarnedMicroBucks = 2500
            elif level == 2:
                EarnedMicroBucks = 12500
            self.cursor.execute(f"UPDATE UserTable SET MicroBucks = MicroBucks + {EarnedMicroBucks}, CompletedOrderMilestone{level + 1} = 1 WHERE UserID = {self.UserData.UserID}")
        self.mydb.commit()
        if type == 0:
            self.AcceptedOrdersPage.grid_forget()
            self.GeneratingAcceptedOrdersMilestone().grid(row = 0, column = 1, sticky = "nsew",padx = 30, pady = 30)
            EarnedCoinsLabel = CTkLabel(self.AcceptedOrdersPage, text = f"Earned {EarnedMicroBucks} microbucks",font = CTkFont(size= 25)).grid(row = 4, column = 0 , pady = 20)
        elif type == 1:
            self.CompletedOrdersPage.grid_forget()
            self.GeneratingCompletedOrdersMilestone().grid(row = 0, column = 1, sticky = "nsew", padx = 30, pady = 30)
            EarnedCoinsLabel = CTkLabel(self.CompletedOrdersPage, text = f"Earned {EarnedMicroBucks} microbucks",font = CTkFont(size = 25)).grid(row = 4, column = 0,pady = 20)
        
    def ForgettingFrames(self):
        self.AcceptedOrdersPage.grid_forget()
        self.CompletedOrdersPage.grid_forget()
        
    def LoadingMilestone(self, MilestonePage: CTkFrame):
        self.ForgettingFrames()
        MilestonePage.grid(row = 0, column = 1, sticky = "nsew", padx = 30, pady = 30)
      
    
    def DeletignWidgetsOfFrame(self,Frame: CTkFrame):
        for widget in Frame.winfo_children():
            widget.destroy()
    
    
    #Moves the start pointer 1 place forward so that the program knows what page/array to load
    #If the User goes past the end then they will go back to the start
    def NextPage(self):
        if self.StartPointer + 1 == self.EndPointer:
            self.StartPointer = 0
        else:
            self.EndPointer = self.StartPointer
            self.StartPointer += 1
        self.GeneratingFrameWithAllJobs(self.type)

    def ViewingOrderInDetail():
        pass
    #Moves the start pointer 1 place backwards so that the program knows what page/array to load
    #If the User goes past the start then they will go back to the end
    def previousPage(self):
        if self.StartPointer -1 == -1:
            self.StartPointer = (self.EndPointer - 1)
        else:
            self.EndPointer = self.StartPointer
            self.StartPointer -= 1
        self.GeneratingFrameWithAllJobs(self.type)    
