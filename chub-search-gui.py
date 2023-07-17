import tkinter as tk
import os
import re
import json
from PIL import Image, ImageTk
import base64
import platform

# Obtain subdirectories
def get_subdirectories(path):
    subdirectories = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            subdirectories.append(item)
    return subdirectories

# Show the image for the character card in the subdirectory
def show_image(subdirectory):
    current_directory = os.getcwd()
    image_path = os.path.join(current_directory, subdirectory)
    image_files = [filename for filename in os.listdir(image_path) if filename.endswith('.png')]
    if image_files:
        image_file = image_files[0]
        image = Image.open(os.path.join(image_path, image_file))
        image.thumbnail((300, 300))  # Resize the image
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo
        canvas.bind("<Button-1>", lambda event: open_subdirectory(subdirectory))
        show_metadata(subdirectory, image)
    else:
        canvas.delete("all")  # Clear the canvas if no image found
        clear_metadata()

# Display the relevant metadata from metadata.json in the subdirectory
def show_metadata(subdirectory, image):
    metadata_file = os.path.join(subdirectory, "metadata.json")
    if os.path.isfile(metadata_file):
        with open(metadata_file) as f:
            metadata = json.load(f)
            description = metadata.get("description")
            tagline = metadata.get("tagline")
            topics = ", ".join(metadata.get("topics", []))
            card_data = base64.b64decode(image.info['chara'])
            card_parsed = json.loads(card_data)
            card_name = card_parsed.get("data", []).get("name")
            card_creator = card_parsed.get("data", []).get("creator")
            card_creator_notes = card_parsed.get("data", []).get("creator_notes")
            card_tags = ", ".join(card_parsed.get("data", []).get("tags", []))
            card_description = card_parsed.get("data", []).get("description")
            card_first_mes = card_parsed.get("data", []).get("first_mes")
            card_example = card_parsed.get("data", []).get("mes_example")
            card_scenario = card_parsed.get("data", []).get("scenario")
            card_system_prompt = card_parsed.get("data", []).get("system_prompt")
            card_related_lorebooks = ", ".join(card_parsed.get("data", []).get("related_lorebooks", []))
            card_expressions = ", ".join(card_parsed.get("data", []).get("expressions", []))
            card_spec = card_parsed.get("data", []).get("spec")
            card_spec_version = card_parsed.get("data", []).get("spec_version")
            metadata_text.config(state=tk.NORMAL)
            metadata_text.delete("1.0", tk.END)
            metadata_text.insert(tk.END, f"---------- JSON DATA ----------\n\n")
            metadata_text.insert(tk.END, f"Description: {description}\n\n")
            metadata_text.insert(tk.END, f"Tagline: {tagline}\n\n")
            metadata_text.insert(tk.END, f"Topics: {topics}\n\n")
            metadata_text.insert(tk.END, f"---------- CARD DATA ----------\n\n")
            metadata_text.insert(tk.END, f"Name: {card_name}\n\n")
            metadata_text.insert(tk.END, f"Creator: {card_creator}\n\n")
            metadata_text.insert(tk.END, f"Creator Notes: {card_creator_notes}\n\n")
            metadata_text.insert(tk.END, f"Tags: {card_tags}\n\n")
            metadata_text.insert(tk.END, f"Description:\n{card_description}\n\n")
            metadata_text.insert(tk.END, f"First Message:\n{card_first_mes}\n\n")
            metadata_text.insert(tk.END, f"Example Messages:\n{card_example}\n\n")
            metadata_text.insert(tk.END, f"Scenario: {card_scenario}\n\n")
            metadata_text.insert(tk.END, f"System Prompt:\n{card_system_prompt}\n\n")
            metadata_text.insert(tk.END, f"Related Lorebooks: {card_related_lorebooks}\n\n")
            metadata_text.insert(tk.END, f"Expressions: {card_expressions}\n\n")
            metadata_text.insert(tk.END, f"Card Spec: {card_spec}\n\n")
            metadata_text.insert(tk.END, f"Card Spec Version: {card_spec_version}\n\n")
            metadata_text.config(state=tk.DISABLED)
    else:
        clear_metadata()

# Self explanatory
def clear_metadata():
    metadata_text.config(state=tk.NORMAL)
    metadata_text.delete("1.0", tk.END)
    metadata_text.config(state=tk.DISABLED)

# Search subdirectories and relevant metadata
def filter_subdirectories(search_term):
    filtered_subdirectories = []
    for subdirectory in subdirectories:
        metadata_file = os.path.join(subdirectory, "metadata.json")
        if os.path.isfile(metadata_file):
            with open(metadata_file) as f:
                metadata = json.load(f)
                if (
                    re.search(search_term, metadata.get("description", ""), re.IGNORECASE)
                    or re.search(search_term, metadata.get("tagline", ""), re.IGNORECASE)
                    or any(re.search(search_term, topic, re.IGNORECASE) for topic in metadata.get("topics", []))
                ):
                    filtered_subdirectories.append(subdirectory)
    return filtered_subdirectories

# Update the listbox with the search terms
def update_listbox(event=None):
    search_term = search_entry.get()
    filtered_subdirectories = filter_subdirectories(search_term)
    listbox.delete(0, tk.END)  # Clear the listbox
    for subdirectory in filtered_subdirectories:
        listbox.insert(tk.END, subdirectory)

# Open the subdirectory when the user clicks on the image
def open_subdirectory(subdirectory):
    current_directory = os.getcwd()
    subdirectory_path = os.path.join(current_directory, subdirectory)
    if platform.system() == "Windows":
        os.startfile(subdirectory_path)  # Open the subdirectory on Windows
    elif platform.system() == "Linux":
        os.system(f"xdg-open '{subdirectory_path}'")  # Open the subdirectory on Linux

# Update when the user selects a subdirectory
def on_select(event):
    widget = event.widget
    selection = widget.curselection()
    if selection:
        index = int(selection[0])
        subdirectory = widget.get(index)
        show_image(subdirectory)

# Set title
root = tk.Tk()
root.title("Chub Archive Search GUI")

# Create a search bar
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Search:")
search_label.pack(side=tk.LEFT)

search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side=tk.LEFT)
search_entry.bind("<KeyRelease>", update_listbox)

# Create a scrollbar for the listbox
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a listbox
listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)
listbox.bind("<<ListboxSelect>>", on_select)

# Create a canvas for the image display
canvas = tk.Canvas(root, width=300, height=300)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a frame for metadata display
metadata_frame = tk.Frame(root)
metadata_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

metadata_label = tk.Label(metadata_frame, text="Metadata:")
metadata_label.pack(pady=10)

metadata_text = tk.Text(metadata_frame, wrap=tk.WORD, state=tk.DISABLED)
metadata_text.pack(fill=tk.BOTH, expand=True)

# Get the subdirectories in the current directory
current_directory = os.getcwd()
subdirectories = get_subdirectories(current_directory)

# Sort the subdirectories alphabetically
subdirectories.sort()

# Add subdirectories to the listbox
for subdirectory in subdirectories:
    listbox.insert(tk.END, subdirectory)

# Configure the scrollbar
scrollbar.config(command=listbox.yview)

# Start the tkinter event loop
root.mainloop()
