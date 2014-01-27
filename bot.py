#Kevin Law
#Irc bot for remote server acccess when SSH, VNC, and all else have failed.
#
#
#Can be run with screen to be ran as service.
#Run in linux for full functionality.
#Run as sudo for full rights.
#Usage: 
# sudo python bot.py
# sudo python bot.py | tee logfile.log

###################### IMPORTS ######################
import socket  #the bot connects using the socket library
import random
import platform
import commands

###################### VARIABLES ####################     
buffsize = 2048
server = "irc.freenode.net" #Edit to your IRC server
port = 6667
channel = "#rawr" #Edit to the channel you want
nick = "ServerAdminBot" #Edit nick

###################### DEFINES ######################

def connect():
	try:
		ircwrench.connect((server, port)) #connect to server
	except socket.error:
		print "There has been an error, let's try that again."
		ircwrench.connect((server, port)) #connect to server again
	else:
		ircwrench.send("USER "+ nick +" "+ nick +" "+ nick + " ServerAdmin\n") #USER <username> <hostname> <servername> <realname> (RFC 1459)
		ircwrench.send("NICK "+ nick +"\n") #assign a nick to bot


def join(chan):
  ircwrench.send("JOIN "+ chan +"\n")
  
def ping(): #respond to server pings.
  ircwrench.send("PONG :Pong\n")

def sendmessage(chan , msg): #This simplifies sending messages to the channel.
  ircwrench.send("PRIVMSG "+ chan +" :"+ msg +"\n")
 
def hello():
  sendmessage(channel, "HELLO THERE.")

def joke():
	lines = open('/home/nuke/Documents/python/joke.txt').read().splitlines()
	myline =random.choice(lines)
	sendmessage(channel, str(myline))
					
def assist():
	sendmessage(channel, "ServerAdminBot ready for service.")
	sendmessage(channel, "commands are: " + "\n")
	sendmessage(channel, "$hello, $info, $quit, $backup, $command, and $joke")
	
			
def initiate():
	while 1:
		stream = ircwrench.recv(buffsize) #data from the server
		stream = stream.strip('\n\r') #strips data of line breaks
		print(stream) # Here we print what's coming from the server


#Commands from the IRC server
		if stream.find(":Nickname is already in use") != -1:
			newnick = nick + str(random.randint(1,100))
			ircwrench.send("NICK "+ newnick +"\n") 
			join(channel)

		if stream.find("PING :") != -1: # if the server pings us then we've got to respond!
			ping()
  
  
#Commands from user:
		if stream.find("$quit") != -1:
			ircwrench.send("QUIT" + "\n")
			break
      
		if stream.find("$hello") != -1:
			hello()
  
		if stream.find("$info") != -1:
			info = platform.uname()
			sendmessage(channel, str(info))

		if stream.find("$joke") != -1:
			joke()
	  
		if stream.find("$backup") != -1:  #Making this a subroutine would require nested while loops, which ended up bad.
			try:
				parts = stream.split()# parts: [':User@champlain.edu', 'PRIVMSG', '#rawr', ':$backup', 'source', 'dest']
				source = parts[4]
				dest = parts[5]
				sendmessage(channel, "source: " + source)
				sendmessage(channel, "destination: " + dest)
				
			except IndexError:
				sendmessage(channel, "Invalid syntax, $backup /source/directory/ /dest/directory/")
				print parts
			else:
				info = str(commands.getstatusoutput("cp -r -u -x " + source + " " + dest))
				sendmessage(channel, info)
				sendmessage(channel, "command successful")
 
		if stream.find("$command") != -1: #Same as backup
		#useful: http://www.howtoforge.com/useful_linux_commands
		#usage: $command [command1] [arg]
		#Will add support for more arguments.
			try:
				command = " "
				arg = " "
				parts = stream.split()# parts =  [':User@champlain.edu', 'PRIVMSG', '#rawr', ':$command', 'command', 'arg']
				if len(parts) > 5:# Checks LENGTH, not index in list
					command = parts[4]
					arg = parts[5]
				elif len(parts) == 5:
					command = parts[4]
					arg = ''
			except IndexError:
				sendmessage(channel, "Invalid syntax, usage: $command <command> [arg]")
				print parts
			else:
				info = str(commands.getoutput(command + " " + arg))
				info = info.replace('\n', ' ')

				sendmessage(channel, info)
		

		if stream.find("$help") != -1:
			assist()		
		
###################### START PROGRAM ################				
ircwrench = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect()
join(channel) #Join the channel
sendmessage(channel, "ServerAdminBot Connected.")
initiate()
