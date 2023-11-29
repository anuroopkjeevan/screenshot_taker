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

        tk.Label(self.master, text="Unique Identifier:").pack()
        self.unique_id_entry = tk.Entry(self.master)
        self.unique_id_entry.pack()

        # Create a button to take a screenshot and upload
        tk.Button(self.master, text="Take Screenshot", command=self.take_and_upload).pack()

    def take_and_upload(self):
        # Get the application name and unique identifier from the entry widgets
        app_name = self.app_name_entry.get()
        unique_id = self.unique_id_entry.get()

        if not app_name or not unique_id:
            messagebox.showerror("Error", "Please enter Application Name and Unique Identifier.")
            return

        try:
            # Take a screenshot
            screenshot = ImageGrab.grab()

            # Save the screenshot locally
            screenshot_path = "screenshot.png"
            screenshot.save(screenshot_path)

            # Prepare data for API request
            api_url = "https://trogon.info/interview/python/index.php"
            files = {'image': open(screenshot_path, 'rb')}
            data = {'remarks': app_name, 'phone': unique_id}

            # Make the API request
            response = requests.post(api_url, files=files, data=data)

            # Process the API response
            self.handle_api_response(response)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def handle_api_response(self, response):
        try:
            # Parse the JSON response
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
