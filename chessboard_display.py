#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 15:04:34 2018

@author: amadej
"""

#2x2 chessboard



from tkinter import *
import board_model
from math import *
from helper import *



def pixelsToModel(x,y,margin=30):
    i = floor((y-margin)/90)
    j = floor((x-margin)/90)
    return (i,j)


def moveFirst(event,margin=30):
    # This function is bound to the left mouse click. It highlights the piece we want to move. 
    position = pixelsToModel(event.x,event.y,margin)
    if((position[0] < 8 and position[0] >= 0) and (position[1] < 8 and position[1] >= 0)):
        pieceColor = board_model.chessboard.board[position[0]][position[1]].piece.color
        turnColor = board_model.chessboard.getPlayerTurn()
        if (turnColor == pieceColor):  
            board_model.chessboard.setHighlightedField(position)
            game_status['text'] = "Game looking good."
            board_model.chessboard.game_status = "Game in full progress."
            
            drawChessboard(canvas,margin)
            highlight = canvas.create_rectangle(margin+90*position[1],margin+90*position[0],margin+90+90*position[1],margin+90+90*position[0],fill='green')
            for move in board_model.chessboard.possibleMoves(position[0],position[1]):
                canvas.create_rectangle(margin+90*move[1],margin+90*move[0],margin+90+90*move[1],margin+90+90*move[0],fill='light green')
            
            drawChessPieces(canvas,margin)
        else:
            #print("Piece of incorrect color selected for this turn!!!")
            game_turn['text'] = "Incorrect color!!!"
            game_status['text'] = "Please select correct color piece!"
def moveSecond(event,margin=30):
    # This function is bound to the right mouse click. It moves the piece to where we click on (if valid). 
    destination = pixelsToModel(event.x,event.y,margin)
    if((destination[0] < 8 and destination[0] >= 0) and (destination[1] < 8 and destination[1] >= 0)):
        start = board_model.chessboard.getHighlightedField()
        startPiece = board_model.chessboard.hasPiece(start[0],start[1])
        #If an actual piece was highlighted by moveFirst we attempt to move the piece
        if (start != (8,8) and startPiece != "None"): 
            i1 = start[0]
            j1 = start[1]
            i2 = destination[0]
            j2 = destination[1]
            current_board = board_model.chessboard.board
            player_color = startPiece.split("_")[1]
            new_board = board_model.chessboard.movePiece(i1,j1,i2,j2,current_board,player_color)
            board_model.chessboard.updateBoard(new_board,player_color)
            
            
            #The rest of this function handles the outputs in the interface
            
            king_checked = board_model.chessboard.kingInCheck(player_color)
            if (king_checked):
                game_status['text'] = "King in check!!!"

            turnColor = board_model.chessboard.getPlayerTurn()
            display_string = "It's "+ turnColor + " player's turn."
            game_turn['text'] = display_string
            
            drawChessboard(canvas,margin)
            drawChessPieces(canvas,margin)
            
            updated = board_model.chessboard.updateGameStatus(oppositeColor(player_color))
            
            no_repetitions = True
            if board_model.chessboard.game_status == "Three repeptitions reached! You may claim a draw now.":
                game_status['text'] = "Three repeptitions reached! You may claim a draw now."
                no_repetitions = False
                
            if(updated and no_repetitions):
                game_result['text'] = board_model.chessboard.game_status
                #print(player_color," won")
                #print(board_model.chessboard.game_status)
                game_turn['text'] = "No more turns."
                game_status['text'] = "Game over!"
            

    else:
        print("out of bounds")
    board_model.chessboard.setHighlightedField((8,8))
    
def hasHere(i,j):
    #gets the piece code (for example "knight_black") from a piece at position i,j in the board
    pieceCode = board_model.chessboard.hasPiece(i,j)
    return pieceCode


def pathFromCode(pieceCode):
    path = "chess_pieces/" + pieceCode + ".gif"
    return path


def drawChessPieces(canvas,margin):
    for i in range(0,8):
        for j in range(0,8):
            
            pieceCode = hasHere(i,j)
            if (pieceCode != "None"):
                #We inverted the natural Point coordinates to the Chessboard coordinates
                #Point aggrees with Cartesian setting, board with Matrix setting
                path = pathFromCode(pieceCode)
                img = PhotoImage(file=path)
                label = Label(image=img)
                label.image = img
                canvas.create_image(margin+45+90*j,margin+45+90*i, image=img)           

def drawChessboard(canvas,margin):
    for i in range(8):
        for j in range(8):
            colour = "brown"
            if ((i+j)%2 == 0):
                colour = "white"
            canvas.create_rectangle(margin+90*i,margin+90*j,margin+90+90*i,margin+90+90*j,fill=colour)



root = Tk()
root.configure(background = "light blue")
margin = 30
canvas = Canvas(root,width=780,height=780)
canvas.configure(background = "black")


drawChessboard(canvas,margin)
drawChessPieces(canvas,margin)


game_turn = Label(root,text="White's turn")
game_status = Label(root,text="Game looking good.")
game_result = Label(root,text="Game in full progress")

game_status.pack({'side':'right'})
game_turn.pack({'side':'right'})
game_result.pack({'side':'top'})


#Here we bind the clicks with the functions
canvas.bind("<Button-1>",moveFirst)
canvas.bind("<Button-2>",moveSecond) #BE CAREFUL ABOUT BUTTONS
canvas.pack()
    
root.mainloop()
    
