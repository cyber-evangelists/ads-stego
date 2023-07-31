import customtkinter as CTk
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from crypto import encrypt, decrypt
from binder import bind_data_to_file, unbind_data_from_file
import pickle
import json

encrypted_file_ext = ''
path_to_main_video_file =  ''
path_to_secret_file = ''
path_to_binded_file = ''
encrypted_dir = "Encrypted"
decrypted_dir = "Decrypted"
unbinded_dir = "Unbinded"
root = CTk.CTk()
    
def encrypt_file():
    file_name = path_to_secret_file.split('/')[-1].split('.')[0]
    with open(path_to_secret_file, "rb") as file:
        content = file.read()
    encrypted_content = encrypt(content)
    with open(f'{encrypted_dir}/{file_name}.cph', 'w') as file:
        file.write(json.dumps(encrypted_content))
        print(f"File encrypted, stored: {encrypted_dir}/{file_name}.cph")

def bind_file():
    file_name = path_to_secret_file.split('/')[-1].split('.')[0]
    with open(f'{encrypted_dir}/{file_name}.cph', 'rb') as file:
        encrypted_content = file.read()
    response = bind_data_to_file(path_to_main_video_file, encrypted_content)
    print(f"{response}, stored: {path_to_main_video_file}")

def unbind_file():
    print(path_to_main_video_file)
    encrypted_content = unbind_data_from_file(path_to_main_video_file)
    with open(f'{unbinded_dir}/secret_enc.cph', 'wb') as file:
        file.write(encrypted_content) 
    print(f"File unbinded, stored: {unbinded_dir}/secret.cph")
    
def decrypt_file():
    file_name = path_to_secret_file.split('/')[-1].split('.')[0]
    extension = encrypted_file_ext
    with open(f'{unbinded_dir}/secret_enc.cph', 'rb') as file:
        encrypted_content = json.load(file)  
    decrypted_content = decrypt(encrypted_content) 

    with open(f'{decrypted_dir}/secret.{extension}', 'wb') as file:
        file.write(decrypted_content) 
    print(f"File decrypted, stored: {decrypted_dir}/secret.{extension}")
     

def _on_select_file(button, path_to_file):
    """Opens a file dialog and selects a file."""
    
    global path_to_main_video_file, path_to_secret_file, path_to_binded_file
    file_path = filedialog.askopenfilename()
    print("Selected File:", file_path)
    file = file_path.split('/')[-1]
    button.config(text=file)
    if button.cget("text") == "":
        button.config(text="No File Selected")
    
    if path_to_file == "main_video_file":
        path_to_main_video_file =  file_path    
    elif  path_to_file == "secret_file":
        path_to_secret_file =  file_path   
    elif  path_to_file == "binded_file":
        path_to_binded_file =  file_path
    else:
        pass
    
    # Enable the Encrypt and button
    if secret_file_button.cget("text") != "Browse File" and secret_file_button.cget("text") != "No File Selected":
        encrypt_button.config(state="normal")
        
    # Enable the Encrypt and Bind buttons if both files have been selected
    if main_video_file_button.cget("text") != "Browse File" and main_video_file_button.cget("text") != "No File Selected" and secret_file_button.cget("text") != "Browse File" and secret_file_button.cget("text") != "No File Selected":
        bind_button.config(state="normal")

    # Enable the Decrypt and Unbind buttons if file have been selected
    if binded_file_button.cget("text") != "Browse File" and binded_file_button.cget("text") != "No File Selected" and encrypted_file_ext != '':
        decrypt_button.config(state="normal")
        unbind_button.config(state="normal")

def on_select_option(event):
    """Prints the selected option from the dropdown."""

    global encrypted_file_ext
    encrypted_file_ext = drop_down.get()
    if encrypted_file_ext:
        decrypt_button.config(state="normal")
        unbind_button.config(state="normal")

    
# Create the left panel
left_panel = CTk.CTkFrame(root)
left_panel.pack(side="left", fill="both", expand=True)

# Create the right panel
right_panel = CTk.CTkFrame(root)
right_panel.pack(side="right", fill="both", expand=True)

# Add a label to the left panel
label = CTk.CTkLabel(left_panel, text="Binding & Encryption", font=CTk.CTkFont(family='Arial', size=20, weight='bold'), text_color='Green')
label.pack(pady=(10, 30))

# Add a label to the right panel
label = CTk.CTkLabel(right_panel, text="Unbinding & Decryption", font=CTk.CTkFont(family='Arial', size=20, weight='bold'), text_color='Green')
label.pack(pady=(10, 30))

# Add a line between the panels
separator = ttk.Separator(root, orient="horizontal")
separator.pack(fill="both", padx=10, pady=0, expand=True)

# Increase the size of the window
root.geometry("800x500")

# Add a "please select main video" text on the top of the file select button
text = CTk.CTkLabel(left_panel, text="Please select main video", font=CTk.CTkFont(family='Arial', size=12, weight='bold'))
text.pack(fill="x", pady=10)
main_video_file_button = ttk.Button(left_panel, text="Browse File", command=lambda: _on_select_file(main_video_file_button, "main_video_file"))
main_video_file_button.pack(pady=(0, 30))

# Add a "please select secret file" text on the top of the file select button
text = CTk.CTkLabel(left_panel, text="Please select secret file", font=CTk.CTkFont(family='Arial', size=12, weight='bold'))
text.pack(fill="x", pady=10)
secret_file_button = ttk.Button(left_panel, text="Browse File", command=lambda: _on_select_file(secret_file_button, "secret_file"))
secret_file_button.pack()

# Add two buttons in parallel
encrypt_button = ttk.Button(left_panel, text="Encrypt", command=lambda: encrypt_file())
encrypt_button.config(state="disabled")
bind_button = ttk.Button(left_panel, text="Bind", command=lambda: bind_file())
bind_button.config(state="disabled")
encrypt_button.pack(side="left", pady=0, padx=(50, 0))
bind_button.pack(side="right", pady=0, padx=(0, 50))



# Start right pannel
# Add a "please select secret file" text on the top of the file select button
text = CTk.CTkLabel(right_panel, text="Please select video file", font=CTk.CTkFont(family='Arial', size=12, weight='bold'))
text.pack(fill="x", pady=10)
binded_file_button = ttk.Button(right_panel, text="Browse File", command=lambda: _on_select_file(binded_file_button, "binded_file"))
binded_file_button.pack(pady=(0, 30))

# Add a dropdown in the right panel
text = CTk.CTkLabel(right_panel, text="Please select hidden file extension", font=CTk.CTkFont(family='Arial', size=12, weight='bold'))
text.pack(fill="x", pady=10)
drop_down = ttk.Combobox(right_panel, values=["jpeg", "png", "mp3", "mp4", "txt", "doc", "docx", "html", "pdf"])
drop_down.pack(pady=(0, 10))
drop_down.bind("<<ComboboxSelected>>", on_select_option)

# Add two buttons in parallel
decrypt_button = ttk.Button(right_panel, text="Decrypt", command=lambda: decrypt_file())
decrypt_button.config(state="disabled")
unbind_button = ttk.Button(right_panel, text="Unbind", command=lambda: unbind_file())
unbind_button.config(state="disabled")
decrypt_button.pack(side="left", padx=(50, 0))
unbind_button.pack(side="right", padx=(0, 50))



root.mainloop()
