import customtkinter as ctk
import pywinstyles

# Initialize the application
app = ctk.CTk()
app.geometry("800x600")
app.title("Modern VM Manager")

# Apply Windows 11 Mica style
pywinstyles.apply_style(app, style="mica")

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: "System", "Light", "Dark"
ctk.set_default_color_theme("blue")  # Themes: "blue", "dark-blue", "green"

# Create a frame for VM controls
frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Add widgets to the frame
label = ctk.CTkLabel(master=frame, text="Virtual Machine Name:")
label.pack(pady=12, padx=10)

entry = ctk.CTkEntry(master=frame)
entry.pack(pady=12, padx=10)

def create_vm():
    vm_name = entry.get()
    # Placeholder for VM creation logic using VirtualBox API
    print(f"Creating VM: {vm_name}")

button = ctk.CTkButton(master=frame, text="Create VM", command=create_vm)
button.pack(pady=12, padx=10)

# Run the application
app.mainloop()
