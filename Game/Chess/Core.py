from pyparsing import col
import Board
import Pieces


GameBoard = Board.Board()

def AddPiece(Piece):
    GameBoard.WhitePieces.append(Piece)
    GameBoard.AllPieces.append(Piece)


for i in range(0, 8):
    Pawn = Pieces.Pawn([i, 1], GameBoard, -1)
    AddPiece(Pawn)

    Pawn = Pieces.Pawn([i, 6], GameBoard, 1)
    AddPiece(Pawn)

KNIGHT_POSITIONS = [[1,0], [6,0], [1,7], [6,7]]
ROOK_POSITIONS = [[0, 0], [7, 0], [0, 7], [7, 7]]
BISHOP_POSITIONS = [[2,0], [5,0], [2,7], [5,7]]

for i in range(4):
    colourPiece = 1 if i == 2 or i == 3 else -1
    knight = Pieces.Knight(KNIGHT_POSITIONS[i], GameBoard,  colourPiece)
    rook = Pieces.Rook(ROOK_POSITIONS[i], GameBoard, colourPiece)
    bishop = Pieces.Bishop(BISHOP_POSITIONS[i], GameBoard, colourPiece)

    AddPiece(knight)
    AddPiece(rook)
    AddPiece(bishop)
 
KingBlack = Pieces.King([4, 0], GameBoard, -1)
GameBoard.BlackK = KingBlack

KingWhite = Pieces.King([3, 7], GameBoard, 1)
GameBoard.WhiteK = KingWhite
AddPiece(KingBlack)
AddPiece(KingWhite)


GameBoard.VisualiseBoard()
while True:
    command = input()
    if command == "stop":
        break
    else:
        From, To = command.split(";")
        From = list(map(int, From.split()))
        To = list(map(int, To.split()))
        GameBoard.Move(From, To)
        GameBoard.VisualiseBoard()

    