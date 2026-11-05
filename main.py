import customtkinter

def button_callback():
    print("button pressed")

app = customtkinter.CTk()
app.title("JustConvertIt")
app.geometry("400x150")

button = customtkinter.CTkButton(app, text="my button", command=button_callback)
# button.grid(row=0, column=0, padx=20, pady=20)

# make the button the whole width of the window
button.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

# center the button
app.grid_columnconfigure(0, weight=1)

app.mainloop()