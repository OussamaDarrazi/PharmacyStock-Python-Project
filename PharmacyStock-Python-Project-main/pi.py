from tkinter import ttk
import tkinter as tk
# Assuming 'root' is an instance of Tk
root = tk.Tk()

# Create a Notebook widget
notebook = ttk.Notebook(root)

# Create two frames to be used as tabs in the notebook
med_tab = ttk.Frame(notebook)
add_tab = ttk.Frame(notebook)

# You can add widgets or content to the frames here if needed

# Add the frames as tabs to the notebook
notebook.add(med_tab, text='Medicine Tab')
notebook.add(add_tab, text='Add Tab')

# Pack or grid the notebook to make it visible
notebook.pack(fill='both', expand=True)

# Start the Tkinter event loop
root.mainloop()
