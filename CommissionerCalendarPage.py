from UsersDataClass import User
from customtkinter import *
from FreelancerCode.OrdersCode.CommissionerOrdersFrame import CommissionerOrdersFrame
import mysql.connector

class CommissionerCalendarPage():
    
    def __init__(self,root,UserData: User) -> None:
        self.UserData = UserData
        #Calendar screen
        self.CalendarScreen = CTkFrame(root, corner_radius= 10)
        #Connecting to database
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="#########",
            database = "ProjectDatabaseNew"
        )
        self.cursor = self.mydb.cursor()
        #Calling CommissionerOrdersFrame so that allows for the commissioner to view that ordeer in detail\
        self.CommissionerOrdersObject = CommissionerOrdersFrame(root, self.mydb, UserData)
    
    def GettingDataInArrangedForm(self,SQLStatment,NumberOfJobsForEachPage):
        #SQl statment is executed
        self.cursor.execute(SQLStatment)
        #Data is fetched
        CurrentOrdersData = self.cursor.fetchall()
        #Data is put into an arranged way that I can use
        NewArrangedOrdersData = []
        NumberOfPages = len(CurrentOrdersData) // NumberOfJobsForEachPage
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
        #Checks if there are any jobs and if there isn't then it sets teh arranged data to none which tells my code to display "look like there is no jobs"
        try: 
            NewArrangedOrdersData[0]
        except IndexError:
            NewArrangedOrdersData = None
        return NewArrangedOrdersData
    
    def GeneratingCalendarPage(self):
        self.DeletingWidgetsOfAFrame(self.CalendarScreen)
        self.CalendarScreen.columnconfigure((0,1,2,3,4), weight = 1)
        self.CalendarScreen.rowconfigure((0,1,2,3,4), weight = 1)
        CalendarData = self.GettingDataInArrangedForm(f"SELECT UserTable.FullName, OrdersTable.OrderID, OrdersTable.Status,  OrdersTable.Wants, JobTable.JobTitle, UserTable.Email FROM UserTable \
							INNER JOIN OrdersTable ON UserTable.UserID = OrdersTable.FreelancerID \
                            INNER JOIN JobTable ON OrdersTable.JobID = JobTable.JobID \
                            WHERE OrdersTable.CommissionerID = '{self.UserData.UserID}' \
                            AND OrdersTable.Status = 'Working' \
                            AND OrdersTable.Accepted = 1",4)
        MondayLabel = CTkLabel(self.CalendarScreen, text = "Monday",font=CTkFont(size = 20)).grid(row = 0, column = 0)
        Lines = CTkLabel(self.CalendarScreen, text = "| \n| \n| \n| \n| \n| \n| \n| \n", font = CTkFont(size = 20)).grid(row = 0, column = 0,sticky = "w")
        TuesdayLabel = CTkLabel(self.CalendarScreen, text = "Tuesday",font=CTkFont(size = 20)).grid(row = 0, column = 1)
        Lines = CTkLabel(self.CalendarScreen, text = "| \n| \n| \n| \n| \n| \n| \n| \n", font = CTkFont(size = 20)).grid(row = 0, column = 0,sticky = "e")
        WednesdayLabel = CTkLabel(self.CalendarScreen, text = "Wednesday",font=CTkFont(size = 20)).grid(row = 0, column = 2)
        Lines = CTkLabel(self.CalendarScreen, text = "| \n| \n| \n| \n| \n| \n| \n| \n", font = CTkFont(size = 20)).grid(row = 0, column = 1,sticky = "e")
        ThursdayLabel = CTkLabel(self.CalendarScreen, text = "Thursday",font=CTkFont(size = 20)).grid(row = 0, column = 3)
        Lines = CTkLabel(self.CalendarScreen, text = "| \n| \n| \n| \n| \n| \n| \n| \n", font = CTkFont(size = 20)).grid(row = 0, column = 2,sticky = "e")
        FridayLabel = CTkLabel(self.CalendarScreen, text = "Friday",font=CTkFont(size = 20)).grid(row = 0, column = 4)
        Lines = CTkLabel(self.CalendarScreen, text = "| \n| \n| \n| \n| \n| \n| \n| \n", font = CTkFont(size = 20)).grid(row = 0, column = 3,sticky = "e")
        Lines = CTkLabel(self.CalendarScreen, text = "| \n| \n| \n| \n| \n| \n| \n| \n", font = CTkFont(size = 20)).grid(row = 0, column = 4,sticky = "e")
        CurrentDay = 0
        for DayOrders in CalendarData:
            NumberOfOrders = len(DayOrders)
            for OrderPointer in range(0,NumberOfOrders):
                self.CalendarOrder(DayOrders[OrderPointer],OrderPointer + 1, CurrentDay)
            CurrentDay += 1
    
        self.LoadingCalendarFrame(self.CalendarScreen)
            
            
    def CalendarOrder(self,OrderData,rowValue,columnValue):
        OrderTitle = CTkLabel(self.CalendarScreen,text = f"OrderID = {OrderData[1]}").grid(row = rowValue, column = columnValue)
        ViewInDetailButton = CTkButton(self.CalendarScreen, text = "View order in detail"
                                       ,command= lambda:self.CommissionerOrdersObject.LoadingFrame(self.CommissionerOrdersObject.ViewingCurrentOrderInMoreDetail(OrderData))).grid(row = rowValue, column = columnValue,sticky = "s")

    def LoadingCalendarFrame(self,FrameBeingLoaded : CTkFrame):
        FrameBeingLoaded.grid(row = 0, column = 1, padx = 30, pady = 30, sticky= "nsew")
        
        
    def DeletingWidgetsOfAFrame(self,Frame: CTkFrame):
        for widget in Frame.winfo_children():
            widget.destroy()
        
    
        
        