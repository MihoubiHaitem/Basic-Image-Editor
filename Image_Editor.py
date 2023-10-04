import tkinter as tk
from tkinter import filedialog, messagebox as msgb
from PIL import Image, ImageTk
from PIL.ExifTags import TAGS

class ImageEditor:
    def __init__(self):
        # Main parameters:
        self.root = tk.Tk()
        #self.root.geometry("900x800")
        self.root.title("Image Metadata Viewer and Editor")
        self.label_title = tk.Label(text="Welcome To Image Metadata Viewer and Editor")
        self.label_title.config(pady=20)
        self.label_title.grid(row=0, column=0, columnspan=2, sticky="ew", padx=45)
        self.image = self.img_display = self.image_path = self.x_dim = self.y_dim = None
        self.metadata = {}
        self.image_all = None

        # Creating labels widgets and buttons widgets:
        self.select_btn = tk.Button(self.root, text="Select", width=110, height=4, command=self.select_file)
        self.select_btn.grid(row=1, column=0, columnspan=2, sticky="ew", padx=45)

        self.rotate_btn = tk.Button(self.root, text="Rotate", width=50, height=3, command=self.rotate_image)
        self.rotate_btn.grid(row=2, column=0, columnspan=1, sticky="ew", padx=45)

        self.resize_btn = tk.Button(self.root, text="Resize", width=50, height=3, command=self.resizing_image)
        self.resize_btn.grid(row=2, column=1, columnspan=1, sticky="ew", padx=45)

        self.grayscale_btn = tk.Button(self.root, text="Grayscale", width=50, height=3, command=self.grayscale)
        self.grayscale_btn.grid(row=3, column=0, columnspan=1, sticky="ew", padx=45)

        self.blackwhite_btn = tk.Button(self.root, text="Black & white", width=50, height=3, command=self.black_white)
        self.blackwhite_btn.grid(row=3, column=1, columnspan=1, sticky="ew", padx=45)

        self.original_btn = tk.Button(self.root, text="Original Image", width=50, height=3, command=self.original_img)
        self.original_btn.grid(row=4, column=0, columnspan=1, sticky="ew", padx=45)

        self.display_btn = tk.Button(self.root, text="Display Image", width=50, height=3, command=self.display_image)
        self.display_btn.grid(row=4, column=1, columnspan=1, sticky="ew", padx=45)

        self.save_btn = tk.Button(self.root, text="Save", width=110, height=4, command=self.save_image)
        self.save_btn.grid(row=5, column=0, columnspan=2, sticky="ew", padx=45)

        self.metadata_btn = tk.Button(self.root, text="Metadata", width=110, height=4, command=self.md_image)
        self.metadata_btn.grid(row=6, column=0, columnspan=2, sticky="ew", padx=45)

        # Creating Canvas
        self.canvas1 = tk.Canvas(self.root, width=400, height=300)
        self.canvas1.grid(row=7, column=0, columnspan=1, sticky="ew")

        self.canvas2 = tk.Canvas(self.root, width=400, height=300)
        self.canvas2.grid(row=7, column=1, columnspan=1, sticky="ew")

        # Start main loop
        self.root.mainloop()

    # Select function to select the image from a file:
    def select_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.image_path = filepath
            self.image_all = Image.open(self.image_path)
            self.display_image1(filepath)

    # Function to display the selected image on the right side of the canvas:
    def display_image1(self, path):
        img = Image.open(path)
        img = img.resize((300, 250))
        self.image = ImageTk.PhotoImage(img)
        # Display image:
        self.canvas1.create_image((200, 150), image=self.image)

    # Rotate function to rotate the image:
    def rotate_image(self):
        """
        image_changed
        """
        if self.image_path:
            # Rotating the image:
            self.image_all = self.image_all.transpose(Image.ROTATE_90)
            #self.image_all.show()
        else:
            msgb.showerror(title="error", message="Please choose an image")

    # Function to display the edited image on the left side:
    def display_image(self):
        if self.image_path:
            img = self.image_all.resize((300, 250))
            self.img_display = ImageTk.PhotoImage(img)
            # Clean the canvas before display the image:
            self.canvas2.delete(tk.ALL)
            # Display image:
            self.canvas2.create_image((200, 150), image=self.img_display)
        else:
            msgb.showerror(title="error", message="Please choose an image")

    # Resizing function to resize the selected image:
    def resizing_image(self):
        # Create a popup window.
        popup = tk.Toplevel(self.root)
        if self.image_path:
            x_label = tk.Label(popup, text="Width Dimension:")
            x_label.pack()
            self.x_dim = tk.Entry(popup)
            self.x_dim.pack()
            y_label = tk.Label(popup, text="Height Dimension:")
            y_label.pack()
            self.y_dim = tk.Entry(popup)
            self.y_dim.pack()

            # Save the entered values from user:
            def save_value():
                x = self.x_dim.get()
                y = self.y_dim.get()
                if x and y:
                    # Resizing for the place:
                    self.image_all = self.image_all.resize((int(x), int(y)))
                    # self.image_all.show()

            buttonxy = tk.Button(popup, text="Save", command=save_value)
            buttonxy.pack()

        else:
            msgb.showerror(title="error", message="Please choose an image")
            return
        # Mainloop of popup
        popup.mainloop()

    def grayscale(self):
        if self.image_path:
            self.image_all = self.image_all.convert('L')
            # self.image_all.show()
        else:
            msgb.showerror(title="error", message="Please choose an image")

    def black_white(self):
        if self.image_path:
            self.image_all = self.image_all.convert('1')
            # self.image_all.show()
        else:
            msgb.showerror(title="error", message="Please choose an image")

    def original_img(self):
        if self.image_all:
            self.image_all = Image.open(self.image_path)
            pop_img = tk.Toplevel(self.root)
            execp_label = tk.Label(pop_img, text="Your image has been updated. \n", padx=40, pady=30)
            execp_label.pack()
            pop_img.mainloop()
        else:
            msgb.showerror(title="error", message="Please choose an image")

    def md_image(self):
        # Create a popup window.
        popup = tk.Toplevel(self.root)
        if self.image_path:
            image = Image.open(self.image_path)
            exif_data = image.getexif()
            image.close()
            metadata = {}
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                metadata[tag_name] = value

            if metadata:
                for tag_name, value in metadata.items():
                    md_label = tk.Label(popup, text=f"{tag_name}: {value} \n")
                    md_label.pack()
            else:
                md_label = tk.Label(popup, text="Can't read the MetaData from this picture \n")
                md_label.pack()
        else:
            execp_label = tk.Label(popup, text="Please choose an image \n")
            execp_label.pack()
        # Mainloop of popup
        popup.mainloop()

    # Save function to save the image in a folder:
    def save_image(self):
        if not self.image_all:
            msgb.showerror(title="error", message="Please choose an image")
            return
        self.image_all.save(filedialog.asksaveasfilename(), quality=100)


if __name__ == "__main__":
    app = ImageEditor()
