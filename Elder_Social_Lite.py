import tkinter as tk
from tkinter import messagebox, scrolledtext, colorchooser
import random
import pygame
import cv2  # OpenCV for camera functionality
from PIL import Image, ImageTk

# Initialize pygame for sound
pygame.mixer.init()

# Sample contact list (Initially empty)
contacts = []
statuses = []  # List to store status updates

# User Profile
user_profile = {"username": "", "phone": "", "image": ""}
# List of default profile icons
profile_icons = ["profile-2.jpg", "profile-1.jpg", "profile-2.jpg", "profile-1.jpg"]

# Function to play call sound effect
def play_call_sound():
    pygame.mixer.music.load("call_sound.mp3")  # Replace with actual sound file
    pygame.mixer.music.set_volume(0.5)  # Set volume to medium
    pygame.mixer.music.play()

# Function to switch between different tabs
def switch_tab(tab_name, contact_name=None):
    """ Replaces the main content with the selected screen """
    for widget in main_frame.winfo_children():
        widget.destroy()

    if tab_name == "chats":
        update_contact_list()
    elif tab_name == "calls":
        show_calls_screen()
    elif tab_name == "statuses":
        show_status_screen()
    elif tab_name == "settings":
        open_settings_window()
    elif tab_name == "chat" and contact_name:
        open_chat_window(contact_name)

# Function to update the contact list
def update_contact_list():
    """ Updates the contact list dynamically """
    for widget in main_frame.winfo_children():
        widget.destroy()
        

    for contact in contacts:
        frame = tk.Frame(main_frame, bg="#FFFFFF", pady=5)
        frame.pack(fill="x", padx=10, pady=5)

        # Load profile picture
        try:
            img = Image.open(contact["image"])
            img = img.resize((40, 40))
            profile_pic = ImageTk.PhotoImage(img)
        except:
            profile_pic = None
        
        profile_label = tk.Label(frame, image=profile_pic, bg="#FFFFFF")
        profile_label.image = profile_pic
        profile_label.pack(side=tk.LEFT, padx=10)
        
        contact_name = tk.Label(frame, text=f"{contact['name']}", font=("Arial", 14), bg="#FFFFFF")
        contact_name.pack(side=tk.LEFT)
           
        chat_button = tk.Button(frame, text="💬Chat", font=("Arial", 12), command=lambda name=contact["name"]: switch_tab("chat", name))
        chat_button.pack(side=tk.RIGHT, padx=5)

        call_button = tk.Button(frame, text="📞Audio", font=("Arial", 12), command=lambda: (play_call_sound(), start_call()))
        call_button.pack(side=tk.RIGHT, padx=5)
        
        Vedio_button = tk.Button(frame, text="📷Vedio", font=("Arial", 12), command=open_video_call)
        Vedio_button.pack(side=tk.RIGHT, padx=5)
        

# Function to show the calls screen
def show_calls_screen():
    """ Displays the call screen in place of the contact list """
    label = tk.Label(main_frame, text="📞 Call History", font=("Arial", 16))
    label.pack(pady=20)
    
    for widget in main_frame.winfo_children():
        widget.destroy()
        

    for contact in contacts:
        frame = tk.Frame(main_frame, bg="#FFFFFF", pady=5)
        frame.pack(fill="x", padx=10, pady=5)

        # Load profile picture
        try:
            img = Image.open(contact["image"])
            img = img.resize((40, 40))
            profile_pic = ImageTk.PhotoImage(img)
        except:
            profile_pic = None
        
        profile_label = tk.Label(frame, image=profile_pic, bg="#FFFFFF")
        profile_label.image = profile_pic
        profile_label.pack(side=tk.LEFT, padx=10)
        
        contact_name = tk.Label(frame, text=f"{contact['name']}", font=("Arial", 14), bg="#FFFFFF")
        contact_name.pack(side=tk.LEFT)


        call_button = tk.Button(frame, text="📞Audio", font=("Arial", 12), command=lambda: (play_call_sound(), start_call()))
        call_button.pack(side=tk.RIGHT, padx=5)


# Function to show the status screen
def show_status_screen():
    """ Displays the status updates in place of the contact list """
    label = tk.Label(main_frame, text="📝 Status Updates", font=("Arial", 16))
    label.pack(pady=10)

    for status in statuses:
        status_label = tk.Label(main_frame, text=status, font=("Arial", 12), bg="#FFFFFF", pady=5)
        status_label.pack(fill="x", padx=10, pady=5)

    add_status_button = tk.Button(main_frame, text="➕ Add Status", font=("Arial", 12), command=add_status)
    add_status_button.pack(pady=10)

# Function to start a call (Dummy function for now)
def start_call():
    messagebox.showinfo("Call", "Starting a call...")

    
# Function to add a new status
def add_status():
    """ Opens a window to add a new status """
    def save_status():
        status_text = status_entry.get()
        if status_text:
            statuses.append(status_text)
            switch_tab("statuses")
            add_status_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter a status.")

    add_status_window = tk.Toplevel(root)
    add_status_window.title("Add Status")
    add_status_window.geometry("300x200")

    tk.Label(add_status_window, text="Enter Status:", font=("Arial", 12)).pack(pady=5)
    status_entry = tk.Entry(add_status_window, font=("Arial", 12))
    status_entry.pack(pady=5)

    save_button = tk.Button(add_status_window, text="Post", font=("Arial", 12), command=save_status)
    save_button.pack(pady=10)

# Function to display the chat interface
def open_chat_window(contact_name):
    """ Displays the chat interface in place of the contact list """
    
    # Get the contact's information (name, phone, and image)
    contact_info = next(contact for contact in contacts if contact["name"] == contact_name)
    contact_name_text = contact_info["name"]
    contact_phone_text = contact_info["phone"]
    contact_image = contact_info["image"]  # Profile image filename
    
    # Create the header frame to hold the Back button, profile picture, name, and phone number
    header_frame = tk.Frame(main_frame, bg="#ECE5DD")
    header_frame.pack(fill="x", padx=10, pady=5)

    # Back Button on the left
    back_button = tk.Button(header_frame, text="⬅Back", font=("Arial", 12), command=lambda: switch_tab("chats"))
    back_button.pack(side="left", padx=10)

    # Load and display the profile picture
    try:
        img = Image.open(contact_image)
        img = img.resize((40, 40))  # Resize to fit well
        profile_pic = ImageTk.PhotoImage(img)
    except:
        profile_pic = None  # Fallback if image doesn't load

    # Display Profile Picture
    profile_label = tk.Label(header_frame, image=profile_pic, bg="#ECE5DD")
    profile_label.image = profile_pic  # Keep reference to prevent garbage collection
    profile_label.pack(side="left", padx=10)

    # Display Contact's Name and Phone Number
    contact_info_label = tk.Label(header_frame, text=f"{contact_name_text}\n{contact_phone_text}", font=("Arial", 14), bg="#ECE5DD")
    contact_info_label.pack(side="left", padx=10)
    
    
    chat_display = scrolledtext.ScrolledText(main_frame, state=tk.DISABLED, font=("Arial", 14), height=10)
    chat_display.pack(fill="both", expand=True, padx=10, pady=5)

    entry_frame = tk.Frame(main_frame)
    entry_frame.pack(fill="x", padx=10, pady=5)

    message_entry = tk.Entry(entry_frame, font=("Arial", 14))
    message_entry.pack(side=tk.LEFT, fill="both", expand=True, padx=5)

    send_button = tk.Button(entry_frame, text="Send", font=("Arial", 12), command=lambda: send_message(contact_name, chat_display, message_entry))
    send_button.pack(side=tk.RIGHT, padx=5)

# Function to send a message
def send_message(contact_name, chat_display, message_entry):
    """ Displays and saves sent messages """
    message = message_entry.get()
    if message.strip():
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You to {contact_name}: {message}\n")
        chat_display.config(state=tk.DISABLED)
        message_entry.delete(0, tk.END)

# Function to open camera for video call
def open_video_call():
    """ Opens the computer's camera for video call """
    cap = cv2.VideoCapture(0)  # 0 for default webcam
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Video Call", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit the video call
            break
    cap.release()
    cv2.destroyAllWindows()

# Function to display settings menu
def open_settings_window():
    """ Displays the settings menu in place of the contact list """
    back_button = tk.Button(main_frame, text="⬅ Back", font=("Arial", 12), command=lambda: switch_tab("chats"))
    back_button.pack(anchor="w", padx=10, pady=5)
    
    def save_settings():
        # Update user profile with new information
        user_profile["username"] = username_entry.get()
        user_profile["phone"] = phone_entry.get()
        messagebox.showinfo("Settings", "Your settings have been updated!")
        
    tk.Label(main_frame, text="Username:").pack(pady=5)
    username_entry = tk.Entry(main_frame, font=("Arial", 12))
    username_entry.insert(0, user_profile["username"])  # Pre-fill with current data
    username_entry.pack(pady=5)

    tk.Label(main_frame, text="Phone Number:").pack(pady=5)
    phone_entry = tk.Entry(main_frame, font=("Arial", 12))
    phone_entry.insert(0, user_profile["phone"])  # Pre-fill with current data
    phone_entry.pack(pady=5)

    settings_label = tk.Label(main_frame, text="⚙ Settings Menu", font=("Arial", 16))
    settings_label.pack(pady=20)

    # Color Picker
    color_button = tk.Button(main_frame, text="Change Color", font=("Arial", 12), command=change_color)
    color_button.pack(pady=10)

    # Font Type Picker
    font_button = tk.Button(main_frame, text="Change Font", font=("Arial", 12), command=change_font)
    font_button.pack(pady=10)

    # Font Size Picker
    size_button = tk.Button(main_frame, text="Change Font Size", font=("Arial", 12), command=change_font_size)
    size_button.pack(pady=10)

def change_color():
    color_code = colorchooser.askcolor()[1]
    if color_code:
        root.configure(bg=color_code)

def change_font():
    fonts = ["Arial", "Helvetica", "Times New Roman"]
    selected_font = tk.simpledialog.askstring("Select Font", "Enter font (Arial, Helvetica, Times New Roman):")
    if selected_font in fonts:
        for widget in main_frame.winfo_children():
            widget.configure(font=(selected_font, 12))

def change_font_size():
    size = tk.simpledialog.askinteger("Font Size", "Enter font size:")
    if size:
        for widget in main_frame.winfo_children():
            widget.configure(font=("Arial", size))

# Function to add a new contact
def add_new_contact():
    def save_contact():
        name = name_entry.get()
        phone = phone_entry.get()
        if name and phone:
            # Assign a random profile icon
            random_profile = random.choice(profile_icons)
            contacts.append({"image": random_profile, "name": name, "phone": phone})
            update_contact_list()
            add_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter both name and phone number.")

    add_window = tk.Toplevel(root)
    add_window.title("Add New Contact")
    add_window.geometry("300x200")

    tk.Label(add_window, text="Name:", font=("Arial", 12)).pack(pady=5)
    name_entry = tk.Entry(add_window, font=("Arial", 12))
    name_entry.pack(pady=5)

    tk.Label(add_window, text="Phone:", font=("Arial", 12)).pack(pady=5)
    phone_entry = tk.Entry(add_window, font=("Arial", 12))
    phone_entry.pack(pady=5)

    save_button = tk.Button(add_window, text="Save", font=("Arial", 12), command=save_contact)
    save_button.pack(pady=10)


# Login Screen
def login_window():
    """ Show the login window to get username and phone number """
    def save_login():
        username = username_entry.get()
        phone = phone_entry.get()
        if username and phone:
            # Store the username and phone number
            user_profile["username"] = username
            user_profile["phone"] = phone
            login_window.destroy()  # Close the login window
            create_ui()  # Proceed to the main UI
        else:
            messagebox.showwarning("Input Error", "Please enter both username and phone number.")

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Enter Username:", font=("Arial", 12)).pack(pady=5)
    username_entry = tk.Entry(login_window, font=("Arial", 12))
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Enter Phone Number:", font=("Arial", 12)).pack(pady=5)
    phone_entry = tk.Entry(login_window, font=("Arial", 12))
    phone_entry.pack(pady=5)

    save_button = tk.Button(login_window, text="Login", font=("Arial", 12), command=save_login)
    save_button.pack(pady=10)

    login_window.mainloop()

# Function to create the main UI
def create_ui():
    global root, main_frame

    root = tk.Tk()
    root.title("Elder Social Lite - WhatsApp Style")
    root.geometry("400x600")
    root.configure(bg="#075E54")
    # Header Section with Fixed Tabs
    header_frame = tk.Frame(root, bg="#128C7E")
    header_frame.pack(side="top", fill="x")
    
    title_label = tk.Label(header_frame, text="Elder Social Lite", font=("Arial", 18, "bold"), bg="#128C7E", fg="white")
    title_label.pack(pady=10)

    # Header Section with Tabs (with Icons)
    header_frame = tk.Frame(root, bg="#128C7E", height=50)
    header_frame.pack(fill="x")

    tabs = [("💬 Chats", "chats"), ("📞 Calls", "calls"), ("📝 Statuses", "statuses"), ("⚙ Settings", "settings")]
    for tab_text, tab_command in tabs:
        tab_button = tk.Button(header_frame, text=tab_text, font=("Arial", 12), bg="#128C7E", fg="white",
                               command=lambda command=tab_command: switch_tab(command))
        tab_button.pack(side="left", padx=5, pady=5)

    # Main Content Area
    main_frame = tk.Frame(root, bg="#ECE5DD")
    main_frame.pack(fill="both", expand=True)

    # Bottom Add Contact Button
    add_contact_button = tk.Button(root, text="➕ Add Contact", font=("Arial", 14), command=add_new_contact, bg="#25D366", fg="white")
    add_contact_button.pack(side="bottom", fill="x", pady=10)

    # Show initial contact list
    switch_tab("chats")
    root.mainloop()

# Run the login window first
login_window()
