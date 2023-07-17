import tkinter as tk
from tkinter import font
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
        try:
            image = Image.open(os.path.join(image_path, image_file))
        except:
            print(f"Image failed to parse for subdirectory {subdirectory}")
            canvas.delete("all")
            clear_metadata()
            return
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
            card_personality = card_parsed.get("data", []).get("personality")
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
            metadata_text.insert(tk.END, f"---------- JSON DATA ----------\n\n", "custom_font")
            metadata_text.insert(tk.END, f"Description: {description}\n\n", "custom_font")
            metadata_text.insert(tk.END, f"Tagline: {tagline}\n\n", "custom_font")
            metadata_text.insert(tk.END, f"Topics: {topics}\n\n", "custom_font")
            metadata_text.insert(tk.END, f"---------- CARD DATA ----------\n\n", "custom_font")
            metadata_text.insert(tk.END, f"Name: {card_name}\n\n", "custom_font")
            metadata_text.insert(tk.END, f"Creator: {card_creator}\n\n", "custom_font")
            metadata_text.insert(tk.END, f"Creator Notes: {card_creator_notes}\n\n", "custom_font")
            metadata_text.insert(tk.END, f"Tags: {card_tags}\n\n", "custom_font")
            metadata_text.insert(tk.END, f"Personality: {card_personality}\n\n", "custom_font")
            metadata_text.insert(tk.END, f"Description:\n{card_description}\n\n", "custom_font")
            metadata_text.insert(tk.END, f"First Message:\n{card_first_mes}\n\n", "custom_font")
            metadata_text.insert(tk.END, f"Example Messages:\n{card_example}\n\n", "custom_font")
            metadata_text.insert(tk.END, f"Scenario: {card_scenario}\n\n", "custom_font")
            metadata_text.insert(tk.END, f"System Prompt:\n{card_system_prompt}\n\n", "custom_font")
            metadata_text.insert(tk.END, f"Related Lorebooks: {card_related_lorebooks}\n\n", "custom_font")
            metadata_text.insert(tk.END, f"Expressions: {card_expressions}\n\n", "custom_font")
            metadata_text.insert(tk.END, f"Card Spec: {card_spec}\n\n", "custom_font")
            metadata_text.insert(tk.END, f"Card Spec Version: {card_spec_version}\n\n", "custom_font")
            metadata_text.config(state=tk.DISABLED)
    else:
        clear_metadata()

# Self explanatory
def clear_metadata():
    metadata_text.config(state=tk.NORMAL)
    metadata_text.delete("1.0", tk.END)
    metadata_text.config(state=tk.DISABLED)

# Search subdirectories and relevant metadata
def filter_subdirectories(search_terms):
    filtered_subdirectories = []
    for subdirectory in subdirectories:
        metadata_file = os.path.join(subdirectory, "metadata.json")
        if (card_checkbox_var.get() == 1):
            current_directory = os.getcwd()
            image_path = os.path.join(current_directory, subdirectory)
            image_files = [filename for filename in os.listdir(image_path) if filename.endswith('.png')]
            if image_files:
                image_file = image_files[0]
                try:
                    image = Image.open(os.path.join(image_path, image_file))
                except:
                    continue
                try:
                    card_data = base64.b64decode(image.info['chara'])
                except:
                    continue
                card_parsed = json.loads(card_data)
                card_name = card_parsed.get("data", []).get("name")
                if (card_name is None):
                    card_name = ""
                card_creator = card_parsed.get("data", []).get("creator")
                if (card_creator is None):
                    card_creator = ""
                card_personality = card_parsed.get("data", []).get("personality")
                if (card_personality is None):
                    card_personality = ""
                card_tags = card_parsed.get("data", []).get("tags", [])
                if (card_tags is None):
                    card_tags = [""]
                card_description = card_parsed.get("data", []).get("description")
                if (card_description is None):
                    card_description = ""
                if (desc_checkbox_var.get() == 1):
                    if os.path.isfile(metadata_file):
                        with open(metadata_file) as f:
                            metadata = json.load(f)
                            if all(
                                any(
                                    re.search(search_term, card_name, re.IGNORECASE)
                                    or re.search(search_term, card_creator, re.IGNORECASE)
                                    or re.search(search_term, card_personality, re.IGNORECASE)
                                    or re.search(search_term, card_description, re.IGNORECASE)
                                    or any(re.search(search_term, tag, re.IGNORECASE) for tag in card_tags)
                                    or re.search(search_term, metadata.get("description"), re.IGNORECASE)
                                    or re.search(search_term, metadata.get("tagline"), re.IGNORECASE)
                                    or any(re.search(search_term, topic, re.IGNORECASE) for topic in metadata.get("topics", []))
                                    for metadata in [metadata]
                                )
                                for search_term in search_terms
                            ):
                                filtered_subdirectories.append(subdirectory)
                else:
                    if os.path.isfile(metadata_file):
                        with open(metadata_file) as f:
                            metadata = json.load(f)
                            if all(
                                any(
                                    re.search(search_term, card_name, re.IGNORECASE)
                                    or re.search(search_term, card_creator, re.IGNORECASE)
                                    or re.search(search_term, card_personality, re.IGNORECASE)
                                    or any(re.search(search_term, tag, re.IGNORECASE) for tag in card_tags)
                                    or re.search(search_term, metadata.get("description"), re.IGNORECASE)
                                    or re.search(search_term, metadata.get("tagline"), re.IGNORECASE)
                                    or any(re.search(search_term, topic, re.IGNORECASE) for topic in metadata.get("topics", []))
                                    for metadata in [metadata]
                                )
                                for search_term in search_terms
                            ):
                                filtered_subdirectories.append(subdirectory)
        else:
            if os.path.isfile(metadata_file):
                with open(metadata_file) as f:
                    metadata = json.load(f)
                    if all(
                        any(
                            re.search(search_term, metadata.get("description"), re.IGNORECASE)
                            or re.search(search_term, metadata.get("tagline"), re.IGNORECASE)
                            or any(re.search(search_term, topic, re.IGNORECASE) for topic in metadata.get("topics", []))
                            for metadata in [metadata]
                        )
                        for search_term in search_terms
                    ):
                        filtered_subdirectories.append(subdirectory)
    return filtered_subdirectories

# Update the listbox with the search terms
def update_listbox(event=None):
    search_terms = [search_term.strip() for search_term in search_entry.get().split(",")]
    filtered_subdirectories = filter_subdirectories(search_terms)
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

# Change font size
def toggle_font_size():
    global default_font_size
    default_font_size = 16 if checkbox_var.get() else 10
    default_font.configure(size=default_font_size)
    metadata_text.tag_configure("custom_font", font=("TkDefaultFont", default_font_size))

def off_focus(event):
    if search_entry.get() == "":
        search_entry.configure(foreground='gray')
        search_entry.insert(0, placeholder_text)

def on_focus(event):
    if search_entry.get() == placeholder_text:
        search_entry.delete(0, tk.END)
        search_entry.configure(foreground='black')

# Set title
root = tk.Tk()
root.title("Chub Archive Search GUI")

# Default font size
default_font_size = 10

# Set the default font size for all widgets
default_font = tk.font.nametofont("TkDefaultFont")
default_font.configure(size=default_font_size)

# Add checkbox variables
desc_checkbox_var = tk.IntVar()
card_checkbox_var = tk.IntVar(value=1)

# Create a search bar
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_button = tk.Button(search_frame, text="Search:", command=update_listbox)
search_button.pack(side=tk.LEFT)

search_entry = tk.Entry(search_frame, width=50)
search_entry.pack(side=tk.LEFT)
search_entry.bind("<Return>", update_listbox)

search_entry.configure(foreground='gray')
placeholder_text = "Enter comma-separated search terms here..."
search_entry.insert(0, placeholder_text)
search_entry.bind('<FocusIn>', on_focus)
search_entry.bind('<FocusOut>', off_focus)

# Create checkbox for big (old man) mode
checkbox_var = tk.BooleanVar()
checkbox = tk.Checkbutton(search_frame, text="Old Man Mode", variable=checkbox_var, command=toggle_font_size)
checkbox.pack(side=tk.RIGHT)

# Create checkbox for card metadata search
card_checkbox = tk.Checkbutton(search_frame, text="Search Card Metadata", variable=card_checkbox_var)
card_checkbox.pack(side=tk.RIGHT)

# Create checkbox for description search
desc_checkbox = tk.Checkbutton(search_frame, text="Search Card Description", variable=desc_checkbox_var)
desc_checkbox.pack(side=tk.RIGHT)

# Create a scrollbar for the listbox
list_scrollbar = tk.Scrollbar(root)
list_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

# Create a scrollbar for the metadata textbox
metadata_scrollbar = tk.Scrollbar(root)
metadata_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a listbox
listbox = tk.Listbox(root, yscrollcommand=list_scrollbar.set)
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

metadata_text = tk.Text(metadata_frame, wrap=tk.WORD, state=tk.DISABLED, yscrollcommand=metadata_scrollbar.set)
metadata_text.pack(fill=tk.BOTH, expand=True)

metadata_text.tag_configure("custom_font", font=("TkDefaultFont", default_font_size))

# Get the subdirectories in the current directory
current_directory = os.getcwd()
subdirectories = get_subdirectories(current_directory)

# Sort the subdirectories alphabetically
subdirectories.sort()

# Add subdirectories to the listbox
for subdirectory in subdirectories:
    listbox.insert(tk.END, subdirectory)

# Configure the scrollbars
list_scrollbar.config(command=listbox.yview)
metadata_scrollbar.config(command=metadata_text.yview)

# Start the tkinter event loop
root.mainloop()
