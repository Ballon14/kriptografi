"""
Secure File Vault GUI.

Desktop interface using ttkbootstrap.
"""


import threading

import time


from pathlib import Path


import ttkbootstrap as ttk


from ttkbootstrap.constants import *


from tkinter import (
    filedialog,
    messagebox
)



from encrypt import FileEncryptor

from decrypt import FileDecryptor

from rsa_key import RSAKeyManager


from about import APP_INFORMATION



from config import APP_NAME, APP_VERSION




class SecureFileVaultGUI:


    def __init__(self):

        self.window = ttk.Window(

            title=APP_NAME,

            themename="darkly",

            size=(950,650)

        )


        self.selected_file = None


        self.encryptor = FileEncryptor()

        self.decryptor = FileDecryptor()

        self.key_manager = RSAKeyManager()



        self.create_interface()



    def create_interface(self):

        self.create_menu()

        self.create_dashboard()



    def create_menu(self):


        menu = ttk.Menu(
            self.window
        )


        file_menu = ttk.Menu(
            menu,
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



        menu.add_cascade(

            label="File",

            menu=file_menu

        )



        security_menu = ttk.Menu(

            menu,

            tearoff=False

        )


        security_menu.add_command(

            label="Generate RSA Key",

            command=self.generate_key

        )


        menu.add_cascade(

            label="Security",

            menu=security_menu

        )



        help_menu = ttk.Menu(

            menu,

            tearoff=False

        )


        help_menu.add_command(

            label="About",

            command=self.show_about

        )



        menu.add_cascade(

            label="Help",

            menu=help_menu

        )


        self.window.config(

            menu=menu

        )




    def create_dashboard(self):


        frame = ttk.Frame(

            self.window,

            padding=30

        )


        frame.pack(

            expand=True,

            fill=BOTH

        )



        ttk.Label(

            frame,

            text=APP_NAME,

            font=(

                "Segoe UI",

                26,

                "bold"

            )

        ).pack(

            pady=15

        )



        self.file_label = ttk.Label(

            frame,

            text="File: -"

        )


        self.file_label.pack()



        self.progress = ttk.Progressbar(

            frame,

            length=600,

            mode="determinate"

        )


        self.progress.pack(

            pady=20

        )



        button_frame = ttk.Frame(

            frame

        )


        button_frame.pack()



        ttk.Button(

            button_frame,

            text="Encrypt",

            bootstyle="success",

            command=self.encrypt_file

        ).grid(

            row=0,

            column=0,

            padx=15

        )



        ttk.Button(

            button_frame,

            text="Decrypt",

            bootstyle="danger",

            command=self.decrypt_file

        ).grid(

            row=0,

            column=1,

            padx=15

        )



        self.status = ttk.Label(

            frame,

            text="Ready"

        )


        self.status.pack(

            pady=20

        )




    def browse_file(self):


        selected = filedialog.askopenfilename()



        if selected:


            self.selected_file = Path(

                selected

            )


            self.file_label.config(

                text=f"File: {self.selected_file.name}"

            )



    def generate_key(self):


        result = (

            self.key_manager.generate_key_pair()

        )


        if result:


            messagebox.showinfo(

                "Success",

                "RSA key generated"

            )




    def encrypt_file(self):


        if not self.selected_file:


            messagebox.showwarning(

                "Warning",

                "Select file first"

            )

            return



        thread = threading.Thread(

            target=self.run_encrypt

        )


        thread.start()




    def run_encrypt(self):


        try:


            self.update_status(

                "Encrypting..."

            )


            self.progress.start()



            output = (

                self.encryptor.encrypt_file(

                    self.selected_file

                )

            )



            self.progress.stop()



            self.update_status(

                "Encryption complete"

            )



            messagebox.showinfo(

                "Success",

                str(output)

            )


        except Exception as error:


            messagebox.showerror(

                "Error",

                str(error)

            )




    def decrypt_file(self):


        if not self.selected_file:


            messagebox.showwarning(

                "Warning",

                "Select encrypted file"

            )


            return



        thread = threading.Thread(

            target=self.run_decrypt

        )


        thread.start()




    def run_decrypt(self):


        try:


            self.update_status(

                "Decrypting..."

            )


            self.progress.start()



            output = (

                self.decryptor.decrypt_file(

                    self.selected_file

                )

            )


            self.progress.stop()



            self.update_status(

                "Decryption complete"

            )


            messagebox.showinfo(

                "Success",

                str(output)

            )


        except Exception as error:


            messagebox.showerror(

                "Error",

                str(error)

            )




    def update_status(

        self,

        message: str

    ):


        self.status.config(

            text=message

        )




    def show_about(self):


        messagebox.showinfo(

            "About",

            (
                f"{APP_INFORMATION['name']}\n\n"

                f"Version: {APP_VERSION}\n"

                f"Algorithm: "
                f"{APP_INFORMATION['algorithm']}\n\n"

                f"{APP_INFORMATION['description']}"

            )

        )




    def run(self):

        self.window.mainloop()
