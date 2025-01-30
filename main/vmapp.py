import customtkinter as ctk
import tkinter.filedialog as fd
import subprocess
import tkinter as tk
from pynput import mouse, keyboard
from threading import Thread
import os

# Initialize the app
app = ctk.CTk()
app.geometry("500x600")
app.title("Modern VM Manager")

# Configuration variables
vm_name_var = ctk.StringVar()
iso_path_var = ctk.StringVar()
ram_var = ctk.IntVar(value=2048)  # Default to 2GB RAM
cpu_cores_var = ctk.IntVar(value=2)
disk_size_var = ctk.IntVar(value=20)  # Default to 20GB

# Function to browse for ISO
def browse_iso():
    iso_path = fd.askopenfilename(filetypes=[("ISO Files", "*.iso")])
    if iso_path:
        iso_path_var.set(iso_path)

# Function to run the VM in a new window
def run_vm():
    vm_name = vm_name_var.get()
    if not vm_name:
        ctk.CTkMessagebox.show_error("Error", "Please provide a VM name to run.")
        return

    try:
        subprocess.Popen(["VBoxManage", "startvm", vm_name, "--type", "gui"], shell=True)
    except subprocess.CalledProcessError as e:
        ctk.CTkMessagebox.show_error("Error", f"Failed to run VM: {e}")

# Fullscreen toggle
fullscreen = False

def toggle_fullscreen(event=None):
    global fullscreen
    fullscreen = not fullscreen
    app.attributes('-fullscreen', fullscreen)

# Mouse and Keyboard Detectors
def mouse_listener():
    def on_click(x, y, button, pressed):
        if pressed:
            print(f"Mouse clicked at ({x}, {y}) with {button}")

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


def keyboard_listener():
    def on_press(key):
        try:
            if key.char == 'f':
                toggle_fullscreen()
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Start mouse and keyboard listeners in background threads
Thread(target=mouse_listener, daemon=True).start()
Thread(target=keyboard_listener, daemon=True).start()

# Function to create the VM
def create_vm():
    vm_name = vm_name_var.get()
    iso_path = iso_path_var.get()
    ram_size = ram_var.get()
    cpu_cores = cpu_cores_var.get()
    disk_size = disk_size_var.get()

    if not (vm_name and iso_path):
        ctk.CTkMessagebox.show_error("Error", "Please provide a VM name and ISO path.")
        return

    try:
        # Example VirtualBox CLI commands
        subprocess.run(["VBoxManage", "createvm", "--name", vm_name, "--register"], check=True)
        subprocess.run(["VBoxManage", "modifyvm", vm_name, "--memory", str(ram_size), "--cpus", str(cpu_cores)], check=True)
        subprocess.run(["VBoxManage", "createhd", "--filename", f"{vm_name}.vdi", "--size", str(disk_size * 1024)], check=True)
        subprocess.run(["VBoxManage", "storagectl", vm_name, "--name", "SATA Controller", "--add", "sata"], check=True)
        subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", f"{vm_name}.vdi"], check=True)
        subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "1", "--device", "0", "--type", "dvddrive", "--medium", iso_path], check=True)

        ctk.CTkMessagebox.show_info("Success", f"VM '{vm_name}' created successfully!")
    except subprocess.CalledProcessError as e:
        ctk.CTkMessagebox.show_error("Error", f"Failed to create VM: {e}")

# UI Layout
ctk.CTkLabel(app, text="Virtual Machine Name:").pack(pady=10)
ctk.CTkEntry(app, textvariable=vm_name_var).pack(pady=5)

ctk.CTkLabel(app, text="Select ISO File:").pack(pady=10)
iso_frame = ctk.CTkFrame(app)
iso_frame.pack(pady=5, padx=10, fill="x")
ctk.CTkEntry(iso_frame, textvariable=iso_path_var, width=300).pack(side="left", padx=5)
ctk.CTkButton(iso_frame, text="Browse", command=browse_iso).pack(side="right", padx=5)

ctk.CTkLabel(app, text="RAM (MB):").pack(pady=10)
ctk.CTkSlider(app, from_=512, to=16384, variable=ram_var).pack(pady=5)

ctk.CTkLabel(app, text="CPU Cores:").pack(pady=10)
ctk.CTkSlider(app, from_=1, to=8, variable=cpu_cores_var).pack(pady=5)

ctk.CTkLabel(app, text="Disk Size (GB):").pack(pady=10)
ctk.CTkSlider(app, from_=10, to=200, variable=disk_size_var).pack(pady=5)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=20)
ctk.CTkButton(button_frame, text="Create VM", command=create_vm).pack(side="left", padx=10)
ctk.CTkButton(button_frame, text="Run VM", command=run_vm).pack(side="right", padx=10)

# Run the app
app.bind("<F>", toggle_fullscreen)
app.mainloop()
