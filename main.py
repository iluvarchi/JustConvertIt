import os
import cv2
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, showerror
from customtkinter import CTk, CTkButton, CTkTextbox, CTkFrame, CTkSlider, CTkLabel

# create the root window
root = CTk()
root.title("JustConvertIt")
root.resizable(False, False)
root._set_appearance_mode("dark")

# window height and width
app_width = 500
app_height = 550

# holds the picked file path and the chosen save folder
selected_file = ""
output_folder = ""

# to center the window 
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# helper to change the text in a locked/disabled text box
def set_textbox(box, text):
    box.configure(state="normal")
    # clear all contents from line 0, character 0 ("0.0") to the end
    box.delete("0.0", "end")
    box.insert("0.0", text)
    box.configure(state="disabled")

# helper to get the folder files will be saved in
def get_save_folder():
    if output_folder:
        return output_folder
    return os.path.dirname(selected_file)

# helper to build the full save path
def build_output_path(suffix, ext):
    base = os.path.splitext(os.path.basename(selected_file))[0]
    return os.path.join(get_save_folder(), f"{base}{suffix}{ext}")

# turn buttons/sliders on or off based on the file type
def update_controls():
    ext = os.path.splitext(selected_file)[1].lower() if selected_file else ""
    is_jpg = ext in (".jpg", ".jpeg")
    is_png = ext == ".png"
    supported = is_jpg or is_png

    jpg_to_png_button.configure(state="normal" if is_jpg else "disabled")
    png_to_jpg_button.configure(state="normal" if is_png else "disabled")
    quality_slider.configure(state="normal" if is_jpg else "disabled")
    size_slider.configure(state="normal" if supported else "disabled")
    compress_file_button.configure(state="normal" if supported else "disabled")

    if is_jpg:
        info_label.configure(
            text="JPG selected: you can convert to PNG, or compress as JPG "
                 "using both sliders."
        )
    elif is_png:
        info_label.configure(
            text="PNG selected: you can convert to JPG, or compress as PNG. "
                 "Quality is off because PNG is lossless. Lower the Size "
                 "slider to shrink the file."
        )
    elif selected_file:
        info_label.configure(
            text="This file type isn't supported. Pick a JPG or PNG."
        )
    else:
        info_label.configure(text="Open a JPG or PNG file to get started.")

# one frame that holds everything, centered in the window
container = CTkFrame(root, fg_color="transparent")
container.pack(expand=True)

# text box to show the selected file's name and path
selected_file_textbox = CTkTextbox(
    master=container,
    width=350,
    height=60,
    corner_radius=10,
    border_width=2,
    border_color="#ea2845",
    text_color=("black", "white"),
    font=("Helvetica", 14),
    wrap="word"
)
selected_file_textbox.pack(pady=(0, 10))
selected_file_textbox.insert("0.0", "No file selected")
selected_file_textbox.configure(state="disabled")

# text box to show where the file will be saved
output_path_textbox = CTkTextbox(
    master=container,
    width=350,
    height=60,
    corner_radius=10,
    border_width=2,
    border_color="#ea2845",
    text_color=("black", "white"),
    font=("Helvetica", 14),
    wrap="word"
)
output_path_textbox.pack(pady=(0, 10))
output_path_textbox.insert("0.0", "Save folder: same folder as the original")
output_path_textbox.configure(state="disabled")

# message that tells the user what works for the selected file
info_label = CTkLabel(
    container,
    text="",
    font=("Helvetica", 14, "italic"),
    wraplength=350,
    justify="center",
    text_color="white"
)

# open file functionality
def select_file():
    global selected_file
    filetypes = (
        ("png files", "*.png"),
        ("jpeg files", "*.jpg"),
        ("All files", "*.*")
    )

    path = fd.askopenfilename(
        title="Open a file",
        initialdir="/",
        filetypes=filetypes
    )

    # only save if user didn't hit cancel
    if path:
        selected_file = path
        set_textbox(
            selected_file_textbox,
            f"Name: {os.path.basename(path)}\nPath: {path}"
        )
        # if no custom folder was picked, show the original's folder
        if not output_folder:
            set_textbox(
                output_path_textbox,
                f"Save folder: {os.path.dirname(path)}"
            )
        update_controls()

# choose where to save functionality
def select_output_folder():
    global output_folder

    folder = fd.askdirectory(
        title="Choose where to save",
        initialdir=os.path.dirname(selected_file) if selected_file else "/"
    )

    # only save if user didn't hit cancel
    if folder:
        output_folder = folder
        set_textbox(output_path_textbox, f"Save folder: {folder}")

# function to convert jpg to png
def convert_jpg_to_png():
    if not selected_file:
        showerror(title="Error", message="Pick a file first.")
        return

    try:
        image = cv2.imread(selected_file)

        if image is None:
            showerror(title="Error", message="Couldn't read that file as an image.")
            return

        output_path = build_output_path("", ".png")
        success = cv2.imwrite(output_path, image)

        if success:
            showinfo(
                title="Status",
                message=f"Image converted and saved successfully!\n\nSaved as:\n{output_path}"
            )
        else:
            showerror(title="Error", message="Couldn't save the image.")

    except Exception as e:
        showerror(title="Error", message=f"Something went wrong: {e}")

# function to convert png to jpg
def convert_png_to_jpg():
    if not selected_file:
        showerror(title="Error", message="Pick a file first.")
        return

    try:
        image = cv2.imread(selected_file)

        if image is None:
            showerror(title="Error", message="Couldn't read that file as an image.")
            return

        output_path = build_output_path("", ".jpg")
        success = cv2.imwrite(output_path, image)

        if success:
            showinfo(
                title="Status",
                message=f"Image converted and saved successfully!\n\nSaved as:\n{output_path}"
            )
        else:
            showerror(title="Error", message="Couldn't save the image.")

    except Exception as e:
        showerror(title="Error", message=f"Something went wrong: {e}")

# function to compress the image using the slider values
def compress_image():
    if not selected_file:
        showerror(title="Error", message="Pick a file first.")
        return

    ext = os.path.splitext(selected_file)[1].lower()
    if ext not in (".jpg", ".jpeg", ".png"):
        showerror(title="Error", message="Only JPG and PNG files can be compressed.")
        return

    try:
        image = cv2.imread(selected_file)

        if image is None:
            showerror(title="Error", message="Couldn't read that file as an image.")
            return

        quality = int(quality_slider.get())
        scale = int(size_slider.get())

        # shrink the image if size is below 100%
        if scale < 100:
            new_w = max(1, int(image.shape[1] * scale / 100))
            new_h = max(1, int(image.shape[0] * scale / 100))
            image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

        output_path = build_output_path("_compressed", ext)

        if ext == ".png":
            params = [cv2.IMWRITE_PNG_COMPRESSION, 9]
        else:
            params = [cv2.IMWRITE_JPEG_QUALITY, quality]

        success = cv2.imwrite(output_path, image, params)

        if success:
            before = os.path.getsize(selected_file) / 1024
            after = os.path.getsize(output_path) / 1024
            showinfo(
                title="Status",
                message=f"Compressed!\n\nBefore: {before:.1f} KB\nAfter: {after:.1f} KB\n\nSaved as:\n{output_path}"
            )
        else:
            showerror(title="Error", message="Couldn't save the image.")

    except Exception as e:
        showerror(title="Error", message=f"Something went wrong: {e}")

# open file button
open_button = CTkButton(
    container,
    text="Open a File",
    fg_color="#ea2845",
    font=("Helvetica", 14, "bold"),
    hover_color="#8c192a",
    command=select_file
)

# choose save folder button
output_folder_button = CTkButton(
    container,
    text="Choose Save Folder",
    fg_color="#ea2845",
    font=("Helvetica", 14, "bold"),
    hover_color="#8c192a",
    command=select_output_folder
)

# jpg to png convert button
jpg_to_png_button = CTkButton(
    container,
    text="Convert JPEG/JPG to PNG",
    fg_color="#ea2845",
    font=("Helvetica", 14, "bold"),
    hover_color="#8c192a",
    command=convert_jpg_to_png
)

# png to jpg convert button
png_to_jpg_button = CTkButton(
    container,
    text="Convert PNG to JPEG/JPG",
    fg_color="#ea2845",
    font=("Helvetica", 14, "bold"),
    hover_color="#8c192a",
    command=convert_png_to_jpg
)

# quality slider (JPG only)
quality_label = CTkLabel(container, text="Quality: 80 (JPG only)", font=("Helvetica", 14))
quality_slider = CTkSlider(
    container,
    from_=1,
    to=100,
    number_of_steps=99,
    button_color="#ea2845",
    button_hover_color="#8c192a",
    command=lambda v: quality_label.configure(text=f"Quality: {int(v)} (JPG only)")
)
quality_slider.set(80)

# size slider (JPG and PNG)
size_label = CTkLabel(container, text="Size: 100%", font=("Helvetica", 14))
size_slider = CTkSlider(
    container,
    from_=10,
    to=100,
    number_of_steps=90,
    button_color="#ea2845",
    button_hover_color="#8c192a",
    command=lambda v: size_label.configure(text=f"Size: {int(v)}%")
)
size_slider.set(100)

# compress button
compress_file_button = CTkButton(
    container,
    text="Compress File",
    fg_color="#ea2845",
    font=("Helvetica", 14, "bold"),
    hover_color="#8c192a",
    command=compress_image
)

# layout
info_label.pack(pady=(0, 10))
open_button.pack(pady=5)
output_folder_button.pack(pady=5)
jpg_to_png_button.pack(pady=5)
png_to_jpg_button.pack(pady=5)
quality_label.pack(pady=(10, 0))
quality_slider.pack()
size_label.pack(pady=(10, 0))
size_slider.pack()
compress_file_button.pack(pady=15)

# set the starting state (everything off until a file is picked)
update_controls()

center_window(root, app_width, app_height)

root.mainloop()