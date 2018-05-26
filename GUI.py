from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image  
from markov import MarkovTextBot

PATH = 'datasets/'

class GUI:
	def __init__(self, root):
		self.root = root
		self.root.title("Literary Text Generator")
		self.generated_text = ''
		self.bot = None

		# Create the frame
		self.frame = Frame(root)

		self.menubar = Menu(root)
		filemenu = Menu(self.menubar, tearoff=0)# tearoff = 0 => can't be seperated from window
		filemenu.add_command(label="Reset", underline=1, 
							command=self.reset, accelerator="Ctrl+R")
		filemenu.add_command(label="Custom dataset", underline=1, 
							command=self.get_dataset, accelerator="Ctrl+O")
		filemenu.add_command(label="Save", underline=1, 
							command=self.save_file, accelerator="Ctrl+S")
		filemenu.add_separator()
		filemenu.add_command(label="Quit", underline=2, 
							command=root.quit, accelerator="Ctrl+Q")
		self.menubar.add_cascade(label="Menu", underline=0, menu=filemenu)
		# display the menu
		root.config(menu=self.menubar)

		self.frame.config(bg='LightSteelBlue1')
		self.frame.pack_propagate(False)

		# Create the top label
		self.title_label = Label(root, text="Literary Text Generator")
		self.title_label.config(fg="royal blue")
		self.title_label.pack() # add label to frame
		root.config(menu=self.menubar)

		# Create the text area
		self.text_area = Text(root, height=40, width=180)
		self.yscrollbar = Scrollbar(self.frame, orient="vertical")
		self.yscrollbar.pack(side="right", fill="y")
		self.yscrollbar.config(command=self.text_area.yview)

		# Create the generate button
		self.generate_button = Button(root,
									  text="Generate!",
									  command=self.action_generate)

		self.title_label.config(font=("Helvetica Neue", 44))
		self.choice_label = Label(root, text="Choose dataset:")

		self.fmode = StringVar(root)
		# Dictionary with options
		self.choices = ['George R.R. Martin - A Song of Ice and Fire',
				   		'J.K. Rowling - Harry Potter and the Deathly Hallows'
				   	   ]
		self.file_array = ['gameofthrones.txt', 'hp7.txt']
		for i in range(len(self.file_array)):
			self.file_array[i] = PATH + self.file_array[i]
		self.fmode.set('--') # set the default option

		self.files = OptionMenu(root, self.fmode, *self.choices)
		self.choice_label.pack()
		self.files.pack()
		self.files.config(width=20)

		self.text_area.config(state=DISABLED)
		self.text_area.config(bg='whitesmoke')
		self.text_area.pack()
		self.generate_button.pack()

	def action_generate(self):
		if self.fmode.get() not in ('--', "Custom"):
			file = self.file_array[self.choices.index(self.fmode.get())]
			self.bot = MarkovTextBot(file)
			self.bot.fill_chart()
		self.reset()
		self.generated_text = self.bot.generate_text(1200)
		self.text_area.config(state=NORMAL)
		self.text_area.insert("end",self.generated_text)
		self.text_area.config(state=DISABLED)

	def save_file(self, event=None, filepath=None):
		if filepath == None:
			filepath = filedialog.asksaveasfilename(filetypes=(('Text files', '*.txt'), ('Python files', '*.py *.pyw'), ('All files', '*.*'))) #defaultextension='.txt'
		try:
			with open(filepath, 'wb') as f:
				text = self.text_area.get(1.0, "end-1c")
				f.write(bytes(text, 'UTF-8'))
				self.text_area.edit_modified(False)
				self.file_path = filepath
				self.set_title()
				return "saved"
		except FileNotFoundError:
			print('FileNotFoundError')
			return "cancelled"

	def get_dataset(self, event=None, filepath=None):
		if filepath == None:
			filepath = filedialog.askopenfilename()
		if filepath != None  and filepath != '':
			self.bot = MarkovTextBot(filepath)
			self.bot.fill_chart()
			self.reset()
			self.fmode.set("Custom")

	def reset(self):
		self.text_area.config(state=NORMAL)
		self.text_area.delete(1.0, END)
		self.text_area.config(state=DISABLED)

	def bind_keys(self):
		self.text_area.bind("<Control-o>", self.get_dataset)
		self.text_area.bind("<Control-O>", self.get_dataset)
		self.text_area.bind("<Control-S>", self.save_file)
		self.text_area.bind("<Control-s>", self.save_file)
		self.text_area.bind("<Control-r>", self.reset)
		self.text_area.bind("<Control-R>", self.reset)

if __name__ == '__main__':
	root = Tk()
	gui = GUI(root)
	gui.bind_keys()
	root.mainloop()
