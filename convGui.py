import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

from converter import encode_text_in_image, decode_text_from_image

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TextToPixels")
        self.root.geometry("600x500")


        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))


        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        self.encode_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.encode_frame, text="Encode")
        self.create_encode_tab()


        self.decode_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.decode_frame, text="Decode")
        self.create_decode_tab()

    def create_encode_tab(self):

        ttk.Label(self.encode_frame, text="Select Cover Image:").pack(pady=(10,0))
        self.encode_img_path = tk.StringVar()
        self.encode_img_button = ttk.Button(
            self.encode_frame, 
            text="Browse Image", 
            command=self.select_encode_image
        )
        self.encode_img_button.pack(pady=5)


        self.encode_img_preview = ttk.Label(self.encode_frame)
        self.encode_img_preview.pack(pady=5)


        ttk.Label(self.encode_frame, text="Enter Secret Text:").pack(pady=(10,0))
        self.secret_text = tk.Text(
            self.encode_frame, 
            height=4, 
            width=50
        )
        self.secret_text.pack(pady=5)


        ttk.Label(self.encode_frame, text="Save Encoded Image:").pack(pady=(10,0))
        self.output_img_path = tk.StringVar()
        self.output_img_button = ttk.Button(
            self.encode_frame, 
            text="Choose Save Location", 
            command=self.select_output_image
        )
        self.output_img_button.pack(pady=5)


        self.encode_button = ttk.Button(
            self.encode_frame, 
            text="Encode Image", 
            command=self.perform_encoding
        )
        self.encode_button.pack(pady=10)

    def create_decode_tab(self):

        ttk.Label(self.decode_frame, text="Select Encoded Image:").pack(pady=(10,0))
        self.decode_img_path = tk.StringVar()
        self.decode_img_button = ttk.Button(
            self.decode_frame, 
            text="Browse Image", 
            command=self.select_decode_image
        )
        self.decode_img_button.pack(pady=5)


        self.decode_img_preview = ttk.Label(self.decode_frame)
        self.decode_img_preview.pack(pady=5)


        ttk.Label(self.decode_frame, text="Decoded Message:").pack(pady=(10,0))
        self.decoded_text = tk.Text(
            self.decode_frame, 
            height=6, 
            width=50, 
            state='disabled'
        )
        self.decoded_text.pack(pady=5)


        self.decode_button = ttk.Button(
            self.decode_frame, 
            text="Decode Image", 
            command=self.perform_decoding
        )
        self.decode_button.pack(pady=10)

    def select_encode_image(self):
        filepath = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if filepath:
            self.encode_img_path.set(filepath)

            img = Image.open(filepath)
            img.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(img)
            self.encode_img_preview.config(image=photo)
            self.encode_img_preview.image = photo

    def select_output_image(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        if filepath:
            self.output_img_path.set(filepath)

    def select_decode_image(self):
        filepath = filedialog.askopenfilename(
            title="Select Encoded Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if filepath:
            self.decode_img_path.set(filepath)

            img = Image.open(filepath)
            img.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(img)
            self.decode_img_preview.config(image=photo)
            self.decode_img_preview.image = photo

    def perform_encoding(self):
        try:
            input_path = self.encode_img_path.get()
            output_path = self.output_img_path.get()
            secret_text = self.secret_text.get("1.0", tk.END).strip()

            if not input_path or not output_path or not secret_text:
                messagebox.showerror("Error", "Please fill all fields")
                return

            encode_text_in_image(input_path, secret_text, output_path)
            messagebox.showinfo("Success", f"Text encoded in {os.path.basename(output_path)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def perform_decoding(self):
        try:
            input_path = self.decode_img_path.get()
            if not input_path:
                messagebox.showerror("Error", "Please select an image")
                return

            decoded_text = decode_text_from_image(input_path)
            

            self.decoded_text.config(state='normal')
            self.decoded_text.delete('1.0', tk.END)
            self.decoded_text.insert(tk.END, decoded_text)
            self.decoded_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()