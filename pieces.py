#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 19:17:17 2018

@author: amadej
"""
from helper import *

class Piece():
    
    def __init__(self,i,j,color):
        self.pieceCode = "None"
        self.color = color
        self.i = i
        self.j = j
        self.movesMade = 0
    
    def getPieceCode(self):
        return self.pieceCode
    
    def setPieceCode(self,pieceCode):
        self.pieceCode = pieceCode
    
    def move(self,new_i,new_j):
        self.i = new_i
        self.j = new_j
        self.movesMade += 1
        
    def computeRange(self,chessboard):
        """
        The list of places the piece can move to according to its basic move abilities.
        """
        return []

    def checkMoves(self,range_list,a,b,distance,chessboard):
        for k in range (1,1+distance):
            
            if(isInChessboard((self.i+a*k,self.j+b*k))):
                pieceCode = chessboard[self.i+a*k][self.j+b*k].getPieceCode()
                if (pieceCode == "None"):
                    range_list.append((self.i+a*k,self.j+b*k))
                else:
                    infoList = pieceCode.split('_')
                    if(infoList[1]!=self.color):
                        range_list.append((self.i+a*k,self.j+b*k))
                        break
                    else:
                        break
        return range_list
    
    def checkAttacks(self,range_list,a,b,distance,chessboard):
        """
        CheckAttacks and other check functions here browse through the plausible moving directions until 
        the range of the piece is exhausted or an opponent's piece is in the way.
        """
        for k in range (1,1+distance):
            if(isInChessboard((self.i+a*k,self.j+b*k))):
                pieceCode = chessboard[self.i+a*k][self.j+b*k].getPieceCode()
                if (pieceCode == "None"):
                    range_list.append((self.i+a*k,self.j+b*k))
                else:
                    range_list.append((self.i+a*k,self.j+b*k))
                    break

        return range_list

class Knight(Piece):
    def __init__(self,i,j,color):
        super().__init__(i,j,color)
        self.name = "knight"
        self.pieceCode = self.name + "_" + self.color
    
    def computeRange(self,chessboard):
        """The list of places the piece can move to according to its basic move abilities."""
        attack_range = self.attackRange(chessboard)
        
        valid_range = []
        for x in attack_range:
            pieceCode = chessboard[x[0]][x[1]].piece.getPieceCode()
            if (pieceCode == "None"):
                valid_range.append(x)
            else:
                infoList = pieceCode.split('_')
                if(infoList[1]!=self.color):
                    valid_range.append(x)
                    
        return valid_range
    
    def attackRange(self,chessboard):
        """The list of places the piece can attack according to its basic move abilities."""
        rangeList = []
        rangeList.append((self.i+1,self.j+2))
        rangeList.append((self.i+1,self.j-2))
        rangeList.append((self.i-2,self.j-1))
        rangeList.append((self.i-2,self.j+1))
        rangeList.append((self.i+2,self.j+1))
        rangeList.append((self.i+2,self.j-1))
        rangeList.append((self.i-1,self.j-2))
        rangeList.append((self.i-1,self.j+2))
        
        range_in_board = list(filter(isInChessboard,rangeList))
        
        return range_in_board
    
class Bishop(Piece):
    def __init__(self,i,j,color):
        super().__init__(i,j,color)
        self.name = "bishop"
        self.pieceCode = self.name + "_" + self.color
        
    def computeRange(self,chessboard):
        """The list of places the piece can move to according to its basic move abilities."""
        valid_range = []
        
        valid_range = self.checkMoves(valid_range,1,1,7,chessboard)
        valid_range = self.checkMoves(valid_range,-1,1,7,chessboard)
        valid_range = self.checkMoves(valid_range,1,-1,7,chessboard)
        valid_range = self.checkMoves(valid_range,-1,-1,7,chessboard)
        
        range_in_board = list(filter(isInChessboard,valid_range))
                    
        return range_in_board
    
    def attackRange(self,chessboard):
        """The list of places the piece can attack according to its basic move abilities."""
        valid_range = []
        
        valid_range = self.checkAttacks(valid_range,1,1,7,chessboard)
        valid_range = self.checkAttacks(valid_range,-1,1,7,chessboard)
        valid_range = self.checkAttacks(valid_range,1,-1,7,chessboard)
        valid_range = self.checkAttacks(valid_range,-1,-1,7,chessboard)
        
        range_in_board = list(filter(isInChessboard,valid_range))
                    
        return range_in_board
    

class Rook(Piece):
    def __init__(self,i,j,color):
        super().__init__(i,j,color)
        self.name = "rook"
        self.pieceCode = self.name + "_" + self.color
        
    def computeRange(self,chessboard):
        """The list of places the piece can move to according to its basic move abilities."""
        valid_range = []
        
        valid_range = self.checkMoves(valid_range,0,1,7,chessboard)
        valid_range = self.checkMoves(valid_range,0,-1,7,chessboard)
        valid_range = self.checkMoves(valid_range,1,0,7,chessboard)
        valid_range = self.checkMoves(valid_range,-1,0,7,chessboard)
        
        range_in_board = list(filter(isInChessboard,valid_range))
                    
        return range_in_board
    
    def attackRange(self,chessboard):
        """The list of places the piece can attack according to its basic move abilities."""
        valid_range = []
        
        valid_range = self.checkAttacks(valid_range,0,1,7,chessboard)
        valid_range = self.checkAttacks(valid_range,0,-1,7,chessboard)
        valid_range = self.checkAttacks(valid_range,1,0,7,chessboard)
        valid_range = self.checkAttacks(valid_range,-1,0,7,chessboard)
        
        range_in_board = list(filter(isInChessboard,valid_range))
                    
        return range_in_board
    
        
class Queen(Piece):
    def __init__(self,i,j,color):
        super().__init__(i,j,color)
        self.name = "queen"
        self.pieceCode = self.name + "_" + self.color
        
    def computeRange(self,chessboard):
        """The list of places the piece can move to according to its basic move abilities."""
        valid_range = []
        
        valid_range = self.checkMoves(valid_range,1,1,7,chessboard)
        valid_range = self.checkMoves(valid_range,-1,1,7,chessboard)
        valid_range = self.checkMoves(valid_range,1,-1,7,chessboard)
        valid_range = self.checkMoves(valid_range,-1,-1,7,chessboard)
        
        valid_range = self.checkMoves(valid_range,0,1,7,chessboard)
        valid_range = self.checkMoves(valid_range,0,-1,7,chessboard)
        valid_range = self.checkMoves(valid_range,1,0,7,chessboard)
        valid_range = self.checkMoves(valid_range,-1,0,7,chessboard)
        
        range_in_board = list(filter(isInChessboard,valid_range))
                    
        return range_in_board
    
    def attackRange(self,chessboard):
        """The list of places the piece can attack according to its basic move abilities."""
        valid_range = []
        
        valid_range = self.checkAttacks(valid_range,1,1,7,chessboard)
        valid_range = self.checkAttacks(valid_range,-1,1,7,chessboard)
        valid_range = self.checkAttacks(valid_range,1,-1,7,chessboard)
        valid_range = self.checkAttacks(valid_range,-1,-1,7,chessboard)
        
        valid_range = self.checkAttacks(valid_range,0,1,7,chessboard)
        valid_range = self.checkAttacks(valid_range,0,-1,7,chessboard)
        valid_range = self.checkAttacks(valid_range,1,0,7,chessboard)
        valid_range = self.checkAttacks(valid_range,-1,0,7,chessboard)
        
        range_in_board = list(filter(isInChessboard,valid_range))
                    
        return range_in_board

class King(Piece):
    def __init__(self,i,j,color):
        super().__init__(i,j,color)
        self.name = "king"
        self.pieceCode = self.name + "_" + self.color
        
    def canCastle(self,chessboard,checkboard,with_piece):
        if(self.movesMade > 0 or with_piece.movesMade > 0):
            return False
        else:
            if(with_piece.getPieceCode().split("_")[0] == "rook"):
                if(with_piece.j == 0):
                    for x in range(3):
                        if(checkboard[self.i][self.j-x]):
                            return False
                    
                    #can I castle because no pieces in the way?
                    for x in range(3):
                        x+=1
                        if("None" != chessboard[self.i][self.j-x].piece.getPieceCode()):
                            return False
                elif(with_piece.j == 7):
                    for x in range(3):
                        if(checkboard[self.i][self.j+x]):
                            return False
                        
                    #can I castle because no pieces in the way?
                    for x in range(2):
                        x+=1
                        if("None" != chessboard[self.i][self.j+x].piece.getPieceCode()):
                            return False
                else:
                    print("Castling attempt invalid, rook not at correct place!")
                    return False
                return True
            return False

    def computeRange(self,chessboard):
        """The list of places the piece can move to according to its basic move abilities."""
        valid_range = []
        
        if(self.movesMade == 0):
            valid_range = self.checkMoves(valid_range,0,1,2,chessboard)
            valid_range = self.checkMoves(valid_range,0,-1,2,chessboard)
        
        valid_range = self.checkMoves(valid_range,1,1,1,chessboard)
        valid_range = self.checkMoves(valid_range,-1,1,1,chessboard)
        valid_range = self.checkMoves(valid_range,1,-1,1,chessboard)
        valid_range = self.checkMoves(valid_range,-1,-1,1,chessboard)
        
        valid_range = self.checkMoves(valid_range,0,1,1,chessboard)
        valid_range = self.checkMoves(valid_range,0,-1,1,chessboard)
        valid_range = self.checkMoves(valid_range,1,0,1,chessboard)
        valid_range = self.checkMoves(valid_range,-1,0,1,chessboard)
        
        range_in_board = list(filter(isInChessboard,valid_range))
        
        """ will do this in boardValid, so no need for checkboard anymore
        actual_range = []
        for field in range_in_board:
            if (checkboard[field[0]][field[1]] == False):
                actual_range.append(field)
        
        return actual_range
        """
        return range_in_board
    
    def attackRange(self,chessboard):
        """The list of places the piece can attack according to its basic move abilities."""
        valid_range = []
        
        valid_range = self.checkAttacks(valid_range,1,1,1,chessboard)
        valid_range = self.checkAttacks(valid_range,-1,1,1,chessboard)
        valid_range = self.checkAttacks(valid_range,1,-1,1,chessboard)
        valid_range = self.checkAttacks(valid_range,-1,-1,1,chessboard)
        
        valid_range = self.checkAttacks(valid_range,0,1,1,chessboard)
        valid_range = self.checkAttacks(valid_range,0,-1,1,chessboard)
        valid_range = self.checkAttacks(valid_range,1,0,1,chessboard)
        valid_range = self.checkAttacks(valid_range,-1,0,1,chessboard)
        
        range_in_board = list(filter(isInChessboard,valid_range))
        
        return range_in_board

    
    
    def checkCheck(checkboard,i,j):
        return checkboard[i][j]
    
    def castleRange(self):
        rangeList = []
        if (self.color == "white"):
            rangeList.append((7,2))
            rangeList.append((7,6))
        elif(self.color == "black"):            
            rangeList.append((0,2))
            rangeList.append((0,6))
        else:
            print("Pawn must be either black or white!!!")
        return rangeList
        

class Pawn(Piece):
    def __init__(self,i,j,color):
        super().__init__(i,j,color)
        self.name = "pawn"
        self.pieceCode = self.name + "_" + self.color
        self.previous_position = (i,j)
        self.justMoved = False
    

    def updatePreviousPosition(self,i,j):
        self.previous_position = (i,j)
    
    def justMoved():
        return self.justMoved
    def setJustMoved():
        self.justMoved = True
    
    def computeRange(self,chessboard):
        """The list of places the piece can move to according to its basic move abilities."""
        valid_range = []
        
        if (self.color == "white"):
            if(self.movesMade==0):
                valid_range = self.checkPawnMoves(valid_range,-1,0,2,chessboard)
            valid_range = self.checkPawnMoves(valid_range,-1,0,1,chessboard)
            
            valid_range = self.checkPawnMoves(valid_range,-1,1,1,chessboard)
            valid_range = self.checkPawnMoves(valid_range,-1,-1,1,chessboard)
        
        elif(self.color == "black"):
            if(self.movesMade==0):
                valid_range = self.checkPawnMoves(valid_range,1,0,2,chessboard)
            valid_range = self.checkPawnMoves(valid_range,1,0,1,chessboard)
            
            valid_range = self.checkPawnMoves(valid_range,1,-1,1,chessboard)
            valid_range = self.checkPawnMoves(valid_range,1,1,1,chessboard)

        else:
            print("Pawn must be either black or white!!!")
            
        range_in_board = list(filter(isInChessboard,valid_range))
        
        return range_in_board
    
    def attackRange(self,chessboard):
        """The list of places the piece can attack according to its basic move abilities."""
        rangeList = []
        
        if (self.color == "white"):
            rangeList.append((self.i-1,self.j-1))
            rangeList.append((self.i-1,self.j+1))
        
        elif(self.color == "black"):            
            rangeList.append((self.i+1,self.j-1))
            rangeList.append((self.i+1,self.j+1))

        else:
            print("Pawn must be either black or white!!!")
            
        range_in_board = list(filter(isInChessboard,rangeList))
        
        return range_in_board
    
    def pawnRange(self):
        """The list of places the pawn can move to according to its basic move abilities,
        but not taking into account the presence of lack of other pieces on relevant fields,
        or whether it can even do the move by 2 fields anymore."""
        i = self.i
        j = self.j
        if(self.color == "white"):
            adj = -1
        elif(self.color == "black"):
            adj = 1
        else:
            print("Very big issue with pawn color!")
        pawn_range = [(i+adj,j-1),(i+adj,j),(i+adj,j+1),(i+2*adj,j)]
        range_in_board = list(filter(isInChessboard,pawn_range))
        return range_in_board
        
    
    
    def checkPawnMoves(self,range_list,a,b,distance,chessboard):
        
        if (b == 0):
            #It's a straight move
            for k in range (1,1+distance):
                i_coord = self.i+a*k
                j_coord = self.j+b*k
                if(isInChessboard((i_coord,j_coord))):
                    pieceCode = chessboard[i_coord][j_coord].getPieceCode()
                    if (pieceCode == "None"):
                        range_list.append((i_coord,j_coord))
                    else:
                        break
            return range_list
        
        if (b != 0):
            #It's a diagonal move
            for k in range (1,1+distance):
                i_coord = self.i+a*k
                j_coord = self.j+b*k
                
                if(isInChessboard((i_coord,j_coord))):
                    pieceCode = chessboard[i_coord][j_coord].getPieceCode()
                    if (pieceCode == "None"):
                        if(self.color == "white"):
                            rank5 = 3
                            difference_needed = 2
                            adjustment = 1
                        elif(self.color == "black"):
                            rank5 = 4
                            difference_needed = -2
                            adjustment = -1
                        
                        has_rank5 = (self.i == rank5)
                        
                        neighbourPiece = chessboard[i_coord+adjustment][j_coord].piece
                        neighbourPieceCode = neighbourPiece.getPieceCode()
                        if (neighbourPieceCode.split("_")[0] == "pawn"):
                            previous = chessboard[i_coord+adjustment][j_coord].piece.previous_position
                            en_passant = (((i_coord+adjustment)-previous[0])==difference_needed)
                            
                            if (has_rank5 and en_passant):
                                #only if move just happened en passant can happen
                                range_list.append((i_coord,j_coord))

                            break
                        break
                    else:
                        infoList = pieceCode.split('_')
                        if(infoList[1]!=self.color):
                            range_list.append((i_coord,j_coord))
                            break
                        else:
                            break
            return range_list

class NonePiece(Piece):
    def __init__(self,i,j,color):
        super().__init__(i,j,color)
        self.name = "nonepiece"
        self.pieceCode = "None"
        self.i = i
        self.j = j
        self.color = color
