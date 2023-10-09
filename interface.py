"""
This is the interface the player uses to make their moves and communicate
with the engine.   Nothing in this file should be modified by you.

Author: Sean Strout (sps@cs.rit.edu)
Author: Paul Solt (paul.solt@gmail.com)
"""

class PlayerMove(object):
	"""
		The player uses this class to communicate information about their
		next move to the engine.  The engine uses this class internally
		to verify the player's move and update the board display.
    """
	__slots__ = ("playerId", "move", "start", "end")
	
	def __init__(self, playerId, move, start, end):
		"""
		Initialize the object.
		
		playerId: the id for this player, 0-3
		move: True if the player is moving, False if the player is placing a Wall, True/False
		start: If move is True, the initial player's cell coordinate.  Otherwise one of the
			end coordinate of the wall to be placed.
		end: If move is True, the cell coordinate the player moved to.  Otherwise the other
			end coordinate of the wall to be placed.
		"""
		
		self.playerId = playerId
		self.move = move
		self.start = start
		self.end = end

	def __str__(self):
		"""Return a string representation of this object"""
		
		result = "PlayerMove:\n"
		result += "\tplayerId: " + str(self.playerId)
		result += "\n\tmove: " + str(self.move)
		result += "\n\tstart: " + str(self.start)
		result += "\n\tend: " + str(self.end)

		return result
	
# CONSTANTS

# the square dimension of the board
BOARD_DIM = 9

# the total number of board cells
NUM_SQUARES = BOARD_DIM**2