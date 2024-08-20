import mysql.connector
from customtkinter import *
from UsersDataClass import User
class GettingChallengesAndPuttingItIntoAFrame():
    
    def __init__(self, root,UserData: User, Dbconnection: mysql.connector.connect) -> None:
        self.db = Dbconnection
        self.cursor = self.db.cursor()
        self.FrameWithChallengesInIt = CTkFrame(root, corner_radius= 10)
        self.FrameWithMoreDetailToIt = CTkFrame(root, corner_radius= 10)
        self.UserData = UserData
        self.StartPointer = 0
        self.EndPointer = 0
        self.ArrangedData = [[]]
        
    def GettingDataInArrangedForm(self,SQLStatment,NumberOfJobsForEachPage):
        if NumberOfJobsForEachPage != 1:
            #Arranging grid so that it works with the NumberOfJobsForEachPage
            for x in range(NumberOfJobsForEachPage + 1):
                self.FrameWithChallengesInIt.grid_rowconfigure((x), weight = 1)
                self.FrameWithChallengesInIt.grid_columnconfigure((0), weight = 1)
        else:
            self.FrameWithChallengesInIt.grid_columnconfigure(0, weight = 1)
        #SQL statment is executed to get the data
        self.cursor.execute(SQLStatment)
        #Data is fetched
        CurrentOrdersData = self.cursor.fetchall()
        #Data is put into an arranged way that I can use
        NewArrangedOrdersData = []
        NumberOfPages = len(CurrentOrdersData) // NumberOfJobsForEachPage
        print(NumberOfPages)
        #Had to rearrange the array so that it was a array with arrays (2D array) of size 5 as each array represented the data on a page so having arrays of size 5 seperate was needed
        #Instead of [0,1,2,3,4,5,6,7,8,9,10,11,12] I wanted [[0,1,2,3,4],[5,6,7,8,9],[10,11,12]] as each array represented the data in each page
        for x in range(NumberOfPages + 1):
            Page = []
            if ((x + 1) * NumberOfJobsForEachPage) <= len(CurrentOrdersData):
                for y in range((x) * NumberOfJobsForEachPage, NumberOfJobsForEachPage * (x+ 1)):
                    Page.append(CurrentOrdersData[y])
            else:
                for y in range(x * NumberOfJobsForEachPage,((x) * NumberOfJobsForEachPage) + (len(CurrentOrdersData) % NumberOfJobsForEachPage)):
                    Page.append(CurrentOrdersData[y])
            if Page != [] and NewArrangedOrdersData is not [[]]:
                NewArrangedOrdersData.append(Page)
        self.EndPointer = len(NewArrangedOrdersData)
        #Checks if there are any jobs and if there isn't then it sets teh arranged data to none which tells my code to display "look like there is no jobs"
        try: 
            NewArrangedOrdersData[0]
        except IndexError:
            NewArrangedOrdersData = None
        print(NewArrangedOrdersData)
        return NewArrangedOrdersData
    
    def DeletignWidgetsOfFrame(self,Frame: CTkFrame):
        for widget in Frame.winfo_children():
            widget.destroy()
            
    def GeneratingFrameWithAllChallenges(self, type):
        self.DeletignWidgetsOfFrame(self.FrameWithChallengesInIt)
        self.type = type
        #The userID here represents the freelancer ID
        #Have a big problem teh tables userChallengersTable and Challenges Table has a many to many relationship whihch prevents me from 
        #stopping already challenge in from showing up so need to fix that
        if self.type == "Finding_Challenges":
            DropBoxValues = ["Art",""]
            ChallengeTitleInputedValue = StringVar()
            self.FrameWithChallengesInIt.columnconfigure(0, weight = 1)
            ChallengeTitleInputBox = CTkEntry(self.FrameWithChallengesInIt, placeholder_text= "Challenge Title", textvariable=ChallengeTitleInputedValue, height = 30, width = 100).grid(row = 0, column = 0)
            FindingChallengesButton = CTkButton(self.FrameWithChallengesInIt, text = "Find challenge", command=lambda: self.FindingChallenges(ChallengeTitleInputedValue.get())).grid(row = 0, column = 1)
        elif self.type == "Current_Challenges_In":
            TitleLabel = CTkLabel(self.FrameWithChallengesInIt, text = "Current Challenges In", font = CTkFont(size =20)).grid(row = 0, column = 0, pady = (10,5))
            self.ArrangedData = self.GettingDataInArrangedForm(f"SELECT ChallengesTable.ChallengeID, ChallengesTable.ChallengeTitle, ChallengesTable.Description, ChallengesTable.NumberOfChallengers,ChallengesTable.Date_Due\
                            ,ChallengesTable.MaxNumberOfChallengers, ChallengesTable.Tag, UserChallengersTable.FreelancerID FROM ChallengesTable INNER JOIN UserChallengersTable \
                            ON ChallengesTable.ChallengeID = UserChallengersTable.ChallengeID\
                            INNER JOIN UserTable ON UserChallengersTable.FreelancerID = UserTable.UserID\
                            WHERE UserTable.UserId = {self.UserData.UserID} \
                            AND ChallengesTable.Status != 'Completed'",1)
            if self.ArrangedData == None:
                NothingThereLabel = CTkLabel(self.FrameWithChallengesInIt, text = "Seems you don't have any current challenges", font = CTkFont(size = 20)).grid(row = 0, column = 0, sticky = "nsew")
        elif self.type == "Previous_Challenges":
            self.ArrangedData = self.GettingDataInArrangedForm(f"SELECT ChallengesTable.ChallengeTitle, ChallengesTable.Description,ChallengesTable.Date_Due , ChallengesTable.WinnerID, UserTable.Email, UserChallengersTable.Place,ChallengesTable.NumberOfChallengers\
                            FROM ChallengesTable \
                            INNER JOIN UserChallengersTable ON UserChallengersTable.ChallengeID = ChallengesTable.ChallengeID \
                            INNER JOIN UserTable ON UserTable.UserID = ChallengesTable.WinnerID \
                            WHERE UserChallengersTable.FreelancerId = {self.UserData.UserID} \
                            AND ChallengesTable.Status = 'Completed'              ",4)
        if self.ArrangedData != None:  
            for PageDataPointer in range(len(self.ArrangedData[self.StartPointer])):
                if self.type == "Current_Challenges_In":
                    TitleLabel = CTkLabel(self.FrameWithChallengesInIt, text = "Current Challenges In", font = CTkFont(size = 40)).grid(row = 0, column = 0, sticky = "nsew", pady = (10,5))
                    self.GeneratingASingleCurrentChallengeFrame(self.ArrangedData[self.StartPointer][PageDataPointer]).grid(row = PageDataPointer + 1, column = 0, sticky = "nsew", padx = 10, pady = 10)
                elif self.type == "Completed_Orders":
                    TitleLabel = CTkLabel(self.FrameWithChallengesInIt, text = "Completed Orders", font = CTkFont(size = 40)).grid(row = 0, column = 0, sticky = "nsew", pady = (10,5))
                    self.GeneratingASingleCompletedJobFrame(self.ArrangedData[self.StartPointer][PageDataPointer]).grid(row = PageDataPointer + 1, column = 0,sticky = "nsew", padx = 10, pady = 10)
                elif self.type == "Previous_Challenges":
                    TitleLabel = CTkLabel(self.FrameWithChallengesInIt, text = "Previous Challenges", font = CTkFont(size = 40)).grid(row = 0, column = 0, sticky = "nsew", pady = (10,5))
                    self.GeneratingASinglePreviousChallengeInFrame(self.ArrangedData[self.StartPointer][PageDataPointer]).grid(row = PageDataPointer + 1, column = 0,sticky = "nsew", padx = 10, pady = 10)
        if self.type != "Current_Challenges_In":
            PagesButtonFrame = CTkFrame(self.FrameWithChallengesInIt, fg_color="transparent")
            PagesButtonFrame.grid_columnconfigure((0,1,2), weight = 1)
            MovingPagesbackwardsButton = CTkButton(PagesButtonFrame, text = "<", command= self.previousPage).grid(row = 0, column = 0, padx = (20,10))
            CurrentPageLabel = CTkLabel(PagesButtonFrame, text = f"{self.StartPointer + 1}").grid(row = 0, column = 1, padx = (10,10))
            MovingPagesForwardButton = CTkButton(PagesButtonFrame, text = ">", command = self.NextPage).grid(row = 0, column = 2, padx = (20,10))
            PagesButtonFrame.grid(row = 6, column = 0, pady = (0,10))
            
        return self.FrameWithChallengesInIt
    
    def FindingChallenges(self, ChallengeTitle):
        self.ArrangedData = self.GettingDataInArrangedForm(f"SELECT ChallengesTable.ChallengeID, ChallengesTable.ChallengeTitle, ChallengesTable.Description, \
                                                                ChallengesTable.NumberOfChallengers, ChallengesTable.MaxNumberOfChallengers, ChallengesTable.Tag, ChallengesTable.Date_Due FROM ChallengesTable\
                                                                INNER JOIN UserChallengersTable ON ChallengesTable.ChallengeID = UserChallengersTable.ChallengeID\
                                                                WHERE UserChallengersTable.FreelancerId != {self.UserData.UserID}\
                                                                AND ChallengesTable.Status = 'OnGoing'\
                                                                 AND ChallengesTable.NumberOfChallengers != ChallengesTable.MaxNumberOfChallengers\
                                                                AND ChallengesTable.ChallengeTitle LIKE '%{ChallengeTitle}%'",4)
        
        for PageDataPointer in range(len(self.ArrangedData[self.StartPointer])):
            self.GeneratingASingleChallengeFrame(self.ArrangedData[self.StartPointer][PageDataPointer]).grid(row = PageDataPointer + 1, column = 0, sticky = "nsew", padx = 10, pady = 10)
            
        PagesButtonFrame = CTkFrame(self.FrameWithChallengesInIt, fg_color="transparent")
        PagesButtonFrame.grid_columnconfigure((0,1,2), weight = 1)
        MovingPagesbackwardsButton = CTkButton(PagesButtonFrame, text = "<", command= self.previousPage).grid(row = 10, column = 0, padx = (20,10))
        CurrentPageLabel = CTkLabel(PagesButtonFrame, text = f"{self.StartPointer + 1}").grid(row = 10, column = 1, padx = (10,10))
        MovingPagesForwardButton = CTkButton(PagesButtonFrame, text = ">", command = self.NextPage).grid(row = 10, column = 2, padx = (20,10))
        PagesButtonFrame.grid(row = 6, column = 0, pady = (0,10))
    
        
    def GeneratingASingleChallengeFrame(self,UserValues: []) -> CTkFrame:
        CurrentChallengesFrame = CTkFrame(self.FrameWithChallengesInIt, corner_radius= 5, width = 1000000)
        CurrentChallengesFrame.grid_rowconfigure((0,1,2,3), weight = 1)
        CurrentChallengesFrame.grid_columnconfigure((0), weight = 1)
        TitleOfChallenge = CTkLabel(CurrentChallengesFrame, text = f"Challenge Title: {UserValues[1]}", font = CTkFont(size = 20)).grid(row = 0, column = 0,sticky = "ns", padx = 20,pady = (10,0))
        ShortDescriptionTitle = CTkLabel(CurrentChallengesFrame, text = "Short description: ",font = CTkFont(size = 17)).grid(row = 1, column = 0,padx = 20,sticky = "w")
        ShortDescriptionOfJob = CTkLabel(CurrentChallengesFrame, text = f"{UserValues[2][:100]}...",font = CTkFont(size = 15))
        ShortDescriptionOfJob.grid(row = 2, column = 0,padx = 20,pady = (0.20), sticky = "w")
        NumberOfCurrentParticipants = CTkLabel(CurrentChallengesFrame, text = f"Number of participants: {UserValues[3]}/{UserValues[4]}").grid(row = 1, column = 0, padx = (0,20), pady = (10,0), sticky = "e")
        DateDue = CTkLabel(CurrentChallengesFrame, text = f"Due Date is {UserValues[6]}",font = CTkFont(size = 15)).grid(row = 1, column = 0,padx = (0,20),pady = (10,0))
        ViewInMoreDetailButton = CTkButton(CurrentChallengesFrame, text = "View challenge in more detail", command= lambda: self.LoadingChallengesInDetailFrame(self.ViewingListedChallengeInMoreDetail(UserValues))).grid(row = 3, column = 0)
        return CurrentChallengesFrame
    
    def GeneratingASingleCurrentChallengeFrame(self,ChallengeDetails: []) -> CTkFrame:
        ChallengeCurrentlyIn = CTkFrame(self.FrameWithChallengesInIt, corner_radius= 5, width = 1000000)
        ChallengeCurrentlyIn.grid_columnconfigure((0,2), weight = 1)
        ChallengeCurrentlyIn.grid_columnconfigure((1), weight = 3)
        ChallengeCurrentlyIn.grid_rowconfigure((0,1), weight = 1)
        ChallengeCurrentlyIn.grid_rowconfigure((2,3), weight = 1)
        TitleLabel = CTkLabel(ChallengeCurrentlyIn, text = f"Challenge Title: {ChallengeDetails[1]}", font = CTkFont(size = 30)).grid(row = 0, column = 1, padx = (10,0),pady = (0,40),sticky = "s")
        DescriptionTitle = CTkLabel(ChallengeCurrentlyIn, text = "Wants: ",font = CTkFont(size = 19)).grid(row = 1, column = 1,padx = 20,pady = 30,sticky = "sw")
        DescriptionOfJob = CTkTextbox(ChallengeCurrentlyIn,font = CTkFont(size = 15))
        DescriptionOfJob.grid(row = 2, column = 1,padx = 20,pady = (0,20), sticky = "nesw")
        DescriptionOfJob.insert("0.0",ChallengeDetails[2])
        DescriptionOfJob.configure(state = DISABLED)
        NumberOfDaysToBeCompletedBy = CTkLabel(ChallengeCurrentlyIn, text = f"Due Date is {ChallengeDetails[4]}",font = CTkFont(size = 15)).grid(row = 1, column = 2,sticky = "s", padx = (0,10),pady = (30,0))
        NumberOfCurrentParticipants = CTkLabel(ChallengeCurrentlyIn, text = f"Number of participants: {ChallengeDetails[3]}/{ChallengeDetails[5]}").grid(row = 2, column = 2, padx = (0,20), pady = (10,0), sticky = "s")
        RewardForWinning = CTkLabel(ChallengeCurrentlyIn,text = f"Prize Pool: Will increase on joining as \n prizes scale based on number of participants \n 1st Place: {ChallengeDetails[3] * 80} MicroBucks \n 2nd Place: {ChallengeDetails[3] * 40} MicroBucks \n 3rd Place {ChallengeDetails[3] * 20} MicroBucks \n 4th place and below: 10 MicroBucks").grid(row = 2, column = 2)
        JoinChallenge = CTkButton(ChallengeCurrentlyIn, text = "Leave Challenge", command = lambda: [self.LeavingChallenge(ChallengeDetails),self.ForgettingFrames()]).grid(row = 3, column = 1)
        return ChallengeCurrentlyIn
    
    def GeneratingASinglePreviousChallengeInFrame(self, UserValues: []) -> CTkFrame:
        SinglePreviousChallengeInFrame = CTkFrame(self.FrameWithChallengesInIt,corner_radius= 5)
        SinglePreviousChallengeInFrame.grid_rowconfigure((0,1,2,3), weight = 1)
        SinglePreviousChallengeInFrame.grid_columnconfigure((0), weight = 1)
        TitleOfChallenge = CTkLabel(SinglePreviousChallengeInFrame, text = f"Title {UserValues[0]} ",font = CTkFont(size = 17)).grid(row = 0, column = 0,padx = 20,sticky = "w")        
        ShortDescriptionChallenge = CTkLabel(SinglePreviousChallengeInFrame, text = "Short description: ",font = CTkFont(size = 17)).grid(row = 1, column = 0,padx = 20,sticky = "w")
        ShortDescriptionOfJob = CTkLabel(SinglePreviousChallengeInFrame, text = f"{UserValues[1][:100]}...",font = CTkFont(size = 18))
        ShortDescriptionOfJob.grid(row = 2, column = 0,padx = 20,pady = (0.20), sticky = "w")
        NumberOfCurrentParticipants = CTkLabel(SinglePreviousChallengeInFrame, text = f"Number of participants: {UserValues[5]}", font = CTkFont(size = 18)).grid(row = 1, column = 0, sticky = "e", padx = (30))
        DateDue = CTkLabel(SinglePreviousChallengeInFrame, text = f"Due date was : {UserValues[2]}",font = CTkFont(size = 18)).grid(row = 0, column = 0, sticky = "e", padx = (0, 30), pady = 10)
        ViewinMoreDetailButton = CTkButton(SinglePreviousChallengeInFrame, text = "View order in more detail", command = lambda: self.LoadingChallengesInDetailFrame(self.ViewingPreviousChallengeInMoreDetail(UserValues))).grid(row = 3, column = 0, padx = (50,0))
        return SinglePreviousChallengeInFrame
    
    def ViewingListedChallengeInMoreDetail(self,ListedChallengeDetails: []):
        self.DeletignWidgetsOfFrame(self.FrameWithMoreDetailToIt)
        self.FrameWithMoreDetailToIt.grid_columnconfigure((0,2), weight = 1)
        self.FrameWithMoreDetailToIt.grid_columnconfigure((1), weight = 3)
        self.FrameWithMoreDetailToIt.grid_rowconfigure((0,1), weight = 1)
        self.FrameWithMoreDetailToIt.grid_rowconfigure((2,3), weight = 1)
        backButton = CTkButton(self.FrameWithMoreDetailToIt, text = f"Back", font = CTkFont(size = 10),command = lambda: self.LoadingChallengesInDetailFrame(self.GeneratingFrameWithAllChallenges(self.type))).grid(row = 0, column = 0, padx = 30, pady = 30)
        TitleLabel = CTkLabel(self.FrameWithMoreDetailToIt, text = f"Title: {ListedChallengeDetails[1]}", font = CTkFont(size = 30)).grid(row = 0, column = 1, padx = (10,0),pady = (0,40),sticky = "s")
        DescriptionTitle = CTkLabel(self.FrameWithMoreDetailToIt, text = "Wants: ",font = CTkFont(size = 19)).grid(row = 1, column = 1,padx = 20,pady = 30,sticky = "sw")
        DescriptionOfJob = CTkTextbox(self.FrameWithMoreDetailToIt,font = CTkFont(size = 15))
        DescriptionOfJob.grid(row = 2, column = 1,padx = 20,pady = (0.20), sticky = "nesw")
        DescriptionOfJob.insert("0.0",ListedChallengeDetails[2])
        DescriptionOfJob.configure(state = DISABLED)
        #StatusOfTheJob = CTkLabel(self.FrameWithMoreDetailToIt, text = "Status: Completed").grid(row = 3, column = 2, sticky = "n",padx = (0,30))
        NumberOfDaysToBeCompletedBy = CTkLabel(self.FrameWithMoreDetailToIt, text = f"Due Date is {ListedChallengeDetails[6]}",font = CTkFont(size = 15)).grid(row = 1, column = 2,sticky = "s", padx = (0,10),pady = (30,0))
        NumberOfCurrentParticipants = CTkLabel(self.FrameWithMoreDetailToIt, text = f"Number of participants: {ListedChallengeDetails[3]}/{ListedChallengeDetails[4]}").grid(row = 2, column = 2, padx = (0,20), pady = (10,0), sticky = "s")
        RewardForWinning = CTkLabel(self.FrameWithMoreDetailToIt,text = f"Prize Pool: Will increase on joining as \n prizes scale based on number of participants \n 1st Place: {ListedChallengeDetails[3] * 80} MicroBucks \n 2nd Place: {ListedChallengeDetails[3] * 40} MicroBucks \n 3rd Place {ListedChallengeDetails[3] * 20} MicroBucks \n 4th place and below: 10 MicroBucks").grid(row = 2, column = 2)
        JoinChallenge = CTkButton(self.FrameWithMoreDetailToIt, text = "Join Challenge", command= lambda: [self.JoiningChallenge(ListedChallengeDetails), self.ForgettingFrames()]).grid(row = 3, column = 1)
        return self.FrameWithMoreDetailToIt
    
    def ViewingPreviousChallengeInMoreDetail(self,PreviousChallengeDetails: []):
        PlaceWihCorrespondingNumberOfMicroBucks = [80, 40, 20, 0]
        self.DeletignWidgetsOfFrame(self.FrameWithMoreDetailToIt)
        self.FrameWithMoreDetailToIt.grid_columnconfigure((0,2), weight = 1)
        self.FrameWithMoreDetailToIt.grid_columnconfigure((1), weight = 3)
        self.FrameWithMoreDetailToIt.grid_rowconfigure((0,1), weight = 1)
        self.FrameWithMoreDetailToIt.grid_rowconfigure((2,3), weight = 1)
        backButton = CTkButton(self.FrameWithMoreDetailToIt, text = f"Back", font = CTkFont(size = 10),command = lambda: self.LoadingChallengesInDetailFrame(self.GeneratingFrameWithAllChallenges(self.type))).grid(row = 0, column = 0, padx = 30, pady = 30)
        TitleLabel = CTkLabel(self.FrameWithMoreDetailToIt, text = f"Title: {PreviousChallengeDetails[0]}", font = CTkFont(size = 30)).grid(row = 0, column = 1, padx = (10,0),pady = (0,40),sticky = "s")
        DescriptionTitle = CTkLabel(self.FrameWithMoreDetailToIt, text = "Wants: ",font = CTkFont(size = 19)).grid(row = 1, column = 1,padx = 20,pady = 30,sticky = "sw")
        DescriptionOfJob = CTkTextbox(self.FrameWithMoreDetailToIt,font = CTkFont(size = 15))
        DescriptionOfJob.grid(row = 2, column = 1,padx = 20,pady = (0,20), sticky = "nesw")
        DescriptionOfJob.insert("0.0",PreviousChallengeDetails[1])
        DescriptionOfJob.configure(state = DISABLED)
        #StatusOfTheJob = CTkLabel(self.FrameWithMoreDetailToIt, text = "Status: Completed").grid(row = 3, column = 2, sticky = "n",padx = (0,30))
        DueDate = CTkLabel(self.FrameWithMoreDetailToIt, text = f"Due Date was {PreviousChallengeDetails[2]}",font = CTkFont(size = 15)).grid(row = 1, column = 2,sticky = "s", padx = (0,10),pady = (30,0))
        Place = CTkLabel(self.FrameWithMoreDetailToIt, text = f"You placed rank {PreviousChallengeDetails[5]} in this challenge").grid(row = 2, column = 2, sticky = "n", pady = 50)
        NumberOfCoinsWon = CTkLabel(self.FrameWithMoreDetailToIt, text = f"The number of MicroBucks you earnt was {PlaceWihCorrespondingNumberOfMicroBucks[int(PreviousChallengeDetails[5]) - 1] * PreviousChallengeDetails[6]}").grid(row = 2, column = 2)
        return self.FrameWithMoreDetailToIt
    
    def ForgettingFrames(self):
        self.FrameWithChallengesInIt.grid_forget()
        self.FrameWithMoreDetailToIt.grid_forget()
        
    def LoadingChallengesInDetailFrame(self, ChallengeInDetail: CTkFrame):
        self.ForgettingFrames()
        ChallengeInDetail.grid(row = 0, column = 1, sticky = "nsew", padx = 30, pady = 30)
        
    #Moves the start pointer 1 place forward so that the program knows what page/array to load
    #If the User goes past the end then they will go back to the start
    def NextPage(self):
        if self.StartPointer + 1 == self.EndPointer:
            self.StartPointer = 0
        else:
            self.EndPointer = self.StartPointer
            self.StartPointer += 1
        self.GeneratingFrameWithAllChallenges(self.type)

    #Moves the start pointer 1 place backwards so that the program knows what page/array to load
    #If the User goes past the start then they will go back to the end
    def previousPage(self):
        if self.StartPointer -1 == -1:
            self.StartPointer = (self.EndPointer - 1)
        else:
            self.EndPointer = self.StartPointer
            self.StartPointer -= 1
        self.GeneratingFrameWithAllChallenges(self.type)   
    
    def JoiningChallenge(self, ChallengeData):
        ChallengeId = ChallengeData[0]
        self.cursor.execute(f"UPDATE ChallengesTable SET NumberOfChallengers = NumberOfChallengers + 1 WHERE ChallengeID = {ChallengeId}")
        self.cursor.execute(f"INSERT INTO UserChallengersTable(FreelancerID, ChallengeID,Place) VAlUES({self.UserData.UserID}, {ChallengeId},NULL) ")
        self.db.commit()
    
    def LeavingChallenge(self,ChallengeData):
        ChallengeID = ChallengeData[0]
        self.cursor.execute(f"DELETE FROM UserChallengersTable WHERE FreelancerID = {self.UserData.UserID} AND ChallengeID = {ChallengeID}")
        self.cursor.execute(f"UPDATE ChallengesTable SET NumberOfChallengers = NumberOfChallengers - 1 WHERE ChallengeID = {ChallengeID}")
        self.db.commit()