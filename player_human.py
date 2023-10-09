from interface import *
from graph import *
import engine

"""
The player module is called by the engine to conduct game play.  You should
not modify the signatures for the init(), shortest_path(), move() 
and last_move() functions.  You are free to implement any other routines or modules.

Author: Sean Strout (sps@cs.rit.edu)
Author: Paul Solt (paul.solt@gmail.com)
"""

# public routines

def init(gameFile, playerId, numPlayers, playerHomes, wallsRemaining):
    """
    For all parts the engine calls this method so the player can initialize their data.
        gameFile - a string which is the file containing the initial board state.
        playerId - the numeric Id of the player (0-4).
        numPlayers - the number of players (2 or 4).
        playerHomes - a list of coordinates for each players starting cell (PO-P4).
        wallsRemaining - the number of walls remaining (same for all players at start).
    """
    
    # log any message string to standard output and the current log file
    engine.log_msg("player.init called for player " + str(playerId) + " File=" + gameFile +
                   ', playerId=' + str(playerId) + ', numPlayers=' + str(numPlayers) + ', playerHomes=' +
                   str(playerHomes) + ', wallsRemaining=' + str(wallsRemaining))
    
    # the human only needs to keep track of their playerId to play the game
    playerData = playerId

    return playerData

def shortest_path(playerData, start, finish):
    """Returns a list of coordinates representing the shortest path on the
    board between the start and finish coordinates.
        playerData - the player's data
        start - the start coordinate
        finish - the end coordinate
    """
    
    # the human doesn't implement this function
    return []

# private routines

def move(playerData):
    """
    For parts 2-4 the engine calls this method so the player can make a move.
    When it is the player's turn to move, the engine passes the player
    their player data.  The player makes their move and returns their data
    along with a PlayerMove object that contains information about this move.
        playerData - the player's data
    """
    
    engine.log_msg("player.move called for player " + str(playerData) + " with " + str(playerData))
    
    """
    Demonstration function using a human player to generate the next move.  After calling
    this routine you need to update your playerData to represent the new board state.
    Once you can play the game as a human with your board updating correctly, you should remove
    this call and write your own computer based move function.
    """
    playerMove = human_move(playerData)
    
    """Update your playerData here based on the selected playerMove"""
    
    return playerData, playerMove

def human_move(playerData):
    """
    Demonstration of a human making a move in the game.  It returns a PlayerMove object 
    with the move information.
            playerData - the player's data
    """
    
    # loop until an acceptable move has been entered
    while True:
        print "HUMAN player make your move...\n"
        
        # The human first specifies whether they are placing a wall or moving the player
        moveType = raw_input("Enter move type (M=MOVE, W=WALL): ")
        move = moveType == "M"
        
        start = eval(raw_input("Enter start coordinate (r,c): "))
        end = eval(raw_input("Enter end coordinate (r,c): "))
        
        accept = raw_input("Accept this move (y/n)? ")
        if accept == "y" or accept == "Y": break
    
    # construct the PlayerMove object and return it
    playerMove = PlayerMove(playerData, move, start, end)
    return playerMove

def last_move(playerData, playerMove):
    """For parts 3-4 the engine calls this method to notify the player of other player's
    moves.  The method is called with your player's data, as well as the valid move of
    the other player.  The updated player's data should be returned.
        playerData - this player's data
        playerMove - the move of another player in the game
    """
    
    # human doesn't care about doing anything with other player moves, he can figure
    # out what happened by just looking at the UI
    engine.log_msg("player.next_move called for player " + str(playerData) + " with " + str(playerMove))
    
    return playerData