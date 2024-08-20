from customtkinter import *
from FreelancerCode.OrdersCode.ChallengesPages import GettingChallengesAndPuttingItIntoAFrame
import mysql.connector
from Calendarpage import CalendarPage
class ChallengesPage():

    def __init__(self,root: CTk, UserValues) -> None:
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="######",
            database = "ProjectDatabaseNew"
        )
        self.root = root
        self.UserValues = UserValues
        self.CurrentChallengesFrame = CTkFrame(root, corner_radius= 10)
        self.ChallengesObject = GettingChallengesAndPuttingItIntoAFrame(root, UserValues, self.db)
        self.CalendarObject = CalendarPage(root, UserValues)

    def ForgettingFramesInChallenges(self):
       self.CurrentChallengesFrame.grid_forget()
       self.ChallengesObject.FrameWithChallengesInIt.grid_forget()
       self.ChallengesObject.FrameWithMoreDetailToIt.grid_forget()
       self.CalendarObject.CalendarScreen.grid_forget()
    

    def LoadingChallengesFrame(self,FrameBeingLoaded : CTkFrame):
        self.ForgettingFramesInChallenges()
        FrameBeingLoaded.grid(row = 0, column = 1, padx = 30, pady = 30, sticky= "nsew")
        
    def FindingChallengesFrame(self):
        self.ChallengesObject.StartPointer = 0
        FindingChallengesFrame = self.ChallengesObject.GeneratingFrameWithAllChallenges("Finding_Challenges")
        self.CurrentChallengesFrame = FindingChallengesFrame # Need to set the frame to yteh curent challenges frame so that you can forget it later if needed
        return self.CurrentChallengesFrame

 
    def CurrentChallengesInFrame(self):
        self.ChallengesObject.StartPointer = 0
        ChallengesCurrentlyInFrame = self.ChallengesObject.GeneratingFrameWithAllChallenges("Current_Challenges_In")
        self.CurrentChallengesFrame = ChallengesCurrentlyInFrame
        return self.CurrentChallengesFrame
 

    def MakingPreviousChallengesInFrame(self):
        self.ChallengesObject.StartPointer = 0
        PreviousChallengesInFrame = self.ChallengesObject.GeneratingFrameWithAllChallenges("Previous_Challenges")
        self.CurrentChallengesFrame = PreviousChallengesInFrame
        return self.CurrentChallengesFrame