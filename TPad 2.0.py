import tkinter as tk
from tkinter import filedialog, Toplevel, simpledialog

def create_terminal_notepad():
    """
    Creates and runs the TerminalPad application.
    """
    # Create the main window
    root = tk.Tk()
    root.title("TerminalPad")

    # Define colors
    bg_color = "#000000"  # Black
    fg_color = "#00FF00"  # Green
    menu_bg = "#333333"  # Dark gray
    menu_fg = "#FFFFFF"  # White

    # Create the text widget
    text_area = tk.Text(
        root,
        bg=bg_color,
        fg=fg_color,
        insertbackground=fg_color,
        font=("Courier New", 12),
        undo=True,  # Enable undo/redo
        wrap="word"  # Enable word wrapping
    )
    text_area.pack(expand=True, fill="both")

    # --- Functionality ---

    def save_file():
        """Saves the current text content to a file."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return

        content = text_area.get(1.0, tk.END)
        with open(filepath, "w") as file:
            file.write(content)

    def open_file():
        """Opens a file and loads its content into the text area."""
        filepath = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return

        text_area.delete(1.0, tk.END)
        with open(filepath, "r") as file:
            content = file.read()
        text_area.insert(1.0, content)

    def find_text():
        """Finds and highlights all occurrences of a string."""
        find_string = simpledialog.askstring("Find", "Enter text to find:")
        if find_string:
            start_pos = "1.0"
            text_area.tag_remove("found", "1.0", tk.END)
            while True:
                pos = text_area.search(find_string, start_pos, stopindex=tk.END)
                if not pos:
                    break
                end_pos = f"{pos}+{len(find_string)}c"
                text_area.tag_add("found", pos, end_pos)
                start_pos = end_pos
            text_area.tag_config("found", background="#FFFF00", foreground="#000000")

    def replace_text():
        """Replaces all occurrences of a string with a new string."""
        find_string = simpledialog.askstring("Replace", "Enter text to find:")
        if find_string:
            replace_string = simpledialog.askstring("Replace", "Enter replacement text:")
            if replace_string is not None:
                content = text_area.get(1.0, tk.END)
                new_content = content.replace(find_string, replace_string)
                text_area.delete(1.0, tk.END)
                text_area.insert(1.0, new_content)

    # --- Menus ---

    # Create a menu bar
    menu_bar = tk.Menu(root, bg=menu_bg, fg=menu_fg)

    # File menu
    file_menu = tk.Menu(menu_bar, tearoff=0, bg=menu_bg, fg=menu_fg)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Edit menu
    edit_menu = tk.Menu(menu_bar, tearoff=0, bg=menu_bg, fg=menu_fg)
    edit_menu.add_command(label="Undo", command=text_area.edit_undo)
    edit_menu.add_command(label="Redo", command=text_area.edit_redo)
    edit_menu.add_separator()
    edit_menu.add_command(label="Find", command=find_text)
    edit_menu.add_command(label="Replace All", command=replace_text)
    menu_bar.add_cascade(label="Edit", menu=edit_menu)

    # Attach the menu bar to the main window
    root.config(menu=menu_bar)

    # --- Keyboard Shortcuts ---
    root.bind("<Control-s>", lambda event: save_file())
    root.bind("<Control-o>", lambda event: open_file())
    root.bind("<Control-f>", lambda event: find_text())

    # Start the application's main loop
    root.mainloop()

if __name__ == "__main__":
    create_terminal_notepad()
    