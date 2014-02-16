#!/usr/bin/python2
"""
This file is the main start point for the server program. It initialises the webserver, connects
to the camera and performs general housekeeping.
"""

import server

def main():
	"""
	The main entry point. This is the first function called when the program is started standalone.
	"""
	print("PI-Scanner Server\n------------------------------\n")

	print("Initialising Interface...")
	iserver = server.InterfaceServer(('0.0.0.0', 8080), server.APIHandler)
	print("Server Started. Use the shutdown button to close it.")
	iserver.serve_forever()


if(__name__=="__main__"):
	# script is the main module so call main()
	main()
else:
	# the module has been imported so do nothing!
	pass