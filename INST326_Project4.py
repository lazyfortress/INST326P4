# INST326 - 0104 Project 4, Justin Anderson

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import datetime
import os

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("900x400")
        self.title('Project 3 Notes and Snippets')
        self.notes = []     # empty list to store the notes
        self.snippets = []  # empty list to store the code snippets
        
        # Frame for notes and snippets buttons
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(padx=10, pady=10)

        # Buttons for notes
        new_note_button = ttk.Button(self.buttons_frame, text="New Note", command=self.new_note)
        new_note_button.pack(side=tk.LEFT, padx=5)
        open_notebook_button = ttk.Button(self.buttons_frame, text="Open Notebook", command=self.open_notebook)
        open_notebook_button.pack(side=tk.LEFT, padx=5)
        save_notebook_button = ttk.Button(self.buttons_frame, text="Save Notebook", command=self.save_notebook)
        save_notebook_button.pack(side=tk.LEFT, padx=5)

        # Buttons for snippets
        new_snippet_button = ttk.Button(self.buttons_frame, text="New Snippet", command=self.new_snippet)
        new_snippet_button.pack(side=tk.LEFT, padx=5)
        open_snippets_button = ttk.Button(self.buttons_frame, text="Open Snippets", command=self.open_snippets)
        open_snippets_button.pack(side=tk.LEFT, padx=5)
        save_snippets_button = ttk.Button(self.buttons_frame, text="Save Snippets", command=self.save_snippets)
        save_snippets_button.pack(side=tk.LEFT, padx=5)

        # Frame for displaying notes and snippets
        self.display_area = tk.Frame(self)
        self.display_area.pack(fill=tk.BOTH, expand=True)

        # Display area for notes
        self.note_frame = tk.Frame(self.display_area)
        self.note_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Display area for snippets
        self.snippet_frame = tk.Frame(self.display_area)
        self.snippet_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)



# creates new notes 
    def new_note(self):
        note_window = Form(self, self.notes)
    
    def new_notebook(self):
        notebook_window = NotebookForm(self)
        
# can open existing notes that have been saved
    def open_notebook(self):
        initial_dir = os.path.dirname(os.path.realpath(__file__))
        dir_path = filedialog.askdirectory(initialdir=initial_dir)
        
        if dir_path:
            try:
                files = [f for f in os.listdir(dir_path) if f.endswith(".json")]
                self.notes = []
                
                for file in files:
                    file_path = os.path.join(dir_path, file)
                    with open(file_path, "r") as file:
                        note_content = json.load(file)
                        self.notes.append(note_content)
                    
                self.display_notes()
            except FileNotFoundError:
                messagebox.showwarning("Warning", "No notebook found.")
        else:
            messagebox.showwarning("Warning", "No notebook selected.")

    def save_notebook(self):
        initial_dir = os.path.dirname(os.path.realpath(__file__))
        dir_path = filedialog.askdirectory(initialdir=initial_dir)
        
        if dir_path:
            try:
                # WARNING: the following 3 lines will delete all json files in ur folder :D
                json_files = [f for f in os.listdir(dir_path) if f.endswith(".json")]
                for file in json_files:
                    os.remove(os.path.join(dir_path, file))
                
                for note in self.notes:
                    file_path = os.path.join(dir_path, note["title"]) + ".json"
                    with open(file_path, "w") as file:
                        json.dump(note, file)
            except FileNotFoundError:
                messagebox.showwarning("Warning", "No notebook found.")
        else:
            messagebox.showwarning("Warning", "No notebook selected.")
            
    # allows it to appear on the notebook in the main window

    def display_notes(self):
        for widget in self.note_frame.winfo_children():  # winfo_children retrieves all widgets
            widget.destroy()
        for note in self.notes:
            note_button = ttk.Button(self.note_frame, text=note["title"], command=lambda n=note: self.show_note_details(n))
            note_button.pack(pady=5)

    def show_note_details(self, note):
        note_window = Form(self, self.notes, note)

    def new_snippet(self):
        snippet_window = SnippetForm(self, self.snippets)
    
    def open_snippets(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filepath:
            try:
                with open(filepath, "r") as file:
                    self.snippets = json.load(file)
                self.display_snippets()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open snippets: {e}")
    
    def save_snippets(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json")])
        if filepath:
            try:
                with open(filepath, 'w') as file:
                    json.dump(self.snippets, file, indent=4)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save snippets: {e}")
    
    def display_snippets(self):
        for widget in self.snippet_frame.winfo_children():
            widget.destroy()
        for snippet in self.snippets:
            snippet_button = ttk.Button(self.snippet_frame, text=snippet["title"], command=lambda sn=snippet: 
                                        self.show_snippet_details(sn))
            snippet_button.pack(pady=5)

    def show_snippet_details(self, snippet):
        snippet_window = SnippetForm(self, self.snippets, snippet)

# window with a form for the new note
# Notebook class
class NotebookForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Create New Notebook')
        #prompt = ttk.Label(notebook_name_prompt, 
        #      text ="Notebook Title: ")
        #prompt.pack(side=tk.LEFT, padx=10, pady=10, anchor='center')  # Center the button
        # create widgets for title, text, and tags
        self.title_label = ttk.Label(self, text="Notebook Title:")
        self.title_label.pack(side=tk.TOP, padx=10, pady=5)
        self.title_entry = ttk.Entry(self)
        self.title_entry.pack(side=tk.TOP, padx=10, pady=5)
        
        self.submit_button = ttk.Button(self, text="Initialize Notebook", command=self.initNoteBook)
        self.submit_button.pack(side=tk.TOP, padx=10, pady=10)
  
    def initNoteBook(self):
        title = self.title_entry.get()
        timestamp = str(datetime.datetime.now())

        #self.master.new_notebook_save()
        #new_notebook_save code is used below 
        directory = "notebook " + title
        self.master.notebook = title
        
        # Parent Directory path  
        parent_dir = os.path.dirname(os.path.realpath(__file__))
        
        # Path  
        path = os.path.join(parent_dir, directory)
        self.master.notebook_filepath = path
            
        # Create the directory in '/home / User / INST326'  
        os.mkdir(path)  
        print("Directory '% s' created" % directory)  
        
        #figure out how to print notebook name as a button on main screen
        #figure out how to add notes to the labeled notebooks and put things in
        #their file directory
        
        # if directory / file that  is to be created already  
        # exists then 'FileExistsError'  
        # will be raised by os.mkdir() method  

        # if specified path is invalid 'FileNotFoundError' Error  
        # will be raised   
        
        self.master.display_notes()
        self.destroy() 

# Form class
# Edited to include author functionality and edit history in the GUI
class Form(tk.Toplevel):
    def __init__(self, master, notes, note=None):
        super().__init__(master)
        self.title('New Note' if note is None else 'Note Details')

        self.master = master
        self.notes = notes
        self.note = note

        # Create widgets for title, text, tags, and author
        self.title_label = ttk.Label(self, text="Title:")
        self.title_label.pack(side=tk.TOP, padx=10, pady=5)
        self.title_entry = ttk.Entry(self)
        self.title_entry.pack(side=tk.TOP, padx=10, pady=5)

        self.text_label = ttk.Label(self, text="Text:")
        self.text_label.pack(side=tk.TOP, padx=10, pady=5)
        self.text_entry = tk.Text(self, height=10, width=40)
        self.text_entry.pack(side=tk.TOP, padx=10, pady=5)

        self.tags_label = ttk.Label(self, text="Tags:")
        self.tags_label.pack(side=tk.TOP, padx=10, pady=5)
        self.tags_entry = ttk.Entry(self)
        self.tags_entry.pack(side=tk.TOP, padx=10, pady=5)

        self.author_label = ttk.Label(self, text="Author:")
        self.author_label.pack(side=tk.TOP, padx=10, pady=5)
        self.author_entry = ttk.Entry(self)
        self.author_entry.pack(side=tk.TOP, padx=10, pady=5)

        # Create buttons
        self.submit_button = ttk.Button(self, text="Submit", command=self.submit)
        self.submit_button.pack(side=tk.TOP, padx=10, pady=10)

        self.history_button = ttk.Button(self, text="View Edit History", command=self.show_history)
        self.history_button.pack(side=tk.TOP, padx=10, pady=5)

        if note is not None:
            self.fill_form()

    def fill_form(self):
        # Fill form with existing note details
        self.title_entry.insert(0, self.note["title"])
        self.text_entry.insert(tk.END, self.note["text"])
        self.tags_entry.insert(0, self.note.get("tags", ""))
        self.author_entry.insert(0, self.note.get("author", ""))

    def show_history(self):
        history_window = tk.Toplevel(self)
        history_window.title("Edit History")
        history_list = ttk.Treeview(history_window, columns=("timestamp", "details"), show="headings")
        history_list.heading("timestamp", text="Timestamp")
        history_list.heading("details", text="Details")
        history_list.pack(fill=tk.BOTH, expand=True)

        for entry in self.note.get("edit_history", []):
            details = "; ".join([f"{k}: {v}" for k, v in entry["changes"].items()])
            history_list.insert("", tk.END, values=(entry["timestamp"], details))

    def submit(self):
        # Submit or update note details
        title = self.title_entry.get()
        text = self.text_entry.get("1.0", tk.END).strip()
        tags = self.tags_entry.get().strip()
        author = self.author_entry.get().strip()
        timestamp = str(datetime.datetime.now())

        if self.note is None:
            self.notes.append({"title": title, "text": text, "tags": tags,
                               "author": author, "created_at": timestamp, "edit_history": []})
        else:
            changes = {}
            if title != self.note["title"]:
                changes["title"] = title
            if text != self.note["text"]:
                changes["text"] = text
            if tags != self.note["tags"]:
                changes["tags"] = tags
            if author != self.note["author"]:
                changes["author"] = author

            self.note["title"] = title
            self.note["text"] = text
            self.note["tags"] = tags
            self.note["author"] = author

            if changes:
                self.note["edit_history"].append({"timestamp": timestamp, "changes": changes})

        self.master.display_notes()
        self.destroy()

# Snippet class
class SnippetForm(tk.Toplevel):
    def __init__(self, master, snippets, snippet=None):
        super().__init__(master)
        self.title('New Snippet' if snippet is None else 'Snippet Details')

        self.master = master
        self.snippets = snippets
        self.snippet = snippet
        self.edit_mode = False

        # Create widgets for snippet title and code
        self.title_label = ttk.Label(self, text="Title:")
        self.title_label.pack(side=tk.TOP, padx=10, pady=5)
        self.title_entry = ttk.Entry(self)
        self.title_entry.pack(side=tk.TOP, padx=10, pady=5)

        self.code_label = ttk.Label(self, text="Code:")
        self.code_label.pack(side=tk.TOP, padx=10, pady=5)
        self.code_entry = tk.Text(self, height=10, width=40)
        self.code_entry.pack(side=tk.TOP, padx=10, pady=5)

        # Create submit and edit buttons
        self.submit_button = ttk.Button(self, text="Submit", command=self.submit)
        self.submit_button.pack(side=tk.TOP, padx=10, pady=10)
        self.edit_button = ttk.Button(self, text="Edit", command=self.toggle_edit_mode)
        self.edit_button.pack(side=tk.TOP, padx=10, pady=5)

        if snippet is not None:
            self.fill_form()

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        if self.edit_mode:
            self.title_entry.config(state=tk.NORMAL)
            self.code_entry.config(state=tk.NORMAL)
            self.submit_button.config(state=tk.NORMAL, text="Save")
        else:
            self.fill_form()

    def fill_form(self):
        self.title_entry.delete(0, tk.END)
        self.code_entry.delete(1.0, tk.END)
        if self.snippet:
            self.title_entry.insert(0, self.snippet["title"])
            self.code_entry.insert(tk.END, self.snippet["code"])

    def submit(self):
        title = self.title_entry.get()
        code = self.code_entry.get("1.0", tk.END).strip()
        timestamp = str(datetime.datetime.now())

        changes = {}
        if self.snippet is None:
            self.snippets.append({"title": title, "code": code, "created_at": timestamp, "edit_history": []})
        else:
            if title != self.snippet["title"]:
                changes["title"] = title
            if code != self.snippet["code"]:
                changes["code"] = code

            if changes:
                self.snippet["edit_history"].append({"timestamp": timestamp, "changes": changes})
                self.snippet["title"] = title
                self.snippet["code"] = code

        self.master.save_snippets()
        self.master.display_snippets()
        self.destroy()


if __name__ == '__main__':
    main_window = MainWindow()
    main_window.mainloop()
