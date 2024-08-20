from customtkinter import *
import customtkinter as ctk
import mysql.connector
import numpy as np
from UsersDataClass import User
from SendingEmail import SendingEmailsClass

class GetingOrdersAandputtingItIntoAFrame():
    def __init__(self, root,UserData: User, DbConnection: mysql.connector.connect) -> None:
        self.db = DbConnection
        self.UserData = UserData
        self.cursor = self.db.cursor()
        self.StartPointer = 0
        self.EndPointer = 0
        self.OrdersFrame = CTkFrame(root, corner_radius=10)
        self.OrdersInDetailFrame = CTkFrame(root, corner_radius= 10)
        self.type = 0
        self.MyEmailObject = SendingEmailsClass()
        self.TagList = ["Art","Coding","Reviewing Work", "Photography", "Other"]
        #Defining Calendar object
        
        
    def GettingDataInArrangedForm(self,SQLStatment,NumberOfJobsForEachPage):
        #Arranging grid so that it works with the NumberOfJobsForEachPage
        for x in range(NumberOfJobsForEachPage + 1):
            self.OrdersFrame.grid_rowconfigure((x), weight = 1)
        self.OrdersFrame.grid_columnconfigure((0), weight = 1)
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
            print(NewArrangedOrdersData)
        self.EndPointer = len(NewArrangedOrdersData)
        try: 
            NewArrangedOrdersData[0]
        except IndexError:
            NewArrangedOrdersData = None
        print(NewArrangedOrdersData)
        return NewArrangedOrdersData

    def DeletignWidgetsOfFrame(self,Frame: CTkFrame):
        for widget in Frame.winfo_children():
            widget.destroy()
            
    #This frame will call the GeneratingASingleJobFrame a certain amount of times to generate a set number of jobs like 6 and will
    #Place all 6 jobs onto that frame and allows a user to view them. There is also a forwards and backwards button to help with 
    #Navigating.  Page number is also show to show what page the user is on.
    def GeneratingFrameWithAllJobs(self, type):
        self.DeletignWidgetsOfFrame(self.OrdersFrame)
        self.type = type
        #The userID here represents the freelancer ID
        if self.type == "Current_Orders":
            TitleLabel = CTkLabel(self.OrdersFrame, text = "Current Orders", font = CTkFont(size =20)).grid(row = 0, column = 0, pady = (10,5))
            ArrangedData = self.GettingDataInArrangedForm(f"SELECT UserTable.FullName, OrdersTable.OrderID, OrdersTable.Status,  OrdersTable.Wants, JobTable.JobTitle, UserTable.Email FROM UserTable \
							INNER JOIN OrdersTable ON UserTable.UserID = OrdersTable.CommissionerID \
                            INNER JOIN JobTable ON OrdersTable.JobID = JobTable.JobID \
                            WHERE OrdersTable.FreelancerID = '{self.UserData.UserID}' \
                            AND OrdersTable.Status = 'Working' \
                            AND OrdersTable.Accepted = 1",4)
            if ArrangedData == None:
                NothingThereLabel = CTkLabel(self.OrdersFrame, text = "Seems you don't have any current orders", font = CTkFont(size = 20)).grid(row = 0, column = 0, sticky = "nsew")
        elif self.type == "Requested_Orders":
            TitleLabel = CTkLabel(self.OrdersFrame, text = "Requested Orders", font = CTkFont(size =20)).grid(row = 0, column = 0, pady = (10,5))
            ArrangedData = self.GettingDataInArrangedForm(f"SELECT UserTable.FullName,  OrdersTable.Wants, JobTable.JobTitle, UserTable.Email, OrdersTable.NumberOfDays, OrdersTable.OrderID FROM UserTable \
							INNER JOIN OrdersTable ON UserTable.UserID = OrdersTable.CommissionerID \
                            INNER JOIN JobTable ON OrdersTable.JobID = JobTable.JobID \
                            WHERE OrdersTable.FreelancerID = {self.UserData.UserID} \
                            AND OrdersTable.Status = 'Not Accepted' \
                            AND OrdersTable.Accepted = 0",4)
            if ArrangedData == None:
                NothingThereLabel = CTkLabel(self.OrdersFrame, text = "Seems you don't have any requested orders", font = CTkFont(size = 20)).grid(row = 0, column = 0, sticky = "nsew")
        elif self.type == "Completed_Orders":
            ArrangedData = self.GettingDataInArrangedForm(f"SELECT UserTable.FullName,  OrdersTable.Wants, JobTable.JobTitle, UserTable.Email, OrdersTable.NumberOfDays,OrdersTable.Status FROM UserTable \
							INNER JOIN OrdersTable ON UserTable.UserID = OrdersTable.CommissionerID \
                            INNER JOIN JobTable ON OrdersTable.JobID = JobTable.JobID \
                            WHERE OrdersTable.FreelancerID = {self.UserData.UserID} \
                            AND OrdersTable.Status = 'Completed' \
                            ",4)
            NothingThereLabel = CTkLabel(self.OrdersFrame, text = "Seems you don't have any completed orders", font = CTkFont(size = 20)).grid(row = 0, column = 0, sticky = "nsew")
        elif self.type == "Jobs_Made":
            ArrangedData = self.GettingDataInArrangedForm(f"SELECT JobTable.JobID, JobTable.JobTitle, JobTable.Description, \
                                                          JobTable.Tag, UserTable.Email, JobTable.Private  FROM JobTable \
                                                         INNER JOIN UserTable ON UserTable.UserID = JobTable.FreelancerID  \
                                                         WHERE FreelancerID = {self.UserData.UserID}\
                                                          ",4)
        if ArrangedData != None: 
            
            for PageDataPointer in range(len(ArrangedData[self.StartPointer])):
                if self.type == "Current_Orders":
                    self.GeneratingASingleCurrentJobFrame(ArrangedData[self.StartPointer][PageDataPointer]).grid(row = PageDataPointer + 1, column = 0, sticky = "nsew", padx = 10, pady = 10)
                elif self.type == "Requested_Orders":
                    TitleLabel = CTkLabel(self.OrdersFrame, text = "Requested Orders", font = CTkFont(size = 40)).grid(row = 0, column = 0, sticky = "nsew", pady = (10,5))
                    self.GeneratingASingleRequestedJobFrame(ArrangedData[self.StartPointer][PageDataPointer]).grid(row = PageDataPointer + 1, column = 0, sticky = "nsew", padx = 10, pady = 10)
                elif self.type == "Completed_Orders":
                    TitleLabel = CTkLabel(self.OrdersFrame, text = "Completed Orders", font = CTkFont(size = 40)).grid(row = 0, column = 0, sticky = "nsew", pady = (10,5))
                    self.GeneratingASingleCompletedJobFrame(ArrangedData[self.StartPointer][PageDataPointer]).grid(row = PageDataPointer + 1, column = 0,sticky = "nsew", padx = 10, pady = 10)
                elif self.type == "Jobs_Made":
                    TitleLabel = CTkLabel(self.OrdersFrame, text = "Jobs Made", font = CTkFont(size = 40)).grid(row = 0, column = 0, sticky = "nsew", pady = (10,5))
                    self.GeneratingASingleCreatedJobFrame(ArrangedData[self.StartPointer][PageDataPointer]).grid(row = PageDataPointer + 1, column = 0,sticky = "nsew", padx = 10, pady = 10)
                
        PagesButtonFrame = CTkFrame(self.OrdersFrame, fg_color="transparent")
        PagesButtonFrame.grid_columnconfigure((0,1,2), weight = 1)
        MovingPagesbackwardsButton = CTkButton(PagesButtonFrame, text = "<", command= self.previousPage).grid(row = 0, column = 0, padx = (20,10))
        CurrentPageLabel = CTkLabel(PagesButtonFrame, text = f"{self.StartPointer + 1}").grid(row = 0, column = 1, padx = (10,10))
        MovingPagesForwardButton = CTkButton(PagesButtonFrame, text = ">", command = self.NextPage).grid(row = 0, column = 2, padx = (20,10))
        PagesButtonFrame.grid(row = 5, column = 0, pady = (0,10))
        return self.OrdersFrame


    #The function that actually generates the frame that shows off all of the values i.e this frame shows the description of the commission, commissioner name, commissioner email and the job title the
    #freelancer stated themselves
    def GeneratingASingleCurrentJobFrame(self,Values: []) -> CTkFrame:
        CurrentOrderFrame = CTkFrame(self.OrdersFrame, corner_radius= 5, width = 1000000)
        CurrentOrderFrame.grid_rowconfigure((0,1,2,3), weight = 1)
        CurrentOrderFrame.grid_columnconfigure((0), weight = 1)
        TitleOfJob = CTkLabel(CurrentOrderFrame, text = f"Job Title: {Values[-2]}", font = CTkFont(size = 30)).grid(row = 0, column = 0,sticky = "w", padx = 20,pady = (10,0))
        NameOfTheCommissioner = CTkLabel(CurrentOrderFrame, text = f"Commissioner name: {Values[0]}", font = CTkFont(size = 20)).grid(row = 0, column = 0, sticky = "e", padx = (0, 20))
        ShortDescriptionTitle = CTkLabel(CurrentOrderFrame, text = "Short description: ",font = CTkFont(size = 17)).grid(row = 1, column = 0,padx = 20,sticky = "w")
        ShortDescriptionOfJob = CTkLabel(CurrentOrderFrame, text = f"{Values[-3][:100]}...",font = CTkFont(size = 15))
        ShortDescriptionOfJob.grid(row = 2, column = 0,padx = 20,pady = (0.20), sticky = "w")
        DateDue = CTkLabel(CurrentOrderFrame, text = f"Due Date is 29/08/23",font = CTkFont(size = 15)).grid(row = 1, column = 0,padx = (0,20),pady = (10,0))
        CustomerEmail = CTkLabel(CurrentOrderFrame, text = f"Commissioner Email: {Values[-1]}",font = CTkFont(size = 15)).grid(row = 1, column = 0, sticky = "e",padx = (0,20), pady = (10,0))
        OrderStatusLabel = CTkLabel(CurrentOrderFrame, text = f"Status: {Values[2]}",font = CTkFont(size = 15)).grid(row = 3, column = 0, sticky = "e", padx = (0,30))
        ViewInMoreDetailButton = CTkButton(CurrentOrderFrame, text = "View Job in more detail", command = lambda:self.LoadingOrdersInDetailFrame(self.ViewingCurrentOrdersInDetail(Values))).grid(row = 3, column = 0)
        return CurrentOrderFrame
    
    #Function generates a single requested job frame so that it can be put into another frame to display all of the jobs
    def GeneratingASingleRequestedJobFrame(self,Values: []) -> CTkFrame:
        RequestedOrderFrame = CTkFrame(self.OrdersFrame, corner_radius= 5, width = 1000000)
        RequestedOrderFrame.grid_rowconfigure((0,1,2,3), weight = 1)
        RequestedOrderFrame.grid_columnconfigure((0), weight = 1)
        TitleOfJob = CTkLabel(RequestedOrderFrame, text = f"Job Title: {Values[2]}", font = CTkFont(size = 30)).grid(row = 0, column = 0,sticky = "w", padx = 20,pady = (10,0))
        NameOfTheCommissioner = CTkLabel(RequestedOrderFrame, text = f"Commissioner name: {Values[0]}", font = CTkFont(size = 20)).grid(row = 0, column = 0, sticky = "e", padx = (0, 20))
        ShortDescriptionTitle = CTkLabel(RequestedOrderFrame, text = "Short description: ",font = CTkFont(size = 17)).grid(row = 1, column = 0,padx = 20,sticky = "w")
        ShortDescriptionOfJob = CTkLabel(RequestedOrderFrame, text = f"{Values[1][:100]}...",font = CTkFont(size = 15))
        ShortDescriptionOfJob.grid(row = 2, column = 0,padx = 20,pady = (0.20), sticky = "w")
        DateDue = CTkLabel(RequestedOrderFrame, text = f"Days need to be done when accepted: {Values[4]}",font = CTkFont(size = 15)).grid(row = 1, column = 0,padx = (0,20),pady = (10,0))
        CustomerEmail = CTkLabel(RequestedOrderFrame, text = f"Commissioner Email: {Values[3]}",font = CTkFont(size = 15)).grid(row = 1, column = 0, sticky = "e",padx = (0,20), pady = (10,0))
        DeclineButton = CTkButton(RequestedOrderFrame, text = "Decline", command= lambda:self.DecliningOrder(Values[5])).grid(row = 3, column = 0, sticky = "w", padx = (50,0))
        ViewinMoreDetailButton = CTkButton(RequestedOrderFrame, text = "View order in more detail", command = lambda:self.LoadingOrdersInDetailFrame(self.ViewingRequestedOrdesInDetail(Values))).grid(row = 3, column = 0, padx = (50,0))
        AcceptButton = CTkButton(RequestedOrderFrame, text = "Accept", command = lambda: self.AcceptingOrder(Values[-1])).grid(row = 3, column = 0, sticky = "e", padx = (0,50))
        return RequestedOrderFrame
    
    #Function generaets a single comlpleted job frame so that it can be put into another frame to display all of the jobs
    def GeneratingASingleCompletedJobFrame(self,Values: []) -> CTkFrame:
        CompletedOrdersFrame = CTkFrame(self.OrdersFrame, corner_radius= 5, width = 1000000)
        CompletedOrdersFrame.grid_rowconfigure((0,1,2,3), weight = 1)
        CompletedOrdersFrame.grid_columnconfigure((0), weight = 1)
        TitleOfJob = CTkLabel(CompletedOrdersFrame, text = f"Job Title: {Values[2]}", font = CTkFont(size = 30)).grid(row = 0, column = 0,sticky = "w", padx = 20,pady = (10,0))
        NameOfTheCommissioner = CTkLabel(CompletedOrdersFrame, text = f"Commissioner name: {Values[0]}", font = CTkFont(size = 20)).grid(row = 0, column = 0, sticky = "e", padx = (0, 20))
        ShortDescriptionTitle = CTkLabel(CompletedOrdersFrame, text = "Short description: ",font = CTkFont(size = 17)).grid(row = 1, column = 0,padx = 20,sticky = "w")
        ShortDescriptionOfJob = CTkLabel(CompletedOrdersFrame, text = f"{Values[1][:100]}...",font = CTkFont(size = 15))
        ShortDescriptionOfJob.grid(row = 2, column = 0,padx = 20,pady = (0.20), sticky = "w")
        DateDue = CTkLabel(CompletedOrdersFrame, text = f"Due Date is 29/08/23",font = CTkFont(size = 15)).grid(row = 1, column = 0,padx = (0,20),pady = (10,0))
        CustomerEmail = CTkLabel(CompletedOrdersFrame, text = f"Commissioner Email: {Values[3]}",font = CTkFont(size = 15)).grid(row = 1, column = 0, sticky = "e",padx = (0,20), pady = (10,0))
        OrderStatusLabel = CTkLabel(CompletedOrdersFrame, text = f"Status: {Values[-1]}",font = CTkFont(size = 15)).grid(row = 3, column = 0, sticky = "e", padx = (0,30))
        ViewInMoreDetailButton = CTkButton(CompletedOrdersFrame, text = "View Job in more detail", command = lambda:self.LoadingOrdersInDetailFrame(self.ViewingCompletedJobsInDetail(Values))).grid(row = 3, column = 0)
        return CompletedOrdersFrame
    
    def GeneratingASingleCreatedJobFrame(self,Values: []) -> CTkFrame:
        CreatedJobFrame = CTkFrame(self.OrdersFrame, corner_radius= 5, width = 1000000)
        CreatedJobFrame.grid_rowconfigure((0,1,2,3), weight = 1)
        CreatedJobFrame.grid_columnconfigure((0), weight = 1)
        TitleOfJob = CTkLabel(CreatedJobFrame, text = f"Job Title: {Values[1]}", font = CTkFont(size = 30)).grid(row = 0, column = 0,sticky = "w", padx = 20,pady = (10,0))
        ShortDescriptionTitle = CTkLabel(CreatedJobFrame, text = "Short description: ",font = CTkFont(size = 17)).grid(row = 1, column = 0,padx = 20,sticky = "w")
        ShortDescriptionOfJob = CTkLabel(CreatedJobFrame, text = f"{Values[2][:30]}...",font = CTkFont(size = 15))
        ShortDescriptionOfJob.grid(row = 2, column = 0,padx = 20,pady = (0.20), sticky = "w")
        JobTag = CTkLabel(CreatedJobFrame, text = f"Tag: {self.TagList[Values[3]]}", font = CTkFont(size = 17)).grid(row = 0, column = 0, sticky = "e", padx = (0, 40), pady = (15,0))
        FreelancerEmail = CTkLabel(CreatedJobFrame, text = f"Freelancer Email: {Values[4]}", font = CTkFont(size = 14)).grid(row = 3, column = 0, sticky = "e", padx = (0, 40), pady = (0,10))
        JobId = CTkLabel(CreatedJobFrame, text = f"Job ID: {Values[0]}", font = CTkFont(size = 17)).grid(row = 3, column = 0, sticky = "w", padx = (40,0),pady = (0,10))
        ViewInMoreDetailButton = CTkButton(CreatedJobFrame, text = "View Job in more detail / Edit Job", command = lambda:self.LoadingOrdersInDetailFrame(self.ViewingOrEditingJobsCreated(Values))).grid(row = 3, column = 0)
        return CreatedJobFrame
    
    def ViewingCurrentOrdersInDetail(self, ArrangedData):
        self.DeletignWidgetsOfFrame(self.OrdersInDetailFrame)
        self.OrdersInDetailFrame.grid_columnconfigure((0,2), weight = 1)
        self.OrdersInDetailFrame.grid_columnconfigure((1), weight = 3)
        self.OrdersInDetailFrame.grid_rowconfigure((0,1), weight = 1)
        self.OrdersInDetailFrame.grid_rowconfigure((2,3), weight = 1)
        backButton = CTkButton(self.OrdersInDetailFrame, text = f"Back", font = CTkFont(size = 10),command = lambda: self.LoadingOrdersInDetailFrame(self.GeneratingFrameWithAllJobs(self.type))).grid(row = 0, column = 0, padx = 30, pady = 30)
        TitleLabel = CTkLabel(self.OrdersInDetailFrame, text = f"Title: {ArrangedData[4]}", font = CTkFont(size = 30)).grid(row = 0, column = 1, padx = (10,0),pady = (0,40),sticky = "s")
        DescriptionTitle = CTkLabel(self.OrdersInDetailFrame, text = "Description: ",font = CTkFont(size = 19)).grid(row = 1, column = 1,padx = 20,pady = 30,sticky = "sw")
        DescriptionOfJob = CTkTextbox(self.OrdersInDetailFrame,font = CTkFont(size = 15))
        DescriptionOfJob.grid(row = 2, column = 1,padx = 20,pady = (0.20), sticky = "nesw")
        DescriptionOfJob.insert("0.0",ArrangedData[3])
        DescriptionOfJob.configure(state = DISABLED)
        DateDue = CTkLabel(self.OrdersInDetailFrame, text = f"Due Date is \n 29/08/23",font = CTkFont(size = 15)).grid(row = 1, column = 2,sticky = "s", padx = (0,10),pady = (10,0))
        OrderStatusLabel = CTkLabel(self.OrdersInDetailFrame, text = f"Commissioner Email: \n{ArrangedData[-1]}",font = CTkFont(size = 15)).grid(row = 2, column = 2, padx = (0,30))
        TerminateJobButton = CTkButton(self.OrdersInDetailFrame, text = "Terminate Job",font= CTkFont(size = 15), command = lambda:self.TerminatingOrder(ArrangedData[1], ArrangedData[-1],ArrangedData[3])).grid(row = 3, column = 1,sticky = "w",padx = (60,60))
        CompletedJob = CTkButton(self.OrdersInDetailFrame,text = "Complete Job", font = CTkFont(size = 17), command= lambda:self.CompletingOrder(ArrangedData[1])).grid(row = 3, column = 1, sticky = "e",padx = (60,60))
        return self.OrdersInDetailFrame
    
    def ViewingRequestedOrdesInDetail(self,ArrangedData):
        self.DeletignWidgetsOfFrame(self.OrdersInDetailFrame)
        self.OrdersInDetailFrame.grid_columnconfigure((0,2), weight = 1)
        self.OrdersInDetailFrame.grid_columnconfigure((1), weight = 3)
        self.OrdersInDetailFrame.grid_rowconfigure((0,1), weight = 1)
        self.OrdersInDetailFrame.grid_rowconfigure((2,3), weight = 1)
        backButton = CTkButton(self.OrdersInDetailFrame, text = f"Back", font = CTkFont(size = 10),command = lambda: self.LoadingOrdersInDetailFrame(self.GeneratingFrameWithAllJobs(self.type))).grid(row = 0, column = 0, padx = 30, pady = 30)
        TitleLabel = CTkLabel(self.OrdersInDetailFrame, text = f"Title: {ArrangedData[2]}", font = CTkFont(size = 30)).grid(row = 0, column = 1, padx = (10,0),pady = (0,40),sticky = "s")
        DescriptionTitle = CTkLabel(self.OrdersInDetailFrame, text = "Wants: ",font = CTkFont(size = 19)).grid(row = 1, column = 1,padx = 20,pady = 30,sticky = "sw")
        DescriptionOfJob = CTkTextbox(self.OrdersInDetailFrame,font = CTkFont(size = 15))
        DescriptionOfJob.grid(row = 2, column = 1,padx = 20,pady = (0.20), sticky = "nesw")
        DescriptionOfJob.insert("0.0",ArrangedData[1])
        DescriptionOfJob.configure(state = DISABLED)
        NumberOfDaysToBeCompletedBy = CTkLabel(self.OrdersInDetailFrame, text = f"Number of days due by {ArrangedData[4]}",font = CTkFont(size = 15)).grid(row = 1, column = 2,sticky = "s", padx = (0,10),pady = (10,0))
        CommissionerEmailLabel = CTkLabel(self.OrdersInDetailFrame, text = f"Commissioner Email: \n {ArrangedData[3]}",font = CTkFont(size = 10)).grid(row = 2, column = 2, padx = (0,30))
        DeclineJob = CTkButton(self.OrdersInDetailFrame, text = "Decline",font= CTkFont(size = 15), command= lambda:self.DecliningOrder(ArrangedData[5])).grid(row = 3, column = 1,sticky = "w",padx = (60,60))
        AcceptJob = CTkButton(self.OrdersInDetailFrame,text = "Accept", font = CTkFont(size = 17),command = lambda:self.AcceptingOrder(ArrangedData[5])).grid(row = 3, column = 1, sticky = "e",padx = (60,60))
        return self.OrdersInDetailFrame
    
    def ViewingCompletedJobsInDetail(self,ArrangedData):
        self.DeletignWidgetsOfFrame(self.OrdersInDetailFrame)
        self.OrdersInDetailFrame.grid_columnconfigure((0,2), weight = 1)
        self.OrdersInDetailFrame.grid_columnconfigure((1), weight = 3)
        self.OrdersInDetailFrame.grid_rowconfigure((0,1), weight = 1)
        self.OrdersInDetailFrame.grid_rowconfigure((2,3), weight = 1)
        backButton = CTkButton(self.OrdersInDetailFrame, text = f"Back", font = CTkFont(size = 10),command = lambda: self.LoadingOrdersInDetailFrame(self.GeneratingFrameWithAllJobs(self.type))).grid(row = 0, column = 0, padx = 30, pady = 30)
        TitleLabel = CTkLabel(self.OrdersInDetailFrame, text = f"Title: {ArrangedData[2]}", font = CTkFont(size = 30)).grid(row = 0, column = 1, padx = (10,0),pady = (0,40),sticky = "s")
        DescriptionTitle = CTkLabel(self.OrdersInDetailFrame, text = "Wants: ",font = CTkFont(size = 19)).grid(row = 1, column = 1,padx = 20,pady = 30,sticky = "sw")
        DescriptionOfJob = CTkTextbox(self.OrdersInDetailFrame,font = CTkFont(size = 15))
        DescriptionOfJob.grid(row = 2, column = 1,padx = 20,pady = (0.20), sticky = "nesw")
        DescriptionOfJob.insert("0.0",ArrangedData[1])
        DescriptionOfJob.configure(state = DISABLED)
        StatusOfTheJob = CTkLabel(self.OrdersInDetailFrame, text = "Status: Completed").grid(row = 3, column = 2, sticky = "n",padx = (0,30))
        NumberOfDaysToBeCompletedBy = CTkLabel(self.OrdersInDetailFrame, text = f"Date due was 29/08/23",font = CTkFont(size = 15)).grid(row = 1, column = 2,sticky = "s", padx = (0,10),pady = (10,0))
        CommissionerEmailLabel = CTkLabel(self.OrdersInDetailFrame, text = f"Commissioner Email: \n {ArrangedData[3]}",font = CTkFont(size = 15)).grid(row = 2, column = 2, padx = (0,30))
        return self.OrdersInDetailFrame
    
    def ViewingOrEditingJobsCreated(self,ArrangedData):
        #Setting up grid
        self.DeletignWidgetsOfFrame(self.OrdersInDetailFrame)
        self.OrdersInDetailFrame.grid_columnconfigure((0,2), weight = 1)
        self.OrdersInDetailFrame.grid_columnconfigure((1), weight = 3)
        self.OrdersInDetailFrame.grid_rowconfigure((0,1), weight = 1)
        self.OrdersInDetailFrame.grid_rowconfigure((2,3), weight = 1)
        #All the widgets for displaying widgest for changing ttitle and textbox
        backButton = CTkButton(self.OrdersInDetailFrame, text = f"Back", font = CTkFont(size = 10),command = lambda: self.LoadingOrdersInDetailFrame(self.GeneratingFrameWithAllJobs(self.type))).grid(row = 0, column = 0, padx = 30, pady = 30)
        OriginalTitleLabel = CTkLabel(self.OrdersInDetailFrame,text = f"Title: {ArrangedData[1]}", font = CTkFont(size = 30)).grid(row = 0, column = 1, pady = 30,padx = 20)
        ChangedTitleLabel  = CTkLabel(self.OrdersInDetailFrame, text = "Changed Title: ", font = CTkFont(size = 19)).grid(row = 0, column = 1, sticky = "ws", pady = (30,0))
        ChangedTitleTextBox = CTkTextbox(self.OrdersInDetailFrame)
        ChangedTitleTextBox.grid(row = 1, column = 1, padx = (10,0),pady = (0,40),sticky = "ew")
        ChangedTitleTextBox.insert("0.0", f"{ArrangedData[1]}")
        DescriptionTitle = CTkLabel(self.OrdersInDetailFrame, text = "Description: ",font = CTkFont(size = 19)).grid(row = 1, column = 1,padx = 20,pady = 30,sticky = "sw")
        DescriptionOfJob = CTkTextbox(self.OrdersInDetailFrame,font = CTkFont(size = 15))
        DescriptionOfJob.grid(row = 2, column = 1,padx = 20,pady = (0.20), sticky = "nesw")
        DescriptionOfJob.insert("0.0",ArrangedData[2])
        #Radio buttons that can be clicked to change tag:
        GroupOfRadioButtons = CTkFrame(self.OrdersInDetailFrame, corner_radius= 10)
        GroupOfRadioButtons.grid(row = 1, column = 3, rowspan = 3,sticky = "nsew", padx = (10,40), pady = (30, 10))# Need this on a separate line as it the widgets don't go into the box if you don't do it this way
        ChoiceOfTagLabel = CTkLabel(GroupOfRadioButtons, text = "Tag:", font=CTkFont(size=15, weight="bold"), corner_radius= 10).grid(row = 1, column = 0, sticky = "ew")
        SelectedValue = IntVar(value = ArrangedData[3])
        ArtRadioButton = CTkRadioButton(GroupOfRadioButtons, text="Art", variable=SelectedValue,value = 0).grid(row = 2, column = 0,padx = 10, pady = 10,sticky = "ew")
        CodingRadioButton = CTkRadioButton(GroupOfRadioButtons,text="Coding",variable=SelectedValue,value = 1).grid(row = 3, column = 0,padx = 10, pady = 10,sticky = "ew")
        ReviewingWorkRadioButton = CTkRadioButton(GroupOfRadioButtons,text="Reviewing Work",variable=SelectedValue,value = 2).grid(row = 4,padx = 10, column = 0, pady = 10,sticky = "ew")
        PhotographyRadioButton = CTkRadioButton(GroupOfRadioButtons, text = "Photography",variable=SelectedValue,value = 3).grid(row = 5, padx = 10, column = 0, pady = 10,sticky = "ew")
        OtherRadioRadioButton = CTkRadioButton(GroupOfRadioButtons,text = "Other",variable=SelectedValue,value = 4).grid(row = 6, column = 0,padx = 10, pady = 10,sticky = "ew")
        #Buttons to either terminate the job or save changes made to description and title
        DeleteJobButton = CTkButton(self.OrdersInDetailFrame, text = "Delete Job",font= CTkFont(size = 15), command= lambda:self.DeletingCompletedJob(ArrangedData[0])).grid(row = 3, column = 1,sticky = "w",padx = (0,60))
        if ArrangedData[5] == 0:
            MakingJobPrivate = CTkButton(self.OrdersInDetailFrame, text = "Make Job Private", font = CTkFont(size = 15), command = lambda:self.MakingAJobPrivateOrUnPrivate(ArrangedData[0],ArrangedData[5])).grid(row = 3 , column = 1,padx = (0,175))
        else:
            MakingJobUnPrivate = CTkButton(self.OrdersInDetailFrame, text = "Make Job not private", font = CTkFont(size = 15), command = lambda:self.MakingAJobPrivateOrUnPrivate(ArrangedData[0],ArrangedData[5])).grid(row = 3 , column = 1,padx = (0,175))
        SaveChangesMadeToDescriptionAndTtitle = CTkButton(self.OrdersInDetailFrame,text = "Save Changes Made to Textbox and Title", command = lambda:self.ChangingDetailsOfAMadeJob(ArrangedData[0],
                                                                                                                                                                                    ChangedTitleTextBox.get("1.0", "end-1c"),
                                                                                                                                                                                    DescriptionOfJob.get("1.0", "end-1c"),
                                                                                                                                                        SelectedValue.get()), font = CTkFont(size = 17)).grid(row = 3, column = 1, sticky = "e",padx = (60,0))
        return self.OrdersInDetailFrame
        
    def ForgettingFrames(self):
        self.OrdersFrame.grid_forget()
        self.OrdersInDetailFrame.grid_forget()
        
    def LoadingOrdersInDetailFrame(self, OrdersInDetail: CTkFrame):
        self.ForgettingFrames()
        OrdersInDetail.grid(row = 0, column = 1, sticky = "nsew", padx = 30, pady = 30)
      
    def DeletingWidgetsOfAFrame(self,Frame: CTkFrame):
        for widget in Frame.winfo_children():
            widget.destroy()
    
    #Accepts the order, the order record value of accepted should turn from 0 to 1 in database.
    #Number of accepted orders increases by 1, done for teh mielstoen page
    def AcceptingOrder(self, OrderID):
        self.cursor.execute(f"UPDATE OrdersTable SET Accepted = 1,Status = 'Working' WHERE OrderID = {OrderID}")
        self.cursor.execute(f"UPDATE UserTable SET Accepted_Orders = Accepted_Orders + 1 WHERE UserID = {self.UserData.UserID}")
        self.db.commit()
        self.GeneratingFrameWithAllJobs(self.type)
    
    #Declines the order, the order record value of accepted should state 0 and teh status should change to "Rejected"
    def DecliningOrder(self, OrderID):
        self.cursor.execute(f"UPDATE OrdersTable SET Status = 'Rejetced' WHERE OrderID = {OrderID}")
        self.db.commit()
        self.GeneratingFrameWithAllJobs(self.type)
    
    #Terminates the order, the commissioner who made the order should be emailed stating that their order has been terminated
    def TerminatingOrder(self,OrderId, CommissionerEmail, Wants):
        self.cursor.execute(f"DELETE FROM OrdersTable WHERE OrderId = '{OrderId}' ")
        self.LoadingOrdersInDetailFrame(self.GeneratingFrameWithAllJobs(self.type))
        subject = "Cancellation of order"
        Content = f"The order with Order ID of {OrderId} has been terminated by the freelancer. The wants of the order were '{Wants}'"
        Reciever = CommissionerEmail
        self.MyEmailObject.SendingActualEmail(subject,Content,Reciever)
        self.db.commit()
    
    #A job gets completely deleted.
    def DeletingCompletedJob(self, JobId):
        self.cursor.execute(f"DELETE FROM JobTable WHERE JobID = {JobId}")
        self.cursor.execute(f"DELETE FROM OrdersTable WHERE JobID = {JobId}")
        self.db.commit()
        print(f"The job with job id {JobId} and also the orders linked to that job")
        self.LoadingOrdersInDetailFrame(self.GeneratingFrameWithAllJobs(self.type))
    
    #Order is fully completed. Teh finished orders increases for freelancer, for their milestones on the milestone page.
    def CompletingOrder(self,OrderID):
        self.cursor.execute(f"UPDATE OrdersTable SET Status = 'Completed' WHERE OrderID = {OrderID}")
        self.cursor.execute(f"UPDATE UserTable SET Accepted_Orders = Accepted_Orders + 1 WHERE UserID = {self.UserData.UserID}")
        self.db.commit()
        self.GeneratingFrameWithAllJobs(self.type)
    

    #Stops people from ordering that job but can still be viewed by people who have ordered before it was priated and also can be een in completed orders
    def MakingAJobPrivateOrUnPrivate(self,JobId,PrivateOrNot):
        if PrivateOrNot == 0: 
            self.cursor.execute(f"UPDATE JobTable SET Private = 1 WHERE JobID = {JobId}")
            print(f"The job with JobId {JobId} should have been privated")
        else:
            self.cursor.execute(f"UPDATE JobTable SET Private = 0 WHERE JobID = {JobId}")
            print(f"The job with JobId {JobId} should have been unprivated")
        self.db.commit()
        self.LoadingOrdersInDetailFrame(self.GeneratingFrameWithAllJobs(self.type))
    
    #Changes description and title of job they have selected
    def ChangingDetailsOfAMadeJob(self,JobId , NewTitle, NewDescription, NewTag):
        self.cursor.execute(f"UPDATE JobTable SET JobTitle = '{NewTitle}',Description = '{NewDescription}',Tag = '{NewTag}' WHERE JobID = {JobId}")
        self.db.commit()
        print("Should have chnaged the title and description")
        self.LoadingOrdersInDetailFrame(self.GeneratingFrameWithAllJobs(self.type))
        
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


