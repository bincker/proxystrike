#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

import sys
import traceback

class Console:
	def __init__(self,prompt):
		self.prompt=prompt
		self.banner=""

		self.commands={}
		self.cmdorder=[]
		for i in dir(self):
			if "CMD_"==i[:4]:
				cmd=i.split("CMD_")[1].lower()
				self.cmdorder.append(cmd)
				self.commands[cmd]=getattr(self,i)

		#######   DEFAULT VARS (begins with CFG_)  ###########################
		self.CFG_DEBUG=False

		self.configvars={}
		for i in dir(self):
			if "CFG_"==i[:4]:
				var=i.split("CFG_")[1]
				self.configvars[var]=i


	def run(self):
		while True:
			try:
				command=raw_input(self.prompt)
				self.execCommand(command)
			except KeyboardInterrupt:
				break
			except EOFError:
				break
			except Exception,a:
				self.printError (a)

		self.exit()

		print "\r\n\r\nBye!..."


	def exit(self):
		pass

	def printError(self,err):
		sys.stderr.write("-- Error: %s\r\n" % (str(err)))
		if self.CFG_DEBUG:
			pass

	def execCommand(self,cmd):
		words=cmd.split(" ")
		words=[i for i in words if i]
		if not words:
			return
		cmd,parameters=words[0].lower(),words[1:]

		if not cmd in self.commands:
			raise Exception,"Command '"+cmd+"' not found. Try 'help'\r\n"

		self.commands[cmd](*parameters)

	######## DEFAULT COMMANDS (begins with CMD_) ################

	def CMD_help(self,*args):
		'''help					- Show's help'''
		print self.banner

		print "help"
		print "-----------------------------------------------------------------"
		print

		for i in self.cmdorder:
			print "%s" % (self.commands[i].__doc__)

		print


	def CMD_config(self,*args):
		'''config					- Show config variables'''
		print "Configuration variables\r\n---------------------------------------------"
		for i,j in self.configvars.items():
			print "|%20s | %20s|" % (i,getattr(self,j))

		print

	def CMD_set(self,*args):
		'''set [variable_name] [value]		- Set configuration variable value
					Values are python expressions: 1, True, "How are you".lower()'''
		value=" ".join(args[1:])

		if args[0] not in self.configvars:
			raise Exception,"Variable %s doesn't exist" % (args[0])

		setattr(self,"CFG_"+args[0],eval(value))

