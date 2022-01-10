from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os, glob

root = Tk()
root.title('Cookie Clicker')
root['bg'] = '#F7F7F7'
root.geometry('500x425')
style = ttk.Style()
style.configure('W.TButton', bg='#2389FF')
clickers = 0
clicker_cost = 100

def executeterminal(cmd):
	global score
	if cmd[0:8] == 'score +=' and isinstance(score, int):
		score += int(cmd[9:len(cmd)])
		score_update()
	else:
		exec(cmd)

def terminal(*args):
	ter = Toplevel(root)
	ter.title('Terminal')

	ttk.Label(ter, text='Terminal/Console:  ')

	enter = ttk.Entry(ter, width=30)
	enter.pack(fill=X, padx=5, pady=5)

	ttk.Button(ter, text='Execute', command=lambda: executeterminal(enter.get())).pack(pady=15, ipadx=5)

def add_cookie(*args):
	global score
	if isinstance(score, int):
		score += 1
	score_update()
	cookie['image'] = cookie_small
	root.after(60, normal_cookie)

def add_clicker():
	global score, clickers, clicker_buy, clicker_cost
	if score >= clicker_cost:
		score -= clicker_cost
		clickers += 1
		d = int(clicker_cost/2.5)
		clicker_cost += d
		try:
			clickers_view['image'] = mouses[clickers-1]
		except IndexError:
			score+=clicker_cost
			clicker_cost -= d
			messagebox.showinfo('Cookie Clicker', 'All Clickers Sold')
			return 'Error: AllClickersSold {ErrorCode:1}'
		clicker_buy['text'] = f'Clicker ({clicker_cost} Cookies)'
		score_update()
		root.after(1000, clicker_activate)

def clicker_activate():
	global score, clickers
	score += 2
	score_update()
	root.after(1000, clicker_activate)

def score_update():
	global score
	if score >= 1000000000000000000000000000000000000000000000000000000000000:
		score = 'Infinity'
		scoretoscreen()
	elif score == 'Infinity':
		entity_scorelbl['text'] = f'Infinity Cookies'
	else:
		entity_scorelbl['text'] = f'{score} Cookies'

def normal_cookie():
	cookie['image'] = cookie_img

panesys = PanedWindow(root)
panesys.pack(fill='both', expand=1)

game_frame = Frame(root, bg='#F7F7F7', width=450, height=425)
#game_frame.pack(side=LEFT, fill=Y)

score = 0
entity_scorelbl = Label(game_frame, text='0 Cookies', bg='#F7F7F7')
entity_scorelbl.pack(pady=5)
origdir = os.getcwd()
mouses = []
numeral = 0
os.chdir('Lib')

for t in glob.glob('*.png'):
	if t != 'cookie.png':
		numeral += 1
for m in range(numeral+1):
	if m == 0:
		continue
	mouses.append(ImageTk.PhotoImage(Image.open(f'{m}.png')))

cookie_img = ImageTk.PhotoImage(Image.open('cookie.png').resize((410, 380)))
cookie_small = ImageTk.PhotoImage(Image.open('cookie.png').resize((390, 360)))
cookie = Label(game_frame, image=cookie_img, cursor='hand2', bg='#F7F7F7')
cookie.pack()
clickers_view = Label(game_frame, text='No Clickers!', bg='#F7F7F7')
clickers_view.pack()

store = Frame(root, bg='#2389FF')
#store.pack(fill='both', expand=1)

Label(store, text='Store', bg='#2389FF').pack(pady=5)
clicker_buy = ttk.Button(store, text='Clicker (100 Cookies)', command=add_clicker, style='W.TButton')
clicker_buy.pack(pady=10, ipadx=10)

panesys.add(game_frame)
panesys.add(store)


cookie.bind('<Button-1>', add_cookie)
root.bind('<Control-t>', terminal)
root.mainloop()