import json
from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_pw():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    pw = "".join(password_list)

    password_entry.insert(0, pw)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data():
    """Gets the input from entries, saves it, then clears the entry boxes."""
    website = website_entry.get().upper()
    mail = mail_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": mail,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Oops", message="Any fields can't be left empty")

    else:
        is_ok = messagebox.askokcancel(title=website, message=f"Are you sure to save?\nMail/Username: {mail} \n"
                                                              f"Password:{password}")
        if is_ok:
            try:
                with open("entries.json", "r") as file:
                    data = json.load(file)  # read
            except FileNotFoundError:
                with open("entries.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)  # update
                with open("entries.json", "w") as file:
                    json.dump(data, file, indent=4)  # save
            finally:
                website_entry.delete(0, END)
                mail_entry.delete(0, END)
                password_entry.delete(0, END)
                website_entry.focus()
                messagebox.showinfo(title="", message="Saving successful.")

# ---------------------------- FINDING ENTRY ------------------------------- #


def find_pw():
    try:
        with open("entries.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Oops", message="No file exists")
    else:
        try:
            website_to_find = website_entry.get().upper()
            mail = data[website_to_find]["email"]
            pw = data[website_to_find]["password"]
        except KeyError:
            messagebox.showerror(title="Oops", message="No such website found")
        else:
            messagebox.showinfo(title=f"{website_to_find}".capitalize(),
                                message=f"Email/Username:{mail}\nPassword:{pw}")
# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(width=200, height=200, padx=20, pady=20)
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(115, 100, image=logo)
canvas.grid(column=2, row=1)

website_label = Label(text="Website:")
website_label.grid(column=1, row=2)
website_entry = Entry(width=33)
website_entry.focus()
website_entry.grid(column=2, row=2)

mail_label = Label(text="Email/Username:")
mail_label.grid(column=1, row=3)
mail_entry = Entry(width=52)
mail_entry.insert(0, "example@e-mail.com")
mail_entry.grid(column=2, row=3, columnspan=2)

password_label = Label(text="Password:")
password_label.grid(column=1, row=4)
password_entry = Entry(width=33)
password_entry.grid(column=2, row=4)


search_button = Button(text="Search", width=14, command=find_pw)
search_button.grid(column=3, row=2)

pw_button = Button(text="Generate Password", command=generate_pw)
pw_button.grid(column=3, row=4)

add_button = Button(text="Add", width=44, command=save_data)
add_button.grid(column=2, row=5, columnspan=2)


window.mainloop()