import mysql.connector
from tkinter import *
import random
from customtkinter import *
import customtkinter
from Freelancerpage import FreelancerPage
from UsersDataClass import User
from SendingEmail import SendingEmailsClass
import time
from SendingEmail import SendingEmailsClass
from HashingInSha256 import HashingAValue

customtkinter.set_appearance_mode("Light")

root = CTk()
root.title("Starting page")
root.geometry("1500 x 1500")
class StartingPage():
    
    #Defines all of the frames and creates a structure for the sidebar and the frame next to the sidebar
    def __init__(self):
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure((0,2), weight = 0)
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="#########",
            database = "ProjectDatabaseNew"
        )
        self.SendingEmailsObject = SendingEmailsClass()
        self.cursor = self.db.cursor()
        self.LoginFrame = CTkFrame(root, corner_radius= 10, fg_color="transparent")
        self.SignUpPageFrame = CTkFrame(root, fg_color= "transparent")
        self.TwoFactorFrame = CTkFrame(root,fg_color = "transparent")
        self.AskingForEmailFrame = CTkFrame(root, fg_color="transparent")
        self.ChangingPasswordsFrame = CTkFrame(root,fg_color="transparent")
        self.SideBarFrame = CTkFrame(root, corner_radius=0)
        self.RandomCode = None
        self.LoadingFrame(self.LoginPage())
        self.AppearanceMode = StringVar()
        
        #Making sidebar
    
        self.SideBarFrame.grid(row=0, column=0, sticky="nsew")
        self.SideBarFrame.grid_rowconfigure(5, weight=1)

        self.SideBarFrame_label = CTkLabel(self.SideBarFrame, text="Starting Page",
                                                             compound="left", font=CTkFont(size=30, weight="bold"))
        self.SideBarFrame_label.grid(row=0, column=0, padx=20, pady=20)

        LoginOption = CTkButton(self.SideBarFrame, corner_radius=0, height=40, border_spacing=10, text="Log in",  fg_color="transparent", text_color=("gray20", "gray100"), hover_color=("gray80", "gray40"), anchor="w" ,command= lambda:self.LoadingFrame(self.LoginPage()))
        LoginOption.grid(row=1, column=0, sticky="ew")

        SignUpOption = CTkButton(self.SideBarFrame, corner_radius=0, height=40, border_spacing=10, text="Sign up", fg_color="transparent", text_color=("gray20", "gray100"), hover_color=("gray80", "gray40"),anchor="w", command = lambda:self.LoadingFrame(self.SigningUpPage()))
        SignUpOption.grid(row=2, column=0, sticky="ew")
        #Changes apperance based on a switch off = light on = dark
        ChangingAppearanceSwitch = CTkSwitch(self.SideBarFrame, text = "Dark Mode", command=self.Changing_Appearance_Mode,variable = self.AppearanceMode, onvalue= "Dark", offvalue = "Light").grid(row = 6, column = 0, padx = 10, pady = 10)
              
    #Generates me a frame that conatins all of the widgets such as labels and entry boxes and a button as well to submit
    def SigningUpPage(self):
        self.DeletingWidgetsOnFrame(self.SignUpPageFrame)
        self.SignUpPageFrame.grid_columnconfigure(0, weight = 1)
        self.SignUpPageFrame.grid_rowconfigure(0, weight = 2)
        self.SignUpPageFrame.grid_rowconfigure((10), weight = 2)
        UsernameInputted = StringVar()
        PasswordInputted = StringVar()
        EmailInputted = StringVar()
        SingingUpLabel = CTkLabel(self.SignUpPageFrame,text = "Sign Up page", font=CTkFont(size=60, weight="bold")).grid(row = 0, column = 0)
        
        EmailLabel = CTkLabel(self.SignUpPageFrame,text = "Email:", font = CTkFont(size= 15)).grid(row = 2, column = 0, padx = (0, 265), pady = (0,10))
        CTkEntry(self.SignUpPageFrame, textvariable=EmailInputted,placeholder_text= "Email",width = 300, font = CTkFont(size= 15), corner_radius= 30, height = 40).grid(row = 3, column = 0, pady = (0, 50))
        
        PasswordLabel = CTkLabel(self.SignUpPageFrame, text = "Password:", font = CTkFont(size= 15)).grid(row = 4, column = 0, padx = (0, 240),pady = (0,10))
        CTkEntry(self.SignUpPageFrame,textvariable=PasswordInputted,placeholder_text= "Password", show="*",width = 300, font = CTkFont(size= 15), corner_radius= 30, height = 40).grid(row = 5, column = 0, pady = (0, 50))
        
        UsernameLabel = CTkLabel(self.SignUpPageFrame, text = "Full name:", font = CTkFont(size= 15)).grid(row = 6, column = 0, padx = (0, 240),pady = (0,10))
        CTkEntry(self.SignUpPageFrame, textvariable=UsernameInputted,placeholder_text= "Full name",width = 300, font = CTkFont(size= 15), corner_radius= 30, height = 40).grid(row = 7, column = 0, pady = (0, 50))
        
        SendButton = CTkButton(self.SignUpPageFrame, text ="Sign Up", height = 40, width = 160, corner_radius= 30, command=lambda:self.CheckingIfInputsAreValid(EmailInputted.get(),PasswordInputted.get(),UsernameInputted.get())).grid(row = 8, column = 0)
        
        LogInButton = CTkButton(self.SignUpPageFrame, text = "Log in", height = 40, width = 160, corner_radius= 30, command = lambda:self.LoadingFrame(self.LoginPage())).grid(row = 9, column = 0, pady = (50, 10))
        return self.SignUpPageFrame
    
      #Checks if the inputs are valid.
    def CheckingIfInputsAreValid(self,Email,Password,Username):
        self.LoadingFrame(self.SigningUpPage())
        if "@" not in Email:
            InfoLabel = CTkLabel(self.SignUpPageFrame,text = "Missing @", font = CTkFont(size = 20, weight = "bold")).grid(row = 10, column = 0)
        elif ".com" not in Email and ".co.uk" not in Email:
            InfoLabel = CTkLabel(self.SignUpPageFrame,text = "Missing .com or .co.uk",font = CTkFont(size = 20, weight = "bold")).grid(row = 10, column = 0)
        elif len(Password) < 10:
            InfoLabel = CTkLabel(self.SignUpPageFrame, text="Password needs to be greater than 10 charcters",font = CTkFont(size = 20, weight = "bold")).grid(row = 10, column = 0)
        elif self.CheckingIfEmailAlreadyUsed(Email) == True:
            InfoLabel = CTkLabel(self.SignUpPageFrame, text="Email is already being used",font = CTkFont(size = 20, weight = "bold")).grid(row = 10, column = 0)
        elif len(Username) < 5:
            InfoLabel = CTkLabel(self.SignUpPageFrame, text="Full name has to be greater than 5 characters",font = CTkFont(size = 20, weight = "bold")).grid(row = 10, column = 0)
        else:
            self.InsertingData(Email,Password,Username)
            self.LoadingFrame(self.SigningUpPage())
            SuccessfulLogInInfoLabel = CTkLabel(self.SignUpPageFrame,text = "Successfully signed up now you can sign in!",font = CTkFont(size = 20, weight = "bold")).grid(row = 10, column = 0)
    
    #Checks if the email ids already in use
    def CheckingIfEmailAlreadyUsed(self,Email):
        self.cursor.execute(f"SELECT Email FROM UserTable WHERE Email = '{Email}'")
        email = self.cursor.fetchone()
        if email == None:
            return False # Just checks if they are equal to each other (checks if the email is already in the database)
        else:
            return True
        
    #Inserting the data into the table which essentially generates them an account for both freelacner and commissioner
    def InsertingData(self,email,password,Username):
        EncryptedPassword = HashingAValue(password)
        self.cursor.execute(f"INSERT INTO UserTable (Email,Password,FullName) VALUES('{email}','{EncryptedPassword}','{Username}')")
        self.cursor.execute(f"SELECT UserID FROM UserTable WHERE Email = '{email}'")
        UserDataArray = self.cursor.fetchone()
        self.db.commit()

    #Generates me a frame hat conatins all the widgets needed for logging in with extra buttons such as register and forgotten password for user convenience
    def LoginPage(self):
        #Creates structure of the frame
        self.DeletingWidgetsOnFrame(self.LoginFrame)
        self.LoginFrame.grid_columnconfigure(0, weight = 1)
        self.LoginFrame.grid_rowconfigure(0, weight = 2)
        self.LoginFrame.grid_rowconfigure((9), weight = 2)
        #Holds current values of the email and password entry boxes
        EmailInputted = StringVar()
        PasswordInputted = StringVar()
        #Just all of the widgets for solely logging in
        LoginLabel = CTkLabel(self.LoginFrame,text = "Log in page", font=CTkFont(size=60, weight="bold")).grid(row = 0, column = 0)
        
        EmailLabel = CTkLabel(self.LoginFrame,text = "Email:", font = CTkFont(size= 15)).grid(row = 2, column = 0, padx = (0, 265), pady = (0,10))
        CTkEntry(self.LoginFrame,textvariable= EmailInputted, placeholder_text= "Email: ", width = 300, font = CTkFont(size= 15),corner_radius= 30,height = 40).grid(row = 3, column = 0, pady = (0, 50))
        
        PasswordLabel = CTkLabel(self.LoginFrame, text = "Password:", font = CTkFont(size= 15)).grid(row = 4, column = 0, padx = (0, 240),pady = (0,10))
        CTkEntry(self.LoginFrame,textvariable=PasswordInputted,placeholder_text= "Password", show="*",width = 300, font = CTkFont(size= 15), corner_radius= 30, height = 40).grid(row = 5, column = 0, pady = (0, 50))

        SendButton = CTkButton(self.LoginFrame, text ="log in", height = 40, width = 160, corner_radius= 30, command=lambda:self.CheckingValidityOfAccount(EmailInputted.get(),PasswordInputted.get())).grid(row = 6, column = 0, pady = (0,20))
        #Adding Frame for these two buttons to make it look good
        OtherButtonsFrame = CTkFrame(self.LoginFrame, corner_radius= 10, fg_color="transparent")
        OtherButtonsFrame.grid_rowconfigure(0, weight = 1)
        OtherButtonsFrame.grid_columnconfigure((0,1), weight = 1)
        OtherButtonsFrame.grid(row = 7, column = 0,pady = (20,0))
        #Buttons that help the user if they forget their password or if they want to go to the sign up page without needing to go to the sidebar.
        ForgottenPasswordsButton = CTkButton(OtherButtonsFrame, text = "Forgotten password", height = 40, width = 160, corner_radius= 30, command= lambda:self.LoadingFrame(self.AskingForEmailToChangePasswordFrame())).grid(row = 0, column = 0,padx = (20, 80))
        RegisterButton = CTkButton(OtherButtonsFrame, text = "Register", height = 40, width = 160, corner_radius= 30, command = lambda:self.LoadingFrame(self.SigningUpPage())).grid(row = 0, column = 1, padx = (90, 30))
        return self.LoginFrame
        
    
    #Checks if the email exists and if it does then it will chekck if the password inputted matches the one
    #in the database and if it does it moves onto the 2 factor authentication system
    def CheckingValidityOfAccount(self,EmailInputted,PasswordInputted):
        InputtedPasswordButEncrypted = HashingAValue(PasswordInputted)
        self.cursor.execute(f"SELECT Password FROM UserTable WHERE Email = '{EmailInputted}'")
        ActualPassword = self.cursor.fetchone()
        if ActualPassword == None:
            self.LoadingFrame(self.LoginPage())
            InfoLabel = CTkLabel(self.LoginFrame, text = "Account doesn't exist. \n\n Try signing up first!",font = CTkFont(size = 20, weight = "bold")).grid(row = 9, column = 0)
        else:
            if ActualPassword[0] == InputtedPasswordButEncrypted:
                self.TwoStepverificationFunction(EmailInputted)
            else:
                self.LoadingFrame(self.LoginPage())
                InfoLabel = CTkLabel(self.LoginFrame, text = "Password is incorrect",font = CTkFont(size = 20, weight = "bold")).grid(row = 9, column = 0)
    
    #A function that loads the frame that takes the code and also calls a function to generate the code and send the code to the email of the user
    def TwoStepverificationFunction(self, Email):
        self.LoadingFrame(self.TwoStepVerificationFrame(Email,1))
        self.GeneratingCodeForTwoStep(Email)
    
    #When the password is correct and a user gets the 2fa correct, they become logged in
    #This function creates an object from the class User and this value will contain only the necessary data such as email
    #user Id and username and the gives it to the freelancer page class so that they can use it so that they can fetch orders data and milestone
    #data based on who has logged in. No need for passwords due to obvious reasons 
    def FinishedLogIn(self,Email):
        self.cursor.execute(f"SELECT UserID,Email,FullName FROM UserTable WHERE Email = '{Email}'")
        RecordOfUser = self.cursor.fetchone()
        UserLoggedIn = User(RecordOfUser[0],RecordOfUser[1],RecordOfUser[2])
        self.ForgettingFrames()
        self.SideBarFrame.grid_forget()
        FreelancerObject = FreelancerPage(root, UserLoggedIn)
    
    #Start of forgotten passwords 
    
    #This asks for the email of the account that the user has forgotten the password for
    def AskingForEmailToChangePasswordFrame(self) -> CTkFrame:
        self.AskingForEmailFrame.grid_columnconfigure((0,2), weight = 1)
        self.AskingForEmailFrame.grid_columnconfigure((1), weight = 2)
        self.AskingForEmailFrame.grid_rowconfigure((0,5), weight = 1)
        self.DeletingWidgetsOnFrame(self.AskingForEmailFrame)
        EmailInputted = StringVar()
        ForgottenPasswordLabel = CTkLabel(self.AskingForEmailFrame,text = "Changing Password",font = CTkFont(size = 50, weight = "bold")).grid(row = 0, column = 1)
        EmailLabel = CTkLabel(self.AskingForEmailFrame, text = "Email: ",font = CTkFont(size = 15)).grid(row = 2, column = 1, padx = (0, 250), pady = 10)
        CTkEntry(self.AskingForEmailFrame, textvariable=EmailInputted,width = 300, font = CTkFont(size= 15), corner_radius= 30, height = 40).grid(row = 3, column = 1)
        ContinueButton = CTkButton(self.AskingForEmailFrame, text = "Continue", height = 40, width = 160, corner_radius= 30, command = lambda:self.CheckingIfEmailExistsInDatabase(EmailInputted.get())).grid(row = 4, column = 1,pady = (30,0))
        return self.AskingForEmailFrame
    
    #Checks email exists before doing anything if it doens't then the sign up page is loaded and stating that a email is non existant
    def CheckingIfEmailExistsInDatabase(self,Email):
        self.cursor.execute(f"SELECT UserId FROM UserTable WHERE Email = '{Email}'")
        UserId = self.cursor.fetchone()
        print(UserId)
        if UserId == None:
            self.LoadingFrame(self.SigningUpPage())
            InfoLabel = CTkLabel(self.SignUpPageFrame, text = "Email does not exist try make an account first ", font = CTkFont(size = 20)).grid(row = 10, column = 0)
        else:
            self.ChangingForgottenPasswordsFunction(Email)
            
    def ChangingForgottenPasswordsFunction(self, Email):
        self.LoadingFrame(self.TwoStepVerificationFrame(Email, 0))
        self.GeneratingCodeForTwoStep(Email)
    
    
    #This function generates a random code first and changes the code attribute and then sends an email to that email account with the code
    #If the user inputs the correct code then the user will be taken to another frame which allows them to change their password
    def GeneratingCodeForTwoStep(self,Email):
        RandomCode = random.randint(30000, 99999)
        self.RandomCode = RandomCode
        print(self.RandomCode)
        Subject = "This email contains the code"
        Content = f"Your random code is {self.RandomCode}"
        self.SendingEmailsObject.SendingActualEmail(Subject, Content, Email)
    
    #Asks for the new password twice as you need to "confirm" you password by typing it twice
    def AskingForPassword(self,Email):
        self.ChangingPasswordsFrame.grid_columnconfigure((0,2), weight = 1)
        self.ChangingPasswordsFrame.grid_columnconfigure((1), weight = 2)
        self.ChangingPasswordsFrame.grid_rowconfigure((0,6), weight = 1)
        self.DeletingWidgetsOnFrame(self.ChangingPasswordsFrame)
        FirstPasswordInputted = StringVar()
        SecondPasswordInputted = StringVar()
        Title = CTkLabel(self.ChangingPasswordsFrame, text = "Changing password",font = CTkFont(size = 50, weight = "bold")).grid(row = 0, column = 1)
        NewPasswordLabel = CTkLabel(self.ChangingPasswordsFrame, text = "New Password:",font = CTkFont(size = 15)).grid(row = 1, column = 1,padx = (0,200))
        CTkEntry(self.ChangingPasswordsFrame, textvariable=FirstPasswordInputted,width = 300, font = CTkFont(size= 15), show = "*", corner_radius= 30, height = 40).grid(row = 2, column = 1,pady = 10)
        ConfirmPassword = CTkLabel(self.ChangingPasswordsFrame, text = "Confirm Password:",font = CTkFont(size = 15)).grid(row = 3, column = 1,padx = (0,185))
        CTkEntry(self.ChangingPasswordsFrame, textvariable=SecondPasswordInputted,width = 300, font = CTkFont(size= 15), show = "*", corner_radius= 30, height = 40).grid(row = 4, column = 1,pady = 10)
        ChangePasswordButton = CTkButton(self.ChangingPasswordsFrame, text = "Change", height = 40, width = 160, corner_radius= 30, command = lambda:self.ChangingPasswordInDatabase(Email, FirstPasswordInputted.get(), SecondPasswordInputted.get())).grid(row = 5, column = 1,pady = 15)
        return self.ChangingPasswordsFrame
    
    #function that modifies the password 
    def ChangingPasswordInDatabase(self,Email,NewPassword,ConfirmationPassword):
        if len(ConfirmationPassword) < 10:
            self.LoadingFrame(self.AskingForPassword(Email))
            InfoLabel = CTkLabel(self.ChangingPasswordsFrame, text = "Password has to be larger than 10 chraracters",font = CTkFont(size = 20)).grid(row = 6, column = 1)
        elif NewPassword == ConfirmationPassword:
            HashedPassword = HashingAValue(ConfirmationPassword)
            self.cursor.execute(f'''
                                UPDATE UserTable SET Password = '{HashedPassword}' WHERE Email = '{Email}'
                                
                                ''')
            self.db.commit()
            self.LoadingFrame(self.LoginPage())
            InfoLabel = CTkLabel(self.LoginFrame, text = "You have successfully changed your password", font = CTkFont(size = 20)).grid(row = 9, column = 0)
        else:
            self.LoadingFrame(self.AskingForPassword(Email))
            InfoLabel = CTkLabel(self.ChangingPasswordsFrame, text = "Passwords do not match",font = CTkFont(size = 20)).grid(row = 6, column = 1)
    
    #type 1 is for logging in and type 0 is for forgotten passwords as this function is needed for two things and making two seperate function is unnecessary so stating which type it is allows me to 
    #Give the user the change password frame or logging them into the freelancer page
    def TwoStepVerificationFrame(self,Email,type):
        InputtedCode = IntVar()
        #Making a entry box with label and button and allowing a user to submit a value 
        self.DeletingWidgetsOnFrame(self.TwoFactorFrame)
        TitleLabel = CTkLabel(self.TwoFactorFrame, text = "Two factor authentication", font = CTkFont(size = 50, weight = "bold")).place(relx = 0.5, rely = 0.2, anchor = CENTER)
        CodeLabel = CTkLabel(self.TwoFactorFrame, text = "Code:",font = CTkFont(size= 15), corner_radius= 30).place(relx = 0.40, rely = 0.45, anchor=CENTER)
        CTkEntry(self.TwoFactorFrame,textvariable=InputtedCode,width = 300, font = CTkFont(size= 15), corner_radius= 30, height = 40 ).place(relx = 0.5,rely = 0.5,anchor=CENTER)
        ExplanationLabel = CTkLabel(self.TwoFactorFrame, text = f"An email should have been sent with the code to {Email}. \n The email used to send the code is called 'ComputingProjectAlerts@outlook.com'. \n The email may be in your junk/spam mail.", font = CTkFont(size=20))
        ExplanationLabel.place(relx = 0.5, rely = 0.7, anchor = CENTER)
        SubmitButton = CTkButton(self.TwoFactorFrame, text = "Submit", height = 40, width = 160, corner_radius= 30, command = lambda:self.CheckingCode(InputtedCode.get(),Email, type)).place(relx = 0.5, rely = 0.57, anchor = CENTER)
        return self.TwoFactorFrame
    
    #type 1 is for logging in and type 0 is for forgotten password
    def CheckingCode(self, InputtedCode,Email,type):
        if InputtedCode == self.RandomCode and type == 1:
            self.FinishedLogIn(Email)
        elif InputtedCode != self.RandomCode and type == 1:
            self.TwoStepverificationFunction(Email)
            InfoLabel = CTkLabel(self.TwoFactorFrame, text = "Incorrect code try again \n \n A new code has been sent", font = CTkFont(size = 20)).place(relx = 0.5, rely = 0.9, anchor = CENTER)
        elif InputtedCode == self.RandomCode and type == 0:
            print("Should be changing password")
            self.LoadingFrame(self.AskingForPassword(Email))
        elif InputtedCode != self.RandomCode and type == 0:
            self.ChangingForgottenPasswordsFunction(Email)
            InfoLabel = CTkLabel(self.TwoFactorFrame, text = "Incorrect code try again \n \n A new code has been sent", font = CTkFont(size = 20)).place(relx = 0.5, rely = 0.9, anchor = CENTER)

    #End of forgotten passwords   
        
    #Functions for laoding frames, forgetting frames and deleting widgets off frames
        
    #Removes widgets from current frame which helps when switching between frames. If this wasn;t made the frames data will repeat for example
    #If I pressed the log in button twice I would have two username input boxes as well s 2 passsword input boxes which isn't good
    def DeletingWidgetsOnFrame(self,frameGiven: CTkFrame):
        for widget in frameGiven.winfo_children():
            widget.destroy()
    
    #removes the frame we are currently on hence the name forgetting frame and then loads the new one which is what the loading frame function does
    def ForgettingFrames(self):
        self.LoginFrame.grid_forget()
        self.SignUpPageFrame.grid_forget()
        self.TwoFactorFrame.grid_forget()
        self.ChangingPasswordsFrame.grid_forget()
        self.AskingForEmailFrame.grid_forget()
    
    #Forgets frae you are currently on and loads the frame that was passed through
    def LoadingFrame(self,frame : CTkFrame):
        self.ForgettingFrames()
        frame.grid(row = 0, column = 1, sticky = 'nsew')
    

    #Changing appearance
    def Changing_Appearance_Mode(self):
        customtkinter.set_appearance_mode(self.AppearanceMode.get())
        
Start = StartingPage()
root.mainloop()

        


        