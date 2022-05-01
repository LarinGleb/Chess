def ValidMove(Move):
    if Move[0] >= 0 and Move[0] <= 7:
        if Move[1] >= 0 and Move[1] <=7:
            return True
        return False
    return False

def Difference(MoveCell, positionSelf):
    deltaX = 1 if MoveCell[0] > positionSelf[0] else -1
    deltaY = 1 if MoveCell[1] > positionSelf[1] else -1
    return [deltaX, deltaY]

class Piece():
    def __init__(self, position, symbol, board, colour, EatFunc, MoveFunc):
        self.board = board
        self.colour = colour
        self.eatFunction = EatFunc
        self.moveFunction = MoveFunc
        self.symbol = symbol
        self.Position = position


    def CanMove(self, MoveToCell):
        if MoveToCell == self.Position:
            return False
        return self.moveFunction(MoveToCell) or self.CanEat(MoveToCell)


    def CanEat(self, EatCell):
        figureToEat = self.board.GetPiece(EatCell)
        if figureToEat == None:
            return False

        if figureToEat.colour == self.colour:
            return False
        if self.Position == EatCell:
            return False

        return self.eatFunction(EatCell)


class Pawn(Piece):
    def __init__(self, position, board, colour):
        super().__init__(position, "P", board, colour, self.EatPawn, self.MovePawn)
        self.FirstMove = True


    def EatPawn(self, EatTo):
        if self.Position[0] - self.colour == EatTo[0] and self.Position[1] - self.colour == EatTo[1]:
            return True
        return False


    def MovePawn(self, MoveTo):
        if MoveTo[0] != self.Position[0]:
            return False
        
        if self.Position[1] - self.colour == MoveTo[1]:
            return True

        elif self.Position[1] - 2 * self.colour == MoveTo[1] and self.FirstMove:
            if self.board.GetPiece([self.Position[0], self.Position[1] - self.colour]) == None:
                self.FirstMove = False
                return True

        return False


POSSIBLE_KING_MOVES = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]


class King(Piece):
    def __init__(self, position, board, colour):
        super().__init__(position, "K", board, colour, self.EatKing, self.MoveKing)

    def EatKing(self, EatCell):
        return self.MoveKing(EatCell)
    
    def GetValidsMoveKing(self):
        validsMoveKing = []
        for kingMove in POSSIBLE_KING_MOVES:
            if ValidMove([self.Position[0] + kingMove[0], self.Position[1] + kingMove[1]]):
                validsMoveKing.append(kingMove)
        return validsMoveKing
    
    def MoveKing(self, MoveCell):
        for move in self.GetValidsMoveKing():
            if MoveCell[0] == self.Position[0] + move[0]:
                if MoveCell[1] == self.Position[1] + move[1]:
                    return True
        
        return False
            

KNIGHT_POSSIBLE_MOVES = [[1, 2], [2, 1], [-1, 2], [2, -1], [-1, -2], [-2, -1], [-2, 1], [1, -2]]
class Knight(Piece):
    def __init__(self, position, board, colour):
        super().__init__(position, "k", board, colour, self.MoveKnight, self.EatKnight)

    def EatKnight(self, EatCell):
        return self.MoveKnight(EatCell)

    def MoveKnight(self, MoveCell):
        for move in KNIGHT_POSSIBLE_MOVES:
            if move[0] + self.Position[0] == MoveCell[0]:
                if move[1] + self.Position[1] == MoveCell[1]:
                    return True

        return False

def GetDeltaXandY(position, MoveCell):
    deltaX = -1 if MoveCell[0] < position[0] else 1
    deltaY = -1 if MoveCell[1] > position[1] else 1
    return deltaX, deltaY

class Bishop(Piece):
    def __init__(self, position, board, colour):
        super().__init__(position, "B", board, colour, self.EatBishop, self.MoveBishop)

    def MoveBishop(self, MoveCell):
        distanceX = abs(MoveCell[0] - self.Position[0])
        distanceY = abs(MoveCell[1] - self.Position[1])

        if distanceX != distanceY:
            return False
        
        deltaX, deltaY = GetDeltaXandY(self.Position, MoveCell)
        
        
        for i in range(1, distanceX):
            for j in range(1, distanceY):
                piece = self.board.GetPiece([self.Position[0] + i * deltaX, self.Position[1] + j * deltaY])
                if piece.colour == self.colour:
                    return False

        return True
    
    def EatBishop(self, EatCell):
        return self.MoveBishop(EatCell)


class Rook(Piece):
    def __init__(self, position, board, colour):
        super().__init__(position, "R", board, colour, self.EatRook, self.MoveRook)

    
    def MoveRook(self, MoveCell):
        distanceX = abs(MoveCell[0] - self.Position[0])
        distanceY = abs(MoveCell[1] - self.Position[1])
        
        if distanceX != 0 or distanceY != 0:
            return False
    
        deltaX, deltaY = GetDeltaXandY(self.Position, MoveCell)

        for i in range(1, distanceX):
            for j in range(1, distanceY):
                piece = self.board.GetPiece([self.Position[0] + i * deltaX, self.Position[1] + j * deltaY])
                if piece.colour == self.colour:
                    return False
        return True

    def EatRook(self, EatCell):
        return self.MoveRook(EatCell)

class Queen(Piece):
    def __init__(self, position, board, colour):
        super().__init__(position, "Q", board, colour, self.EatQueen, self.MoveQueen)

    def MoveQueen(self, MoveCell):
        distanceX = abs(MoveCell[0] - self.Position[0])
        distanceY = abs(MoveCell[1] - self.Position[1])

        if (distanceX != distanceY) or (distanceX != 0 or distanceY != 0):
            return False
        
        deltaX, deltaY = GetDeltaXandY(self.Position, MoveCell)
        
        
        for i in range(1, distanceX):
            for j in range(1, distanceY):
                piece = self.board.GetPiece([self.Position[0] + i * deltaX, self.Position[1] + j * deltaY])
                if piece.colour == self.colour:
                    return False

        return True

    
    def EatQueen(self, EatCell):
        return self.MoveQueen(EatCell)

    