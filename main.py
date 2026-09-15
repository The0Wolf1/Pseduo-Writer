import os
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import *
from tkinter.filedialog import *
from PIL import Image, ImageTk

window = Tk()
window.title("Pseduo Writer")
file = None

ico = Image.open("icon.png")
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)

window_width = 500
window_height = 500
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

font_name = StringVar(window)
font_name.set("Arial")

font_size = StringVar(window)
font_size.set("20")

text_area = Text(window, font=(font_name.get(), font_size.get()))
text_area.insert(INSERT, "# ")

def new_file():
    window.title("Untitled")
    text_area.delete(1.0, END)
    text_area.insert(1.0, "# ")


def open_file():
    file = askopenfilename(defaultextension=".txt",
                           file=[("All Files", "*.*"),
                                 ("Text Documents", "*.txt"),
                                 ("Python Files", "*.py")])

    if file is None:
        return

    else:
        try:
            window.title(os.path.basename(file))
            text_area.delete(1.0, END)

            file = open(file, "r")

            content = file.read().upper()

            lines = content.splitlines()
            content = "\n".join(
                 line if line.startswith("#") else "# " + line
                 for line in lines
			)

            text_area.insert(1.0, content)

        except Exception:
            print("couldn't read file")

        finally:
            file.close()


def save_file():
    file = filedialog.asksaveasfilename(initialfile='unititled.txt',
                                        defaultextension=".txt",
                                        filetypes=[("All Files", "*.*"),
                                                   ("Text Documents", "*.txt"),
                                                   ("Python Files", "*.py")])

    if file is None:
        return

    else:
        try:
            window.title(os.path.basename(file))
            file = open(file, "w")

            file.write(text_area.get(1.0, END))

        except Exception:
            print("couldn't save file")

        finally:
            file.close()


def cut():
    text_area.event_generate("<<Cut>>")


def copy():
    text_area.event_generate("<<Copy>>")


def paste():
    text_area.event_generate("<<Paste>>")


def about():
    showinfo("About Pseudo Writer", 
             """
             I thought of this during a software programming lesson where we had three easy tasks (I found them easy cause I was a little experienced with Python) and we had to provide pseudo code. 
             Now, the way I write pseudo code is by adding hashtags and CAPS LOCK, Markdown style, but I found it tedious to keep having to enter a hashtag on every new line. So I created this to help me.
             ---
             This isn't made to be MS Word or LibreOffice Writer. It's a simple text editor for my style of pseudo code. If you don't like it, then go somewhere else
             """)


def quit():
    window.destroy()

def on_key_pressed(event):
    if event.state & 0x4:
        return

    cursor = text_area.index(INSERT)
    line_start = text_area.index(f"{cursor} linestart")

    if event.keysym == "BackSpace":
        if text_area.compare(cursor, "==", f"{line_start}+2c"):
            return "break"

    if event.keysym == "Delete":
        if text_area.compare(cursor, "<", f"{line_start}+2c"):
            return "break"

    if event.keysym == "Return":
        text_area.insert(INSERT, "\n# ")
        return "break"

    if event.char and event.char.isalpha():
        text_area.insert(INSERT, event.char.upper())
        return "break"

def main():
    scroll_bar = Scrollbar(text_area)
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    text_area.grid(sticky=N + E + S + W)
    scroll_bar.pack(side=RIGHT, fill=Y)
    text_area.bind("<Key>", on_key_pressed)
    text_area.config(yscrollcommand=scroll_bar.set)

    frame = Frame(window)
    frame.grid()

    menu_bar = Menu(window)
    window.config(menu=menu_bar)

    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=new_file)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=quit)

    edit_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Cut", command=cut)
    edit_menu.add_command(label="Copy", command=copy)
    edit_menu.add_command(label="Paste", command=paste)

    help_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=about)

    window.mainloop()

main()