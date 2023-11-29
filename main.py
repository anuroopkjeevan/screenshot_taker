import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab
import requests
import json

class ScreenshotApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Screenshot Uploader")

        # Create labels and entry widgets for user input
        tk.Label(self.master, text="Application Name:").pack()
        self.app_name_entry = tk.Entry(self.master)
        self.app_name_entry.pack()

        tk.Label(self.master, text="Phone:").pack()  # Changed label to "Phone"
        self.phone_entry = tk.Entry(self.master)     # Changed entry variable to "phone_entry"
        self.phone_entry.pack()

        tk.Button(self.master, text="Take Screenshot", command=self.take_and_upload).pack()

    def take_and_upload(self):
        app_name = self.app_name_entry.get()
        phone = self.phone_entry.get()  # Changed variable name to "phone"

        if not app_name or not phone:
            messagebox.showerror("Error", "Please enter Application Name and Phone.")
            return

        try:
            screenshot = ImageGrab.grab()
            screenshot_path = "screenshot.png"
            screenshot.save(screenshot_path)

            api_url = "https://trogon.info/interview/python/index.php"
            files = {'image': open(screenshot_path, 'rb')}
            data = {'remarks': app_name, 'phone': phone}  # Changed variable name to "phone"

            response = requests.post(api_url, files=files, data=data)
            self.handle_api_response(response)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def handle_api_response(self, response):
        try:
            api_response = response.json()

            if api_response["status"] == "success":
                file_path = api_response["data"]["file_path"]
                remarks = api_response["data"]["remarks"]
                phone = api_response["data"]["phone"]
                timestamp = api_response["data"]["timestamp"]

                message = f"File uploaded successfully\nFile Path: {file_path}\nRemarks: {remarks}\nPhone: {phone}\nTimestamp: {timestamp}"
                messagebox.showinfo("Success", message)

            else:
                error_message = f"API Error: {api_response['message']}"
                messagebox.showerror("API Error", error_message)

        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to parse API response.")

def run_application():
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_application()
