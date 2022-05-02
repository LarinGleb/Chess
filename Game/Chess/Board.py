from dataclasses import replace
from .Pieces import Bishop, Knight, Pawn, Piece, Queen, Rook, ValidMove, King
from colorama import init
from termcolor import colored
init()

COUNT_CELLS = 8

figures = {'k': Knight,
           'K': King,
           'Q': Queen,
           'P': Pawn,
           'B':Bishop,
           'R': Rook}

STANDART_DESK = "RkBQKBkR/PPPPPPPP/......../......../......../......../PPPPPPPP/RkBKQBkR"

class Board():
    def __init__(self, game = STANDART_DESK):
        self.BlackPieces = []
        self.WhitePieces = []
        self.AllPieces = []
        currentRow = 0
        currentColumn = 0
        self.desk = game.split("/")
        for row in self.desk:
            
            for figure in row:
                if figure != ".": 
                    color = 1 if "w" in figure else -1 
                    symbol = figure.replace('b', '').replace('w', '')
                    figure = figures[symbol]([currentColumn, currentRow], self, color)
                    if color == 1:
                        self.WhitePieces.append(figure)
                    else:
                        self.BlackPieces.append(figure)
                    self.AllPieces.append(figure)

                    if symbol == 'K':
                        if color == -1:
                            self.BlackK = figure
                        else:
                            self.WhiteK = figure

                currentColumn += 1

            currentRow  += 1
        
    def GetBoardString(self):
        boardString = ""
        for i in range(COUNT_CELLS):
            for j in range(COUNT_CELLS):
                figure = self.GetPiece([j, i])
                if figure:
                    color = "w" if figure.colour == 1 else "n"
                    boardString += (figure.symbol + color)
                else:
                    boardString += "☐ "
            boardString += "\n"
        
        return boardString
    
    def GetPiece(self, Coords):
        for piece in self.AllPieces:
            if piece.Position == Coords:
                return piece
        return None

    def Move(self, From, To):
        figureMove = self.GetPiece(From)
        if figureMove != None:
            colourMove = figureMove.colour
            figureEat = self.GetPiece(To)
            enemyPieces = self.WhitePieces if colourMove == -1 else self.BlackPieces
            if figureMove.CanMove(To):
                figureMove.Position = To
                if figureEat != None:
                    enemyPieces.remove(figureEat)

                if self.CheckShah(colourMove):
                    figureMove.Position = From
                    if figureEat != None:
                        enemyPieces.append(figureEat)
                        return False

                if self.CheckMate(-1 if colourMove == 1 else 1):
                    return "Мат!"

                self.desk[figureMove.Position[1]][figureMove.Position[0]] = "☐ "
                color = "w" if figureMove.colour == 1 else "n"
                self.desk[To[1]][To[0]] = color + figureMove.symbol
                return True
            else:
                return False
        else:
            return False
        

    def CheckShah(self, colour, moveKing = [0, 0]):
        king = self.WhiteK if colour == 1 else self.BlackK
        pieces = self.BlackPieces if colour == 1 else self.WhitePieces

        for piece in pieces:
            if piece.CanEat([king.Position[0] + moveKing[0], king.Position[1] + moveKing[1]]):
                return True
        return False

    def ValidMove(self, Move):
        if Move[0] >= 0 and Move[0] <= 7:
            if Move[1] >= 0 and Move[1] <=7:
                return True
            return False
        return False

    def CheckMate(self, colour):
        king = self.WhiteK if colour == 1 else self.BlackK
        validsMoveKing = [[0, 0]]
        validsMoveKing.extend(king.GetValidsMoveKing())
        
        for validMove in validsMoveKing:
            if not self.CheckShah(self, colour, validMove):
                return False
            
        colourPieces = self.WhitePieces if colour == 1 else self.BlackPieces
        enemyPieces = self.WhitePieces if colour == -1 else self.BlackPieces

        for piece in colourPieces:
            moves = piece.GetPossibleMoves()
            
            for move in moves:
                oldPosition = piece.Position
                pieceOnMove = self.GetPiece(move)
                piece.MoveTo(move)
                if not self.CheckShah(self, colour):
                    piece.MoveTo(oldPosition)
                    if pieceOnMove not in enemyPieces and pieceOnMove != None:
                        enemyPieces.append(pieceOnMove)
                    return False
       
        return True


                 