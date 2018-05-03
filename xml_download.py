"""
	MAL lists downloader
	Realistically, just creates back-ups of your anime & manga lists (in raw xml form)
	My last use of the official MAL API didn't go well, so I will just be using web-scraping
"""

import argparse
import requests
from bs4 import BeautifulSoup
from os import path, listdir
from re import search, compile, escape, sub
from datetime import date
from math import ceil

MANGA="manga"
ANIME="anime"

#get commandline arguments
#return argparse object
def get_args():
	parser = argparse.ArgumentParser()
	
	parser.add_argument("-u", help="username", nargs=1, required=True, metavar="username", dest="username")
	parser.add_argument("-o", help="output destination", nargs=1, required=False, metavar="output destination", dest="out", default=["./"])
	
	args_in = parser.parse_args()
	
	return args_in
	
#retrieves the list's xml text
#type -> (ANIME or MANGA constants)
#return -> xml text
def get_list(type):
	args_in = get_args()
	url = "https://myanimelist.net/malappinfo.php?u=" + args_in.username[0] + "&status=all&type=" + type

	#get page
	page = requests.get(url)
	
	#200 means the page downloaded correctly
	if not (page.status_code == 200):
		raise Exception("ERROR: bad status code. Page returned with status " + page.status_code)
	
	soup = BeautifulSoup(page.text, "html.parser")
	return soup.prettify()

#determines output path for file
#pth -> input path from arguments
#username -> input username from argumeents
#type -> (ANIME or MANGA constants)
#return -> path to use
def get_final_path(pth, username, type):
	
	#if the user gives a file, we output there
	if path.isfile(pth):
		return pth
	
	#otherwise, we have to make our own file name in the given folder
	#file name format = USERNAME_(ANIME/MANGA)_list_YEAR_MONTH_DAY_UNIQUE-IDENTIFIER.xml
	if path.isdir(pth):
		curr_date = date.today()
		num_to_use = 0
		def_file = username + "_" + type + "_list_" + str(curr_date.year) + "_" + str(curr_date.month) + "_" + str(curr_date.day)
		fl_ptn = compile(escape(def_file))
		
		#find any files with a similar naming scheme - we want the unique identifier to actually be unique
		files = [f for f in listdir(pth) if (path.isfile(f) and (not (((search(fl_ptn,f)) is None))))]
			
		#find the highest identifier and we want ours to be +1 to indicate that it is the newest addition
		for f in files:
			num = sub(compile(escape(pth)), "", f)
			num = sub(fl_ptn, "", num)
			
			try:
				num = int(num)
				if num >= num_to_use:
					num_to_use = num + 1
			except:
				pass
		
		#finalize the path
		out_file = pth + def_file + str(num_to_use) + ".xml"
		return out_file

	#if we got here, then the path given is neither a file or folder
	raise Exception("ERROR: path '" + pth + "' could not be found")
			
#had to make a function for this (regrettably) due to some unicode output errors
#pain in the ass, but it gets the job done
#seems to be a windows problem
#internet folks keep saying it was fixed as of 3.0 - I'm on 3.6 so no, it wasn't
def output_file(text, outfile):
	try:
		oufile.write(text)
	except:
		#some error, so we'll localize it
		
		if (len(text) <= 10):
			#if it's small, loop through it
			for char in text:
				try:
					outfile.write(char)
				except:
					pass
		else:
			#otherwise, we'll do a binary split
			half = ceil(len(text)/2)
			output_file(text[:half], outfile)
			output_file(text[half:], outfile)
			
#outputs the list the user wants
#type -> ANIME or MANGA constants
def output_list(type):
	args_in = get_args()

	pth = get_final_path(args_in.out[0], args_in.username[0], type)
	xml_data = get_list(type)
	
	with open(pth, 'w') as outfile:
		output_file(xml_data, outfile)
	
output_list(ANIME)
output_list(MANGA)