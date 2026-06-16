import tkinter as tk
from tkinter import messagebox, ttk
import secrets
import random
import json
import os
from datetime import datetime

# =====================================
# CONFIG
# =====================================

DATA_FILE = "defcon_data.json"
VALID_ADMIN_ID = "vatsyayankabir"
VALID_ADMIN_PW = "KiloAlphaBravoIndiaRomeo"

MATRIX_GREEN = "#00FF41"

root = tk.Tk()
root.title("DEFCON TERMINAL")
root.configure(bg="black")
root.attributes('-fullscreen', True)

current_frame = None
current_user = None
users = {}
saved_encryptions = []

def load_data():
    global users, saved_encryptions
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                users = data.get('users', {})
                saved_encryptions = data.get('saved_encryptions', [])
        except:
            pass
    if VALID_ADMIN_ID not in users:
        users[VALID_ADMIN_ID] = VALID_ADMIN_PW
        save_data()

def save_data():
    data = {'users': users, 'saved_encryptions': saved_encryptions}
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

load_data()

def clear_screen():
    global current_frame
    if current_frame:
        current_frame.destroy()

def kill_program(event=None):
    if messagebox.askyesno("TERMINATE", "Terminate DEFCON session?"):
        root.destroy()

root.bind('<Escape>', kill_program)

class MatrixRain:
    def __init__(self, canvas):
        self.canvas = canvas
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        self.columns = self.width // 20
        self.drops = [random.randint(-50, 0) for _ in range(self.columns)]
        self.running = True
        self.animate()

    def animate(self):
        if not self.running: return
        self.canvas.delete("rain")
        for i in range(self.columns):
            x = i * 20
            self.drops[i] += 1
            y = self.drops[i] * 20
            char = random.choice("01")
            self.canvas.create_text(x, y, text=char, fill=MATRIX_GREEN,
                                  font=("Courier", 16, "bold"), tags="rain")
            if y > self.height and random.random() > 0.975:
                self.drops[i] = random.randint(-20, 0)
        self.canvas.after(50, self.animate)

def typewriter(label, text, speed=30, callback=None):
    def write(i=0):
        if i <= len(text):
            label.config(text=text[:i])
            label.after(speed, lambda: write(i + 1))
        else:
            if callback: callback()
    write()

# =====================================
# REGISTRATION
# =====================================

def register_user():
    reg_win = tk.Toplevel(root)
    reg_win.title("Register New User")
    reg_win.configure(bg="black")
    reg_win.geometry("520x420")

    tk.Label(reg_win, text="CREATE NEW OPERATOR ACCOUNT", fg=MATRIX_GREEN, bg="black",
             font=("Courier", 16, "bold")).pack(pady=20)

    tk.Label(reg_win, text="Username:", fg=MATRIX_GREEN, bg="black", font=("Courier", 12)).pack(anchor="w", padx=50)
    new_user_entry = tk.Entry(reg_win, width=30, font=("Courier", 12), bg="#021602", fg=MATRIX_GREEN)
    new_user_entry.pack(pady=5)

    tk.Label(reg_win, text="Password:", fg=MATRIX_GREEN, bg="black", font=("Courier", 12)).pack(anchor="w", padx=50)
    new_pass_entry = tk.Entry(reg_win, width=30, show="*", font=("Courier", 12), bg="#021602", fg=MATRIX_GREEN)
    new_pass_entry.pack(pady=5)

    tk.Label(reg_win, text="Confirm Password:", fg=MATRIX_GREEN, bg="black", font=("Courier", 12)).pack(anchor="w", padx=50)
    confirm_pass_entry = tk.Entry(reg_win, width=30, show="*", font=("Courier", 12), bg="#021602", fg=MATRIX_GREEN)
    confirm_pass_entry.pack(pady=5)

    def submit_registration():
        username = new_user_entry.get().strip()
        password = new_pass_entry.get().strip()
        confirm = confirm_pass_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Error", "All fields are required")
            return
        if password != confirm:
            messagebox.showwarning("Error", "Passwords do not match")
            return
        if username in users:
            messagebox.showerror("Error", "Username already exists")
            return
        if len(username) < 3:
            messagebox.showwarning("Error", "Username must be at least 3 characters")
            return

        users[username] = password
        save_data()
        messagebox.showinfo("Success", f"User '{username}' created successfully!\nYou can now login.")
        reg_win.destroy()

    tk.Button(reg_win, text="CREATE ACCOUNT", command=submit_registration,
              bg="#003300", fg=MATRIX_GREEN, font=("Courier", 12, "bold")).pack(pady=25)

# =====================================
# LOGIN
# =====================================

def verify_login():
    global current_user
    user = user_entry.get().strip()
    pw = pass_entry.get().strip()
    if user in users and users[user] == pw:
        current_user = user
        show_boot_sequence()
    else:
        messagebox.showerror("ACCESS DENIED", "INVALID CREDENTIALS")

def guest_mode():
    global current_user
    current_user = "GUEST"
    show_boot_sequence()

def show_login():
    global current_frame, user_entry, pass_entry
    clear_screen()
    login = tk.Frame(root, bg="black")
    login.pack(fill="both", expand=True)
    current_frame = login

    tk.Label(login, text="DEFCON SECURE TERMINAL", fg=MATRIX_GREEN, bg="black",
             font=("Courier", 28, "bold")).pack(pady=50)

    tk.Label(login, text="OPERATOR ID", fg=MATRIX_GREEN, bg="black", font=("Courier", 14)).pack()
    user_entry = tk.Entry(login, width=35, font=("Courier", 14), bg="#021602", fg=MATRIX_GREEN, insertbackground=MATRIX_GREEN)
    user_entry.pack(pady=10)

    tk.Label(login, text="ACCESS KEY", fg=MATRIX_GREEN, bg="black", font=("Courier", 14)).pack()
    pass_entry = tk.Entry(login, show="*", width=35, font=("Courier", 14), bg="#021602", fg=MATRIX_GREEN, insertbackground=MATRIX_GREEN)
    pass_entry.pack(pady=10)

    tk.Button(login, text="AUTHORIZE", command=verify_login,
              bg="#003300", fg=MATRIX_GREEN, font=("Courier", 14, "bold")).pack(pady=10)

    tk.Button(login, text="REGISTER NEW USER", command=register_user,
              bg="#003300", fg="#00FF41", font=("Courier", 12, "bold")).pack(pady=8)

    tk.Button(login, text="GUEST MODE", command=guest_mode,
              bg="#003300", fg="#00FF41", font=("Courier", 12, "bold")).pack(pady=8)

    tk.Label(login, text="Anyone can register or use Guest Mode", fg="#555555", bg="black", font=("Courier", 10)).pack(pady=10)

# =====================================
# BOOT SEQUENCE
# =====================================

def show_boot_sequence():
    global current_frame
    clear_screen()
    boot = tk.Frame(root, bg="black")
    boot.pack(fill="both", expand=True)
    current_frame = boot

    canvas = tk.Canvas(boot, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    MatrixRain(canvas)

    title = tk.Label(boot, text="", fg=MATRIX_GREEN, bg="black", font=("Courier", 24, "bold"))
    title.place(relx=0.5, rely=0.3, anchor="center")

    messages = ["CONNECTING TO DEFCON SERVER...", "AUTHENTICATING OPERATOR...",
                "ESTABLISHING ENCRYPTED TUNNEL...", "ACCESS LEVEL: OMEGA", "CONNECTED"]

    def next_message(index=0):
        if index >= len(messages):
            if current_user == VALID_ADMIN_ID:
                boot.after(1500, show_admin_control)
            else:
                boot.after(1500, show_user_control)
            return
        typewriter(title, messages[index], 35, lambda: boot.after(900, lambda: next_message(index + 1)))
    next_message()

# =====================================
# ADMIN CONTROL
# =====================================

def show_admin_control():
    global current_frame
    clear_screen()
    control = tk.Frame(root, bg="black")
    control.pack(fill="both", expand=True)
    current_frame = control

    tk.Label(control, text=f"ADMIN CONTROL — {current_user.upper()}", 
             fg=MATRIX_GREEN, bg="black", font=("Courier", 26, "bold")).pack(pady=40)

    btn_frame = tk.Frame(control, bg="black")
    btn_frame.pack(expand=True)

    big_btn_style = {"bg": "#003300", "fg": MATRIX_GREEN, "font": ("Courier", 16, "bold"), "width": 28, "height": 3}

    tk.Button(btn_frame, text="ENCRYPTOR / DECRYPTER", command=launch_terminal, **big_btn_style).pack(pady=12)
    tk.Button(btn_frame, text="MANAGE USERS", command=show_user_management, **big_btn_style).pack(pady=12)
    tk.Button(btn_frame, text="ENCRYPTED KEYS", command=show_encrypted_keys, **big_btn_style).pack(pady=12)

    tk.Button(control, text="LOGOUT", command=show_login,
              bg="#003300", fg=MATRIX_GREEN, font=("Courier", 12, "bold")).pack(pady=10)
    tk.Button(control, text="TERMINATE SESSION", command=kill_program,
              bg="#330000", fg="#FF6666", font=("Courier", 12, "bold")).pack(pady=10)

# =====================================
# USER CONTROL
# =====================================

def show_user_control():
    global current_frame
    clear_screen()
    control = tk.Frame(root, bg="black")
    control.pack(fill="both", expand=True)
    current_frame = control

    tk.Label(control, text=f"CONTROL PANEL — {current_user.upper()}", 
             fg=MATRIX_GREEN, bg="black", font=("Courier", 26, "bold")).pack(pady=40)

    btn_frame = tk.Frame(control, bg="black")
    btn_frame.pack(expand=True)

    big_btn_style = {"bg": "#003300", "fg": MATRIX_GREEN, "font": ("Courier", 16, "bold"), "width": 28, "height": 3}

    tk.Button(btn_frame, text="ENCRYPTOR / DECRYPTER", command=launch_terminal, **big_btn_style).pack(pady=15)
    tk.Button(btn_frame, text="SAVED ENCRYPTED KEYS", command=show_encrypted_keys, **big_btn_style).pack(pady=15)

    tk.Button(control, text="LOGOUT", command=show_login,
              bg="#003300", fg=MATRIX_GREEN, font=("Courier", 12, "bold")).pack(side="bottom", pady=30)

# =====================================
# ENCRYPTED KEYS (User-specific + Delete)
# =====================================

def show_encrypted_keys():
    global current_frame
    clear_screen()
    keys_page = tk.Frame(root, bg="black")
    keys_page.pack(fill="both", expand=True)
    current_frame = keys_page

    is_admin = current_user == VALID_ADMIN_ID
    title = "ALL ENCRYPTED KEYS" if is_admin else "MY ENCRYPTED KEYS"
    tk.Label(keys_page, text=title, fg=MATRIX_GREEN, bg="black", font=("Courier", 22, "bold")).pack(pady=15)

    tree = ttk.Treeview(keys_page, columns=("ID", "Time", "User", "Preview"), show="headings", height=18)
    tree.heading("ID", text="ID")
    tree.heading("Time", text="Timestamp")
    tree.heading("User", text="User")
    tree.heading("Preview", text="Message Preview")
    tree.pack(fill="both", expand=True, padx=30, pady=10)

    style = ttk.Style()
    style.configure("Treeview", background="#021602", foreground=MATRIX_GREEN, fieldbackground="#021602")

    filtered = saved_encryptions if is_admin else [e for e in saved_encryptions if e.get('user') == current_user]

    for idx, enc in enumerate(filtered):
        preview = (enc['message'][:60] + "...") if len(enc['message']) > 60 else enc['message']
        tree.insert("", "end", values=(idx+1, enc['timestamp'], enc.get('user', 'N/A'), preview))

    def view_key():
        sel = tree.selection()
        if not sel: 
            messagebox.showwarning("Select", "Select an entry")
            return
        idx = int(tree.item(sel[0])['values'][0]) - 1
        enc = filtered[idx]
        win = tk.Toplevel(root)
        win.configure(bg="black")
        for label, key in [("ORIGINAL", "message"), ("CIPHER", "cipher"), ("KEY", "key")]:
            tk.Label(win, text=label, fg=MATRIX_GREEN, bg="black", font=("Courier", 12, "bold")).pack(anchor="w", padx=15, pady=(10,0))
            t = tk.Text(win, height=6, bg="#021602", fg=MATRIX_GREEN)
            t.insert("1.0", enc[key])
            t.pack(fill="x", padx=15, pady=5)

    def delete_key():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select an entry to delete")
            return
        if messagebox.askyesno("Confirm Delete", "Delete this encrypted key permanently?"):
            idx = int(tree.item(sel[0])['values'][0]) - 1
            original_idx = saved_encryptions.index(filtered[idx])
            del saved_encryptions[original_idx]
            save_data()
            show_encrypted_keys()

    tk.Button(keys_page, text="VIEW SELECTED", command=view_key, bg="#003300", fg=MATRIX_GREEN, font=("Courier", 12, "bold")).pack(pady=5)
    tk.Button(keys_page, text="DELETE SELECTED", command=delete_key, bg="#330000", fg="#FF6666", font=("Courier", 12, "bold")).pack(pady=5)

    back_cmd = show_admin_control if is_admin else show_user_control
    back_text = "← BACK TO ADMIN CONTROL" if is_admin else "← BACK TO CONTROL PANEL"
    tk.Button(keys_page, text=back_text, command=back_cmd,
              bg="#003300", fg=MATRIX_GREEN, font=("Courier", 12, "bold")).pack(pady=10)

# =====================================
# USER MANAGEMENT (Admin Only)
# =====================================

def show_user_management():
    global current_frame
    clear_screen()
    um = tk.Frame(root, bg="black")
    um.pack(fill="both", expand=True)
    current_frame = um

    tk.Label(um, text="USER MANAGEMENT", fg=MATRIX_GREEN, bg="black", font=("Courier", 22, "bold")).pack(pady=15)

    tk.Label(um, text="REGISTERED OPERATORS", fg=MATRIX_GREEN, bg="black", font=("Courier", 14, "bold")).pack(anchor="w", padx=30)

    list_frame = tk.Frame(um, bg="black")
    list_frame.pack(fill="both", expand=True, padx=30, pady=5)

    user_list = tk.Listbox(list_frame, bg="#021602", fg=MATRIX_GREEN, font=("Courier", 12), selectbackground="#00FF41")
    user_list.pack(side="left", fill="both", expand=True)

    for u in users:
        user_list.insert(tk.END, u)

    details_frame = tk.LabelFrame(um, text="USER DETAILS", fg=MATRIX_GREEN, bg="black", font=("Courier", 12, "bold"))
    details_frame.pack(fill="x", padx=30, pady=10)

    selected_user_var = tk.StringVar()
    selected_pw_var = tk.StringVar()

    tk.Label(details_frame, text="Username:", fg=MATRIX_GREEN, bg="black").pack(anchor="w", padx=10)
    username_entry = tk.Entry(details_frame, textvariable=selected_user_var, font=("Courier", 12), bg="#021602", fg=MATRIX_GREEN)
    username_entry.pack(fill="x", padx=10, pady=2)

    pw_row = tk.Frame(details_frame, bg="black")
    pw_row.pack(fill="x", padx=10, pady=2)
    tk.Label(pw_row, text="Password:", fg=MATRIX_GREEN, bg="black").pack(anchor="w", side="left")
    pw_entry = tk.Entry(pw_row, textvariable=selected_pw_var, font=("Courier", 12), bg="#021602", fg=MATRIX_GREEN, show="*")
    pw_entry.pack(side="left", fill="x", expand=True, padx=(5,0))

    def toggle_password():
        pw_entry.config(show="" if pw_entry.cget("show") == "*" else "*")
    tk.Button(pw_row, text="👁", command=toggle_password, bg="#003300", fg=MATRIX_GREEN, width=3).pack(side="right", padx=5)

    def load_user_details():
        sel = user_list.curselection()
        if not sel: return
        username = user_list.get(sel[0])
        selected_user_var.set(username)
        selected_pw_var.set(users[username])

    def save_user_changes():
        sel = user_list.curselection()
        old_name = user_list.get(sel[0]) if sel else None
        new_name = selected_user_var.get().strip()
        new_pw = selected_pw_var.get().strip()
        if not new_name or not new_pw:
            messagebox.showwarning("Error", "Username and Password required")
            return
        if old_name and old_name != new_name and new_name in users:
            messagebox.showerror("Error", "Username already exists")
            return
        if old_name:
            if old_name != new_name:
                del users[old_name]
                idx = list(user_list.get(0, tk.END)).index(old_name)
                user_list.delete(idx)
                user_list.insert(idx, new_name)
            users[new_name] = new_pw
        else:
            users[new_name] = new_pw
            user_list.insert(tk.END, new_name)
        save_data()
        messagebox.showinfo("Success", "User updated")

    def remove_user():
        sel = user_list.curselection()
        if not sel: return
        username = user_list.get(sel[0])
        if username == VALID_ADMIN_ID:
            messagebox.showerror("Protected", "Cannot remove main admin")
            return
        if messagebox.askyesno("Confirm", f"Delete '{username}'?"):
            del users[username]
            user_list.delete(sel[0])
            save_data()
            messagebox.showinfo("Success", "User removed")

    tk.Button(details_frame, text="LOAD SELECTED", command=load_user_details, bg="#003300", fg=MATRIX_GREEN).pack(pady=5)
    tk.Button(details_frame, text="SAVE CHANGES", command=save_user_changes, bg="#003300", fg=MATRIX_GREEN).pack(pady=5)
    tk.Button(details_frame, text="REMOVE USER", command=remove_user, bg="#330000", fg="#FF6666").pack(pady=5)

    tk.Label(um, text="ADD NEW OPERATOR", fg=MATRIX_GREEN, bg="black", font=("Courier", 14, "bold")).pack(pady=(15,5))
    add_frame = tk.Frame(um, bg="black")
    add_frame.pack(fill="x", padx=30, pady=5)

    tk.Label(add_frame, text="Username:", fg=MATRIX_GREEN, bg="black").grid(row=0, column=0, sticky="w")
    new_user_e = tk.Entry(add_frame, width=30, font=("Courier", 12), bg="#021602", fg=MATRIX_GREEN)
    new_user_e.grid(row=0, column=1, padx=5)

    tk.Label(add_frame, text="Password:", fg=MATRIX_GREEN, bg="black").grid(row=1, column=0, sticky="w")
    new_pass_e = tk.Entry(add_frame, width=30, font=("Courier", 12), show="*", bg="#021602", fg=MATRIX_GREEN)
    new_pass_e.grid(row=1, column=1, padx=5)

    def add_new_user():
        nu = new_user_e.get().strip()
        np = new_pass_e.get().strip()
        if nu and np:
            if nu in users:
                messagebox.showerror("Error", "User already exists")
            else:
                users[nu] = np
                save_data()
                user_list.insert(tk.END, nu)
                messagebox.showinfo("Success", f"'{nu}' added")
                new_user_e.delete(0, tk.END)
                new_pass_e.delete(0, tk.END)
        else:
            messagebox.showwarning("Input", "Both fields required")

    tk.Button(add_frame, text="ADD OPERATOR", command=add_new_user, bg="#003300", fg=MATRIX_GREEN, font=("Courier", 12, "bold")).grid(row=2, column=1, pady=10, sticky="e")

    tk.Button(um, text="← BACK TO ADMIN CONTROL", command=show_admin_control,
              bg="#003300", fg=MATRIX_GREEN, font=("Courier", 12, "bold")).pack(pady=15)

# =====================================
# TERMINAL
# =====================================

THEMES = {
    "GREEN": {"bg": "#000000", "fg": "#00FF41", "panel": "#021602"},
    "AMBER": {"bg": "#000000", "fg": "#FFB000", "panel": "#1A1000"},
    "BLUE":  {"bg": "#000000", "fg": "#7AA2FF", "panel": "#081020"}
}
current_theme = "GREEN"

txt_plain = txt_cipher_out = txt_key_out = txt_cipher_in = txt_key_in = txt_plain_out = status_var = None

def change_theme(theme):
    global current_theme
    current_theme = theme
    launch_terminal()

def clear_terminal():
    for w in [txt_plain, txt_cipher_out, txt_key_out, txt_cipher_in, txt_key_in, txt_plain_out]:
        if w: w.delete("1.0", tk.END)
    if status_var: status_var.set("TERMINAL PURGED")

def otp_encrypt(message):
    key = secrets.token_bytes(len(message))
    cipher = [f"{ord(char) ^ k:02X}" for char, k in zip(message, key)]
    key_hex = [f"{k:02X}" for k in key]
    return "".join(cipher), "".join(key_hex)

def otp_decrypt(cipher_hex, key_hex):
    try:
        cipher_bytes = bytes.fromhex(cipher_hex)
        key_bytes = bytes.fromhex(key_hex)
        if len(cipher_bytes) != len(key_bytes):
            return "[ERROR: LENGTH MISMATCH]"
        return "".join(chr(c ^ k) for c, k in zip(cipher_bytes, key_bytes))
    except:
        return "[INVALID DATA]"

def encrypt_action():
    global saved_encryptions
    msg = txt_plain.get("1.0", tk.END).strip()
    if not msg:
        status_var.set("NO MESSAGE PROVIDED")
        return
    cipher, key = otp_encrypt(msg)
    txt_cipher_out.delete("1.0", tk.END)
    txt_key_out.delete("1.0", tk.END)
    txt_cipher_out.insert(tk.END, cipher)
    txt_key_out.insert(tk.END, key)

    saved_encryptions.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": msg,
        "cipher": cipher,
        "key": key,
        "user": current_user
    })
    save_data()
    status_var.set("ENCRYPTION COMPLETE & SAVED")

def decrypt_action():
    cipher = txt_cipher_in.get("1.0", tk.END).strip()
    key = txt_key_in.get("1.0", tk.END).strip()
    result = otp_decrypt(cipher, key)
    txt_plain_out.delete("1.0", tk.END)
    txt_plain_out.insert(tk.END, result)
    status_var.set("DECRYPTION COMPLETE")

def launch_terminal():
    global current_frame, txt_plain, txt_cipher_out, txt_key_out, txt_cipher_in, txt_key_in, txt_plain_out, status_var
    clear_screen()
    theme = THEMES[current_theme]
    terminal = tk.Frame(root, bg=theme["bg"])
    terminal.pack(fill="both", expand=True)
    current_frame = terminal

    tk.Label(terminal, text="DEFCON ENCRYPTION TERMINAL", fg=theme["fg"], bg=theme["bg"],
             font=("Courier", 18, "bold")).pack(fill="x", pady=10)

    controls = tk.Frame(terminal, bg=theme["bg"])
    controls.pack(fill="x")
    for color in ["GREEN", "AMBER", "BLUE"]:
        tk.Button(controls, text=color, command=lambda c=color: change_theme(c), bg="#003300", fg=MATRIX_GREEN).pack(side="left", padx=5)

    back_cmd = show_admin_control if current_user == VALID_ADMIN_ID else show_user_control
    tk.Button(controls, text="← CONTROL PANEL", command=back_cmd, bg="#003300", fg=MATRIX_GREEN).pack(side="right", padx=5)

    body = tk.Frame(terminal, bg=theme["bg"])
    body.pack(fill="both", expand=True, padx=20, pady=20)

    # Encrypt
    left = tk.LabelFrame(body, text="ENCRYPT", fg=theme["fg"], bg=theme["bg"])
    left.pack(side="left", fill="both", expand=True, padx=10)

    txt_plain = tk.Text(left, height=6, bg=theme["panel"], fg=theme["fg"], font=("Courier", 11))
    txt_plain.pack(fill="x", pady=5)
    tk.Button(left, text="ENCRYPT", command=encrypt_action, bg="#003300", fg=MATRIX_GREEN).pack(fill="x", pady=5)

    tk.Label(left, text="ENCRYPTED MESSAGE", fg=theme["fg"], bg=theme["bg"], font=("Courier", 11, "bold")).pack(anchor="w", padx=5)
    txt_cipher_out = tk.Text(left, height=8, bg=theme["panel"], fg=theme["fg"])
    txt_cipher_out.pack(fill="x", pady=2)

    tk.Label(left, text="OTP KEY", fg=theme["fg"], bg=theme["bg"], font=("Courier", 11, "bold")).pack(anchor="w", padx=5)
    txt_key_out = tk.Text(left, height=8, bg=theme["panel"], fg=theme["fg"])
    txt_key_out.pack(fill="x", pady=2)

    # Decrypt
    right = tk.LabelFrame(body, text="DECRYPT", fg=theme["fg"], bg=theme["bg"])
    right.pack(side="right", fill="both", expand=True, padx=10)

    tk.Label(right, text="ENCRYPTED SENTENCE", fg=theme["fg"], bg=theme["bg"], font=("Courier", 11, "bold")).pack(anchor="w", padx=5)
    txt_cipher_in = tk.Text(right, height=6, bg=theme["panel"], fg=theme["fg"])
    txt_cipher_in.pack(fill="x", pady=2)

    tk.Label(right, text="OTP KEY", fg=theme["fg"], bg=theme["bg"], font=("Courier", 11, "bold")).pack(anchor="w", padx=5)
    txt_key_in = tk.Text(right, height=6, bg=theme["panel"], fg=theme["fg"])
    txt_key_in.pack(fill="x", pady=2)

    tk.Button(right, text="DECRYPT", command=decrypt_action, bg="#003300", fg=MATRIX_GREEN).pack(fill="x", pady=5)
    txt_plain_out = tk.Text(right, height=12, bg=theme["panel"], fg=theme["fg"])
    txt_plain_out.pack(fill="x", pady=2)

    status_var = tk.StringVar(value="CONNECTED TO DEFCON SERVER")
    tk.Label(terminal, textvariable=status_var, fg=theme["fg"], bg=theme["bg"], anchor="w", font=("Courier", 10)).pack(fill="x", padx=10, pady=10)

# =====================================
# START
# =====================================

show_login()
root.mainloop()
