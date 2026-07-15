"""
Main GUI interface.
"""


import ttkbootstrap as ttk

from ttkbootstrap.constants import *

from tkinter import filedialog

from pathlib import Path


from config import (
    APP_NAME,
    APP_VERSION
)



class SecureFileVaultGUI:


    def __init__(self):

        self.window = ttk.Window(
            title=APP_NAME,
            themename="darkly",
            size=(900,600)
        )


        self.selected_file = None


        self.create_interface()



    def create_interface(self):

        self.create_menu()

        self.create_dashboard()

        self.create_status()



    def create_menu(self):

        menu_bar = ttk.Menu(
            self.window
        )


        file_menu = ttk.Menu(
            menu_bar,
            tearoff=False
        )


        file_menu.add_command(
            label="Browse File",
            command=self.browse_file
        )


        file_menu.add_separator()


        file_menu.add_command(
            label="Exit",
            command=self.window.destroy
        )


        menu_bar.add_cascade(
            label="File",
            menu=file_menu
        )


        security_menu = ttk.Menu(
            menu_bar,
            tearoff=False
        )


        security_menu.add_command(
            label="Generate RSA Key"
        )


        security_menu.add_command(
            label="Load Key"
        )


        menu_bar.add_cascade(
            label="Security",
            menu=security_menu
        )


        tools_menu = ttk.Menu(
            menu_bar,
            tearoff=False
        )


        menu_bar.add_cascade(
            label="Tools",
            menu=tools_menu
        )


        help_menu = ttk.Menu(
            menu_bar,
            tearoff=False
        )


        help_menu.add_command(
            label="About"
        )


        menu_bar.add_cascade(
            label="Help",
            menu=help_menu
        )


        self.window.config(
            menu=menu_bar
        )



    def create_dashboard(self):


        container = ttk.Frame(
            self.window,
            padding=30
        )


        container.pack(
            fill=BOTH,
            expand=True
        )


        title = ttk.Label(
            container,
            text=APP_NAME,
            font=(
                "Segoe UI",
                24,
                "bold"
            )
        )


        title.pack(
            pady=20
        )



        self.file_label = ttk.Label(
            container,
            text="File : -"
        )


        self.file_label.pack(
            pady=10
        )



        self.progress = ttk.Progressbar(
            container,
            length=500,
            mode="determinate"
        )


        self.progress.pack(
            pady=20
        )



        button_frame = ttk.Frame(
            container
        )


        button_frame.pack()



        ttk.Button(
            button_frame,
            text="Encrypt",
            bootstyle="success"
        ).grid(
            row=0,
            column=0,
            padx=10
        )


        ttk.Button(
            button_frame,
            text="Decrypt",
            bootstyle="danger"
        ).grid(
            row=0,
            column=1,
            padx=10
        )



    def create_status(self):

        self.status = ttk.Label(
            self.window,
            text="Ready",
            anchor="center"
        )

        self.status.pack(
            fill=X
        )



    def browse_file(self):

        file_path = filedialog.askopenfilename()


        if file_path:

            self.selected_file = Path(
                file_path
            )


            self.file_label.config(
                text=f"File : {self.selected_file.name}"
            )


            self.status.config(
                text="File selected"
            )



    def run(self):

        self.window.mainloop()
