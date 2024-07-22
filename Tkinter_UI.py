import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from LeetcodeFinalBot import LeetCodeBot  
from PIL import Image, ImageTk

# Try to add a logo
class LeetCodeBotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LeetCode Bot")
        self.root.configure(bg="#2c2f33")  # Set background color to a lighter shade of dark gray
        self.status= (
            "Execution failed due to one of the following reasons:\n"
            "1) Invalid credentials.\n"
            "2) Unable to log in directly through GitHub.\n"
            "3) GitHub login with Multi-Factor Authentication (MFA) enabled.\n"
            "4) Execution interrupted by an unexpected event.\n"
            "5) Google Chrome browser is not installed on this device.\n"
            "6) This device does not meet the system requirements to run the bot application.\n"
            "7) The account has not been authenticated on this device at least once.")
        # Set the window size and center it on the screen
        window_width = 700
        window_height = 500
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        # Configure the grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)

        # Create and place the email label and entry field
        self.email_label = tk.Label(root, text="Email", font=('Comic Sans MS', 14), bg="#2c2f33", fg="#FFFFFF")  # Set text color to white
        self.email_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        self.email_entry = tk.Entry(root, font=('Comic Sans MS', 14), bd=2, relief=tk.FLAT)
        self.email_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Create and place the password label and entry field (with hidden text)
        self.password_label = tk.Label(root, text="Password", font=('Comic Sans MS', 14), bg="#2c2f33", fg="#FFFFFF")  # Set text color to white
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.password_entry = tk.Entry(root, show="*", font=('Comic Sans MS', 14), bd=2, relief=tk.FLAT)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        
        # Create and place the language label and dropdown menu
        self.language_label = tk.Label(root, text="Language", font=('Comic Sans MS', 14), bg="#2c2f33", fg="#FFFFFF")  # Set text color to white
        self.language_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
        self.language_var = tk.StringVar()
        self.language_dropdown = ttk.Combobox(root, textvariable=self.language_var, font=('Comic Sans MS', 14), state='readonly', width=20)
        self.language_dropdown['values'] = ('Python3', 'C++', 'Java', 'JavaScript')
        self.language_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        self.language_dropdown.current(0)
        self.language_dropdown.bind('<<ComboboxSelected>>', self.update_question_dropdown)
        
         # Create and place the number of questions label and dropdown menu
        self.num_questions_label = tk.Label(root, text="Questions to solve", font=('Comic Sans MS', 14), bg="#2c2f33", fg="#FFFFFF")  # Set text color to white
        self.num_questions_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
        self.num_questions_var = tk.StringVar()
        self.num_questions_dropdown = ttk.Combobox(root, textvariable=self.num_questions_var, font=('Comic Sans MS', 14), state='readonly', width=10)
        self.num_questions_dropdown['values'] = ('10', '20', '40', '80', '100','120','150','180','200')
        self.num_questions_dropdown.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)
        self.num_questions_dropdown.current(0)
        
        # Create and place the "Run Bot" button
        self.run_button = tk.Button(root, text="Let's Code!", font=('Comic Sans MS', 14), command=self.run_bot, bg='#4CAF50', fg='white', bd=2, relief=tk.FLAT)
        self.run_button.grid(row=4, column=0, columnspan=2, pady=20, padx=10)

        # Create and place the note
        self.note_label = tk.Label(root, text="Note: The bot operates only with correct credentials and requires authentication through GitHub. \n Direct login via the LeetCode login page is not supported.", font=('Comic Sans MS', 12, 'bold'), wraplength=500, bg="#2c2f33", fg="#FF7F50")  # Set text color to coral
        self.note_label.grid(row=5, column=0, columnspan=2, pady=(0, 5), padx=10)

         # Create and place the note
        self.note_label = tk.Label(root, text="Ensure you have previously logged in on this device using the credentials you are about to enter.", font=('Comic Sans MS', 12, 'bold'), wraplength=500, bg="#2c2f33", fg="#FF7F50")  # Set text color to coral
        self.note_label.grid(row=6, column=0, columnspan=2, pady=(0, 5), padx=10)
        
        # Create and place the contact email
        self.contact_label = tk.Label(root, text="For any queries, contact: leetcodebothelp@gmail.com", font=('Comic Sans MS', 12), bg="#2c2f33", fg="#1E90FF")  # Set text color to dodger blue
        self.contact_label.grid(row=7, column=0, columnspan=2, pady=(0, 10), padx=10)

    def update_question_dropdown(self, event):
        selected_language = self.language_var.get()
        if selected_language == 'JavaScript':
            self.num_questions_dropdown['values'] = ('10', '20', '40', '80', '100', '120')
        else:
            self.num_questions_dropdown['values'] = ('10', '20', '40', '80', '100', '120', '150', '180', '200')
        self.num_questions_dropdown.current(0)

    def run_bot(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        language = self.language_var.get()
        questions= self.num_questions_var.get()
        

        # Check if email or password is empty and show an error message if they are
        if not email or not password:
            messagebox.showerror("Error", "Email and Password are mandatory fields.")
            return

        # Close the main window
        self.root.destroy()

        # Show a popup window indicating that the bot is running
        self.show_popup("LeetCode Bot","Note: The bot operates only with correct credentials and requires authentication through GitHub. \n Direct login via the LeetCode login page is not supported.")
        self.show_popup("LeetCode Bot", f"Note: Keep the new Chrome browser session open and ensure your device remains active. \n The approximate time required will be greater than or equal to: {self.approximate_time()}")
        self.show_popup("LeetCode Bot","Avoid using copy/paste commands while the bot is running.")
        
        # Run the LeetCode bot
        bot = LeetCodeBot(email, password, language,questions,self)
        bot.run()
        self.show_status_execution()
            
    def show_status_execution(self):
        self.show_popup("LeetCode Bot",f"{self.status}")

    def approximate_time(self):
        approx_time = "5 minutes"
        if int(self.num_questions_var.get()) == 10:
            approx_time = "5 Minutes"
        if int(self.num_questions_var.get()) == 20:
            approx_time = "10 Minutes"
        if int(self.num_questions_var.get()) == 40:        
            approx_time = "20 Minutes"
        if int(self.num_questions_var.get()) == 80:
            approx_time = "40 Minutes"
        if int(self.num_questions_var.get()) == 100:
            approx_time = "50 Minutes"
        if int(self.num_questions_var.get()) == 120:
            approx_time = "60 Minutes"
        if int(self.num_questions_var.get()) == 150:
            approx_time = "75 Minutes"
        if int(self.num_questions_var.get()) == 180:
            approx_time = "90 Minutes"
        if int(self.num_questions_var.get()) == 180:
            approx_time = "100 Minutes"
        return approx_time

    def show_popup(self, title, message):
        # Create a new popup window
        popup = tk.Tk()
        popup.wm_title(title)
        popup.configure(bg="#2c2f33")  # Set background color to a lighter shade of dark gray
        # Set the window size and center it on the screen
        window_width = 800
        window_height = 300
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        popup.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        label = tk.Label(popup, text=message, padx=20, pady=10, font=('Comic Sans MS', 12), bg="#2c2f33", fg="#FFFFFF")  # Set text color to white
        label.pack()
        ok_button = tk.Button(popup, text="OK", command=popup.destroy, padx=20, pady=5, font=('Comic Sans MS', 12), bd=2, relief=tk.FLAT, bg="#4CAF50", fg="white")
        ok_button.pack()
        popup.mainloop()

# If the script is run directly, create the main application window and start the app
if __name__ == "__main__":
    root = tk.Tk()
    app = LeetCodeBotUI(root)
    root.mainloop()

