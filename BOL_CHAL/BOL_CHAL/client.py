# Importing usefull libraries
from tkinter import *
from tkinter import Tk
import tkinter as tk
from tkinter import Frame, filedialog, messagebox
import os
import socket
import customtkinter as ctk
from datetime import datetime
import threading
from PIL import ImageTk, Image
# Set appearance mode and color theme for customtkinter
ctk.set_appearance_mode("default")
ctk.set_default_color_theme("green")
# Define the path for images used in the application 
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

# Function to show the login window
def show_login_window():
    global login_window
    login_window = ctk.CTk()
    login_window.geometry("600x440")
    login_window.title('Login')

    def button_function():
        if entry1.get():
            login_window.destroy()  # Destroy the login window
            root = Tk()
            app = start_chat(root)   # Start the chat application
            receive_thread = threading.Thread(target=app.receive_sms, daemon=True)
            receive_thread.start()
            root.mainloop()  
    
    img1 = ctk.CTkImage(Image.open(os.path.join(image_path, "pattern.png")), size=(1500, 1920))
    l1 = ctk.CTkLabel(master=login_window, image=img1)
    l1.pack()

    frame = ctk.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    l2 = ctk.CTkLabel(master=frame, text="Enter your Name", font=('Century Gothic', 20))
    l2.place(x=50, y=45)

    entry1 = ctk.CTkEntry(master=frame, width=220, placeholder_text='Username')
    entry1.place(x=50, y=100)

    button1 = ctk.CTkButton(master=frame, width=220, text="Enter Chat", command=button_function, corner_radius=6)
    button1.place(x=50, y=150)

    login_window.mainloop()


# Function to start the chat application
class start_chat:
    def __init__(self, master):
        global user_entry
        global send_button
        global chat_frame
        global client_socket
 #==============Initializing communication==============
        

        # Create the GUI master
        # self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.host = socket.gethostname()
        # self.port = 12345
        # self.client = (self.host, self.port)
        self.filename = None
        master.title('Bol Chal')
        master.resizable(False, False)
        master.geometry('600x600')
        master.configure(bg='#34495e')  # Set the background color
        self.send_image = ctk.CTkImage(Image.open(os.path.join(image_path, "send.png")), size=(30, 30))
        self.file_image = ctk.CTkImage(Image.open(os.path.join(image_path, "file.png")), size=(30, 30))
        p1 = PhotoImage(file = 'icon.png') 
        master.iconphoto(False, p1)
        # Create the header text label
        self.header_text = ctk.CTkLabel(master,height=2, width=140, bg_color='green',  text='Bol Chal',font=('Impact', 30), fg_color='black',text_color='white')
        self.header_text.pack(side='top', fill='x')

        
        
        # Create the chat message frame with a vertical scrollbar
        self.chat_frame = ctk.CTkScrollableFrame(master, fg_color='white',bg_color="white" )  # Set the background color
        self.chat_frame.pack(side='top', fill='both', expand=True)

        

        # Create the entry frame and send button frame
        self.entry_frame = ctk.CTkFrame(master, height=60, width=500, bg_color='white',border_color='white',fg_color='white')  # Set the background color
        self.entry_frame.pack(side='left', fill='x')
        
        self.send_button_frame = ctk.CTkFrame(master, height=60, width=90, bg_color='white',fg_color='#ffffff' ,border_color="white",corner_radius=25)  # Set the background color
        self.send_button_frame.pack(side='left', fill='y')

        self.file_button_frame = ctk.CTkFrame(master, height=60, width=65, bg_color='black', border_color="white",corner_radius=25)  # Set the background color
        self.file_button_frame.pack(side='left', fill='y')

        

        # Create the user entry field
        self.user_entry = ctk.CTkEntry(self.entry_frame, width=450, bg_color='white', fg_color='black',text_color='white', font=('Helvetica', 14),corner_radius=27,border_width=3)  # Set the font size
        self.user_entry.pack(side='left', fill='both', expand=True, padx=5, pady=5)  # Add padding
        self.user_entry.insert(0, 'Enter message...')
        # user_entry.config(fg='#5c5a5a')
        self.user_entry.bind("<FocusIn>", lambda e: self.user_entry.delete(0, 'end'))
        self.user_entry.bind("<FocusOut>", lambda e: self.user_entry.insert(0, 'Enter message...'))
        self.user_entry.bind("<Return>", self.send_msg)
        

        # Create the send button
        
        self.send_button = ctk.CTkButton(self.send_button_frame, width=65, bg_color='white', text='', font=('Helvetica', 12),
                            fg_color='#25D366',corner_radius=100, hover_color='#075E54', image=self.send_image , compound='left', command=self.send_msg)

        self.send_button.pack(side='top', fill='both', expand=True,padx=5)
        # Create the send button
        self.file_button = ctk.CTkButton(self.file_button_frame, width=70, bg_color='white', text='', font=('Helvetica', 12),
                            fg_color='#25D366',corner_radius=100,hover_color="#075E54",image=self.file_image ,command=self.select_file)

        self.file_button.pack(side='top', fill='both', expand=True)
        

    def get_filename(self, folder):
        self.temp_filename = folder.split("/")
        self.temp_filename = self.temp_filename[-1]
        return self.temp_filename


    def select_file(self, event=None):
        self.select_file = filedialog.askopenfilename()
        self.filename = self.select_file
        self.temp_filename = self.get_filename(self.select_file)
        print(self.select_file)

    def receive_file(self, size, name):
        with open(name, "wb") as rec_file:
            print(size)
            print(name)
            while size>0:
                received_buffer = self.real_server.recv(1024)
                rec_file.write(received_buffer)
                size = size-len(received_buffer)
                print(size)
            print("File received successful")
            self.real_server.send(("ready_received").encode())
            self.received_message = None

    def receive_sms_txt(self, receive_txt=None):
        print("Receiving sms again")
        print(self.received_message)
        if receive_txt:
            self.sm = receive_txt
            # print('hvhghghg')
        else:
            self.sm = self.received_message
            print('self.received_message')
            # timestamp = datetime.now().strftime("%I:%M %p")
        timestamp = datetime.now().strftime("%I:%M %p")
        self.message_frame = ctk.CTkFrame(self.chat_frame, bg_color='white',fg_color="black", corner_radius=10)
        self.message_label = ctk.CTkLabel(self.message_frame, text=f'Islam: {self.sm}', font=('Helvetica', 12),wraplength=250)
        self.message_label.pack(padx=5, pady=2)
        self.timestamp_label = ctk.CTkLabel(self.message_frame, text=timestamp, justify='right', text_color='white',font=("Arial", 8))
        self.timestamp_label.pack(side='right', padx=(0, 5), pady=(0, 2))
        self.message_frame.pack(anchor='w', pady=2)
        self.received_message=None

    def try_sample1(self):
        self.receive_sms_thread= threading.Thread(target=self.receive_file, args=(self.received_size, self.received_name))
        self.receive_sms_thread.start()
        self.receive_sms_thread.join()



    def receive_sms(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.host = socket.gethostname()
        self.host = '0.0.0.0'
        self.port = 12345
        self.client = (self.host, self.port)
        print(self.client)
        self.server.bind((self.client))
        self.server.listen(1)
        print("connection successful made")
        self.real_server, self.clientip = self.server.accept()
        while True:
            try:
                # print("receiving messages")
                self.received_message = self.real_server.recv(1024).decode()
                print(self.received_message)
                if "&&&" in self.received_message:
                    self.received_message = self.received_message.split("&&&")
                    self.received_size = self.received_message[0]
                    self.received_name = self.received_message[1]
                    self.received_size = int(self.received_size)
                    self.receive_sms_txt(receive_txt="File Received" +"\n"+self.received_name)
                    self.try_sample1()

                else:
                    if self.received_message:
                        self.receive_sms_txt()
            except:
                continue

    def send_sms_txt(self, file_message=None):
        if file_message:
            self.sms = file_message
        else:
            self.sms= self.user_entry.get()
            self.real_server.send(self.sms.encode())
            self.user_entry.delete(0, "end")
                # Check if the message is not empty before sending
            # Display the sent message in the chat frame
        if self.sms.strip():
            timestamp = datetime.now().strftime("%I:%M %p")
            self.message_frame = ctk.CTkFrame(self.chat_frame, bg_color='white',fg_color="#075E54", corner_radius=10)
            self.message_label = ctk.CTkLabel(self.message_frame, text=f'Farhan: {self.sms}', font=('Helvetica', 12),wraplength=250)
            self.message_label.pack(padx=5, pady=2)
            self.timestamp_label = ctk.CTkLabel(self.message_frame, text=timestamp, justify='right', text_color='white',font=("Arial", 8))
            self.timestamp_label.pack(side='right', padx=(0, 5), pady=(0, 2))
            self.message_frame.pack(anchor='e', pady=2)
            user_message="Islam : "+self.sms
            print(user_message)
            # Send the message along with the sender's name to the server


    def send_file(self, size):
        print(size)
        with open(self.filename, "rb") as file:
            size = int(size)
            while size>0:
                buffer = file.read()
                self.real_server.send(buffer)
                buffer_size = len(buffer)
                break
        print("File successful sent")

    def try_sample(self):
        sendfile_thread = threading.Thread(target=self.send_file, args=(self.filesize,))
        sendfile_thread.start()
        sendfile_thread.join()
        self.filename = None
        self.file_label.place_forget()
        print("Thread stopped")

    def send_msg(self, event=None):
        if self.filename:
            self.ask_send = messagebox.askyesno("Confirm", "Do you want to send message with file")
            print(self.ask_send)
            if self.ask_send:
                self.file_name = self.get_filename(self.filename)
                self.filesize = str(os.stat(self.filename).st_size)
                print("file size is : {}".format(self.filesize))
                self.embedded_filename = self.filesize+"&&&"+self.file_name
                # self.send_sms_txt()
                self.send_sms_txt(file_message="File has been sent"+"\n"+self.file_name)
                self.real_server.send(self.embedded_filename.encode())
                self.try_sample()
            else:
                self.filename = None
                # self.file_label.place_forget()
                self.send_sms_txt()

        else:
            self.send_sms_txt()

show_login_window()