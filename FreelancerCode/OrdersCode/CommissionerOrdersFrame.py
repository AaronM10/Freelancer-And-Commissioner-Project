from UsersDataClass import User
from customtkinter import *


class CommissionerOrdersFrame():
    
    def __init__(self,root,dbConnection, UserData: User) -> None:
        self.UserData = UserData
        self.db = dbConnection
        self.cursor = self.db.cursor()
        #Defining frames/Screens
        self.CommissionerJobsFrame = CTkFrame(root, corner_radius= 10)
        self.CommissionerOrderFrame = CTkFrame(root, corner_radius= 10)
        self.CommissionerJobsinDetailFrame = CTkFrame(root, corner_radius= 10)
        self.CommissionerOrdersInDetailFrame = CTkFrame(root, corner_radius= 10)
        self.StartPointer = 0
        self.EndPointer = 0
        self.type = ''
        self.ArrangedOrdersData = [[]]
        self.ArrangedJobData = [[]]
        self.TagList = ["Art","Coding","Reviewing Work", "Photography", "Other"]
    
    def GettingDataInArrangedForm(self,SQLStatment,NumberOfJobsForEachPage):
        #Arranging grid
        for x in range(NumberOfJobsForEachPage + 1):
            self.CommissionerOrderFrame.grid_rowconfigure((x), weight = 1)
        self.CommissionerOrderFrame.grid_columnconfigure((0), weight = 1)
        #Arranging grid
        for x in range(NumberOfJobsForEachPage + 1):
            self.CommissionerJobsFrame.grid_rowconfigure((x), weight = 1)
        self.CommissionerJobsFrame.grid_columnconfigure((0), weight = 1)
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
        try: 
            NewArrangedOrdersData[0]
        except IndexError:
            NewArrangedOrdersData = None
        return NewArrangedOrdersData
    
    #Only handles orders data. Adds either previous orders or current orders data onto the screen
    def GeneratingCommissionerOrderFrame(self,type):
        self.type = type
        self.DeletingWidgetsOffAFrame(self.CommissionerOrderFrame)
        if type == "Current_Orders":
            self.ArrangedOrdersData = self.GettingDataInArrangedForm(f"SELECT UserTable.FullName, OrdersTable.OrderID, OrdersTable.Status,  OrdersTable.Wants, JobTable.JobTitle,OrdersTable.Accepted, \
                                                                     OrdersTable.OrderID,JobTable.Description, UserTable.Email FROM UserTable \
							INNER JOIN OrdersTable ON UserTable.UserID = OrdersTable.FreelancerID \
                            INNER JOIN JobTable ON OrdersTable.JobID = JobTable.JobID \
                            WHERE OrdersTable.CommissionerID = {self.UserData.UserID} \
                            AND OrdersTable.Status != 'Completed'" 
                            ,4)
            InfoLabel = CTkLabel(self.CommissionerOrderFrame, text = "No current orders!!!", font = CTkFont(size =30)).grid(row =0, column = 0,pady = 40)
        elif type == "Previous_Orders":
            self.ArrangedOrdersData = self.GettingDataInArrangedForm(f"SELECT UserTable.FullName,  OrdersTable.Wants, JobTable.JobTitle, UserTable.Email, \
                                                                     OrdersTable.NumberOfDays,OrdersTable.OrderID FROM UserTable \
							INNER JOIN OrdersTable ON UserTable.UserID = OrdersTable.CommissionerID \
                            INNER JOIN JobTable ON OrdersTable.JobID = JobTable.JobID \
                            WHERE OrdersTable.CommissionerID = {self.UserData.UserID} \
                            AND OrdersTable.Status = 'Completed'", 4)
            if self.ArrangedOrdersData == None:
                InfoLabel = CTkLabel(self.CommissionerOrderFrame, text = "Looks like you haven't ordered anything before!!!", font = CTkFont(size =30)).grid(row =0, column = 0,pady = 40)
        if self.ArrangedOrdersData != None:
            
            for PageDataPointer in range(len(self.ArrangedOrdersData[self.StartPointer])):
                if self.type == "Current_Orders":
                    TitleLabel = CTkLabel(self.CommissionerOrderFrame, text = "Current Orders: ", font = CTkFont(size = 40)).grid(row = 0, column = 0, sticky = "nsew", pady = (10,5))
                    self.GeneratingASingleCurrentOrderFrame(self.ArrangedOrdersData[self.StartPointer][PageDataPointer]).grid(row = PageDataPointer + 1, column = 0, sticky = "nsew", padx = 10, pady = 10)
                elif self.type == "Previous_Orders":
                    TitleLabel = CTkLabel(self.CommissionerOrderFrame, text = "Previous Orders:", font = CTkFont(size = 40)).grid(row = 0, column = 0, sticky = "nsew", pady = (10,5))
                    self.GeneratingASinglePreviousOrderFrame(self.ArrangedOrdersData[self.StartPointer][PageDataPointer]).grid(row = PageDataPointer + 1, column = 0, sticky = "nsew", padx = 10, pady = 10)
        return self.CommissionerOrderFrame
    
    
    
    def GeneratingCommissionerJobsFrames(self, type, RecommendedJobNumber,FindingOrdersData):
        self.type = type
        self.DeletingWidgetsOffAFrame(self.CommissionerJobsFrame)
        if type == "RecommendedJobs":
            self.ArrangedJobData = self.GettingDataInArrangedForm(f"SELECT JobTable.JobID,JobTable.JobTitle,JobTable.Description, JobTable.Tag, UserTable.UserID,UserTable.Email,UserTable.FullName \
                                FROM JobTable \
                                INNER JOIN UserTable ON UserTable.UserID = JobTable.FreelancerID \
                                WHERE JobTable.Tag = {RecommendedJobNumber} \
                                AND UserTable.UserID != {self.UserData.UserID} \
                                ",3)
        elif type == "FindingJobs":
            if FindingOrdersData[0] != "" and FindingOrdersData[1] != "":
                self.ArrangedJobData = self.GettingDataInArrangedForm(f"SELECT JobTable.JobID,JobTable.JobTitle,JobTable.Description, JobTable.Tag, UserTable.UserID,UserTable.Email,UserTable.FullName \
                                FROM JobTable \
                                INNER JOIN UserTable ON UserTable.UserID = JobTable.FreelancerID \
                                WHERE JobTable.JobTitle LIKE '%{FindingOrdersData[0]}%' \
                                AND JobTable.Tag = {self.TagList.index(FindingOrdersData[1])} \
                                AND UserTable.UserID != {self.UserData.UserID} \
                                ",3)
            elif FindingOrdersData[0] != "" and FindingOrdersData[1] == "":
                self.ArrangedJobData = self.GettingDataInArrangedForm(f"SELECT JobTable.JobID,JobTable.JobTitle,JobTable.Description, JobTable.Tag, UserTable.UserID,UserTable.Email,UserTable.FullName \
                                FROM JobTable \
                                INNER JOIN UserTable ON UserTable.UserID = JobTable.FreelancerID \
                                WHERE JobTable.JobTitle LIKE '%{FindingOrdersData[0]}%'  \
                                AND UserTable.UserID != {self.UserData.UserID} \
                                ",3)
            elif FindingOrdersData[0] == "" and FindingOrdersData[1] != "":
                self.ArrangedJobData = self.GettingDataInArrangedForm(f"SELECT JobTable.JobID,JobTable.JobTitle,JobTable.Description, JobTable.Tag, UserTable.UserID,UserTable.Email,UserTable.FullName \
                                FROM JobTable \
                                INNER JOIN UserTable ON UserTable.UserID = JobTable.FreelancerID \
                                WHERE JobTable.Tag = {self.TagList.index(FindingOrdersData[1])} \
                                AND UserTable.UserID != {self.UserData.UserID} \
                                ",3)
            
        if self.ArrangedJobData != None:
            
            for PageDataPointer in range(len(self.ArrangedJobData[self.StartPointer])):
                if self.type == "RecommendedJobs":
                    TitleLabel = CTkLabel(self.CommissionerJobsFrame, text = "Recommended Jobs:", font = CTkFont(size = 40)).grid(row = 0, column = 0, sticky = "nsew", pady = (10,5))
                    self.GeneratingASingleRecommendedJobFrame(self.ArrangedJobData[self.StartPointer][PageDataPointer]).grid(row = PageDataPointer + 1, column = 0, sticky = "nsew", padx = 10, pady = 10)
                elif self.type == "FindingJobs":
                    TitleLabel = CTkLabel(self.CommissionerJobsFrame, text = "Found Jobs", font = CTkFont(size = 40)).grid(row = 0, column = 0, sticky = "nsew", pady = (10,5))
                    self.GeneratingASingleFoundJobFrame(self.ArrangedJobData[self.StartPointer][PageDataPointer]).grid(row = PageDataPointer + 1, column = 0, sticky = "nsew", padx = 10, pady = 10)
                    
        PagesButtonFrame = CTkFrame(self.CommissionerJobsFrame, fg_color="transparent")
        PagesButtonFrame.grid_columnconfigure((0,1,2), weight = 1)
        MovingPagesbackwardsButton = CTkButton(PagesButtonFrame, text = "<", command= self.previousPage).grid(row = 0, column = 0, padx = (20,10))
        CurrentPageLabel = CTkLabel(PagesButtonFrame, text = f"{self.StartPointer + 1}").grid(row = 0, column = 1, padx = (10,10))
        MovingPagesForwardButton = CTkButton(PagesButtonFrame, text = ">", command = self.NextPage).grid(row = 0, column = 2, padx = (20,10))
        PagesButtonFrame.grid(row = 5, column = 0)
        return self.CommissionerJobsFrame
    
    #For jobs frames/screens
    
    def GeneratingASingleRecommendedJobFrame(self, RecommendedJob):
        RecommendedJobFrame = CTkFrame(self.CommissionerJobsFrame, corner_radius= 5, width = 1000000)
        RecommendedJobFrame.grid_rowconfigure((0,1,2,3), weight = 1)
        RecommendedJobFrame.grid_columnconfigure((0), weight = 1)
        TitleOfJob = CTkLabel(RecommendedJobFrame, text = f"Job Title: {RecommendedJob[1]}", font = CTkFont(size = 30)).grid(row = 0, column = 0,sticky = "w", padx = 20,pady = (10,0))
        NameOfTheFreelancer = CTkLabel(RecommendedJobFrame, text = f"Freelancer name: {RecommendedJob[6]}", font = CTkFont(size = 20)).grid(row = 0, column = 0, sticky = "e", padx = (0, 20))
        ShortDescriptionTitle = CTkLabel(RecommendedJobFrame, text = "Short description: ",font = CTkFont(size = 17)).grid(row = 1, column = 0,padx = 20,sticky = "w")
        ShortDescriptionOfJob = CTkLabel(RecommendedJobFrame, text = f"{RecommendedJob[2][:20]}...",font = CTkFont(size = 15))
        ShortDescriptionOfJob.grid(row = 2, column = 0,padx = 20,pady = (0.20), sticky = "w")
        FreelancerEmail = CTkLabel(RecommendedJobFrame, text = f"Freelancer Email: {RecommendedJob[5]}",font = CTkFont(size = 15)).grid(row = 1, column = 0, sticky = "e",padx = (0,20), pady = (10,0))
        TagOfJob = CTkLabel(RecommendedJobFrame, text = f"Tag: {self.TagList[RecommendedJob[3]]}", font = CTkFont(size = 15)).grid(row = 2, column = 0,sticky = "e", padx = (0,20),pady = (10,0))
        ViewInMoreDetailButton = CTkButton(RecommendedJobFrame, text = "View Job in more detail", command = lambda:[self.LoadingFrame(self.ViewingJobInDetail(RecommendedJob)), self.AddingToClicksAndOrders(RecommendedJob[3], 0)]).grid(row = 3, column = 0)
        return RecommendedJobFrame
    
    def GeneratingASingleFoundJobFrame(self, FoundJob):
        FoundJobFrame = CTkFrame(self.CommissionerJobsFrame, corner_radius= 5, width = 1000000)
        FoundJobFrame.grid_rowconfigure((0,1,2,3), weight = 1)
        FoundJobFrame.grid_columnconfigure((0), weight = 1)
        TitleOfJob = CTkLabel(FoundJobFrame, text = f"Job Title: {FoundJob[1]}", font = CTkFont(size = 30)).grid(row = 0, column = 0,sticky = "w", padx = 20,pady = (10,0))
        NameOfTheFreelancer = CTkLabel(FoundJobFrame, text = f"Freelancer name: {FoundJob[6]}", font = CTkFont(size = 20)).grid(row = 0, column = 0, sticky = "e", padx = (0, 20))
        ShortDescriptionTitle = CTkLabel(FoundJobFrame, text = "Short description: ",font = CTkFont(size = 17)).grid(row = 1, column = 0,padx = 20,sticky = "w")
        ShortDescriptionOfJob = CTkLabel(FoundJobFrame, text = f"{FoundJob[2][:20]}...",font = CTkFont(size = 15))
        ShortDescriptionOfJob.grid(row = 2, column = 0,padx = 20,pady = (0.20), sticky = "w")
        FreelancerEmail = CTkLabel(FoundJobFrame, text = f"Freelancer Email: {FoundJob[5]}",font = CTkFont(size = 15)).grid(row = 1, column = 0, sticky = "e",padx = (0,20), pady = (10,0))
        TagOfJob = CTkLabel(FoundJobFrame, text = f"Tag: {self.TagList[FoundJob[3]]}", font = CTkFont(size = 15)).grid(row = 2, column = 0,sticky = "e", padx = (0,20),pady = (10,0))
        ViewInMoreDetailButton = CTkButton(FoundJobFrame, text = "View Job in more detail", command = lambda: [self.LoadingFrame(self.ViewingJobInDetail(FoundJob)), self.AddingToClicksAndOrders(FoundJob[3], 0)]).grid(row = 3, column = 0)
        return FoundJobFrame
        
    #Viewing recommended job or found job in detail also allows for a user to place order. When a user clicks to view a job in deatiol the tag of that job is logged to be used for the recommendation system.   
        
    def ViewingJobInDetail(self, RecommendedJob):
        self.DeletingWidgetsOffAFrame(self.CommissionerJobsinDetailFrame)
        self.CommissionerJobsinDetailFrame.grid_columnconfigure((0,2), weight = 1)
        self.CommissionerJobsinDetailFrame.grid_columnconfigure((1), weight = 3)
        self.CommissionerJobsinDetailFrame.grid_rowconfigure((0,1), weight = 1)
        self.CommissionerJobsinDetailFrame.grid_rowconfigure((2,3), weight = 1)
        TitleLabel = CTkLabel(self.CommissionerJobsinDetailFrame, text = f"Title: {RecommendedJob[1]}", font = CTkFont(size = 30)).grid(row = 0, column = 1, padx = (10,0),pady = (0,40),sticky = "s")
        DescriptionTitle = CTkLabel(self.CommissionerJobsinDetailFrame, text = "Description: ",font = CTkFont(size = 19)).grid(row = 1, column = 1,padx = 20,pady = 30,sticky = "sw")
        DescriptionOfJob = CTkTextbox(self.CommissionerJobsinDetailFrame,font = CTkFont(size = 15))
        DescriptionOfJob.grid(row = 2, column = 1,padx = 20,pady = (0.20), sticky = "nesw")
        DescriptionOfJob.insert("0.0",RecommendedJob[2])
        DescriptionOfJob.configure(state = DISABLED)
        DateDue = CTkLabel(self.CommissionerJobsinDetailFrame, text = f"Due Date is \n 29/08/23",font = CTkFont(size = 15)).grid(row = 1, column = 2,sticky = "s", padx = (0,10),pady = (10,0))
        OrderStatusLabel = CTkLabel(self.CommissionerJobsinDetailFrame, text = f"Commissioner Email: \n{RecommendedJob[5]}",font = CTkFont(size = 15)).grid(row = 2, column = 2, padx = (0,30))
        PlacingOrderButton = CTkButton(self.CommissionerJobsinDetailFrame, text = "Placing Order",command= lambda: self.LoadingFrame(self.PlacingOrderScreen(RecommendedJob)),width = 200, height = 40, corner_radius= 10).grid(row = 3, column = 1,pady = 30)
        return self.CommissionerJobsinDetailFrame
    
    #Function to take in input from the commissioner, this input are the "wants" of the commissioner. Then the next function it used to add the placed order into the database.
    
    def PlacingOrderScreen(self,FoundJob):
        self.DeletingWidgetsOffAFrame(self.CommissionerOrderFrame)
        self.CommissionerOrderFrame.grid_rowconfigure((0,1), weight = 1)
        self.CommissionerOrderFrame.grid_columnconfigure(0, weight = 1)
        PlacingOrderTitle = CTkLabel(self.CommissionerOrderFrame, text = "Placing Order:", font = CTkFont(size = 30)).grid(row = 0, column = 0)
        WantsLabel = CTkLabel(self.CommissionerOrderFrame, text = "Wants:").grid(row = 0, column = 0, sticky = "ws",padx = 40,pady = 10)
        WantsEntryBox = CTkTextbox(self.CommissionerOrderFrame)
        WantsEntryBox.grid(row = 1, column = 0, sticky = "nsew",padx = 40)
        PlacingOrderButton = CTkButton(self.CommissionerOrderFrame, text = "Place Order!", command = lambda:[self.AddingNewOrderToDatabase(FoundJob,WantsEntryBox.get("1.0", "end-1c")),self.ForgettingFrames()] , width = 250, height = 40).grid(row = 2, column = 0,sticky = "s",pady = 40)
        return self.CommissionerOrderFrame
        
    def AddingNewOrderToDatabase(self, JobData,Wants):
        self.AddingToClicksAndOrders(JobData[3],1)
        self.cursor.execute(f"INSERT INTO OrdersTable(JobID,Status,Wants,CommissionerID,FreelancerID,Accepted,DateStarted,NumberOfDays) \
                            VALUES({JobData[0]},'Not Accepted','{Wants}',{self.UserData.UserID}, {JobData[4]},0, Null, 10) \
                            ")   
        self.db.commit()
    
    #Adds to list in record which states what order tag the user has clicked on. Used for recommendingJobs
    def AddingToClicksAndOrders(self,Tag,Type):
        if Type == 0:
            self.cursor.execute(f"SELECT Clicks_Orders_Tag FROM ProjectDatabaseNew.UserTable WHERE UserID = {self.UserData.UserID}")
            TagData = self.cursor.fetchone()
            TagData = TagData[0]
            Clicks_Orders_Tag = TagData.split(",")
            New_Clicks_Orders_Tag = ""
            for TagPointer in range(len(Clicks_Orders_Tag)):
                if TagPointer == Tag:
                    New_Clicks_Orders_Tag += f"{int(Clicks_Orders_Tag[TagPointer]) + 1},"
                else:
                    New_Clicks_Orders_Tag += f"{Clicks_Orders_Tag[TagPointer]},"
            New_Clicks_Orders_Tag = New_Clicks_Orders_Tag.rstrip(New_Clicks_Orders_Tag[-1])
            self.cursor.execute(f"UPDATE UserTable SET Clicks_Orders_Tag = '{New_Clicks_Orders_Tag}' WHERE UserID = {self.UserData.UserID}")
        elif Type == 1:
            self.cursor.execute(f"SELECT Orders_Tag FROM ProjectDatabaseNew.UserTable WHERE UserID = {self.UserData.UserID}")
            TagData = self.cursor.fetchone()
            TagData = TagData[0]
            Making_Orders_Tag = TagData.split(",")
            New_Making_Orders_Tag = ""
            for TagPointer in range(len(Making_Orders_Tag)):
                if TagPointer == Tag:
                    New_Making_Orders_Tag += f"{int(Making_Orders_Tag[TagPointer]) + 1},"
                else:
                    New_Making_Orders_Tag += f"{Making_Orders_Tag[TagPointer]},"
            New_Making_Orders_Tag = New_Making_Orders_Tag.rstrip(New_Making_Orders_Tag[-1])
            self.cursor.execute(f"UPDATE UserTable SET Orders_Tag = '{New_Making_Orders_Tag}' WHERE UserID = {self.UserData.UserID}")
        self.db.commit()
        
    #For orders page/screens
    
    def GeneratingASingleCurrentOrderFrame(self, CurrentOrder):
        CommissionerCurrentOrderFrame = CTkFrame(self.CommissionerOrderFrame, corner_radius= 5, width = 1000000)
        CommissionerCurrentOrderFrame.grid_rowconfigure((0,1,2,3), weight = 1)
        CommissionerCurrentOrderFrame.grid_columnconfigure((0), weight = 1)
        TitleOfJob = CTkLabel(CommissionerCurrentOrderFrame, text = f"Job Title: {CurrentOrder[4]}", font = CTkFont(size = 30)).grid(row = 0, column = 0,sticky = "w", padx = 20,pady = (10,0))
        NameOfTheCommissioner = CTkLabel(CommissionerCurrentOrderFrame, text = f"Freelancer name: {CurrentOrder[0]}", font = CTkFont(size = 20)).grid(row = 0, column = 0, sticky = "e", padx = (0, 20))
        ShortDescriptionTitle = CTkLabel(CommissionerCurrentOrderFrame, text = "Short description of wants: ",font = CTkFont(size = 17)).grid(row = 1, column = 0,padx = 20,sticky = "w")
        ShortDescriptionOfJob = CTkLabel(CommissionerCurrentOrderFrame, text = f"{CurrentOrder[3][:30]}...",font = CTkFont(size = 15))
        ShortDescriptionOfJob.grid(row = 2, column = 0,padx = 20,pady = (0,20), sticky = "w")
        CustomerEmail = CTkLabel(CommissionerCurrentOrderFrame, text = f"Commissioner Email: {CurrentOrder[-1]}",font = CTkFont(size = 15)).grid(row = 1, column = 0, sticky = "e",padx = (0,20), pady = (10,0))
        OrderStatusLabel = CTkLabel(CommissionerCurrentOrderFrame, text = f"Status: {CurrentOrder[2]}",font = CTkFont(size = 15)).grid(row = 3, column = 0, sticky = "e", padx = (0,30))
        ViewCurrentOrderInDetailButton = CTkButton(CommissionerCurrentOrderFrame, text = "View order in detail", command = lambda:self.LoadingFrame(self.ViewingCurrentOrderInMoreDetail(CurrentOrder))).grid(row = 4, column = 0,pady = 20)
        return CommissionerCurrentOrderFrame
        
    def GeneratingASinglePreviousOrderFrame(self, PreviousOrder):
        CommissionerCompletedOrdersFrame = CTkFrame(self.CommissionerOrderFrame, corner_radius= 5, width = 1000000)
        CommissionerCompletedOrdersFrame.grid_rowconfigure((0,1,2,3), weight = 1)
        CommissionerCompletedOrdersFrame.grid_columnconfigure((0), weight = 1)
        TitleOfJob = CTkLabel(CommissionerCompletedOrdersFrame, text = f"Job Title: {PreviousOrder[2]}", font = CTkFont(size = 30)).grid(row = 0, column = 0,sticky = "w", padx = 20,pady = (10,0))
        NameOfTheCommissioner = CTkLabel(CommissionerCompletedOrdersFrame, text = f"Commissioner name: {PreviousOrder[0]}", font = CTkFont(size = 20)).grid(row = 0, column = 0, sticky = "e", padx = (0, 20))
        ShortDescriptionTitle = CTkLabel(CommissionerCompletedOrdersFrame, text = "Wants: ",font = CTkFont(size = 17)).grid(row = 1, column = 0,padx = 20,sticky = "w")
        ShortDescriptionOfJob = CTkLabel(CommissionerCompletedOrdersFrame, text = f"{PreviousOrder[1][:100]}...",font = CTkFont(size = 15))
        ShortDescriptionOfJob.grid(row = 2, column = 0,padx = 20,pady = (0.20), sticky = "w")
        DateDue = CTkLabel(CommissionerCompletedOrdersFrame, text = f"Due Date is 29/08/23",font = CTkFont(size = 15)).grid(row = 1, column = 0,padx = (0,20),pady = (10,0))
        CustomerEmail = CTkLabel(CommissionerCompletedOrdersFrame, text = f"Commissioner Email: {PreviousOrder[3]}",font = CTkFont(size = 15)).grid(row = 1, column = 0, sticky = "e",padx = (0,20), pady = (10,0))
        OrderStatusLabel = CTkLabel(CommissionerCompletedOrdersFrame, text = f"Status: Completed",font = CTkFont(size = 15)).grid(row = 3, column = 0, sticky = "e", padx = (0,30))
        ViewPreviousOrderInDetailButton = CTkButton(CommissionerCompletedOrdersFrame, text = "View order in detail",command = lambda:self.LoadingFrame(self.ViewingPreviousOrderInMoreDetail(PreviousOrder))).grid(row = 4, column = 0,pady = 20)
        return CommissionerCompletedOrdersFrame
    
    #Viewing current and previous orders in detail
    
    def ViewingCurrentOrderInMoreDetail(self, CurrentOrder):
        self.DeletingWidgetsOffAFrame(self.CommissionerOrdersInDetailFrame)
        self.CommissionerOrdersInDetailFrame.grid_columnconfigure((0,2), weight = 1)
        self.CommissionerOrdersInDetailFrame.grid_columnconfigure((1), weight = 3)
        self.CommissionerOrdersInDetailFrame.grid_rowconfigure((0,1), weight = 1)
        self.CommissionerOrdersInDetailFrame.grid_rowconfigure((2,3), weight = 1)
        backButton = CTkButton(self.CommissionerOrdersInDetailFrame, text = f"Back", font = CTkFont(size = 10),command = lambda: self.LoadingOrdersInDetailFrame(self.GeneratingFrameWithAllJobs(self.type))).grid(row = 0, column = 0, padx = 30, pady = 30)
        TitleLabel = CTkLabel(self.CommissionerOrdersInDetailFrame, text = f"Title: {CurrentOrder[4]}", font = CTkFont(size = 30)).grid(row = 0, column = 1, padx = (10,0),pady = (0,40),sticky = "s")
        DescriptionTitle = CTkLabel(self.CommissionerOrdersInDetailFrame, text = "Wants: ",font = CTkFont(size = 19)).grid(row = 1, column = 1,padx = 20,pady = 30,sticky = "sw")
        DescriptionOfJob = CTkTextbox(self.CommissionerOrdersInDetailFrame,font = CTkFont(size = 15))
        DescriptionOfJob.grid(row = 2, column = 1,padx = 20,pady = (0.20), sticky = "nesw")
        DescriptionOfJob.insert("0.0",CurrentOrder[3])
        if CurrentOrder[-4] == 1:
            DescriptionOfJob.configure(state = DISABLED)
        else:
            MakeChangesButton = CTkButton(self.CommissionerOrdersInDetailFrame, text = "Make changes to wants ",command = lambda:self.ChangingWantsInDatabaseForOrder(CurrentOrder[-3],DescriptionOfJob.get("1.0", "end-1c"))).grid(row = 3, column = 1,pady = 30,sticky = "e")
            CancelOrder = CTkButton(self.CommissionerOrdersInDetailFrame, text = "Cancel Order ",command = lambda:self.RemovingOrderFromDatabase(CurrentOrder[-3])).grid(row = 3 , column = 1, sticky = "w")
        OrderEmailLabel = CTkLabel(self.CommissionerOrdersInDetailFrame, text = f"Commissioner Email: \n{CurrentOrder[-1]}",font = CTkFont(size = 15)).grid(row =1, column = 2, padx = (0,30))
        OrderStatusLabel = CTkLabel(self.CommissionerOrdersInDetailFrame,text = f"Status: \n {CurrentOrder[2]}").grid(row = 2, column = 2, pady = 30, padx = (0,30))
        return self.CommissionerOrdersInDetailFrame
    
    def ChangingWantsInDatabaseForOrder(self,OrderId,NewWants):
        self.cursor.execute(f"UPDATE OrdersTable SET Wants = '{NewWants}' WHERE OrderID = {OrderId}")
        self.db.commit()
        self.ForgettingFrames()
        print("Update completed")
    
    def RemovingOrderFromDatabase(self, OrderId):
        self.cursor.execute(f"DELETE FROM OrdersTable WHERE OrderID = {OrderId}")
        self.db.commit()
    
    def ViewingPreviousOrderInMoreDetail(self, PreviousOrder):
        self.DeletingWidgetsOffAFrame(self.CommissionerOrdersInDetailFrame)
        self.CommissionerOrdersInDetailFrame.grid_columnconfigure((0,2), weight = 1)
        self.CommissionerOrdersInDetailFrame.grid_columnconfigure((1), weight = 3)
        self.CommissionerOrdersInDetailFrame.grid_rowconfigure((0,1), weight = 1)
        self.CommissionerOrdersInDetailFrame.grid_rowconfigure((2,3), weight = 1)
        backButton = CTkButton(self.CommissionerOrdersInDetailFrame, text = f"Back", font = CTkFont(size = 10),command = lambda: self.LoadingOrdersInDetailFrame(self.GeneratingFrameWithAllJobs(self.type))).grid(row = 0, column = 0, padx = 30, pady = 30)
        TitleLabel = CTkLabel(self.CommissionerOrdersInDetailFrame, text = f"Title: {PreviousOrder[2]}", font = CTkFont(size = 30)).grid(row = 0, column = 1, padx = (10,0),pady = (0,40),sticky = "s")
        DescriptionTitle = CTkLabel(self.CommissionerOrdersInDetailFrame, text = "Wants: ",font = CTkFont(size = 19)).grid(row = 1, column = 1,padx = 20,pady = 30,sticky = "sw")
        DescriptionOfJob = CTkTextbox(self.CommissionerOrdersInDetailFrame,font = CTkFont(size = 15))
        DescriptionOfJob.grid(row = 2, column = 1,padx = 20,pady = (0.20), sticky = "nesw")
        DescriptionOfJob.insert("0.0",PreviousOrder[1])
        DescriptionOfJob.configure(state = DISABLED)
        StatusOfTheJob = CTkLabel(self.CommissionerOrdersInDetailFrame, text = "Status: Completed").grid(row = 3, column = 2, sticky = "n",padx = (0,30))
        CommissionerEmailLabel = CTkLabel(self.CommissionerOrdersInDetailFrame, text = f"Commissioner Email: \n {PreviousOrder[3]}",font = CTkFont(size = 15)).grid(row = 2, column = 2, padx = (0,30))
        return self.CommissionerOrdersInDetailFrame
    
    
    
    def DeletingWidgetsOffAFrame(self,Frame: CTkFrame):
        for widget in Frame.winfo_children():
            widget.destroy()
            
    def ForgettingFrames(self):
        self.CommissionerJobsFrame.grid_forget()
        self.CommissionerJobsinDetailFrame.grid_forget()
        self.CommissionerOrderFrame.grid_forget()
        
        
    def LoadingFrame(self, NewFrame: CTkFrame):
        self.ForgettingFrames()
        NewFrame.grid(row = 0, column = 1, sticky = "nsew", padx = 30, pady = 30)
    
    #Moves the start pointer 1 place forward so that the program knows what page/array to load
    #If the User goes past the end then they will go back to the start
    def NextPage(self):
        if self.StartPointer + 1 == self.EndPointer:
            self.StartPointer = 0
        else:
            self.EndPointer = self.StartPointer
            self.StartPointer += 1

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