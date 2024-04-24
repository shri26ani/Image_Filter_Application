import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps





class PhotoEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Editor Pro")

        self.image_path = None
        self.original_image = None
        self.display_image = None

        # Menu bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        # Menu bar consists of two sections
        # section 1: File
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        # section 2: Edit
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Blur", command=self.apply_filter)
        edit_menu.add_command(label="Sharpen", command=self.sharpen_image)
        edit_menu.add_command(label="Invert Colors", command=self.invert_colors)
        edit_menu.add_command(label="Rotate 90°", command=self.rotate_image)
        edit_menu.add_command(label="Resize", command=self.resize_image)

        edit_menu.add_separator()

        edit_menu.add_command(label="Sharpness", command=self.adjust_sharpness)
        edit_menu.add_command(label="Contrast", command=self.adjust_contrast)
        edit_menu.add_command(label="Brightness", command=self.adjust_brightness)

        edit_menu.add_separator()

        edit_menu.add_command(label="Reset", command=self.reset_image)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Canvas to display image
        self.canvas = tk.Canvas(root, bd=0, highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Sliders for adjustments


        self.sharpness_slider = tk.Scale(root, from_=0.5, to=2, resolution=0.05, orient=tk.HORIZONTAL,
                                         label="Sharpness",
                                         command=self.apply_sharpness)
        self.sharpness_slider.set(1.0)  # Set the default position to 1.0
        self.sharpness_slider.pack()

        self.contrast_slider = tk.Scale(root, from_=0.5, to=2, resolution=0.05, orient=tk.HORIZONTAL, label="Contrast",
                                        command=self.apply_contrast)
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack()

        self.brightness_slider = tk.Scale(root, from_=0.5, to=2, resolution=0.05, orient=tk.HORIZONTAL,
                                          label="Brightness", command=self.apply_brightness)
        self.brightness_slider.set(1.0)
        self.brightness_slider.pack()

        # Done buttons
        self.sharpness_done_button = tk.Button(root, text="Done", command=self.done_sharpness)
        self.sharpness_done_button.pack()



    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            self.display_image = ImageTk.PhotoImage(self.original_image)
            self.canvas.config(width=self.display_image.width(), height=self.display_image.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)

    def save_image(self):
        if self.original_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.original_image.save(file_path)
                messagebox.showinfo("Save", f"Image saved to {file_path}")

    def apply_filter(self):
        try:
            if self.original_image:
                self.original_image = self.original_image.filter(ImageFilter.BLUR)
                self.update_display_image()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def sharpen_image(self):
        try:
            if self.original_image:
                self.original_image = self.original_image.filter(ImageFilter.SHARPEN)
                self.update_display_image()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def invert_colors(self):
        try:
            if self.original_image:
                self.original_image = ImageOps.invert(self.original_image)
                self.update_display_image()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def rotate_image(self):
        try:
            if self.original_image:
                self.original_image = self.original_image.rotate(90)
                self.update_display_image()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def resize_image(self):
        try:
            if self.original_image:
                x  = self.original_image.size
                message_width = f"Original image size is {x}. Enter the new width"
                message_height = f"Original image size is {x}. Enter the new height"

                new_width = simpledialog.askinteger("Resize Image", message_width)
                new_height = simpledialog.askinteger("Resize Image", message_height)
                if new_width and new_height:
                    self.original_image = self.original_image.resize((new_width, new_height))
                    self.update_display_image()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def reset_image(self):
        if self.image_path:
            self.original_image = Image.open(self.image_path)
            self.update_display_image()

    def adjust_sharpness(self):
        self.sharpness_slider.set(1.0)
        self.sharpness_slider.pack()
        self.sharpness_done_button.pack()

    def done_sharpness(self):

        self.update_display_image()

    def apply_sharpness(self, value):
        try:
            if self.original_image:
                sharpness_factor = float(value)
                self.original_image = ImageEnhance.Sharpness(self.original_image).enhance(sharpness_factor)
                # Do not call update_display_image here to allow real-time adjustment
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def adjust_contrast(self):
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack()
        self.sharpness_done_button.pack()

    def done_contrast(self):

        self.update_display_image()

    def apply_contrast(self, value):
        try:
            if self.original_image:
                contrast_factor = float(value)
                self.original_image = ImageEnhance.Contrast(self.original_image).enhance(contrast_factor)
                # Do not call update_display_image here to allow real-time adjustment
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def adjust_brightness(self):
        self.brightness_slider.set(1.0)
        self.brightness_slider.pack()
        self.sharpness_done_button.pack()

    def done_brightness(self):

        self.update_display_image()

    def apply_brightness(self, value):
        try:
            if self.original_image:
                brightness_factor = float(value)
                self.original_image = ImageEnhance.Brightness(self.original_image).enhance(brightness_factor)
                # Do not call update_display_image here to allow real-time adjustment
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")



    def update_display_image(self):
        self.display_image = ImageTk.PhotoImage(self.original_image)

        canvas_width = max(512, self.display_image.width())
        canvas_height = max(512, self.display_image.height())

        # Calculate position to center the image
        x_position = (canvas_width - self.display_image.width()) / 2
        y_position = (canvas_height - self.display_image.height()) / 2

        self.canvas.config(width=canvas_width, height=canvas_height)
        self.canvas.create_image(x_position, y_position, anchor=tk.NW, image=self.display_image)



def login():
    username = "Deepak"
    password = "1234"

    if username_entry.get()==username and password_entry.get()==password:
        messagebox.showinfo(title="Login Successful!", message="You successfully logged in.")
        root = tk.Tk()
        app = PhotoEditorApp(root)



    else:
        messagebox.showerror(title="Error", message="Invalid login.")

frame = tk.Frame(bg='#544163')

login_label = tk.Label(frame, text="Login Page Using Python", bg='#544163', fg="#DC143C", font=("Arial", 30))
username_label = tk.Label(frame, text="Username", bg='#8F00FF', fg="#FFFFFF", font=("Arial", 16, 'bold'))
password_label = tk.Label(frame, text="Password", bg='#8F00FF', fg="#FFFFFF", font=("Arial", 16, 'bold'))

username_entry = tk.Entry(frame, font=("Arial", 16))
password_entry = tk.Entry(frame, show="*", font=("Arial", 16))

login_button = tk.Button(frame, text="Login", bg="#544163", fg="#FFFFFF", font=("Arial", 16), command=login)

login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=30)



if __name__ == "__main__":
    window = tk.Tk()
    window.title("Login Page using Python")
    window.geometry('750x550')
    window.configure(bg='#544163')
    frame.pack()
    window.mainloop()