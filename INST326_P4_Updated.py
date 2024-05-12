import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
import datetime
import os
from PIL import Image, ImageTk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x500")
        self.title('Project 4 Notes and Snippets')
        self.notes = []
        self.snippets = []
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame for buttons
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(padx=10, pady=10)

        
        ttk.Button(self.buttons_frame, text="New Note", command=self.new_note).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.buttons_frame, text="Open Notebook", command=self.open_notebook).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.buttons_frame, text="Save Notebook", command=self.save_notebook).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.buttons_frame, text="Search Notes", command=self.search_notes).pack(side=tk.LEFT, padx=5)
        # Add snippet buttons in MainWindow
        ttk.Button(self.buttons_frame, text="New Snippet", command=self.new_snippet).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.buttons_frame, text="Open Snippets", command=self.open_snippets).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.buttons_frame, text="Save Snippets", command=self.save_snippets).pack(side=tk.LEFT, padx=5)

        ttk.Button(self.buttons_frame, text="Show Cinqmars", command=self.show_cinqmars_image).pack(side=tk.LEFT, padx=5)

        # Frame for displaying notes and snippets
        self.display_area = ttk.Frame(self)
        self.display_area.pack(fill=tk.BOTH, expand=True)
        
        self.note_frame = ttk.Frame(self.display_area)
        self.note_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.snippet_frame = ttk.Frame(self.display_area)
        self.snippet_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    def new_note(self):
        note_window = NoteForm(self)
    
    def open_notebook(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if filepath:  
            self.load_notes(filepath)


    def save_notebook(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filepath:
            try:
                with open(filepath, 'w') as file:
                    json.dump(self.notes, file, indent=4)
                messagebox.showinfo("Success", "Notes saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save notes: {str(e)}")

    
    def search_notes(self):
        search_term = simpledialog.askstring("Search Notes", "Enter search term:")
        if search_term:
            found = False  # Flag to track if any note contains the search term
            matching_notes = []
            for note in self.notes:
                if search_term.lower() in note.get('text', '').lower():
                    matching_notes.append(note)
                    messagebox.showinfo("Search Result", f'"{search_term}" was found in "{note.get("title", "Untitled")}".')
                    found = True
            
            if not found:
                messagebox.showinfo("Search Result", "No matches found.")
            
            self.display_notes(matching_notes)


    def show_cinqmars_image(self):
        window = tk.Toplevel(self)
        window.title("R.I.P. Mike 'Cinq' Cinqmars")
        
        # Construct path to image
        script_dir = os.path.dirname(__file__)  # Directory where the script is located
        image_path = os.path.join(script_dir, 'Cinq', 'xgames00cinq10.jpeg')

        # Load and display the image
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        label = ttk.Label(window, image=photo)
        label.image = photo
        label.pack()

    def new_snippet(self):
        snippet_window = SnippetForm(self, self.snippets)
        snippet_window.grab_set()


    def display_notes(self, notes=None):
        if notes is None:
            notes = self.notes
        for widget in self.note_frame.winfo_children():
            widget.destroy()
        for note in notes:
            button = ttk.Button(self.note_frame, text=note["title"], command=lambda n=note: self.show_note_details(n))
            button.pack(pady=5)



    def show_note_details(self, note):
        note_window = NoteForm(self, note)
        note_window.grab_set()


    def open_snippets(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filepath:
            try:
                with open(filepath, 'r') as file:
                    self.snippets = json.load(file)
                self.display_snippets()
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Failed to decode JSON.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_snippets(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json")])
        if filepath:
            try:
                with open(filepath, 'w') as file:
                    json.dump(self.snippets, file, indent=4)
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
    def edit_snippet(self, snippet):
        snippet_window = SnippetForm(self, self.snippets, snippet)
        snippet_window.grab_set()  

    def display_snippets(self):
        for widget in self.snippet_frame.winfo_children():
            widget.destroy()
        for snippet in self.snippets:
            frame = ttk.Frame(self.snippet_frame)
            frame.pack(pady=5)
            ttk.Button(frame, text=snippet["title"], command=lambda s=snippet: self.show_snippet_details(s)).pack(side=tk.LEFT)
            ttk.Button(frame, text="Edit", command=lambda s=snippet: self.edit_snippet(s)).pack(side=tk.LEFT)

    # When loading notes
    def load_notes(self, filepath):
        try:
            with open(filepath, 'r') as file:
                notes = json.load(file)
            self.notes = [self.fill_missing_keys(note) for note in notes]
            self.display_notes()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to decode JSON from file.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def fill_missing_keys(self, note):
        required_keys = {'title': '', 'text': '', 'tags': '', 'author': '', 'edit_history': []}
        for key, default in required_keys.items():
            if key not in note:
                note[key] = default
        return note

    def validate_note_structure(self, note):
        required_keys = ['title', 'text', 'tags', 'author', 'edit_history']
        for key in required_keys:
            if key not in note:
                if key == "edit_history":
                    note[key] = []
                else:
                    note[key] = ""
        return note



class NoteForm(tk.Toplevel):
    def __init__(self, master, note=None):
        super().__init__(master)
        self.note = note if note else {'title': "", 'text': "", 'tags': "", 'author': "", 'edit_history': []}
        self.master = master
        self.setup_ui()

    def setup_ui(self):
        self.title("New Note" if 'title' not in self.note or self.note['title'] == "" else "Edit Note")

        ttk.Label(self, text="Title:").pack(padx=10, pady=5)
        self.title_entry = ttk.Entry(self)
        self.title_entry.insert(0, self.note.get('title', ""))
        self.title_entry.pack(padx=10, pady=5)

        ttk.Label(self, text='Text:').pack(padx=10, pady=5)
        self.text_entry = tk.Text(self, height=10, width=40)
        self.text_entry.insert(tk.END, self.note.get('text', ""))
        self.text_entry.pack(padx=10, pady=5)

        ttk.Label(self, text='Tags:').pack(padx=10, pady=5)
        self.tags_entry = ttk.Entry(self)
        self.tags_entry.insert(0, self.note.get('tags', ""))
        self.tags_entry.pack(padx=10, pady=5)

        ttk.Label(self, text="Author:").pack(padx=10, pady=5)
        self.author_entry = ttk.Entry(self)
        self.author_entry.insert(0, self.note.get('author', ""))
        self.author_entry.pack(padx=10, pady=5)

        ttk.Button(self, text="Submit", command=self.submit).pack(padx=10, pady=10)

    def submit(self):
        updated_note = {
            "title": self.title_entry.get(),
            "text": self.text_entry.get("1.0", tk.END).strip(),
            "tags": self.tags_entry.get().strip(),
            "author": self.author_entry.get().strip(),
            "edit_history": self.note.get("edit_history", [])
        }

        if 'title' in self.note and self.note['title']:  # Check if existing note
            self.note.update(updated_note)
        else:  # New note
            self.master.notes.append(updated_note)

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
