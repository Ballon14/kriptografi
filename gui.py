"""
Secure File Vault GUI.

Desktop interface using ttkbootstrap.
"""

import threading
from pathlib import Path

import ttkbootstrap as ttk
from tkinter import filedialog, messagebox
from ttkbootstrap.constants import *

from about import APP_INFORMATION
from config import APP_NAME, APP_VERSION
from decrypt import FileDecryptor
from encrypt import FileEncryptor
from rsa_key import RSAKeyManager


class SecureFileVaultGUI:
    def __init__(self):
        self.window = ttk.Window(
            title=APP_NAME,
            themename="darkly",
            size=(1000, 700),
        )
        self.window.minsize(900, 650)

        self.selected_file = None
        self.encryptor = FileEncryptor()
        self.decryptor = FileDecryptor()
        self.key_manager = RSAKeyManager()

        self.create_interface()

    def create_interface(self):
        self.create_menu()
        self.create_dashboard()

    def create_menu(self):
        menu = ttk.Menu(self.window)

        file_menu = ttk.Menu(menu, tearoff=False)
        file_menu.add_command(label="Browse File", command=self.browse_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.destroy)
        menu.add_cascade(label="File", menu=file_menu)

        security_menu = ttk.Menu(menu, tearoff=False)
        security_menu.add_command(label="Generate RSA Key", command=self.generate_key)
        menu.add_cascade(label="Security", menu=security_menu)

        help_menu = ttk.Menu(menu, tearoff=False)
        help_menu.add_command(label="About", command=self.show_about)
        menu.add_cascade(label="Help", menu=help_menu)

        self.window.config(menu=menu)

    def create_dashboard(self):
        main_frame = ttk.Frame(self.window, padding=30)
        main_frame.pack(fill=BOTH, expand=True)

        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=X)

        ttk.Label(
            header_frame,
            text=APP_NAME,
            font=("Segoe UI", 26, "bold"),
        ).pack(anchor=W)
        ttk.Label(
            header_frame,
            text="Protect your files with RSA-2048 and AES-256 hybrid encryption.",
            font=("Segoe UI", 11),
        ).pack(anchor=W, pady=(6, 0))

        card = ttk.LabelFrame(main_frame, text="File operation")
        card.pack(fill=BOTH, expand=True, pady=(20, 0))

        card_content = ttk.Frame(card, padding=20)
        card_content.pack(fill=BOTH, expand=True)

        self.file_label = ttk.Label(
            card_content,
            text="Selected file: none",
            font=("Segoe UI", 11, "bold"),
            wraplength=800,
        )
        self.file_label.pack(anchor=W)

        ttk.Label(
            card_content,
            text="Choose a normal file to encrypt or a .filevault file to decrypt.",
            wraplength=800,
        ).pack(anchor=W, pady=(8, 0))

        button_row = ttk.Frame(card_content)
        button_row.pack(fill=X, pady=(16, 0))

        self.browse_button = ttk.Button(button_row, text="Browse file", bootstyle="info", command=self.browse_file)
        self.browse_button.pack(side=LEFT)

        self.key_button = ttk.Button(button_row, text="Generate RSA key", bootstyle="secondary", command=self.generate_key)
        self.key_button.pack(side=LEFT, padx=(10, 0))

        self.progress = ttk.Progressbar(card_content, length=700, mode="indeterminate")
        self.progress.pack(fill=X, pady=(18, 0))

        action_row = ttk.Frame(card_content)
        action_row.pack(fill=X, pady=(16, 0))

        self.encrypt_button = ttk.Button(action_row, text="Encrypt", bootstyle="success", command=self.encrypt_file)
        self.encrypt_button.pack(side=LEFT)

        self.decrypt_button = ttk.Button(action_row, text="Decrypt", bootstyle="danger", command=self.decrypt_file)
        self.decrypt_button.pack(side=LEFT, padx=(10, 0))

        status_frame = ttk.LabelFrame(main_frame, text="Status")
        status_frame.pack(fill=X, pady=(16, 0))

        status_content = ttk.Frame(status_frame, padding=15)
        status_content.pack(fill=BOTH, expand=True)

        self.status = ttk.Label(status_content, text="Ready", font=("Segoe UI", 10, "bold"))
        self.status.pack(anchor=W)

        self.helper_text = ttk.Label(
            status_content,
            text="Select a file and pick an action to begin.",
            wraplength=800,
        )
        self.helper_text.pack(anchor=W, pady=(6, 0))

        ttk.Label(
            main_frame,
            text="Encrypted files are stored in the encrypted folder and restored files appear in the decrypted folder.",
            wraplength=800,
        ).pack(anchor=W, pady=(16, 0))

    def browse_file(self):
        selected = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("All files", "*.*"), ("Encrypted vault files", "*.filevault")],
        )

        if selected:
            self.selected_file = Path(selected)
            if self.selected_file.suffix == ".filevault":
                self.update_status("Encrypted file selected", f"Ready to decrypt {self.selected_file.name}")
            else:
                self.update_status("File selected", f"Ready to encrypt {self.selected_file.name}")
            self.file_label.config(text=f"Selected file: {self.selected_file.name}")

    def generate_key(self):
        self.set_busy(True)
        threading.Thread(target=self.run_generate_key, daemon=True).start()

    def run_generate_key(self):
        try:
            result = self.key_manager.generate_key_pair()
            if result:
                self.window.after(0, lambda: self.update_status("RSA key generated", "The new key pair is available in the keys folder."))
                self.window.after(0, lambda: messagebox.showinfo("Success", "RSA key generated"))
            else:
                self.window.after(0, lambda: messagebox.showerror("Error", "Failed to generate RSA key"))
        except Exception as error:
            self.window.after(0, lambda: messagebox.showerror("Error", str(error)))
        finally:
            self.window.after(0, lambda: self.set_busy(False))

    def encrypt_file(self):
        if not self.selected_file:
            messagebox.showwarning("Warning", "Select a file first")
            return

        if self.selected_file.suffix == ".filevault":
            messagebox.showwarning("Warning", "Select a normal file to encrypt, not an encrypted vault")
            return

        self.set_busy(True)
        self.update_status("Encrypting...", "Creating a secure encrypted package...")
        threading.Thread(target=self.run_encrypt, daemon=True).start()

    def run_encrypt(self):
        try:
            output = self.encryptor.encrypt_file(self.selected_file)
            self.window.after(0, lambda: self.update_status("Encryption complete", f"Saved to {output}"))
            self.window.after(0, lambda: messagebox.showinfo("Success", str(output)))
        except Exception as error:
            self.window.after(0, lambda: messagebox.showerror("Error", str(error)))
        finally:
            self.window.after(0, lambda: self.set_busy(False))

    def decrypt_file(self):
        if not self.selected_file:
            messagebox.showwarning("Warning", "Select an encrypted file")
            return

        if self.selected_file.suffix != ".filevault":
            messagebox.showwarning("Warning", "Select a .filevault encrypted file")
            return

        self.set_busy(True)
        self.update_status("Decrypting...", "Restoring the original file...")
        threading.Thread(target=self.run_decrypt, daemon=True).start()

    def run_decrypt(self):
        try:
            output = self.decryptor.decrypt_file(self.selected_file)
            self.window.after(0, lambda: self.update_status("Decryption complete", f"Restored to {output}"))
            self.window.after(0, lambda: messagebox.showinfo("Success", str(output)))
        except Exception as error:
            self.window.after(0, lambda: messagebox.showerror("Error", str(error)))
        finally:
            self.window.after(0, lambda: self.set_busy(False))

    def update_status(self, message: str, detail: str | None = None):
        self.status.config(text=message)
        if detail is None:
            detail = "Select a file and pick an action to begin."
        self.helper_text.config(text=detail)
        self.file_label.config(text=f"Selected file: {self.selected_file.name if self.selected_file else 'none'}")

    def set_busy(self, busy: bool):
        if busy:
            self.progress.start(10)
            self.encrypt_button.state(["disabled"])
            self.decrypt_button.state(["disabled"])
            self.browse_button.state(["disabled"])
            self.key_button.state(["disabled"])
        else:
            self.progress.stop()
            self.encrypt_button.state(["!disabled"])
            self.decrypt_button.state(["!disabled"])
            self.browse_button.state(["!disabled"])
            self.key_button.state(["!disabled"])

    def show_about(self):
        messagebox.showinfo(
            "About",
            (
                f"{APP_INFORMATION['name']}\n\n"
                f"Version: {APP_VERSION}\n"
                f"Algorithm: {APP_INFORMATION['algorithm']}\n\n"
                f"{APP_INFORMATION['description']}"
            ),
        )

    def run(self):
        self.window.mainloop()
