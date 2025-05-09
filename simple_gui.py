from tkinter import *
root = Tk(

)
root.geometry('600x600')
root.title('Amazon Books Scraper')
myLabel = Label(root, text="Hiiiiiiiiiiiii",padx=300,pady=300)
start_button = Button(root, text="Stat Scraping")
myLabel.grid(row=0,column=0)
start_button.pack()
myLabel.pack()

root.mainloop()