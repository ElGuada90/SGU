# Importacion de librerias
import customtkinter as ctk

# temas y apariencia
ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# definir función
def button_callback():
    print("button clicked")

app = ctk.CTk()
app.geometry("400x150")

button = ctk.CTkButton(app, text="my button", command=button_callback)
button.pack(padx=20, pady=20)

app.mainloop()





