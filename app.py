# imports
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import speech_recognition as sr
from PIL import Image, ImageTk, ImageSequence
import PySimpleGUI as sg
import pyttsx3
import datetime
import os
import ctypes
import webbrowser
import psutil
import pyautogui
import time
import requests
import random
import wikipedia
import PlaySound
import threading

# text 2 speech engine
engine = pyttsx3.init()
voice = engine.getProperty('voices')
engine.setProperty('rate', 180)
engine.setProperty('volume', 2.0)
engine.setProperty('voice', voice[2].id)



'''			Background Animating			'''
class AnimateGif(object):
	def __init__(self, image):
		self._frames = []
		img = Image.open(image)
		for frame in ImageSequence.Iterator(img):
			photo = ImageTk.PhotoImage(frame)
			photo.delay = frame.info['duration'] * 10
			self._frames.append(photo)

	def __len__(self):
		return len(self._frames)
	
	def __getitem__(self, frame_num):
		return self._frames[frame_num]
	
def update_label_image(label, ani_img, ms_delay, frame_num):
	global cancel_id
	label.configure(image=ani_img[frame_num])
	frame_num = (frame_num + 1) % len(ani_img)
	cancel_id = root.after(ms_delay, update_label_image, label, ani_img, ms_delay, frame_num)
	
def enable_animation():
	global cancel_id
	if cancel_id is None:
		ms_delay = 5000 // len(ani_img)
		cancel_id = root.after(ms_delay, update_label_image, animation, ani_img, ms_delay, 0)

def cancel_animation():
	global cancel_id
	if cancel_id is not None:
		root.after_cancel(cancel_id)
		cancel_id = None

'''------------------------------------------'''


# reply methods
try:
	user = psutil.users()[0][0].split()[1]
except Exception as e:
	user = psutil.users()[0][0].split()[0]
greeting = ["Hello sir", "Hello", "Hi", "oh hello sir", f"hello {user}!"]
ok = ["As you wish", "As you wish sir", "As you wish boss", "OK sir", "OK", "Yes sir", "OK boss", "Will do sir"]

# Functions
def talk(audio):
	engine.say(audio)
	engine.runAndWait()

def upTime():
	lib = ctypes.windll.kernel32
	t = lib.GetTickCount64()
	t = int(str(t)[:-3])

	mins, sec = divmod(t, 60)
	hours, mins = divmod(mins, 60)
	days, hours = divmod(hours, 24)
	if days == 0:
		talk('Sir, You have used your computer for ' + str(hours) + ' hours, and ' + str(mins) + ' minuts.')
	else:
		talk('Sir, You have used your computer for ' + str(days) + ' days, ' + str(hours) + ' hours, and ' + str(mins) + ' minuts.')

def take_screenshot():
	#root.iconify()
	talk(random.choice(ok))
	ss = pyautogui.screenshot()
	ss.save(os.environ['USERPROFILE']+'\\Pictures\\JARVIS - Screenshot.png')
	talk('This is the screenshot taken by me')
	os.startfile(os.environ['USERPROFILE']+'\\Pictures\\JARVIS - Screenshot.png')
	time.sleep(2)
	talk('Here is your screenshot. I renamed the screenshot as, JARVIS - Screenshot.png')
	os.startfile(os.environ['USERPROFILE']+'\\Pictures')

def takeCommand():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		PlaySound.playSound("media/sounds/listening.wav")
		print("Listening")
		audio = r.listen(source)
		query = ""

		try:
			PlaySound.playSound("media/sounds/recognized.wav")
			print("Recognizing...")
			query = r.recognize_google(audio, language="en-IN")
			print(f"User said: {query}")
		except Exception as e:
			pass
	return query.lower()


def run():
	while True:
		command = takeCommand()
		if 'time' in command:
			talk('The current time is ' +
				datetime.datetime.now().strftime('%I:%M %p') + '.')
			print("JARVIS: " + 'The current time is ' +
				datetime.datetime.now().strftime('%I:%M %p') + '.')

		elif any([i in command for i in ['hello', 'hi']]):
			talk(random.choice(greeting))
		
		elif any([i in command for i in ['are you there', 'you up', 'you in there']]):
			talk("For you sir, always")

		elif any([i in command for i in ['offline', 'go to sleep']]):
			talk(" alright then, I am switching off")
			exit(1)
			root.destroy()

		elif any([i in command for i in ['today', 'date', 'day']]):
			talk('Today is ' + str(datetime.date.today()) + ' sir.')

		elif any([i in command for i in ['who are you', 'about you', 'yourself']]):
			talk('Hello sir! I am NIX. Your PC Assistant. I am here to assist you with the varieties tasks is best I can.')

		elif 'version' in command:
			talk('NIX version 1.7')
			messagebox.showinfo("NIX", "NIX Voice Assistant \n\nCore Version:\t\t1.7\nGUI Version:\t\t1.1")

		elif "wikipedia" in command:
			try:
				talk(random.choice(ok) + ', Searching Wikipedia...') 
				query = command.replace("wikipedia", "") 
				results = wikipedia.summary(query, sentences=2) 
				talk("According to Wikipedia, ") 
				print(results) 
				talk(results)
			except Exception as e:
				talk("Make sure you have connected with the internet!")
				print(e)
				pass

		elif 'pc usage' in command:
			upTime()

		elif any([i in command for i in ['take screenshot', 'take snapshot', 'screenshot']]):
			take_screenshot()
		
		elif all([i in command for i in ['open', 'facebook']]):
			talk('Opening Facebook from your web browser. Just a moment')
			webbrowser.open('www.facebook.com')

		elif all([i in command for i in ['open', 'instagram']]):
			talk('Opening Instagram from your web browser. Just a moment')
			webbrowser.open('www.instagram.com')

		elif all([i in command for i in ['open', 'youtube']]):
			talk('Opening YouTube from your web browser. Just a moment')
			webbrowser.open('www.youtube.com')

		elif all([i in command for i in ['open', 'stackoverflow']]):
			talk('Opening stackoverflow from your web browser. Just a moment')
			webbrowser.open('www.stackoverflow.com')

		elif all([i in command for i in ['open', 'google']]):
			talk('Opening Google Search Engine. Just a moment')
			webbrowser.open('www.google.com')

		elif 'cpu' in command:
			talk('CPU is at ' + str(psutil.cpu_percent()) + '%.')

		elif 'ram percentage' in command:
			talk('System Memory is at ' + str(psutil.virtual_memory().percent) + '%.')

		elif 'cores' in command:
			talk('There are ' + str(psutil.cpu_count()) + ' logical CPUs in your Computer')

		elif 'available ram' in command:
			ram = round((psutil.virtual_memory().available) / (1024 ** 3), 2)
			talk('Available System Memory is ' + str(ram) + 'GB')

		elif 'used ram' in command:
			ram = round((psutil.virtual_memory().used) / (1024 ** 3), 2)
			talk('Used System Memory is ' + str(ram) + 'GB')

		elif 'total ram' in command:
			ram = round((psutil.virtual_memory().total) / (1024 ** 3), 2)
			talk('Total System Memory is ' + str(ram) + 'GB')

		elif all([i in command for i in ['create', 'python', 'file']]):
			try:
				talk(random.choice(ok) + ', Creating Python File')
				path = os.environ['USERPROFILE']+'\\Desktop'
				f = open(f'{path}\\Python File.py', 'w')
				f.write('# Made by NIX AI Assistant\n\n')
				f.close()
				sg.popup_notify(f'File Created\nin {path}\\Python File.py', title='Done')
			except:
				talk('Error creating Python File')
				pass

		elif all([i in command for i in ['create', 'html', 'file']]):
			try:
				talk(random.choice(ok) + ', Creating a HTML Document')
				path = os.environ['USERPROFILE']+'\\Desktop'
				f = open(f'{path}\\HTML File.html', 'w')
				f.write('<!DOCTYPE html>\n<html lang="en-us">\n<head>\n\t<title>HTML File</title>\n</head>\n<body>\n\t<h1>Made by NIX AI Assistant</h1>\n</body>\n</html>')
				f.close()
				sg.popup_notify(f'File Created\nin {path}\\HTML File.html', title='Done')
			except:
				talk('Error creating HTML File')
				pass

		elif all([i in command for i in ['create', 'java', 'file']]):
			try:
				talk(random.choice(ok) + ', Creating a JAVA File')
				path = os.environ['USERPROFILE']+'\\Desktop'
				f = open(f'{path}\\Java_File.java', 'w')
				f.write('public class Java_File\n{\t// Made by NIX\n\tpublic static void main(String args[])\n\t{\n\tSystem.out.println("Made by NIX AI Assistant");\n\t}\n}')
				f.close()
				sg.popup_notify(f'File Created\nin {path}\\Java_File.java', title='Done')
			except:
				talk('Error creating Java File')
				pass

		elif all([i in command for i in ['create', 'css', 'file']]):
			try:
				talk(random.choice(ok) + ', Creating a CSS styling sheet document')
				path = os.environ['USERPROFILE']+'\\Desktop'
				f = open(f'{path}\\style.css', 'w')
				f.write('body\n{\n\tbackground-color: #ff0;\n}')
				f.close()
				sg.popup_notify(f'File Created\nin {path}\\style.css', title='Done')
			except:
				talk('Error creating CSS document')
				pass

		elif all([i in command for i in ['create', 'php', 'file']]):
			try:
				talk(random.choice(ok) + ', Creating a PHP file. To run the file, you need to move this file into your server or server folder')
				path = os.environ['USERPROFILE']+'\\Desktop'
				f = open(f'{path}\\action.php', 'w')
				f.write('// Made with NIX\n\necho "Made by NIX AI Assistant";')
				f.close()
				sg.popup_notify(f'File Created\nin {path}\\action.php', title='Done')
			except:
				talk('Error creating PHP file')
				pass

		elif all([i in command for i in ['create', 'python', 'file']]):
			try:
				talk(random.choice(ok) + ', Creating a JavaScript file.')
				path = os.environ['USERPROFILE']+'\\Desktop'
				f = open(f'{path}\\script.js', 'w')
				f.write('// Made with NIX\n\ndocument.write("Made by NIX AI Assistant");')
				f.close()
				sg.popup_notify(f'File Created\nin {path}\\action.php', title='Done')
			except:
				talk('Error creating PHP file')
				pass

		elif any([i in command for i in ['volume up', 'increase volume']]):
			talk('Increasing volume')
			pyautogui.press("volumeup")
			pyautogui.press("volumeup")
			pyautogui.press("volumeup")
			pyautogui.press("volumeup")

		elif any([i in command for i in ['volume down', 'decrease volume']]):
			talk('Decreasing volume')
			pyautogui.press("volumedown")
			pyautogui.press("volumedown")
			pyautogui.press("volumedown")
			pyautogui.press("volumedown")

		elif any([i in command for i in ['mute', 'unmute']]):
			talk('Sound muted')
			pyautogui.press("volumemute")

		elif all([i in command for i in ['ip', 'address']]):
			talk("Checking") 
			try: 
				ipAdd = requests.get('https://api.ipify.org').text 
				talk("your ip adress is " + ipAdd)
			except Exception as e: 
				talk("network is weak, please try again some time later")

		elif any([i in command for i in ['minimize the window', 'minimise the window', 'minimize', 'minimise']]):
			talk(random.choice(ok))
			root.iconify()

		# elif 'play song' in command:
		# 	talk('The songs has been playing started. If you want to pause it, you can cant do it just selecting, Pause Song ')
		# 	playSong()

		# elif 'pause song' in command:
		# 	pauseSong()

		# elif 'stop song' in command:
		# 	stopSong()

		# elif 'video' in command:
		# 	try:
		# 		talk('Please select a video file to play')
		# 		path = filedialog.askopenfilename(filetypes=[('MP4 Files', '*.mp4')], defaultextension=('.mp4'), title='Choose a Video to play')
		# 		if path == '':
		# 			talk('Process canceled by user.')
		# 			pass
		# 		else:
		# 			talk('Playing the video you selected! Just a moment')
		# 			os.startfile(os.path.join(path))
		# 	except:
		# 		pass

		elif 'shutdown' in command:
			talk('Closing JARVIS PC Assistant')
			talk('Initializing shutdown sequence. Shutting System down.')
			os.system('shutdown.exe -s -t 00')

		elif 'restart' in command:
			talk('Closing JARVIS PC Assistant')
			talk('Initializing shutdown sequence. Restarting System.')
			os.system('shutdown.exe -r -t 00')

		elif 'log off' in command:
			talk('Closing JARVIS PC Assistant')
			talk('Initializing shutdown sequence. Logging System off.')
			os.system('shutdown.exe -l')

		elif 'lock' in command:
			talk('Locking your PC. Just a moment.')
			os.system('rundll32.exe user32.dll, LockWorkStation')

		elif 'hibernate' in command:
			try:
				talk('Hibernating Your PC.')
				talk('Initializing shutdown sequence. Logging System off.')
				os.system('rundll32.exe powrprof.dll, SetSuspendState')
			except:
				talk('Sorry Sir, your PC has no hibernation ability. To hibernate your PC, You need to activate it.')
				talk('This video will help you.')
				webbrowser.open('https://youtu.beYU681US3NS8')

		elif any([i in command for i in ['open file explorer', 'open explorer']]):
			talk('Opening Windows Explorer')
			path = 'C:\\Windows\\explorer.exe'
			os.startfile(os.path.join(path))

		elif all([i in command for i in ['open', 'notepad']]):
			talk('Openin Windows Notepad')
			path = 'C:\\WINDOWS\\system32\\notepad.exe'
			os.startfile(os.path.join(path))

		elif 'about windows' in command:
			talk('Getting details about the Main Operating System')
			path = 'C:\\WINDOWS\\system32\\winver.exe'
			os.startfile(os.path.join(path))

		elif all([i in command for i in ['open', 'wordpad']]):
			talk('Opening Windows Wordpad')
			path = 'C:\\Windows\\write.exe'
			os.startfile(os.path.join(path))

		elif 'management' in command:
			talk('Opening Windows System Management Utility')
			path = 'C:\\WINDOWS\\System32\\compmgmt.msc'
			os.startfile(os.path.join(path))

		elif 'programs' in command:
			talk('Opening Add or Remove Programs utility in Control Panel')
			path = 'C:\\WINDOWS\\System32\\appwiz.cpl'
			os.startfile(os.path.join(path))

		elif all([i in command for i in ['open', 'system infomation']]):
			talk('Getting System Information')
			path = 'C:\\WINDOWS\\System32\\msinfo32.exe'
			os.startfile(os.path.join(path))

		elif all([i in command for i in ['open', 'command prompt']]):
			talk('Opening Windows Command Prompt')
			path = 'C:\\WINDOWS\\System32\\cmd.exe'
			os.startfile(os.path.join(path))

		elif all([i in command for i in ['open', 'task manager']]):
			talk('Opening Windows Task Manager')
			path = 'C:\\WINDOWS\\System32\\taskmgr.exe'
			os.startfile(os.path.join(path))

		elif all([i in command for i in ['open', 'registry editor']]):
			talk('Opening Windows Registry Editor')
			path = 'C:\\WINDOWS\\System32\\regedt32.exe'
			os.startfile(os.path.join(path))

		elif 'system volume' in command:
			talk('Launching System Volume Mixer')
			os.startfile('C:\\Windows\\System32\\SndVol.exe')

		elif all([i in command for i in ['open', 'services']]):
			talk('Opening Windows Services. Just a moment.')
			os.startfile('C:\\Windows\\System32\\services.msc')

		elif all([i in command for i in ['open', 'system', 'restore']]):
			try:
				os.startfile('C:\\Windows\\System32\\rstrui.exe')
				talk('Opening Windows System Restore Utility. Just a moment.')
			except:
				talk('Unknown error found on opening Windows System Restore Utility.')
				pass

		elif 'mrt' in command:
			try:
				os.startfile('C:\\Windows\\System32\\MRT.exe')
				talk('Opening Microsoft Malicious software Removal Tool. Just a moment sir')
			except:
				talk('Sorry sir, The Microsoft Malicious software Removal Tool is not available on your Operating System!')

		elif any([i in command for i in ['open defrag tool', 'open defragmentation tool']]):
			talk('Opening Windows Disk Optimizer')
			os.startfile('C:\\Windows\\System32\\dfrgui.exe')

		elif all([i in command for i in ['open', 'control panel']]):
			talk('Opening Windows Control Panel')
			os.startfile('C:\\Windows\\System32\\control.exe')

		elif any([i in command for i in ['open',  'disk cleanup tool']]):
			talk('Opening Windows Disk Cleanup Tool')
			os.startfile('C:\\Windows\\System32\\cleanmgr.exe')

		elif all([i in command for i in ['open', 'character map']]):
			talk('Opening Windows Character Map')
			os.startfile('C:\\Windows\\System32\\charmap.exe')

		elif 'diskpart' in command:
			talk('Opening Windows Diskpart utility')
			os.startfile('C:\\Windows\\System32\\diskpart.exe')

		# application

		elif all([i in command for i in ['open', 'vlc', 'player']]):
			try:
				path = 'C:\\Program Files\\VideoLAN\\VLC\\vlc.exe'
				talk('Opening VLC Media Player')
				os.startfile(os.path.join(path))
			except:
				talk('Sorry sir, you have not installed VLC Media Player on your computer.')
				pass

		elif 'aimp' in command:
			try:
				talk('Opening AIMP Music Player')
				os.startfile('C:\\Program Files (x86)\\AIMP\\AIMP.exe')
			except:
				talk('Sorry sir, you have not installed AIMP Music Player on your computer.')
				pass

		elif all([i in command for i in ['open', 'zoom']]):
			try:
				path = '\\AppData\\Roaming\\Zoom\\bin\\zoom.exe'
				talk('Opening Zoom Cloud Meeting Service')
				os.startfile(os.path.join(os.environ['USERPROFILE']+path))
			except:
				talk('Sorry sir, you have not installed Zoom Cloud Meeting Service on your computer')
				pass

		elif all([i in command for i in ['open', 'sublime text']]):
			try:
				path = 'C:\\Program Files\\Sublime Text\\sublime_text.exe'
				talk('Opening Sublime Text')
				os.startfile(os.path.join(path))
			except:
				talk('Sorry sir, you have not installed Sublime Text on your computer')
				pass

		elif any([i in command for i in ['open visual studio code', 'vs code']]):
			try:
				path = '\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
				talk('Opening Visual Studio Code')
				os.startfile(os.path.join(os.environ['USERPROFILE'] + path))
			except:
				talk('Sorry sir, you have not installed Visual Studio Code on your computer')
				pass
		else:
			talk("Command is not defined, please try another command.")
			pass



root = Tk()
root.title('NIX Assistant')
#ico = root.iconbitmap('icon.ico')
root.resizable(0, 0)
root.config(bg='black')

width_of_window = 260
height_of_window = 250
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = (screen_width / 2) - (width_of_window / 2)
y_cordinate = (screen_height / 2) - (height_of_window / 2)
root.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_cordinate, y_cordinate))

ani_img = AnimateGif("media/gifs/back.gif")
cancel_id = None
animation = Label(image=ani_img[0], bd=0)
#animation.place(x=-110, y=-80)
animation.pack()
enable_animation()
# while True:
# 	run()
#Button(root, text='OK', command=threading.Thread(target=run).start()).pack()
t = 0
def threadStart():
	t = threading.Thread(target=run)
	t.start()

def stop():
	talk("Shutting down NIX AI Assistant")
	exit(1)
	root.destroy()
	

Button(root, text="Start", font="Arial 13", command=threadStart).place(x=50, y=210)
Button(root, text="Stop", font="Arial 13", command=stop).place(x=170, y=210)

root.mainloop()