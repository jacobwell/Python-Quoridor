"""
The main program for the quoridor game.  The program can be run with one
command line argument which is the name of the config file.	

Author: Sean Strout (sps@cs.rit.edu)
Author: Paul Solt (paul.solt@gmail.com)
"""

import sys
import engine
import config

def main():
	"""Run the engine and start the game"""
		
	if len(sys.argv) == 1:
		sys.argv.append("quoridor.cfg")
		
	if len(sys.argv) != 2:
		print "Usage: python quoridor [config-file]"
		return
	
	cfg = config.Config(sys.argv[1])        # use custom config file
	winningPlayer = engine.run(cfg)
	if winningPlayer != None and not cfg.shortestPath:
		print "Player", winningPlayer, "won the game in", engine.get_num_moves(), "moves."
		return winningPlayer
	else:
		print "No winner."
		return -1
	
if __name__ == "__main__":
    main()