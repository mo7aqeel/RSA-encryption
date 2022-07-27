from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
import tkinter.scrolledtext as scrolledtext
import pandas as pd
import socket
import pyDes

root = Tk()
root.geometry("600x600")

# connect with the server.
s = socket.socket()  # Create a socket object.
ip = '127.0.0.1'  # Get local machine name.
port = 12320  # Reserve a port for your service.
s.connect((ip, port))
print(s.recv(1024).decode())

MasterKey = "DESCRYPT"
k = pyDes.des(MasterKey, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)

# Logo
logo = Image.open("logo.png")
logo = logo.resize((250, 200), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)
logo_label = Label(image=logo)
logo_label.image = logo
logo_label.pack(side=TOP)

# Frames
file_paths_frame = Frame(root)
file_paths_frame.pack(side=BOTTOM)
main_frame = Frame(root)
main_frame.pack(side=BOTTOM)
encryption_frame = Frame(root)
decryption_frame = Frame(root)
decryption_text_frame = Frame(root)
search_frame = Frame(root)

# Browse file
id_list = []
name_list = []
case_list = []
collect_list = []
huge_list = []
encrypt_huge_list = []
main_data_var = StringVar()


def open_file():
    file = askopenfile(parent=root, mode='rb', title="Choose a file", filetypes=[("Excel Document", "*.xlsx")])
    if file:
        print("file was successfully loaded")
        file_name.set(file.name)
        df = pd.read_excel(file_name.get())
        print(df.__str__())

        # show file path as label.
        l = Label(file_paths_frame, text=file_name.get())
        l.config(font=("Cairo", 10))
        l.pack(side=BOTTOM)
        for i in range((df.size / 3).__int__()):
            id_list.append(str(df.loc[i, 'ID']))
            name_list.append(str(df.loc[i, 'Name']))
            case_list.append(str(df.loc[i, 'Case']))

        # read data from file.
        for i in range(len(id_list)):
            collect_list.append(id_list[i])
            collect_list.append("    ")
            collect_list.append(name_list[i])
            collect_list.append("    ")
            collect_list.append(case_list[i])
            collect_list.append("\n")

        print(collect_list)

        for i in range(len(collect_list)):
            huge_list.append(collect_list[i])

        s = ""
        for i in range(len(huge_list)):
            s += huge_list[i]

        print(s)
        main_data_var.set(s)
        # show Entry password to encrypt data.
        password_input_entry.pack(side=BOTTOM)
        collect_list.clear()
        id_list.clear()
        name_list.clear()
        case_list.clear()


file_name = StringVar()
browse_btn = Button(main_frame, text="Browse file", bg="#20bebe", fg="white", font="Cairo", height=1, width=15,
                    command=lambda: open_file())
browse_btn.pack(side=BOTTOM)


# -------------------------------------------------------------------------------------

# Encrypt data with password.


def send_data():
    for i in range(len(huge_list)):
        Encrypted_word = k.encrypt(huge_list[i])
        encrypt_huge_list.append(Encrypted_word)

    print("The data has been encrypted successfully")
    print("______________________________________________")
    print("Encrypted word lst:", encrypt_huge_list)
    # Convert To String
    Encrypt_huge_list = str(encrypt_huge_list)
    encryption_list_var.set(Encrypt_huge_list)
    # Encode String
    Encrypt_huge_list = Encrypt_huge_list.encode()
    # Send Encoded String version of the List
    s.send(Encrypt_huge_list)


def back_to_main_frame():
    encryption_frame.pack_forget()
    main_frame.pack(side=BOTTOM)
    file_paths_frame.pack(side=BOTTOM)


def start_encryption_frame():
    txt.delete('1.0', END)
    txt.insert(INSERT, encryption_list_var.get())
    encryption_frame.pack(side=TOP)


def encrypt_data():
    incorrect_pass_label.pack_forget()
    if password_input_entry.get() == password:
        send_data()
        file_paths_frame.pack_forget()
        main_frame.pack_forget()
        start_encryption_frame()

    else:
        incorrect_pass_label.pack(side=BOTTOM)


def start_search_frame():
    search_frame.pack(side=TOP)
    encryption_frame.pack_forget()


encryption_list_var = StringVar()
password = "123"
encrypt_btn = Button(main_frame, text="Encrypt data", bg="#20bebe", fg="white", font="Cairo", height=1, width=15,
                     command=lambda: encrypt_data())
encrypt_btn.pack(side=BOTTOM)

password_input_entry = Entry(main_frame, width=50)
password_input_entry.pack(side=BOTTOM)
enter_pass_label = Label(main_frame, text="Enter password")
enter_pass_label.pack(side=BOTTOM)

incorrect_pass_label = Label(main_frame, text="Password is incorrect")

main_data_label = Label(encryption_frame, text="Main data", font=12)
main_data_label.pack()

txt = scrolledtext.ScrolledText(encryption_frame, undo=True, width=60, height=10)
txt['font'] = ('consolas', '10')
txt.pack(expand=True)

search_btn = Button(encryption_frame, text="Search", bg="#20bebe", fg="white", font="Cairo", height=1, width=15,
                    command=lambda: start_search_frame())
search_btn.pack(side=TOP)
# Back to main frame
back_btn = Button(encryption_frame, text="Back", bg="#20bebe", fg="white", font="Cairo", height=1, width=15,
                  command=lambda: back_to_main_frame())
back_btn.pack(side=BOTTOM)


# ---------------------------------------------------------------
# Search frame


def search_word():
    found_label.pack_forget()
    word = word_entry.get()
    # Encode String
    worde = word.encode()
    # Send Encoded String version of the List
    s.send(worde)
    # print("this word you want to search : ", word, type(word))
    # print("________________________________ ")

    # receive result after search
    msg = s.recv(1024).decode()
    case_var.set(msg)
    found_label.config(text=case_var.get(), font=24)
    found_label.pack(side=TOP)
    print(msg)
    print("________________________________ ")
    send_data()
    s.close  # Close the socket when done


enter_label = Label(search_frame, text="Enter the word to search for")
enter_label.pack(side=TOP)
word_entry = Entry(search_frame, width=50)
word_entry.pack(side=TOP)
case_var = StringVar()
found_label = Label(search_frame)
search_btn = Button(search_frame, text="Search", bg="#20bebe", fg="white", font="Cairo", height=1, width=15,
                    command=lambda: search_word())
search_btn.pack(side=TOP)
back_search_btn = Button(search_frame, text="Back", bg="#20bebe", fg="white", font="Cairo", height=1, width=15,
                         command=lambda: back_to_encryption_frame())
back_search_btn.pack(side=TOP)

# ----------------------------------------------------------------
# Decryption data with password.


def start_decryption_frame():
    encryption_frame.pack_forget()
    decryption_frame.pack(side=TOP)


def start_decryption_text_frame():
    if password_decrypt_entry.get() == password:
        decryption_frame.pack_forget()
        txt_dec.delete('1.0', END)

        txt_dec.insert(INSERT, main_data_var.get())
        decryption_text_frame.pack(side=TOP)
    else:
        incorrect_pass_dec_label.pack(side=BOTTOM)


decryption_btn = Button(encryption_frame, text="Decrypt", bg="#20bebe", fg="white", font="Cairo", height=1, width=15,
                        command=lambda: start_decryption_frame())
decryption_btn.pack(side=BOTTOM)

password_decrypt_label = Label(decryption_frame, text="Enter password")
password_decrypt_label.pack(side=TOP)
password_decrypt_entry = Entry(decryption_frame, width=50)
password_decrypt_entry.pack(side=TOP)

incorrect_pass_dec_label = Label(decryption_frame, text="Password is incorrect")

enter_btn = Button(decryption_frame, text="Enter", bg="#20bebe", fg="white", font="Cairo", height=1, width=15,
                   command=lambda: start_decryption_text_frame())
enter_btn.pack(side=TOP)


# --------------------------------------------------------------------------
# Decryption text frame


def back_to_encryption_frame():
    decryption_text_frame.pack_forget()
    search_frame.pack_forget()
    encryption_frame.pack(side=TOP)


txt_dec = scrolledtext.ScrolledText(decryption_text_frame, undo=True, width=60, height=10)
txt_dec['font'] = ('consolas', '10')
txt_dec.pack(expand=True)

back_decryption_frame_btn = Button(decryption_text_frame, text="Back", bg="#20bebe", fg="white", font="Cairo",
                                   height=1, width=15, command=lambda: back_to_encryption_frame())
back_decryption_frame_btn.pack(side=TOP)

root.mainloop()
