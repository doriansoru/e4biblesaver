#!/usr/bin/python3
import math, random
import re
import time
import tkinter as tk
import e4biblelib

# Factors to resize text
MAX_VERSE_LEN_FACTOR = 41472
FONT_SIZE_FACTOR = 59245

class E4BibleSaver():	
	def __init__(self):
		global FONT_SIZE_FACTOR, MAX_VERSE_LEN_FACTOR
		self.window = tk.Tk()
		product = self.window.winfo_screenwidth() * self.window.winfo_screenheight()
		self.max_verse_len = math.floor(product / MAX_VERSE_LEN_FACTOR)
		self.font_size = math.floor(product / FONT_SIZE_FACTOR)
		self.interval = 10
		self.window.attributes('-fullscreen', True)
		self.window.configure(bg = 'black')
		self.verse = tk.Label(self.window, text = '', font = ('Sans Italic', self.font_size), fg = 'white', bg = 'black')
		self.verse.pack()
		self.set_verse()
		self.window.after(1000, self.bind_events)
		self.window.mainloop()
	
	def end_program(self, handler):
		self.window.destroy()
			
	def move_verse(self):
		new_x = self.verse.winfo_x()
		new_y = self.verse.winfo_y()
		new_y = new_y - 1
		if (new_y + self.verse.winfo_height()) > 0:
			self.verse.place(x = new_x, y = new_y)
			self.window.after(self.interval, self.move_verse)
		else:
			self.set_verse()
	
	def bind_events(self):
		self.window.bind('<KeyPress>', self.end_program)
		self.window.bind('<Motion>', self.end_program)
		self.window.bind('<Button-1>', self.end_program)
		self.window.bind('<Button-2>', self.end_program)
		
	def set_verse(self):
		self.verse.config(text = e4biblelib.get_verse())
		self.window.update()
		screen_width = self.window.winfo_screenwidth()
		screen_height =  self.window.winfo_screenheight()
		verse_width = self.verse.winfo_width()
		verse_height = self.verse.winfo_height()
		self.verse.place(x = random.randrange(0, screen_width - verse_width), y = screen_height + verse_height - round(screen_height / 2, 0))
		self.window.after(self.interval, self.move_verse)
			
if __name__ == "__main__":
	bible = E4BibleSaver()
