import ctypes
import inflect
from .import math, date, explorer, savedata
def messagebox(title, message):
	#This function displays message box on the user's screen.
	user32 = ctypes.windll.user32
	user32.MessageBoxA(0, message.encode("utf-8"), title.encode("utf-8"), 0x00000050)
def number_to_words(numbers, include_and=False):
	#number_to_words converter.
	p = inflect.engine()
	words = p.number_to_words(numbers)
	if not include_and:
		words = words.replace(" and ", " ")
	words=words.replace(",", "")
	return words
def convert_list(self,arr,each=", "):
	lists = ""
	if len(arr) == 0: return ""
	if len(arr) == 1: return arr[0]
	for i in range(len(arr)):
		if i == len(arr) - 1:
			lists += f"and {arr[i]}"
		else:
			lists += f"{arr[i]}{each}"
	return lists
def is_over_value(pars, currentc = 0):
	if currentc < 0 or currentc > len(pars) - 1: return True
	else: return False
def is_over_value(lena, currentc = 0):
	if currentc < 0 or currentc > lena - 1: return True
	else: return False
def var_replace(text, replacers = [], opening = "%", closing = "%"):
	if len(replacers) < 1:
		return text
	for i, replacer in enumerate(replacers):
		if text.find(f"{opening}{i+1}{closing}") > -1:
			text = text.replace(f"{opening}{i+1}{closing}", replacer, 1)
	return text
def var_replace2(text, fir = [], sec = []):
	if len(fir) < 1:
		return text
	if len(fir) != len(sec):
		return text
	for i, f in enumerate(fir):
		if text.find(f) > -1:
			text = text.replace(f, sec[i], 1)
	return text