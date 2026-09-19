import tkinter as tk
from tkinter import messagebox, filedialog
import random


# -----------------------------
# Main Window
# -----------------------------
root = tk.Tk()
root.title("🎵 Music Playlist Manager")
root.geometry("700x650")
root.resizable(False, False)
root.configure(bg="#121212")


# -----------------------------
# Variables
# -----------------------------
playlist = []
current_index = -1


# -----------------------------
# Functions
# -----------------------------
def update_playlist():
    playlist_box.delete(0, tk.END)

    for i, song in enumerate(playlist):
        playlist_box.insert(tk.END, f"{i + 1}. {song}")

    count_label.config(text=f"🎵 Total Songs: {len(playlist)}")


def add_song():
    song = song_entry.get().strip()

    if not song:
        messagebox.showwarning("Empty", "Please enter a song name.")
        return

    playlist.append(song)
    song_entry.delete(0, tk.END)

    update_playlist()


def remove_song():
    selected = playlist_box.curselection()

    if not selected:
        messagebox.showwarning("Select Song", "Please select a song to remove.")
        return

    index = selected[0]
    playlist.pop(index)

    update_playlist()
    current_label.config(text="🎶 No song selected")


def select_song(event=None):
    global current_index

    selected = playlist_box.curselection()

    if not selected:
        return

    current_index = selected[0]
    song = playlist[current_index]

    current_label.config(text=f"🎶 Now Selected: {song}")


def next_song():
    global current_index

    if not playlist:
        messagebox.showwarning("Empty Playlist", "Add some songs first.")
        return

    current_index = (current_index + 1) % len(playlist)

    playlist_box.selection_clear(0, tk.END)
    playlist_box.selection_set(current_index)
    playlist_box.see(current_index)

    current_label.config(
        text=f"🎶 Now Selected: {playlist[current_index]}"
    )


def previous_song():
    global current_index

    if not playlist:
        messagebox.showwarning("Empty Playlist", "Add some songs first.")
        return

    current_index = (current_index - 1) % len(playlist)

    playlist_box.selection_clear(0, tk.END)
    playlist_box.selection_set(current_index)
    playlist_box.see(current_index)

    current_label.config(
        text=f"🎶 Now Selected: {playlist[current_index]}"
    )


def shuffle_playlist():
    global current_index

    if not playlist:
        messagebox.showwarning("Empty Playlist", "Add some songs first.")
        return

    random.shuffle(playlist)
    current_index = -1

    update_playlist()
    current_label.config(text="🔀 Playlist Shuffled!")


def search_song():
    search_text = search_entry.get().strip().lower()

    if not search_text:
        update_playlist()
        return

    playlist_box.delete(0, tk.END)

    found = False

    for i, song in enumerate(playlist):
        if search_text in song.lower():
            playlist_box.insert(tk.END, f"{i + 1}. {song}")
            found = True

    if not found:
        playlist_box.insert(tk.END, "❌ No song found")


def save_playlist():
    if not playlist:
        messagebox.showwarning("Empty Playlist", "There are no songs to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )

    if not file_path:
        return

    with open(file_path, "w", encoding="utf-8") as file:
        for song in playlist:
            file.write(song + "\n")

    messagebox.showinfo("Saved", "Playlist saved successfully! 🎵")


def load_playlist():
    global playlist, current_index

    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )

    if not file_path:
        return

    with open(file_path, "r", encoding="utf-8") as file:
        playlist = [line.strip() for line in file if line.strip()]

    current_index = -1

    update_playlist()
    current_label.config(text="🎶 Playlist Loaded!")

    messagebox.showinfo("Loaded", "Playlist loaded successfully! 🎵")


def clear_playlist():
    global playlist, current_index

    if not playlist:
        return

    answer = messagebox.askyesno(
        "Clear Playlist",
        "Are you sure you want to clear the playlist?"
    )

    if answer:
        playlist.clear()
        current_index = -1

        update_playlist()
        current_label.config(text="🎶 No song selected")


# -----------------------------
# Title
# -----------------------------
title_label = tk.Label(
    root,
    text="🎵 Music Playlist Manager",
    font=("Arial", 24, "bold"),
    bg="#121212",
    fg="white"
)
title_label.pack(pady=(20, 5))


subtitle = tk.Label(
    root,
    text="Create • Manage • Shuffle • Save",
    font=("Arial", 11),
    bg="#121212",
    fg="#aaaaaa"
)
subtitle.pack(pady=(0, 15))


# -----------------------------
# Add Song Section
# -----------------------------
input_frame = tk.Frame(root, bg="#121212")
input_frame.pack(pady=5)


song_entry = tk.Entry(
    input_frame,
    width=38,
    font=("Arial", 12),
    bg="#242424",
    fg="white",
    insertbackground="white",
    relief="flat"
)
song_entry.grid(row=0, column=0, padx=5, ipady=8)


add_button = tk.Button(
    input_frame,
    text="➕ Add Song",
    command=add_song,
    font=("Arial", 10, "bold"),
    bg="#1db954",
    fg="white",
    activebackground="#1ed760",
    relief="flat",
    padx=15,
    pady=8
)
add_button.grid(row=0, column=1, padx=5)


# -----------------------------
# Search Section
# -----------------------------
search_frame = tk.Frame(root, bg="#121212")
search_frame.pack(pady=12)


search_entry = tk.Entry(
    search_frame,
    width=35,
    font=("Arial", 11),
    bg="#242424",
    fg="white",
    insertbackground="white",
    relief="flat"
)
search_entry.grid(row=0, column=0, padx=5, ipady=6)


search_button = tk.Button(
    search_frame,
    text="🔍 Search",
    command=search_song,
    font=("Arial", 10, "bold"),
    bg="#333333",
    fg="white",
    activebackground="#444444",
    relief="flat",
    padx=15,
    pady=6
)
search_button.grid(row=0, column=1, padx=5)


# -----------------------------
# Playlist Box
# -----------------------------
playlist_box = tk.Listbox(
    root,
    width=62,
    height=13,
    font=("Arial", 12),
    bg="#1e1e1e",
    fg="white",
    selectbackground="#1db954",
    selectforeground="white",
    relief="flat",
    activestyle="none"
)
playlist_box.pack(pady=8)

playlist_box.bind("<<ListboxSelect>>", select_song)


# -----------------------------
# Current Song
# -----------------------------
current_label = tk.Label(
    root,
    text="🎶 No song selected",
    font=("Arial", 12, "bold"),
    bg="#121212",
    fg="#1db954"
)
current_label.pack(pady=5)


# -----------------------------
# Navigation Buttons
# -----------------------------
control_frame = tk.Frame(root, bg="#121212")
control_frame.pack(pady=10)


previous_button = tk.Button(
    control_frame,
    text="⏮ Previous",
    command=previous_song,
    font=("Arial", 10, "bold"),
    bg="#333333",
    fg="white",
    relief="flat",
    padx=12,
    pady=7
)
previous_button.grid(row=0, column=0, padx=5)


next_button = tk.Button(
    control_frame,
    text="Next ⏭",
    command=next_song,
    font=("Arial", 10, "bold"),
    bg="#333333",
    fg="white",
    relief="flat",
    padx=12,
    pady=7
)
next_button.grid(row=0, column=1, padx=5)


shuffle_button = tk.Button(
    control_frame,
    text="🔀 Shuffle",
    command=shuffle_playlist,
    font=("Arial", 10, "bold"),
    bg="#333333",
    fg="white",
    relief="flat",
    padx=12,
    pady=7
)
shuffle_button.grid(row=0, column=2, padx=5)


remove_button = tk.Button(
    control_frame,
    text="🗑 Remove",
    command=remove_song,
    font=("Arial", 10, "bold"),
    bg="#8b2e2e",
    fg="white",
    relief="flat",
    padx=12,
    pady=7
)
remove_button.grid(row=0, column=3, padx=5)


# -----------------------------
# File Buttons
# -----------------------------
file_frame = tk.Frame(root, bg="#121212")
file_frame.pack(pady=5)


save_button = tk.Button(
    file_frame,
    text="💾 Save Playlist",
    command=save_playlist,
    font=("Arial", 10, "bold"),
    bg="#333333",
    fg="white",
    relief="flat",
    padx=15,
    pady=7
)
save_button.grid(row=0, column=0, padx=5)


load_button = tk.Button(
    file_frame,
    text="📂 Load Playlist",
    command=load_playlist,
    font=("Arial", 10, "bold"),
    bg="#333333",
    fg="white",
    relief="flat",
    padx=15,
    pady=7
)
load_button.grid(row=0, column=1, padx=5)


clear_button = tk.Button(
    file_frame,
    text="🧹 Clear All",
    command=clear_playlist,
    font=("Arial", 10, "bold"),
    bg="#8b2e2e",
    fg="white",
    relief="flat",
    padx=15,
    pady=7
)
clear_button.grid(row=0, column=2, padx=5)


# -----------------------------
# Song Counter
# -----------------------------
count_label = tk.Label(
    root,
    text="🎵 Total Songs: 0",
    font=("Arial", 10),
    bg="#121212",
    fg="#aaaaaa"
)
count_label.pack(pady=8)


# -----------------------------
# Start Application
# -----------------------------
root.mainloop()