import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter.filedialog import askdirectory
from tkinter import Tk
import tkinter.font as tkfont
import yt_dlp
import os

def resize_window(width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

window = tk.Tk()
window.title("YouTube Downloader")
resize_window(400,200)
window.wm_iconbitmap("youtube.ico")
window.resizable(False, False)
window.configure(bg="#3e4359")

#Frame for YouTube URL and Resolution Dropdown
top_frame = tk.Frame(window, bg="#3e4359")
top_frame.pack(fill="x", padx=10, pady=(40,0))

#Frame to display size of the video
middle_frame = tk.Frame(window, bg="#3e4359")
middle_frame.pack(fill="x", pady=(10, 0))

#Frame to download the Video
bottom_frame = tk.Frame(window, bg="#3e4359")
bottom_frame.pack(fill="x", pady=10)

normal_font = tkfont.Font(family="Arial", size=10, weight=tkfont.NORMAL)
button_font = tkfont.Font(family="Arial", size=10, weight=tkfont.BOLD)

##Top Frame

#URL configuration
inputbox_url = tk.Entry(top_frame, font=normal_font, width=35)
inputbox_url.pack(side="left", padx=(10,0))

#Resolution configuration
dropdown_res = ttk.Combobox(top_frame, font=normal_font, width=15)
dropdown_res.pack(side="left", padx=(10,0))

##Middle Frame
#Show Video Size
label_video_size = tk.Label(middle_frame, text="Welcome to YouTube Downloader", font=normal_font, bg="#3e4359", fg="#ffffff")
label_video_size.pack(pady=(2,2))

#Bottom Frame
#Download Button

format_id_list = []

# Function to display available streams
def list_streams():
    label_video_size.config(text="Fetching Resolution and Size...")
    try:
        url = inputbox_url.get()
        stream_details = []
        global format_id_list

        if url != "":
            ydl_opts = {
                'listformats': True,
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                for fmt in info['formats']:
                    if fmt.get('vcodec') != 'none' and fmt.get('acodec') == 'none' and fmt.get('filesize'):
                        resolution = fmt.get('height', 'Unknown')
                        size_mb = round(fmt.get('filesize', 0) / (1024 * 1024), 2)
                        stream_details.append(f"{resolution} -> {size_mb}mb")
                        format_id_list.append(fmt['format_id'])

                dropdown_res["values"] = stream_details

            label_video_size.config(text="Resolutions and size fetched")
        else:
            showinfo("Error", "URL not provided")
    except Exception as e:
        showinfo("Error", f"An error occurred: {e}")

# Function to download the chosen video
def download_video(url, chosen_format_id, save_path):
    label_video_size.config(text="Downloading...")
    ydl_opts = {
        'format': chosen_format_id,
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    label_video_size.config(text=f"Downloaded successfully and saved")
    global format_id_list
    format_id_list = []

def get_download_directory():
    Tk().withdraw()
    directory = askdirectory(title="Select Download Directory")
    return directory if directory else os.getcwd()

def download():
    try:
        url = inputbox_url.get()
        global format_id_list
        if url != "":
            if format_id_list:
                selected_index = dropdown_res.current()
                download_directory = get_download_directory

                if selected_index != -1:
                    download_video(url, format_id_list[selected_index], download_directory)
                else:
                    download_video(url, format_id_list[len(format_id_list) - 1], download_directory)
            else:
                showinfo("Error", "Please click 'Get Res and Size'")

            download_directory = get_download_directory()
            ydl_opts = {
                'outtmpl': f'{download_directory}/%(title)s.%(ext)s',
                'format': 'bestvideo+bestaudio/best',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        else:
            showinfo("Error", "URL not provided")
    except Exception as e:
        showinfo("Error", f"An error occurred: {e}")


button_get_resolution = tk.Button(bottom_frame, text="Get Res and Size", font=button_font, bg="#000000", fg="#ffffff", command=list_streams, cursor="hand2", padx=10, pady=2)
button_get_resolution.pack(side="left", padx=(80,10))
button_download = tk.Button(bottom_frame, text="Download", font=button_font, bg="#f03c18", fg="#ffffff", command=download, cursor="hand2", padx=10, pady=2)
button_download.pack(side="left", padx=10)


window.mainloop()