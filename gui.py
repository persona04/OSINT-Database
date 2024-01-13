import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

COLOR_0 = "#353941"
COLOR_1 = "#26282B"
COLOR_2 = "#5F85DB"
COLOR_3 = "#90B8F8"
from PIL import ImageTk, Image
import mysqlfunc

privilege = None

class LoginPage():
    
    def __init__(self,window,screen_size):
        
        #For passing values to QueryPanel
        self.window = window
        self.screen_size = screen_size
        
        # login page frame
        self.login_frame = ctk.CTkFrame(master=window,fg_color=COLOR_1,width=screen_size[0],height=screen_size[1])
        self.login_frame.place(x=0,y=0)
        
        # Login panel frame
        self.center_frame = ctk.CTkFrame(master=self.login_frame,fg_color=COLOR_0,width=screen_size[0]/3,height=screen_size[1],corner_radius=10)
        self.center_frame.place(relx=0.5,rely=0.5, anchor= tk.CENTER)
        

        # Entry field for username and password
        self.password_entry = ctk.CTkEntry(master=self.center_frame,height=screen_size[1]/22,width=screen_size[0]/9*2,placeholder_text="Password...",show="*",font=("SEE-go",15,"bold",))
        self.password_entry.place(relx=0.5,rely=0.6, anchor=tk.CENTER)
        self.username_entry = ctk.CTkEntry(master=self.center_frame,height=screen_size[1]/22,width=screen_size[0]/9*2,placeholder_text="Username...",font=("SEE-go",15,"bold",))
        self.username_entry.place(relx=0.5,rely=0.53, anchor = tk.CENTER)

        # Login button
        self.login_button = ctk.CTkButton(master=self.center_frame,text="Login",command= lambda:LoginPage.auth(self,self.password_entry,self.username_entry),width=screen_size[0]/9*2,height=screen_size[1]/22)
        self.login_button.place(relx=0.5,rely=0.67, anchor= tk.CENTER)

        # Register button
        self.register_button = ctk.CTkButton(master=self.center_frame,text="Register",command=lambda: self.register_func(self.username_entry,self.password_entry),width=screen_size[0]/9*2,height=screen_size[1]/22)
        self.register_button.place(relx=0.5, rely=0.74,anchor=tk.CENTER)

        # Message
        self.err_msg = ctk.CTkLabel(master=self.center_frame,text="",width=screen_size[0]/9*2,height=screen_size[1]/22)
        self.err_msg.place(relx=0.5,rely=0.81,anchor=tk.CENTER)
        
        # Logo
        self.img = ImageTk.PhotoImage(Image.open("logo.png"))
        self.logo_label = ctk.CTkLabel(master=self.center_frame, image=self.img, text="",width=500,height=500,corner_radius=300,bg_color=COLOR_0)
        self.logo_label.place(relx=0.5,rely=0.27, anchor= tk.CENTER)

    def auth(self,password_entry,username_entry):
        # Get strings from entry fields
        self.passwd = password_entry.get()
        self.username = username_entry.get()
        
        # Using authentication method and handling feedback.
        self.sql = mysqlfunc.MySQLConnect()
        self.result = self.sql.login_authentication(self.username,self.passwd)
        if self.result[0] == 200:
            global privilege 
            privilege = self.result[1]
            QueryPanel(self.window,self.screen_size)
            self.drop_page()
        elif self.result[0] == 401:
            self.err_msg.configure(text="Invalid credentials!")
        elif self.result[0] == 500:
            self.err_msg.configure(text="Server connection problem...")
    
    # For delete the page.
    def drop_page(self):
        for self.i in self.login_frame.winfo_children():
            self.i.destroy()

    def register_func(self,username,password):
        self.passwd = password.get()
        self.user = username.get()
        self.res = mysqlfunc.MySQLConnect().register_query(self.user,self.passwd)
        self.err_msg.configure(text="Registered!")

#iamhere
class QueryPanel():
    def __init__(self,window,screen_size):
        
        # For passing the other page.
        self.window = window
        self.screen_size = screen_size
        
        # Query panel frame
        self.query_frame = ctk.CTkFrame(master=window,fg_color=COLOR_1,width=screen_size[0],height=screen_size[1])
        self.query_frame.place(x=0,y=0)

        # Tabs for diffrent query types.
        self.tabview = ctk.CTkTabview(master=self.query_frame,fg_color=COLOR_0,width=screen_size[0]-70,height=screen_size[1]-160,corner_radius=20)
        self.tabview.place(relx=0.5,rely=0.5, anchor = tk.CENTER)
        self.tab_1 = self.tabview.add("Search by person".center(30))
        self.tab_2 = self.tabview.add("Search account".center(30))
        self.tab_3 = self.tabview.add("Search address".center(30))
        self.tab_4 = self.tabview.add("Search phone number".center(30))

        # Logout button.
        self.logout_button = ctk.CTkButton(master=self.query_frame,corner_radius=10,width=180,height=35,text="Logout",font=("SEE-go",15,"normal",),command=self.logout)
        self.logout_button.place(x=screen_size[0]/2-125,y=35, anchor = tk.CENTER)

        # Edit button. 
        self.edit_button = ctk.CTkButton(master=self.query_frame,corner_radius=10,width=180,height=35,text="Edit Page",font=("SEE-go",15,"normal"),command=lambda:self.editPage())
        self.edit_button.place(x=screen_size[0]/2+125,y=35, anchor = tk.CENTER)

        # Frames for tabs. When we want to delete table for new one, we can destroy all childs of frame in loop. 
        
        self.tab_1_frame = ctk.CTkFrame(master=self.tab_1,width=1700,height=630,corner_radius=20)
        self.tab_1_frame.place(x=50, y=200)

        self.tab_2_frame = ctk.CTkFrame(master=self.tab_2,width=1700,height=630,corner_radius=20)
        self.tab_2_frame.place(x=50, y=200)

        self.tab_3_frame = ctk.CTkFrame(master=self.tab_3,width=1700,height=630,corner_radius=20)
        self.tab_3_frame.place(x=50,y=200)

        self.tab_4_frame = ctk.CTkFrame(master=self.tab_4,width=1700,height=630,corner_radius=20)
        self.tab_4_frame.place(x=50,y=200)

        # Persons tab

        self.tab_1_button1 = ctk.CTkButton(master= self.tab_1,width=200,height=50,corner_radius=10,text="List Persons",command=lambda: self.table_for_persons())
        self.tab_1_button1.place(relx=0.58, rely=0.05, anchor=tk.CENTER)
        self.tab_1_button2 = ctk.CTkButton(master=self.tab_1, width=200,height=50,corner_radius=10,text="Search",command=lambda:self.table_for_persons(False))
        self.tab_1_button2.place(relx=0.58, rely=0.15,anchor=tk.CENTER)
        self.tab_1_entry1 = ctk.CTkEntry(master=self.tab_1,width=300,height=50,placeholder_text="Name + Surname...")
        self.tab_1_entry1.place(relx=0.43,rely=0.05, anchor=tk.CENTER)
        self.tab_1_entry2 = ctk.CTkEntry(master=self.tab_1,width=300,height=50,placeholder_text="Enter ID...")
        self.tab_1_entry2.place(relx=0.43,rely=0.15, anchor=tk.CENTER)
        self.tab_1_combobox = ctk.CTkComboBox(master=self.tab_1,corner_radius=10,state="readonly",values=("Email","Credential","Account","Address","Notes","Phone Numbers"))
        self.tab_1_combobox.place(relx=0.3, rely=0.15, anchor=tk.CENTER)

        # Address Tab

        self.tab_3_button = ctk.CTkButton(master=self.tab_3,width=300,height=50,corner_radius=10,text="Search", command= lambda: self.table_for_address())
        self.tab_3_button.place(relx=0.5,rely=0.15, anchor= tk.CENTER)
        self.tab_3_entry = ctk.CTkEntry(master=self.tab_3,width=500,height=50,placeholder_text="Enter a address...")
        self.tab_3_entry.place(relx=0.5,rely=0.05, anchor=tk.CENTER)

        # Phone numbers tab

        self.tab_4_button = ctk.CTkButton(master=self.tab_4,width=300,height=50,corner_radius=10,text="Search",command= lambda:self.table_for_phone_number())
        self.tab_4_button.place(relx=0.5,rely=0.15, anchor= tk.CENTER)
        self.tab_4_entry = ctk.CTkEntry(master=self.tab_4,width=500,height=50,placeholder_text="Enter a phone number...")
        self.tab_4_entry.place(relx=0.5,rely=0.05, anchor=tk.CENTER)
        
        # Accounts tab
        self.tab_2_button = ctk.CTkButton(master=self.tab_2,width=300,height=50,corner_radius=10,text="Search",command= lambda:self.table_for_accounts())
        self.tab_2_button.place(relx=0.5,rely=0.15, anchor= tk.CENTER)
        self.tab_2_entry = ctk.CTkEntry(master=self.tab_2,width=500,height=50,placeholder_text="Select a search method...")
        self.tab_2_entry.place(relx=0.5,rely=0.05, anchor=tk.CENTER)
        self.tab_2_combobox = ctk.CTkComboBox(master=self.tab_2,corner_radius=20,values=("email","username","site"),state="readonly",command=self.set_mode )
        self.tab_2_combobox.place(relx=0.3,rely=0.05, anchor=tk.CENTER)
        
        # Stylig treeview
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview",background=COLOR_0,fieldbackground=COLOR_0,font=('Ariel',12),foreground="white")
        self.style.configure("Treeview.Heading",backgorund="gray",fieldbackground=COLOR_0,font=('Ariel',13))

        # error message for edit page
        self.err_msg = ctk.CTkLabel(master=self.query_frame,text="")
        self.err_msg.place(x=screen_size[0]/2+300,y=35, anchor = tk.CENTER)
    
    # Logout method.
    def logout(self):
        LoginPage(self.window,self.screen_size)
        for e in self.query_frame.winfo_children():
            e.destroy()


    def table_for_address(self):
        self.query = self.tab_3_entry.get()
        self.query = "%"+self.query+"%"
        self.sql = mysqlfunc.MySQLConnect()
        self.results = self.sql.address_table_query(self.query)
        for self.i in self.tab_3_frame.winfo_children():
            self.i.destroy()
        columns = ["person_id","p_name","p_surname","dsc","address","evidence_id"]
        self.tab_3_table = ttk.Treeview(master=self.tab_3_frame,show="headings",columns=columns, height=27)
        self.tab_3_table.heading("person_id",text="Person ID",anchor=tk.CENTER)
        self.tab_3_table.heading("p_name",text="Name", anchor=tk.CENTER)
        self.tab_3_table.heading("p_surname",text="Surname")
        self.tab_3_table.heading("dsc",text="Description")
        self.tab_3_table.heading("address",text="Address")
        self.tab_3_table.heading("evidence_id",text="Evidence ID")
        self.tab_3_table.column(column="person_id",width=100,anchor=tk.CENTER)
        self.tab_3_table.column(column="p_name",width=150,anchor=tk.CENTER)
        self.tab_3_table.column(column="p_surname",width=150,anchor=tk.CENTER)
        self.tab_3_table.column(column="dsc",anchor=tk.CENTER)
        self.tab_3_table.column(column="address",width=300,anchor=tk.CENTER)
        self.tab_3_table.column(column="evidence_id",width=150,anchor=tk.CENTER)

        if self.results==500:
            self.err_label = ctk.CTkLabel(master=self.tab_3_frame,text="Connection problem...",fg_color="red")
            self.err_label.place(relx=0.5,rely=0.5, anchor= tk.CENTER)
        else:
            for self.i in self.results:
                self.tab_3_table.insert("",tk.END,values=self.i)
            self.tab_3_table.place(relx=0.5,rely=0.5, anchor=tk.CENTER)

    def table_for_phone_number(self):
        self.number = self.tab_4_entry.get()
        self.number = self.number.replace(" ","")
        self.number = self.number.split("+")
        self.sql = mysqlfunc.MySQLConnect()
        self.results = self.sql.phone_number_table_query(self.number)
        for self.i in self.tab_4_frame.winfo_children():
            self.i.destroy()
        self.columns = ["person_id","p_name","p_surname","dsc","phone_number","evidence_id"]
        self.tab_4_table = ttk.Treeview(master=self.tab_4_frame,show="headings",columns=self.columns, height=27)
        self.tab_4_table.heading("person_id",text="Person ID",anchor=tk.CENTER)
        self.tab_4_table.heading("p_name",text="Name", anchor=tk.CENTER)
        self.tab_4_table.heading("p_surname",text="Surname")
        self.tab_4_table.heading("dsc",text="Description")
        self.tab_4_table.heading("phone_number",text="Phone Number")
        self.tab_4_table.heading("evidence_id",text="Evidence ID")
        self.tab_4_table.column(column="person_id",width=100,anchor=tk.CENTER)
        self.tab_4_table.column(column="p_name",width=150,anchor=tk.CENTER)
        self.tab_4_table.column(column="p_surname",width=150,anchor=tk.CENTER)
        self.tab_4_table.column(column="dsc",anchor=tk.CENTER)
        self.tab_4_table.column(column="phone_number",width=300,anchor=tk.CENTER)
        self.tab_4_table.column(column="evidence_id",width=150,anchor=tk.CENTER)

        if self.results==500:
            self.err_label = ctk.CTkLabel(master=self.tab_4_frame,text="Connection problem...",fg_color="red")
            self.err_label.place(relx=0.5,rely=0.5, anchor= tk.CENTER)
        else:
            for self.i in self.results:
                self.tab_4_table.insert("",tk.END,values=self.i)
            self.tab_4_table.place(relx=0.5,rely=0.5, anchor=tk.CENTER)
    
    def set_mode(self,mode):
        self.mode_flag = mode
        self.text = f"Enter a {mode}..."
        self.tab_2_entry.configure(placeholder_text=self.text)
    
    def table_for_accounts(self):
        self.input = self.tab_2_entry.get()
        self.sql = mysqlfunc.MySQLConnect()
        self.results = self.sql.account_table_query(self.input,self.tab_2_combobox.get())
        
        for self.i in self.tab_2_frame.winfo_children():
            self.i.destroy()

        self.columns = ["person_id","dsc","mail_address","username","evidence_id"]
        self.tab_2_table = ttk.Treeview(master=self.tab_2_frame,show="headings",columns=self.columns, height=27)
        self.tab_2_table.heading("person_id",text="Person ID")
        self.tab_2_table.heading("dsc",text="Description")
        self.tab_2_table.heading("mail_address",text="Mail Address")
        self.tab_2_table.heading("username",text="Username")
        self.tab_2_table.heading("evidence_id",text="Evidence ID")
        self.tab_2_table.column(column="person_id",width=100,anchor=tk.CENTER)
        self.tab_2_table.column(column="dsc",width=300,anchor=tk.CENTER)
        self.tab_2_table.column(column="mail_address",width=300,anchor=tk.CENTER)
        self.tab_2_table.column(column="username",width=150,anchor=tk.CENTER)
        self.tab_2_table.column(column="evidence_id",width=150,anchor=tk.CENTER)

        for accounts in self.results:
            self.tab_2_table.insert("",tk.END,values=accounts)
        self.tab_2_table.place(relx=0.5,rely=0.5, anchor=tk.CENTER)

    def table_for_persons(self,plist:bool=True):
        

        for child in self.tab_1_frame.winfo_children():
            child.destroy()
        
        if  plist:
            self.info = self.tab_1_entry1.get()
            self.result = mysqlfunc.MySQLConnect.person_table_query(self,self.info,"list")
            self.columns = ["person_id","p_name","p_surname","p_birthdate"]
            self.tab_1_table = ttk.Treeview(master=self.tab_1_frame,show="headings",columns=self.columns, height=27)
            self.tab_1_table.heading("person_id",text="ID")
            self.tab_1_table.heading("p_name",text="Name")
            self.tab_1_table.heading("p_surname",text="Surname")
            self.tab_1_table.heading("p_birthdate",text="Birthdate")

            for person in self.result:
                self.tab_1_table.insert("",tk.END,values=person)
            self.tab_1_table.place(relx=0.5,rely=0.5,anchor=tk.CENTER)

        else:
            self.info = self.tab_1_entry2.get()
            self.flag = self.tab_1_combobox.get()
            self.result = mysqlfunc.MySQLConnect.person_table_query(self,self.info,self.flag)
            if self.flag == "Email":
                self.columns = ["dsc","mail_address","evidence_id"]
                self.tab_1_table = ttk.Treeview(master=self.tab_1_frame,show="headings",columns=self.columns, height=27)
                self.tab_1_table.heading("dsc",text="Description")
                self.tab_1_table.heading("mail_address",text="Mail Address")
                self.tab_1_table.heading("evidence_id",text="Evidence ID")
                for person in self.result:
                    self.tab_1_table.insert("",tk.END,values=person)
                self.tab_1_table.place(relx=0.5,rely=0.5,anchor=tk.CENTER)

            elif self.flag =="Credential":
                self.columns=["username","passwd","evidence_id"]
                self.tab_1_table = ttk.Treeview(master=self.tab_1_frame,show="headings",columns=self.columns, height=27)
                self.tab_1_table.heading("username",text="Username")
                self.tab_1_table.heading("passwd",text="Password")
                self.tab_1_table.heading("evidence_id",text="Evidence ID")
                for person in self.result:
                    self.tab_1_table.insert("",tk.END,values=person)
                self.tab_1_table.place(relx=0.5,rely=0.5,anchor=tk.CENTER)

            elif self.flag == "Account":
                self.columns=["dsc","mail_address","username","evidence_id"]
                self.tab_1_table = ttk.Treeview(master=self.tab_1_frame,show="headings",columns=self.columns, height=27)
                self.tab_1_table.heading("dsc",text="Description")
                self.tab_1_table.heading("username",text="Username")
                self.tab_1_table.heading("mail_address",text="Mail Adress")
                self.tab_1_table.heading("evidence_id",text="Evidence ID")
                for person in self.result:
                    self.tab_1_table.insert("",tk.END,values=person)
                self.tab_1_table.place(relx=0.5,rely=0.5,anchor=tk.CENTER)

            elif self.flag == "Address":
                self.columns = ["dsc","address","evidence_id"]
                self.tab_1_table = ttk.Treeview(master=self.tab_1_frame,show="headings",columns=self.columns, height=27)
                self.tab_1_table.heading("dsc",text="Description")
                self.tab_1_table.heading("address",text="address")
                self.tab_1_table.heading("evidence_id",text="Evidence ID")
                for person in self.result:
                    self.tab_1_table.insert("",tk.END,values=person)
                self.tab_1_table.place(relx=0.5,rely=0.5,anchor=tk.CENTER)

            elif self.flag == "Notes":
                self.columns=["note","evidence_id"]
                self.tab_1_table = ttk.Treeview(master=self.tab_1_frame,show="headings",columns=self.columns, height=27)
                self.tab_1_table.heading("note",text="Note")
                self.tab_1_table.heading("evidence_id",text="Evidence ID")
                for person in self.result:
                    self.tab_1_table.insert("",tk.END,values=person)
                self.tab_1_table.place(relx=0.5,rely=0.5,anchor=tk.CENTER)


            elif self.flag == "Phone Numbers":
                self.columns=["dsc","phone_number","evidence_id"]
                self.tab_1_table = ttk.Treeview(master=self.tab_1_frame,show="headings",columns=self.columns, height=27)
                self.tab_1_table.heading("dsc",text="Description")
                self.tab_1_table.heading("phone_number",text="Phone Number")
                self.tab_1_table.heading("evidence_id",text="Evidence ID")
                for person in self.result:
                    self.tab_1_table.insert("",tk.END,values=person)
                self.tab_1_table.place(relx=0.5,rely=0.5,anchor=tk.CENTER)

    def editPage(self):
        if privilege == 1:
            self.drop_page()
        else:
            self.err_msg.configure(text="NOT PRIVILEGED!")
    
    def drop_page(self):
        for child in self.query_frame.winfo_children():
            child.destroy()
        EditPanel(self.window,self.screen_size)

class EditPanel():
    def __init__(self,window,screen_size):
        self.window = window
        self.screen_size = screen_size

        self.edit_frame = ctk.CTkFrame(master=self.window,fg_color=COLOR_1,width=screen_size[0],height=screen_size[1])
        self.edit_frame.place(x=0,y=0)

        self.tabview = ctk.CTkTabview(master=self.edit_frame,fg_color=COLOR_0,width=screen_size[0]-70,height=screen_size[1]-160,corner_radius=20)
        self.tabview.place(relx=0.5,rely=0.5, anchor = tk.CENTER)
        self.tab_1 = self.tabview.add("Add Record".center(30))
        self.tab_2 = self.tabview.add("Delete Record".center(30))
        self.tab_3 = self.tabview.add("Update Record".center(30))

         # Logout button.
        self.logout_button = ctk.CTkButton(master=self.edit_frame,corner_radius=10,width=180,height=35,text="Logout",font=("SEE-go",15,"normal",),command=self.logout)
        self.logout_button.place(x=screen_size[0]/2-125,y=35, anchor = tk.CENTER)

        # Edit button. 
        self.search_page_button = ctk.CTkButton(master=self.edit_frame,corner_radius=10,width=180,height=35,text="Search Page",font=("SEE-go",15,"normal"),command=lambda:self.search_page())
        self.search_page_button.place(x=screen_size[0]/2+125,y=35, anchor = tk.CENTER)

        
        self.tab_1_frame = ctk.CTkFrame(master=self.tab_1,width=1700,height=630,corner_radius=20)
        self.tab_1_frame.place(x=50, y=200)

        self.tab_2_frame = ctk.CTkFrame(master=self.tab_2,width=1700,height=630,corner_radius=20)
        self.tab_2_frame.place(x=50, y=200)

        self.tab_3_frame = ctk.CTkFrame(master=self.tab_3,width=1700,height=630,corner_radius=20)
        self.tab_3_frame.place(x=50,y=200)

        # Add Record Tab
        
        self.tab_1_button = ctk.CTkButton(master=self.tab_1,width=300,height=50,text="Add",command=lambda:self.insert_func())
        self.tab_1_combobox = ctk.CTkComboBox(master=self.tab_1,corner_radius=10,state="readonly",values=("Email","Credential","Account","Address","Note","Phone Number"),command=self.set_entries)
        self.tab_1_button.place(relx=0.5,rely=0.15,anchor=tk.CENTER)
        self.tab_1_combobox.place(relx=0.5,rely=0.05,anchor=tk.CENTER)

        self.entry_1 = ctk.CTkEntry(master=self.tab_1_frame,width=300,height=50)
        self.entry_1.place(relx=0.35,rely=0.2,anchor=tk.CENTER)
        self.entry_2 = ctk.CTkEntry(master=self.tab_1_frame,width=300,height=50)
        self.entry_2.place(relx=0.35,rely=0.35,anchor=tk.CENTER) 
        self.entry_3 = ctk.CTkEntry(master=self.tab_1_frame,width=300,height=50)
        self.entry_3.place(relx=0.35,rely=0.5,anchor=tk.CENTER)
        self.entry_4 = ctk.CTkEntry(master=self.tab_1_frame,width=300,height=50)
        self.entry_4.place(relx=0.35,rely=0.65,anchor=tk.CENTER)
        self.time_entry= ctk.CTkEntry(master=self.tab_1_frame,width=300,height=50,placeholder_text="Date...")
        self.time_entry.place(relx=0.65,rely=0.2,anchor=tk.CENTER)
        self.source_entry = ctk.CTkEntry(master=self.tab_1_frame,width=300,height=50,placeholder_text="Source...")
        self.source_entry.place(relx=0.65,rely=0.35,anchor=tk.CENTER)
        self.score_entry = ctk.CTkEntry(master=self.tab_1_frame,width=300,height=50,placeholder_text="Reliability Score...")
        self.score_entry.place(relx=0.65,rely=0.5,anchor=tk.CENTER)
        print(type(self.entry_1.get()))

    def drop_page(self):
        for child in self.edit_frame.winfo_children():
            child.destroy()
        
    def search_page(self):
        QueryPanel(self.window,self.screen_size)
        self.drop_page()
    
    def logout(self):
        LoginPage(self.window,self.screen_size)
        self.drop_page()

    def set_entries(self,x):
        self.x = x
        self.e4 = ""
        self.e3 = ""
        
        if self.x == "Email":
            self.e1 = "Person ID..."
            self.e2 = "Description..."
            self.e3 = "Email address..."
        
        elif self.x == "Account":
            self.e1 = "Person ID..."
            self.e2 = "Description..."
            self.e3 = "Email ID..."
            self.e4 = "Credential ID..."
        
        elif self.x == "Credential":
            self.e1 = "Person ID..."
            self.e2 = "Username..."
            self.e3 = "Password..."
        
        elif self.x == "Address":
            self.e1 = "Person ID..."
            self.e2 = "Description..."
            self.e3 = "Address..."
        
        elif self.x == "Note":
            self.e1 = "Person ID..."
            self.e2 = "Note..."
        
        elif self.x == "Phone Number":
            self.e1 = "Person ID..."
            self.e2 = "Description..."
            self.e3 = "Phone Number..."

        self.entry_1.configure(placeholder_text=self.e1)
        self.entry_2.configure(placeholder_text=self.e2)
        self.entry_3.configure(placeholder_text=self.e3)
        self.entry_4.configure(placeholder_text=self.e4)

    def insert_func(self):
        self.qtype = self.tab_1_combobox.get()
        self.arg1 = self.entry_1.get()
        self.arg2 = self.entry_2.get()
        self.arg3 = self.entry_3.get()
        self.arg4 = self.entry_4.get()
        self.ev1 = self.time_entry.get()
        self.ev2 = self.source_entry.get()
        self.ev3 = self.score_entry.get()
        
        if self.qtype == "Note":
            self.args = (self.ev1,self.ev2,self.ev3,self.arg1,self.arg2)
        elif self.qtype == "Account":
            self.args = (self.ev1,self.ev2,self.ev3,self.arg1,self.arg2,self.arg3,self.arg4)
        else:
            self.args = (self.ev1,self.ev2,self.ev3,self.arg1,self.arg2,self.arg3)

        self.res = mysqlfunc.MySQLConnect.add_queries(self,self.qtype,self.args)
        