#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 01:42:42 2018

@author: amadej
"""

#This will be the "model" which has the information of the state of the board

from helper import *
from pieces import *
from copy import *

def pieceGenerator(pieceCode,i,j):
    infoList = pieceCode.split("_")
    
    if (infoList[0] == "pawn"):
        return Pawn(i,j,infoList[1])
    if (infoList[0] == "knight"):
        return Knight(i,j,infoList[1])
    if (infoList[0] == "rook"):
        return Rook(i,j,infoList[1])
    if (infoList[0] == "bishop"):
        return Bishop(i,j,infoList[1])
    if (infoList[0] == "queen"):
        return Queen(i,j,infoList[1])
    if (infoList[0] == "king"):
        return King(i,j,infoList[1])
    
    return NonePiece(i,j,"None")




class Field():
    
    def __init__(self,i,j,piece):
        self.i = i
        self.j = j
        self.pieceCode = piece.getPieceCode()
        self.piece = piece
        
    def getPieceCode(self):
        return self.pieceCode
    
    def setPieceCode(self,newPieceCode):
        self.pieceCode = newPieceCode
    
    
class Chessboard():
    
    def __init__(self):
        my_board = []
        for i in range(8):
            my_row = []
            for j in range(8):
                pieceCode = initialPosition(i,j)
                piece = pieceGenerator(pieceCode,i,j)
                field = Field(i,j,piece)
                my_row.append(field)
            my_board.append(my_row)
            
        self.board = my_board
        self.highlighted_field = (8,8) #Doesn't exist
        self.white_checkboard = [[False for i in range(8)] for i in range(8)]
        self.black_checkboard = [[False for i in range(8)] for i in range(8)]
        self.previous_boards = [my_board]
        self.player_turn = "white"
        self.game_status = "Game in full progress."
    
    def updateGameStatus(self,color):
        #Informs the user about repetitions or end of game
        if(not self.anyMovesPossible(color)):
            if(self.kingInCheck(color)):
                self.game_status = endWithKingString(oppositeColor(color),False)
                return True
            else:
                self.game_status = endWithKingString(oppositeColor(color),True)
                return True
        
        if(self.repetitions()):
            self.game_status = "Three repeptitions reached! You may claim a draw now."
            return True
        
        if(self.drawByInsufficientMaterial()):
            self.game_status = "Draw by insufficient material!"
            return True
        
        if(self.drawByAgreement()):
            self.game_status = "Draw by agreement"
            return True
        
        return False
    
    def getPlayerTurn(self):
        return self.player_turn
        
    def setPlayerTurn(self,player):
        self.player_turn = player
        
        
    def hasPiece(self,i,j):
        if ((i in range(8)) and (j in range(8))):
            return self.board[i][j].piece.getPieceCode()
        else:
            print("Please select starting field, currently default",i,j)
        
    def movePiece(self,i1,j1,i2,j2,old_board,player_color):
        '''
        We create a new board and modify it according to the proposed move.
        Depending on if the move is valid we return the correct board.
        '''
        new_board = deepcopy(old_board)
        movedPiece = new_board[i1][j1].piece        
        
        
        """ 
        Checking if castling is even conceivable.
        """
        with_piece = "No piece yet"
        castle_fail = False
        castling_happening = False
        if(movedPiece.name == "king"):
            #check previous position i.e. if the king is even eligible to castle
            old_check_board = self.computeCheckBoard(new_board,player_color)
            if(movedPiece.movesMade == 0):
                if((j2-j1) == 2):
                    with_piece = new_board[i2][7].piece
                    castle_fail = not movedPiece.canCastle(new_board,old_check_board,with_piece)
                    castling_happening = True
                if((j2-j1) == -2):
                    with_piece = new_board[i2][0].piece
                    castle_fail = not movedPiece.canCastle(new_board,old_check_board,with_piece)
                    castling_happening = True
        
        none_piece = pieceGenerator("none",i1,j1)
        curr_field = Field(i1,j1,none_piece)
        movedPiece.move(i2,j2)
        
        """
        This part of code handles pawn transformations, only into queens for now.
        """
        infoList = movedPiece.pieceCode.split("_")
        if(infoList[0] == "pawn"):
            movedPiece.updatePreviousPosition(i1,j1)
            if (infoList[1] == "white" and i2 == 0):
                #transform white pawn
                newPiece = "queen"
                newPieceCode = newPiece + "_" + infoList[1]
                movedPiece = pieceGenerator(newPieceCode,i2,j2)
            if (infoList[1] == "black" and i2 == 7):
                #transform black pawn
                newPiece = "queen"
                newPieceCode = newPiece + "_" + infoList[1]
                movedPiece = pieceGenerator(newPieceCode,i2,j2)
            
        
        new_field = Field(i2,j2,movedPiece)
        
        new_board[i1][j1] = curr_field
        new_board[i2][j2] = new_field
        
        
        '''
        Handling the en passant rule for pawns.
        '''
        en_passant = False
        passant_fail = False
        pieceThere = old_board[i2][j2].piece.getPieceCode()
        if ((infoList[0] == "pawn") and (pieceThere=="None")):
            if(movedPiece.color == "white"):
                adjustment = 1
            elif(movedPiece.color == "black"):
                adjustment = -1
            #check if move diagonal
            if (j1 != j2):
                #check if move just happened
                if(isInChessboard((i2+adjustment,j2)) and len(chessboard.previous_boards) > 1):
                    pieceBefore = chessboard.previous_boards[-2][i2+adjustment][j2].piece.getPieceCode()
                    if(pieceBefore == "None"):
                        en_passant = True 
                        '''a diagonal move to empty space can only be en_passant, 
                        and the other pawn must've just have made that move'''
                    else:
                        """This move should not have been valid in the first place"""
                        passant_fail = True

        if (en_passant):
            new_none_piece = pieceGenerator("none",i2+adjustment,j2)
            new_noneField = Field(i2+adjustment,j2,new_none_piece)
            new_board[i2+adjustment][j2] = new_noneField
        
        #If castling is viable, perform the castling
        if(not castle_fail and castling_happening):
            #move rook too
            none_piece = pieceGenerator("none",with_piece.i,with_piece.j)
            none_field = Field(with_piece.i,with_piece.j,none_piece)
            
            average = int((j2+j1)/2)
            
            old_rook_coords = (with_piece.i,with_piece.j)
            with_piece.move(with_piece.i,average)
            
            new_rook_field = Field(with_piece.i,average,with_piece)
        
            new_board[old_rook_coords[0]][old_rook_coords[1]] = none_field
            new_board[with_piece.i][average] = new_rook_field
            
            
        if (self.boardValid(new_board,i1,j1,i2,j2,player_color,passant_fail,castle_fail)):
            return new_board
        else:
            return old_board
        
    def updateBoard(self,new_board,player_color):
        if(self.board != new_board):
            self.previous_boards.append(new_board)
            self.board = new_board
            self.setPlayerTurn(oppositeColor(player_color))          
        
        
    def boardValid(self,nominated_board,i1,j1,i2,j2,player_color,passant_fail,castle_fail):
        if (passant_fail or castle_fail):
            return False


        #checks if move compatible with basic move abilities of the piece
        old_board = self.previous_boards[-1]
        if (not ((i2,j2) in self.previous_boards[-1][i1][j1].piece.computeRange(old_board))):
            return False
        
        
        #check checks
        check_board = self.computeCheckBoard(nominated_board,player_color)
        (king_i,king_j) = self.findKing(nominated_board,player_color)
        if (check_board[king_i][king_j]):
            return False
        return True
    
    def findKing(self, board,player_color):
        for x in board:
            for y in x:
                infoList = y.piece.pieceCode.split("_")
                if (infoList[0] == "king" and infoList[1] == player_color):
                    return (y.i,y.j)
        #print("Help! There is no king!!!")
        
    def computeCheckBoard(self,board,player_color):
        #Computes another list of lists of booleans, that tell us which places are under attack
        checkboard = [[False for i in range(8)] for i in range(8)]
        for x in board:
            for y in x:
                if (not (y.piece.pieceCode == "None" or y.piece.color == player_color)):    
                    for z in y.piece.attackRange(board):
                        checkboard[z[0]][z[1]] = True
        return checkboard
    
    def kingInCheck(self,color):
        king_position = self.findKing(self.board,color)
        check_board = self.computeCheckBoard(self.board,color)
        return check_board[king_position[0]][king_position[1]]
        
    
    def pawnMoves(self,pawn,board):
        moves = []
        position = (pawn.i,pawn.j)
        for destination in pawn.pawnRange():
            new_board = self.movePiece(position[0],position[1],destination[0],destination[1],board,pawn.color)
            if(not self.boardsEqual(board,new_board)):
                moves.append(destination)
        return moves
    
    def pieceMoves(self,piece,board):
        moves = []
        position = (piece.i,piece.j)
        for destination in piece.computeRange(board):
            new_board = self.movePiece(position[0],position[1],destination[0],destination[1],board,piece.color)
            if(not self.boardsEqual(board,new_board)):
                moves.append(destination)
        return moves
    
    def kingSteps(self,board,color):
        steps = []
        king_position = self.findKing(board,color)
        king = board[king_position[0]][king_position[1]].piece
        for destination in king.attackRange(board):
            new_board = self.movePiece(king_position[0],king_position[1],destination[0],destination[1],board,color)
            if(not self.boardsEqual(board,new_board)):
                steps.append(destination)
        
        for destination in king.castleRange():
            new_board = self.movePiece(king_position[0],king_position[1],destination[0],destination[1],board,color)
            if(not self.boardsEqual(board,new_board)):
                steps.append(destination)
        
        return steps
    
    def boardsEqual(self,board1,board2):
        for i in range(8):
            for j in range(8):
                if(board1[i][j].piece.getPieceCode() != board2[i][j].piece.getPieceCode()):
                    return False
        return True
    
    def possibleMoves(self,i,j):
        """
        Returns the list of all the possible moves that are verified to be possible for that piece
        in the current state of the game. These will also be highlighted for the user to see.
        """
        piece = self.board[i][j].piece
        if(piece.pieceCode == "None"):
            return []
        
        if(piece.name == "pawn"):
            return self.pawnMoves(piece,self.board)
        elif(piece.name == "king"):
            return self.kingSteps(self.board,piece.color)
        else:
            return self.pieceMoves(piece,self.board)
        
    def allPossibleMoves(self,color):
        allMoves = []
        for i in range(8):
            for j in range(8):
                if (self.board[i][j].piece.color == color):
                    allMoves += self.possibleMoves(i,j)
        return allMoves
    
    def anyMovesPossible(self,color):
        return self.allPossibleMoves(color) != []
    
    def repetitions(self):
        repetitors = 0
        n_boards = len(self.previous_boards)
        if(n_boards>3):
            for i in range(n_boards-1):
                if(self.boardsEqual(self.previous_boards[-i-2],self.board)):
                    repetitors += 1
                    if(repetitors >= 2):
                        return True
        return False
                
    def drawByAgreement(self):
        return False
        
    def drawByInsufficientMaterial(self):
        pieces = []
        for i in range(8):
            for x in self.board[i]:
                if(x.piece.getPieceCode() != "None"):
                    pieces.append(x.piece)
                if(len(pieces) > 5):
                    return False
        
        for piece in pieces:
            if(piece.name == "queen" or piece.name == "rook" or piece.name == "pawn"):
                return False
        
        if(len(pieces)<=3):
            return True
        
        for piece in pieces:
            if(piece.name == "king"):
                pieces.remove(piece)
        
        blackPieces = []
        whitePieces = []
        for piece in pieces:
            if(piece.color == "black"):
                blackPieces.append(piece)
            elif(piece.color == "white"):
                whitePieces.append(piece)
        
        if(len(blackPieces) == 3 or len(whitePieces) == 3):
            return False
        
        #black player has 2 knights, the white one has no pieces
        if(whitePieces == []):
            for piece in blackPieces:
                if(piece.name != "knight"):
                    return False
            return True
        
        #white player has 2 knights, the black one has no pieces
        if(blackPieces == []):
            for piece in whitePieces:
                if(piece.name != "knight"):
                    return False
            return True
        
        return False
        
    def getHighlightedField(self):
        return self.highlighted_field
    
    def setHighlightedField(self,field):
        self.highlighted_field = field
chessboard = Chessboard()
        
        
        
        
        
        
        
        
        
        
        
        
