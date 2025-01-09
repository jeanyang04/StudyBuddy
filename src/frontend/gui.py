import tkinter as tk

from backend.server import handle_query

def chat():
    query = query_entry.get()
    response = handle_query(query)
    chat_display.insert(tk.END, f"You: {query}\nBot: {response}\n\n")

# Create GUI
root = tk.Tk()
root.title("RAG Chat App")

query_entry = tk.Entry(root, width=50)
query_entry.pack()

chat_button = tk.Button(root, text="Ask", command=chat)
chat_button.pack()

chat_display = tk.Text(root, height=20, width=70)
chat_display.pack()

root.mainloop()
