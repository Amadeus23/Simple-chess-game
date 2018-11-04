#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 20:40:39 2018

@author: amadej
"""

#helper

'''
def initialPosition():
    
    [["rook_black", "knight_black", ....],
     ["pawn_black" | i <- 1 .. 8],
     [],
     []]
    
    '''

def initialPosition(i,j):
    pieceCode = "None"
    
    #Draw the black pieces
    if(i==0 and (j==0 or j==7)):
        pieceCode = "rook_black"
    
    if(i==0 and (j==1 or j==6)):
        pieceCode = "knight_black"
    
    if(i==0 and (j==2 or j==5)):
        pieceCode = "bishop_black"
    
    if(i==0 and j==3):
        pieceCode = "queen_black"
    
    if(i==0 and j==4):
        pieceCode = "king_black"
        
    if(i==1):
        pieceCode = "pawn_black"
        
    #Draw the white pieces
    if(i==7 and (j==0 or j==7)):
        pieceCode = "rook_white"
    
    if(i==7 and (j==1 or j==6)):
        pieceCode = "knight_white"
        
    if(i==7 and (j==2 or j==5)):
        pieceCode = "bishop_white"
        
    if(i==7 and j==3):
        pieceCode = "queen_white"
        
    if(i==7 and j==4):
        pieceCode = "king_white"
            
    if(i==6):
        pieceCode = "pawn_white"
    
    return pieceCode

def isInChessboard(position):
    if((position[0] < 8 and position[0] >= 0) and (position[1] < 8 and position[1] >= 0)):
        return True
    else:
        return False

def oppositeColor(col):
    if(col == "white"):
        return "black"
    elif(col == "black"):
        return "white"
    else:
        print("Invalid color")
        return "Invalid color"

def endWithKingString(col,stale):
    if(not stale):
        if(col == "white"):
            return "Checkmate! White won! Congratulations!"
        elif(col == "black"):
            return "Checkmate! Black won! Congratulations!"
        else:
            print("Invalid color")
            return "Invalid color"        
    else:
        return "Stalemate! Game ended in a draw."




    
    