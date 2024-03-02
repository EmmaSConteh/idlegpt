import string
from idlelib.idleai import AICompletion
import tkinter as tk
import tkinter.messagebox as messagebox


class AIExpand:
    wordchars = string.ascii_letters + string.digits + "_"

    def __init__(self, editwin, idleai, font):
        # Initialize the AIExpand instance with an editwin object and AICompletion instance
        self.editwin = editwin
        self.idleai = idleai
        self.tk_font = font

    def create_listbox(self):
        # Create a listbox window to display AI suggestions
        self.listbox_win= tk.Toplevel(self.editwin)

        # Get size of original window so we can base the size of the listbox window on it
        width = self.editwin.winfo_width()
        height = self.editwin.winfo_height()

        self.listbox_win.geometry(f"{width//2}x{height//2}")
        self.listbox = tk.Listbox(self.listbox_win, selectmode=tk.SINGLE, width=60, height=25, font=self.tk_font)
        self.listbox_win.title("AI Suggestions")
        self.listbox.bind('<<ListboxSelect>>', self.display_preview)
        self.listbox_win.protocol("WM_DELETE_WINDOW", self.revert)
        self.initial_content = self.editwin.get("1.0", "end-1c")
        self.cursor_index = self.editwin.index("insert")
        
        #Creating buttons to fill or ignore suggestions
        frame = tk.Frame(self.listbox_win)
        frame.pack(side=tk.BOTTOM)

        button = tk.Button(frame, text="Fill Suggestion", command=self.autofill_suggestion, font=self.tk_font)
        button.pack(side=tk.LEFT)

        button = tk.Button(frame, text="Ignore Suggestions", command=self.revert, font=self.tk_font)
        button.pack(side=tk.LEFT)

        self.listbox.pack()


    def revert(self):
        # Revert the content of the editwin to the initial content and destroy the listbox window. Called when window is exited or ignore suggestions button is clicked.
        self.editwin.delete("1.0", "end")
        self.editwin.insert("insert", self.initial_content)
        self.listbox_win.destroy()
        self.listbox = None

    def display_preview(self, event):
         # Temporary insertion. Display the selected suggestion from the listbox in the editwin
        init = self.initial_content
        cursor = self.cursor_index
        self.editwin.delete("1.0", "end")
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_suggestion = self.listbox.get(selected_index)
            ln, cn = map(int, cursor.split("."))
            new_cursor_pos = f"{ln}.{cn + len(selected_suggestion)}"
            self.editwin.insert("insert", init) 
            self.editwin.insert(cursor, selected_suggestion)   
            self.editwin.mark_set("insert", new_cursor_pos)  
    
    def autofill_suggestion(self):
        # Permanent insertion. Autofill the selected suggestion from the listbox into the editwin and destroy the listbox window
        init = self.initial_content
        cursor = self.cursor_index
        self.editwin.delete("1.0", "end")
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_suggestion = self.listbox.get(selected_index)
            ln, cn = map(int, cursor.split("."))
            new_cursor_pos = f"{ln}.{cn + len(selected_suggestion)}"
            self.editwin.insert("insert", init) 
            self.editwin.insert(cursor, selected_suggestion)   
            self.editwin.mark_set("insert", new_cursor_pos)   
            self.listbox_win.destroy()
            self.listbox_win = None


    def getline(self):
        # Get the current line from the editwin where the cursor is located
        line = self.editwin.get("insert linestart", "insert lineend")
        return line
    
    def getcontext(self):
        # Get the rest of the content of the file, other than the line that is being expanded upon
        line_number = int(self.editwin.index("insert").split(".")[0])
        start_of_line = f"{line_number}.0"
        text = self.editwin.get("1.0", start_of_line)
        return text

    def expand_word_event(self, event):
        #Main function. Gathers suggestions, creates listbox and enters suggestions in the box. 
        line = self.getline()

        context = self.getcontext()
        suggestions = self.get_expansion_suggestions(line, context)
        if not suggestions:
            messagebox.showinfo("No suggestions found", "No suggestions found")
            return "break"
        
        self.suggestions = suggestions
        self.create_listbox()
        self.listbox.delete(0, tk.END)
        for suggestion in suggestions:
            suggestion = suggestion.strip()
            if suggestion.startswith(line):
                suggestion = suggestion[len(line):]
            self.listbox.insert(tk.END, suggestion)
        x, y, _, _ = self.editwin.bbox(tk.INSERT)
        self.listbox_win.geometry(f"+{x}+{y}")
        self.listbox_win.focus_set()
        return "break"

    def get_expansion_suggestions(self, line, context):
        # Get suggestions from AICompletion instance
        cxt = f"{context}"
        prompt = f"{line}"
        return self.idleai.complete(cxt, prompt)
        
