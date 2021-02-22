#!/usr/bin/env python3

import sys
import os
import subprocess
import threading
import argparse
import math
# from termcolor import colored

# with open("host.txt","r+") as hosts:
# 	for line in hosts:
# 		host=line.strip()
# 		# with open(os.devnull,"w+"):
# 		subprocess.call('''cat '''+filename+'''|grep -i '''+host+'''| cut -d '/' -f 1,2,3 --complement|awk '{print "/"$0}' |tee path.txt''',shell=True,stdout=DNULL,stderr=DNULL)
# 		subprocess.call('''meg -c 2000 -d 500 path.txt '''+host+''' meg_out ''',shell=True,stdout=DNULL,stderr=DNULL)

DNULL=open(os.devnull,"w+")



def get_args():
    parser = argparse.ArgumentParser("meg vesion 2 script to pass only one wordlist of all domains endpoints.\n\n")
    parser.add_argument("-t", "--threads", dest="threads", help="[-]Number of threads [default=3]")
    parser.add_argument("-w", "--wordlist", dest="wordlists", help="[-]Enter the wordlist to use [ignore for default]")
    options = parser.parse_args()
    if not options.wordlists:
        parser.error("[-] Specify wordlist, use --help for Help")
    else:
        return options

def num_of_lines(wordlist):
	num_lines=0
	with open(wordlist,"r") as fp:
		for line in fp:
			num_lines +=1           #Everytime the line is read Num_lines is incremented
		return num_lines


def meg_modified(wordlist,starto,endo):
	try:
		start_line = starto                         
		end_line = endo                             
		with open("host.txt", "r") as wordlist:
			for line in range(start_line):         
				wordlist.readline()           
			for line in wordlist:
				host = line.strip()                           
				subprocess.call('''cat '''+filename+'''|grep -i '''+host+'''| cut -d '/' -f 1,2,3 --complement|awk '{print "/"$0}' |tee path.txt''',shell=True,stdout=DNULL,stderr=DNULL)
				print(f"[+] started meg on {host}","yellow")
				subprocess.call('''meg -c 2000 -d 500 path.txt '''+host+''' meg_out ''',shell=True,stdout=True,stderr=True)
				print(f"[-] scan completed on {host}","green")
				start_line +=1
				if(start_line==end_line):      # Traverse until the specified end_line
					break
	except KeyboardInterrupt:
		print ("\n Exiting...")



options = get_args()
filename = options.wordlists

if options.threads:                        
    no_of_threads= int(options.threads)
else:
    no_of_threads=3

subprocess.call('''cat '''+filename+'''| awk -F "/" '{print $1"/"$2"/"$3}'|sort -u | tee host.txt''',shell=True,stdout=DNULL,stderr=DNULL)
print(f"[+] File Read Succesfull [{filename}]")

total_words = num_of_lines("host.txt")
each_thread_words = math.ceil(total_words/no_of_threads)         
begin=0                                                    
end=each_thread_words                      
try:
		
	for i in range(no_of_threads):                                                 #Looping as times as the threads given
		t1 = threading.Thread(target=meg_modified, args=("host.txt",begin,end))      #Creating Thread
		t1.start()                                                            #Starting Thread 
		begin += each_thread_words                                                 #After creating 1st thread add total_words to both begin & end
		end += each_thread_words

except KeyboardInterrupt:
	print ("\n Exiting...")

