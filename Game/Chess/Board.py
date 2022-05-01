from .Pieces import Piece, ValidMove, King
from colorama import init
from termcolor import colored
init()

COUNT_CELLS = 8

class Board():
    def __init__(self):
        self.BlackPieces = []
        self.WhitePieces = []
        self.AllPieces = []
        
        self.WhiteK = None
        self.BlackK = None
        
    def VisualiseBoard(self):
        for i in range(COUNT_CELLS):
            for j in range(COUNT_CELLS):
                figure = self.GetPiece([j, i])
                if figure:
                    color = "white" if figure.colour == 1 else "cyan"
                    print(colored(figure.symbol, color) + " ", end="")
                else:
                    print("☐ ", end="")
            print()
    
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
            else:
                print("Uncorect move")
        else:
            print("None Figure")

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


                 