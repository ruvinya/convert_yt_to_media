import tkinter as tk
import pytube
import datetime 
import os

def convert_seconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    if minutes < 60:
        return "{:02d}:{:02d}".format(minutes, seconds) 
    else:
        hours, minutes = divmod(minutes, 60)
        return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds) 

def convert_bytes(num):
    mb = num / pow(1024,2)
    converted = "{:.2f}MB".format(mb)
    return converted

window = tk.Tk()
window.title("Youtube Media Downloader")
window.geometry('500x500')
window.configure(background='#4a9976')
window.minsize(500, 500)
window.maxsize(500, 500)

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_columnconfigure(3, weight=1)

# Title
title = tk.Label(window, text="YOUTUBE MEDIA DOWNLOADER", font=("Mohave Bold", 32))
title.configure(background='#4a9976')
title.grid(column=0, row=0, sticky=tk.EW, padx=5, columnspan=4)

# Link Entry
link_label = tk.Label(window, text="Youtube Link", font=("Mohave Medium Italic", 18))
link_label.configure(background='#4a9976')
link_label.grid(column=0, row=1, sticky=tk.EW, padx=5, columnspan=4)

yt_link = tk.StringVar()
link = tk.Entry(window, textvariable=yt_link, font=("Courier New", 16))
link.configure(background='#57806e')
link.grid(column=0, row=2, sticky=tk.EW, padx=5, columnspan=4)

# Preferences
preferences = tk.Label(window, text="Preferences", font=("Mohave SemiBold", 24))
preferences.configure(background='#4a9976')
preferences.grid(column=0, row=3, sticky=tk.EW, padx=5, columnspan=4)

# Path
path_label = tk.Label(window, text="Windows Users Folder Name (Needed for Download)", font=("Mohave Medium Italic", 15))
path_label.configure(background='#4a9976')
path_label.grid(column=0, row=4, sticky=tk.EW, padx=5, columnspan=4)

path_str = tk.StringVar()
path = tk.Entry(window, textvariable=path_str, font=("Courier New", 14))
path.configure(background='#57806e')
path.grid(column=0, row=5, sticky=tk.EW, padx=5, columnspan=4)

# Res Enable/Disable
def video_check(selection):
    if selection == "Video":
        res_opt.configure(state='normal')
    else:
        res_opt.configure(state='disabled')

# Dropdown Option Select
option_label = tk.Label(window, text="Option", font=("Mohave Medium Italic", 15))
option_label.configure(background='#4a9976')
option_label.grid(column=0, row=6, sticky=tk.EW, padx=5, pady=2)

variable = tk.StringVar(window)
variable.set("Video") # default value
option = tk.OptionMenu(window, variable, "Video", "Audio", command=video_check)
option.configure(background='#57806e', highlightbackground='#4a9976', width=7)
option.grid(column=0, row=7, sticky=tk.EW, padx=5)

# Dropdown Resolution Select
res_label = tk.Label(window, text="Resolution", font=("Mohave Medium Italic", 15))
res_label.configure(background='#4a9976')
res_label.grid(column=3, row=6, sticky=tk.EW, padx=5, pady=2)

res_var = tk.StringVar(window)
res_var.set("Highest") # default value
res_opt = tk.OptionMenu(window, res_var, "720p", "480p", "360p", "240p", "144p")
res_opt.configure(background='#57806e', highlightbackground='#4a9976', width=7)
res_opt.grid(column=3, row=7, sticky=tk.EW, padx=5)

result_var = tk.StringVar(window)

# Process Button
output = None
title = ""
def process():
    global output, title
    yt_obj = pytube.YouTube(yt_link.get())
    streamQuery_obj = yt_obj.streams
    if variable.get() == "Video":
        if res_var.get() == "Highest":
            output = streamQuery_obj.get_highest_resolution()
        else:
            output = streamQuery_obj.get_by_resolution(res_var.get())
    else:
        output = streamQuery_obj.get_audio_only()
    length = convert_seconds(yt_obj.length)
    size = convert_bytes(output.filesize)
    title = yt_obj.title
    post = (", " + (res_var.get() + "\n") if variable.get() == "Video" else ("\n"))
    pre = "Selected Options: " + variable.get() + post
    info = pre + "Title: " + title + "\n" + "Length: " + length + "\n" + "Size: " + size
    text.configure( state="normal")
    text.insert('1.0', info)
    text.configure( state="disabled")
    result_var.set("READY FOR DOWNLOAD!")

process_button = tk.Button(window, text="Process", command=lambda:process())
process_button.grid(column=0, row=8, padx=5, pady=35, sticky=tk.EW)
process_button.configure(background='#57806e', width=11, height=5)

# Description
text_label = res_label = tk.Label(window, text="Status", font=("Mohave Medium", 15))
text_label.configure(background='#4a9976')
text_label.grid(column=1, row=8, padx=5, sticky=tk.N, columnspan=2)

text = tk.Text(window, wrap='word', height=7, width=22)
text.configure(background='#57806e', state="disabled")
text.grid(column=1, row=8, ipadx=50, pady=5, sticky=tk.S, columnspan=2)

# Download Button
def download_file():
    down_dir = "C:\\Users\\" + path.get() + "\\" + "Downloads"
    cwd = os.getcwd()
    os.chdir(down_dir)
    # Remove if a file with same name exists
    if os.path.isfile(title + ".mp4"):
        os.remove(title + ".mp4")
    output.download(output_path=down_dir)
    os.rename(title + ".mp4", title + ".mp3")
    result_var.set("DOWNLOAD COMPLETED!")

download_button = tk.Button(window, text="Download", command=lambda:download_file())
download_button.grid(column=3, row=8, padx=5, pady=35, sticky=tk.EW)
download_button.configure(background='#57806e', width=11, height=5)

# Result 
result_label = res_label = tk.Label(window, textvariable=result_var, font=("Mohave Medium", 15))
result_label.configure(background='#4a9976', foreground="#23FF00")
result_label.grid(column=1, row=9, padx=5, sticky=tk.N, columnspan=2)

window.mainloop()