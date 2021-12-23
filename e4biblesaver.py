#!/usr/bin/python3
import math, random
import re
import time
import tkinter as tk
import sqlite3 

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
		self.db = "/usr/share/e4biblesaver/bible.sqlite3"
		self.conn = sqlite3.connect(self.db)
		self.interval = 10
		self.total_verses = self.conn.cursor().execute('SELECT COUNT(*) FROM verses').fetchone()[0]
		self.window.attributes('-fullscreen', True)
		self.window.configure(bg = 'black')
		self.verse = tk.Label(self.window, text = '', font = ('Sans Italic', self.font_size), fg = 'white', bg = 'black')
		self.verse.pack()
		self.set_verse()
		self.window.after(1000, self.bind_events)
		self.window.mainloop()
	
	def end_program(self, handler):
		self.conn.close()
		self.window.destroy()
		
	def get_verse(self):
		random_verse_number = random.randrange(0, self.total_verses)
		random_verse = self.conn.cursor().execute(f'SELECT * FROM verses INNER JOIN books ON books.id=verses.book WHERE verses.rowid={random_verse_number}').fetchone()
		chapter = random_verse[1]
		verse_number = random_verse[2]
		verse_text = random_verse[3]
		book = random_verse[5]
		formatted = f'{book} [{chapter}:{verse_number}] {verse_text}'
		formatted_len = len(formatted)
		last_space = 0
		if formatted_len > self.max_verse_len:
			for i in range(0, formatted_len):
				formatted = list(formatted)
				# Current character
				c = formatted[i]
				if c.isspace():
					last_space = i
				if i > 0 and ((i % self.max_verse_len) == 0):
					formatted[last_space] = '\n'
				
		formatted = ''.join(formatted)
		return formatted
	
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
		self.verse.config(text = self.get_verse())
		self.window.update()
		screen_width = self.window.winfo_screenwidth()
		screen_height =  self.window.winfo_screenheight()
		verse_width = self.verse.winfo_width()
		verse_height = self.verse.winfo_height()
		self.verse.place(x = random.randrange(0, screen_width - verse_width), y = screen_height + verse_height - round(screen_height / 2, 0))
		self.window.after(self.interval, self.move_verse)
			
if __name__ == "__main__":
	bible = E4BibleSaver()
