import os
import re
import tkinter as tk
from tkinter import messagebox, filedialog, Menu, Toplevel, Label
from tkinter import ttk
import webbrowser

# Function to move selected item up in the listbox
def move_up(listbox):
    selected_index = listbox.curselection()
    if not selected_index:
        return
    index = selected_index[0]
    if index == 0:
        return
    item = listbox.get(index)
    listbox.delete(index)
    listbox.insert(index - 1, item)
    listbox.select_set(index - 1)

# Function to move selected item down in the listbox
def move_down(listbox):
    selected_index = listbox.curselection()
    if not selected_index:
        return
    index = selected_index[0]
    if index == listbox.size() - 1:
        return
    item = listbox.get(index)
    listbox.delete(index)
    listbox.insert(index + 1, item)
    listbox.select_set(index + 1)

# Function to rename subtitle files to match video files
def rename_files():
    video_files = list(video_listbox.get(0, tk.END))
    subtitle_files = list(subtitle_listbox.get(0, tk.END))

    if len(video_files) != len(subtitle_files):
        messagebox.showerror("Error", "The number of video and subtitle files do not match.")
        return

    for video, subtitle in zip(video_files, subtitle_files):
        video_name, _ = os.path.splitext(video)
        subtitle_ext = os.path.splitext(subtitle)[1]
        new_subtitle_name = video_name + subtitle_ext
        try:
            os.rename(os.path.join(directory, subtitle), os.path.join(directory, new_subtitle_name))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename {subtitle} to {new_subtitle_name}: {e}")
            return

    messagebox.showinfo("Success", "Subtitle files have been renamed successfully.")
    root.quit()

# Function to select a folder and load files
def select_folder():
    global directory
    directory = filedialog.askdirectory()
    if not directory:
        return

    video_files = []
    subtitle_files = []
    for file in os.listdir(directory):
        if file.lower().endswith(('.mp4', '.mkv', '.avi')):
            video_files.append(file)
        elif file.lower().endswith(('.srt', '.sub')):
            subtitle_files.append(file)

    sorted_subtitles = sort_subtitles(video_files, subtitle_files)

    video_listbox.delete(0, tk.END)
    subtitle_listbox.delete(0, tk.END)

    for video in video_files:
        video_listbox.insert(tk.END, video)
    for subtitle in sorted_subtitles:
        subtitle_listbox.insert(tk.END, subtitle)

# Function to extract season and episode from filename
def extract_season_episode(filename):
    season_episode_match = re.search(r'[sS]eason\s?(\d+)[\s_]*[eE]pisode\s?(\d+)', filename)
    if not season_episode_match:
        season_episode_match = re.search(r'(\d+)[xX](\d+)', filename)
    if season_episode_match:
        season, episode = season_episode_match.groups()
        return int(season), int(episode)
    return None, None

# Function to sort subtitle files based on video files
def sort_subtitles(video_files, subtitle_files):
    sorted_subtitles = [''] * len(video_files)
    subtitle_dict = {}
    
    for subtitle in subtitle_files:
        season, episode = extract_season_episode(subtitle)
        if season is not None and episode is not None:
            subtitle_dict[(season, episode)] = subtitle
    
    for i, video in enumerate(video_files):
        season, episode = extract_season_episode(video)
        if (season, episode) in subtitle_dict:
            sorted_subtitles[i] = subtitle_dict[(season, episode)]
        else:
            sorted_subtitles[i] = "Missing subtitle"

    return sorted_subtitles

# Function to toggle dark mode
def toggle_dark_mode():
    # Change the theme to dark mode
    if dark_mode.get():
        root.configure(bg="#2e2e2e")
        video_listbox.configure(bg="gray25", fg="white")
        subtitle_listbox.configure(bg="gray25", fg="white")
        video_up_btn.configure(style="DarkMode.TButton")
        video_down_btn.configure(style="DarkMode.TButton")
        subtitle_up_btn.configure(style="DarkMode.TButton")
        subtitle_down_btn.configure(style="DarkMode.TButton")
        rename_btn.configure(style="DarkMode.TButton")
        folder_btn.configure(style="DarkMode.TButton")
    # Change the theme to light mode
    else:
        root.configure(bg="white")
        video_listbox.configure(bg="white", fg="black")
        subtitle_listbox.configure(bg="white", fg="black")
        video_up_btn.configure(style="TButton")
        video_down_btn.configure(style="TButton")
        subtitle_up_btn.configure(style="TButton")
        subtitle_down_btn.configure(style="TButton")
        rename_btn.configure(style="TButton")
        folder_btn.configure(style="TButton")

# Function to open a popup with credits information
def show_credits():
    credits_window = Toplevel(root)
    credits_window.title("Credits")
    credits_window.geometry("300x120")
    
    
    def open_website(url):
        webbrowser.open(url)
    
    ttk.Label(credits_window, text="GitHub:", font=("Arial", 10)).pack(pady=5)
    ttk.Label(credits_window, text="derpyymuffins", foreground="blue", cursor="hand2", font=("Arial", 10)).pack()
    ttk.Label(credits_window, text="Bluesky:", font=("Arial", 10)).pack(pady=5)
    ttk.Label(credits_window, text="d3rpy.bsky.social", foreground="blue", cursor="hand2", font=("Arial", 10)).pack()
    
    credits_window.pack_propagate(0)
    credits_window.pack_slaves()[1].bind("<Button-1>", lambda e: open_website("https://github.com/derpyymuffins"))
    credits_window.pack_slaves()[3].bind("<Button-1>", lambda e: open_website("https://d3rpy.bsky.social/"))

# Create main window
root = tk.Tk()
root.title("Simple Subtitle Renamer")

# Set default window size
root.geometry("800x400")

# Configure the grid to expand properly
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Menu Bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Dark Mode Toggle
view_menu = Menu(menu_bar, tearoff=0)
dark_mode = tk.BooleanVar(value=False)
view_menu.add_checkbutton(label="Dark Mode", onvalue=True, offvalue=False, variable=dark_mode, command=toggle_dark_mode)
menu_bar.add_cascade(label="View", menu=view_menu)

# Credits Button
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Credits", command=show_credits)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Listboxes & Scrollbars
video_listbox = tk.Listbox(root, selectmode=tk.SINGLE, bg="white", fg="black", relief="flat", highlightthickness=0)
subtitle_listbox = tk.Listbox(root, selectmode=tk.SINGLE, bg="white", fg="black", relief="flat", highlightthickness=0)
video_listbox.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
subtitle_listbox.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

# Up/Down Buttons - Video
video_up_btn = ttk.Button(root, text="▲", command=lambda: move_up(video_listbox), style="TButton")
video_down_btn = ttk.Button(root, text="▼", command=lambda: move_down(video_listbox), style="TButton")
video_up_btn.grid(row=1, column=0, sticky='w', padx=5)
video_down_btn.grid(row=1, column=0, sticky='e', padx=5)

# Up/Down Buttons - Subtitles
subtitle_up_btn = ttk.Button(root, text="▲", command=lambda: move_up(subtitle_listbox), style="TButton")
subtitle_down_btn = ttk.Button(root, text="▼", command=lambda: move_down(subtitle_listbox), style="TButton")
subtitle_up_btn.grid(row=1, column=1, sticky='w', padx=5)
subtitle_down_btn.grid(row=1, column=1, sticky='e', padx=5)

# Rename & Folder Buttons
rename_btn = ttk.Button(root, text="Rename", command=rename_files, style="TButton")
folder_btn = ttk.Button(root, text="Select Folder", command=select_folder, style="TButton")
rename_btn.grid(row=2, column=0, pady=10)
folder_btn.grid(row=2, column=1, pady=10)

# Main loop
root.mainloop()
