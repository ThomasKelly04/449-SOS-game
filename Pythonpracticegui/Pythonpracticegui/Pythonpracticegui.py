import tkinter as tk   
root = tk.Tk()
root.title("Simple GUI")
root.geometry("900x600")

label = tk.Label(root, text="SOS game", font=("Papyrus", 14))
label.pack(pady=10)

canvas = tk.Canvas(root, width=300, height=300, bg="white")
canvas.pack(pady=10)

canvas.create_line(10, 50, 300, 50, fill='black', width=2)
canvas.create_line(10, 80, 300, 80, fill='black', width=2)
canvas.create_line(10, 110, 300, 110, fill='black', width=2)
canvas.create_line(10, 140, 300, 140, fill='black', width=2)
canvas.create_line(10, 170, 300, 170, fill='black', width=2)
canvas.create_line(10, 200, 300, 200, fill='black', width=2)
canvas.create_line(10, 230, 300, 230, fill='black', width=2)
canvas.create_line(10, 260, 300, 260, fill='black', width=2)

canvas.create_line(50, 10, 50, 300, fill='black', width=2)
canvas.create_line(80, 10, 80, 300, fill='black', width=2)
canvas.create_line(110, 10, 110, 300, fill='black', width=2)
canvas.create_line(140, 10, 140, 300, fill='black', width=2)
canvas.create_line(170, 10, 170, 300, fill='black', width=2)
canvas.create_line(200, 10, 200, 300, fill='black', width=2)
canvas.create_line(230, 10, 230, 300, fill='black', width=2)
canvas.create_line(260, 10, 260, 300, fill='black', width=2)



check_var = tk.BooleanVar()

checkbox = tk.Checkbutton(root, text="Advanced mode", variable=check_var)
checkbox.pack(pady=5)

radio_var = tk.StringVar(value="Option 1")

radio1 = tk.Radiobutton(root, text="Singe Player", variable=radio_var, value="Option 1")
radio2 = tk.Radiobutton(root, text="Two player", variable=radio_var, value="Option 2")

radio1.pack()
radio2.pack()

root.mainloop()