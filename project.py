import tkinter.filedialog
from tkinter import *
from math import ceil
from abc import abstractmethod


class Pawn:
    def __init__(self):
        self.list_of_pawn = []
        
    @abstractmethod
    def init_color(self):
        pass

    @abstractmethod
    def add_drag_and_drop(self):
        pass

    def drawpawn(self, posx, posy, color):
        """
        Create a pawn on the canvas.
        This method is used by initPawns().
        :param posx: the number of the case (0 -> 9) on the X axis
        :param posy: the number of the case (0 -> 9) on the Y axis
        :param color: the color of the pawn
        :return: the ID of the pawn
        """
        x = (posx * 50) + 5
        y = (posy * 50) + 5
        x1 = (x + 50) - 10
        y1 = (y + 50) - 10
        return game.can.create_oval(x, y, x1, y1, fill=color)

    def endturn(self):
        """
        End the turn of the current player.
        If a player has no more pawns, the other wins!
        :return: nothing
        """

        global currentPlayerColor
        # check if there is a winner
        if len(game.whitePawns.list_of_pawn) == 0:
            currentPlayerColor = None
            game.generalLabel["text"] = game.BLACK_VICTORY
        elif len(game.blackPawns.list_of_pawn) == 0:
            currentPlayerColor = None
            game.generalLabel["text"] = game.WHITE_VICTORY
        # change the player turn
        elif currentPlayerColor == game.WHITELIST:
            currentPlayerColor = game.BLACKLIST
            game.generalLabel["text"] = game.BLACK_TURN
        elif currentPlayerColor == game.BLACKLIST:
            currentPlayerColor = game.WHITELIST
            game.generalLabel["text"] = game.WHITE_TURN

    def onPawnStopMoving(self, event):
        """
        Callback executed when the mouse is released.
        Used to correctly place the pawn to the nearest case.
        Check if the case is valid (see the rules of the game).
        If not, replace the pawn to its original position.
        If we try to move an enemy pawn, the method returns and nothing happens.
        :param event: used to know the X and Y coordinates of the mouse
        :return: nothing
        """
        pawnId = event.widget.find_withtag('current')[0]
        originalColor = self.getColor(pawnId)
        if originalColor not in currentPlayerColor:
            return
        nearestX = ceil(event.x / 50) * 50
        nearestY = ceil(event.y / 50) * 50
        # destination coordinates
        x = nearestX - 45
        y = nearestY - 45
        x1 = nearestX - 5
        y1 = nearestY - 5
        if self.isValidMove(pawnId, x, y, x1, y1):
            game.can.coords(pawnId, x, y, x1, y1)
            if originalColor in game.WHITELIST and y1 == 45:
                original_coords = game.can.coords(pawnId)
                game.whitePawns.list_of_pawn.remove(pawnId)
                z = game.whitePawns.drawpawn(((original_coords[0] - 5) / 50), ((original_coords[1] - 5) / 50), "yellow")
                game.whitePawns.list_of_pawn.append(z)
                game.can.tag_bind(z, '<Button-1>', game.whitePawns.onPawnClick)
                game.can.tag_bind(z, '<B1-Motion>', game.whitePawns.onPawnMoving)
                game.can.tag_bind(z, '<ButtonRelease-1>', game.whitePawns.onPawnStopMoving)
                game.can.delete(pawnId)
            elif originalColor in game.BLACKLIST and y1 == 495:
                original_coords = game.can.coords(pawnId)
                game.blackPawns.list_of_pawn.remove(pawnId)
                z = game.blackPawns.drawpawn(((original_coords[0] - 5) / 50), ((original_coords[1] - 5) / 50),
                                             "red")
                game.blackPawns.list_of_pawn.append(z)
                game.can.tag_bind(z, '<Button-1>', game.blackPawns.onPawnClick)
                game.can.tag_bind(z, '<B1-Motion>', game.blackPawns.onPawnMoving)
                game.can.tag_bind(z, '<ButtonRelease-1>', game.blackPawns.onPawnStopMoving)
                game.can.delete(pawnId)
            # the player moved a pawn successfully, so his turn is finished
            self.endturn()
        else:
            game.can.coords(pawnId, movingPawnOriginalCoordinates)

    def onPawnClick(self, event):
        """
        Callback executed the first time the mouse interacts with a pawn.
        Used to store the original position of the pawn, so when the pawn is moved then released,
        if the position is invalid, we can move it back to its original position.
        We temporarily store the original position inside the movingPawnOriginalCoordinates variable,
        and its color in the movingPawnColor variable.
        :param event: used to retrieve the ID of the pawn we interact with
        :return: nothing
        """

        global movingPawnOriginalCoordinates, movingPawnColor
        pawnId = event.widget.find_withtag('current')[0]
        movingPawnOriginalCoordinates = game.can.coords(pawnId)
        movingPawnColor = self.getColor(pawnId)
        game.can.tag_raise(pawnId)

    def onPawnMoving(self, event):
        """
        Callback executed during the pawn movement.
        Used to recompute its position as the mouse is moving.
        If we try to move an enemy pawn, the method returns and nothing happens.
        :param event: used to know the X and Y coordinates of the mouse
        :return: nothing
        """
        pawnId = event.widget.find_withtag('current')[0]
        if self.getColor(pawnId) not in currentPlayerColor:
            return
        game.can.coords(pawnId, event.x - 20, event.y - 20, event.x + 20, event.y + 20)

    def isValidMove(self, movingPawnId, destX, destY, destX1, destY1):
        """
        Check if the pawn can be moved to the given coordinates.
        Rules:
        - the case cannot be occupied by another pawn;
        - the pawn can only move 1 case in diagonal, or 2 if he "jumps" above an enemy pawn;
        :return: True if the move is valid, False otherwise
        """
        sourceX = movingPawnOriginalCoordinates[0]
        sourceY = movingPawnOriginalCoordinates[1]
        sourceX1 = movingPawnOriginalCoordinates[2]
        sourceY1 = movingPawnOriginalCoordinates[3]

        global currentPlayerColor

        invalid = []
        for i in range(5,406,100):
            for j in range(5,406,100):
                invalid.append((j,i))
        for i in range(55,456,100):
            for j in range(55,456,100):
                invalid.append((j,i))
        calcx = abs(destX - sourceX)
        calcy = abs(destY - sourceY)
        if calcx != calcy :
            return False
        if (destX,destY) in invalid:
            return False
        # check if the destination case is outside the canvas
        if (destX < 0 or destX > 500) or (destY < 0 or destY > 500) or (destX1 < 0 or destX1 > 500) or (
                destY1 < 0 or destY1 > 500):
            return False

        # check if the move is not 1 case in diagonal
        if (self.getColor(movingPawnId) == "red" or self.getColor(movingPawnId) == "yellow"):
            if self.findPawnByCoordinates(destX, destY, destX1, destY1) != -1:
                return False
            if destX == sourceX:
                return  False
            if destY < sourceY:
                if destX < sourceX:
                    calcul = sourceY - destY
                    calcul = int(calcul)
                    present = False
                    jumpedIP  = -1
                    for i in range(50,calcul+50,50):
                        jumpedPawnId = self.findPawnByCoordinatesTwovalues(sourceX - i, sourceY - i)
                        if jumpedPawnId != -1:
                            if present==False:
                                present = True
                                jumpedIP = jumpedPawnId
                            else:
                                return False
                    if jumpedIP != -1:
                        if self.getColor(jumpedIP) not in currentPlayerColor:
                            self.killPawn(jumpedIP)
                    if self.getColor(jumpedIP) in currentPlayerColor:
                        return False
                    return True
                if destX > sourceX:
                    calcul = sourceY - destY
                    calcul = int(calcul)
                    present = False
                    jumpedIP = -1
                    for i in range(50, calcul + 50, 50):
                        jumpedPawnId = self.findPawnByCoordinatesTwovalues(sourceX + i, sourceY - i)
                        if jumpedPawnId != -1:
                            if present == False:
                                present = True
                                jumpedIP = jumpedPawnId
                            else:
                                return False
                    if jumpedIP != -1:
                        if self.getColor(jumpedIP) not in currentPlayerColor:
                            self.killPawn(jumpedIP)
                    if self.getColor(jumpedIP)  in currentPlayerColor:
                        return False
                    return True
            if destY > sourceY:
                if destX < sourceX:
                    calcul = destY - sourceY
                    calcul = int(calcul)
                    present = False
                    jumpedIP  = -1
                    for i in range(50,calcul+50,50):
                        jumpedPawnId = self.findPawnByCoordinatesTwovalues(sourceX - i, sourceY + i)
                        if jumpedPawnId != -1:
                            if present==False:
                                present = True
                                jumpedIP = jumpedPawnId
                            else:
                                return False
                    if jumpedIP != -1:
                        if self.getColor(jumpedIP) not in currentPlayerColor:
                            self.killPawn(jumpedIP)
                    if self.getColor(jumpedIP)  in currentPlayerColor:
                        return False
                    return True
                if destX > sourceX:
                    calcul = destY - sourceY
                    calcul = int(calcul)
                    present = False
                    jumpedIP = -1
                    for i in range(50, calcul + 50, 50):
                        jumpedPawnId = self.findPawnByCoordinatesTwovalues(sourceX + i, sourceY + i)
                        if jumpedPawnId != -1:
                            if present == False:
                                present = True
                                jumpedIP = jumpedPawnId
                            else:
                                return False
                    if jumpedIP != -1:
                        if self.getColor(jumpedIP) not in currentPlayerColor:
                            self.killPawn(jumpedIP)
                    if self.getColor(jumpedIP)  in currentPlayerColor:
                        return False
                    return True


        if self.findPawnByCoordinates(destX, destY, destX1, destY1) != -1:
            return False
        if (destX != sourceX + 50 and destX != sourceX - 50) or (destY != sourceY + 50 and destY != sourceY - 50) or (
                destX1 != sourceX1 + 50 and destX1 != sourceX1 - 50) or (
                destY1 != sourceY1 + 50 and destY1 != sourceY1 - 50):
            # if so, we also check if the move is 2 cases in diagonal
            # AND if there is an obstacle (enemy pawn) between the destination and the source

            if destX == sourceX - 100 and destY == sourceY - 100 and destX1 == sourceX1 - 100 and destY1 == sourceY1 - 100:
                # we moved 2 cases in the top-left
                jumpedPawnId = self.findPawnByCoordinates(sourceX - 50, sourceY - 50, sourceX1 - 50, sourceY1 - 50)
                if jumpedPawnId != -1 and self.getColor(jumpedPawnId) not in currentPlayerColor:

                    self.killPawn(jumpedPawnId)
                    return True
            elif destX == sourceX + 100 and destY == sourceY - 100 and destX1 == sourceX1 + 100 and destY1 == sourceY1 - 100:
                # we moved 2 cases in the top-right
                jumpedPawnId = self.findPawnByCoordinates(sourceX + 50, sourceY - 50, sourceX1 + 50, sourceY1 - 50)
                if jumpedPawnId != -1 and self.getColor(jumpedPawnId)  not in currentPlayerColor:
                    self.killPawn(jumpedPawnId)
                    return True
            elif destX == sourceX - 100 and destY == sourceY + 100 and destX1 == sourceX1 - 100 and destY1 == sourceY1 + 100:
                # we moved 2 cases in the bottom-left
                jumpedPawnId = self.findPawnByCoordinates(sourceX - 50, sourceY + 50, sourceX1 - 50, sourceY1 + 50)
                if jumpedPawnId != -1 and self.getColor(jumpedPawnId)  not in currentPlayerColor:
                    self.killPawn(jumpedPawnId)
                    return True
            elif destX == sourceX + 100 and destY == sourceY + 100 and destX1 == sourceX1 + 100 and destY1 == sourceY1 + 100:
                # we moved 2 cases in the bottom-right
                jumpedPawnId = self.findPawnByCoordinates(sourceX + 50, sourceY + 50, sourceX1 + 50, sourceY1 + 50)
                if jumpedPawnId != -1 and self.getColor(jumpedPawnId)  not in currentPlayerColor:
                    self.killPawn(jumpedPawnId)
                    return True
            return False
        # the move is valid
        if currentPlayerColor == game.WHITELIST and destY >= sourceY:
            return False
        if currentPlayerColor == game.BLACKLIST and destY <= sourceY:
            return False
        return True

    def killPawn(self, pawnId):
        """
        Kill a pawn, i.e., delete it from the canvas and from the list (whitePawns or blackPawns).
        Update the GUI counter labels.
        :return: nothing
        """
        if self.getColor(pawnId) in game.BLACKLIST:
            game.blackPawns.list_of_pawn.remove(pawnId)
            game.blackLeftCounterLabel["text"] = len(game.blackPawns.list_of_pawn)
        else:
            game.whitePawns.list_of_pawn.remove(pawnId)
            game.whiteLeftCounterLabel["text"] = len(game.whitePawns.list_of_pawn)
        game.can.delete(pawnId)

    def getColor(self, pawnId):
        """
        Return the color of a pawn by its ID on the canvas.
        :return: black of white
        """
        return game.can.itemcget(pawnId, "fill")

    def findPawnByCoordinates(self, x, y, x1, y1):
        """
        Check if there is a pawn on the canvas at the given coordinates.
        :return: the pawn ID, or -1 if no pawn was found
        """
        for pawnId in game.blackPawns.list_of_pawn + game.whitePawns.list_of_pawn:
            pawnCoords = game.can.coords(pawnId)
            if pawnCoords[0] == x and pawnCoords[1] == y and pawnCoords[2] == x1 and pawnCoords[3] == y1:
                return pawnId
        return -1

    def findPawnByCoordinatesTwovalues(self, x, y):
        """
        Check if there is a pawn on the canvas at the given coordinates.
        :return: the pawn ID, or -1 if no pawn was found
        """
        for pawnId in game.blackPawns.list_of_pawn + game.whitePawns.list_of_pawn:
            pawnCoords = game.can.coords(pawnId)
            if pawnCoords[0] == x and pawnCoords[1] == y:
                return pawnId
        return -1

class PawnFactory:
    @staticmethod
    def create_pawn(color):
        if color in game.BLACKLIST:
            return BlackPawn()
        elif color in game.WHITELIST:
            return WhitePawn()
        else:
            raise ValueError("Invalid color for pawn creation")

class BlackPawn(Pawn):
    def init_color(self):
        for i in range(1, 10, 2):
            self.list_of_pawn.append(self.drawpawn(i, 0, game.BLACKLIST[0]))
            self.list_of_pawn.append(self.drawpawn(i, 2, game.BLACKLIST[0]))
            self.list_of_pawn.append(self.drawpawn(i - 1, 1, game.BLACKLIST[0]))
            self.list_of_pawn.append(self.drawpawn(i - 1, 3, game.BLACKLIST[0]))
        self.add_drag_and_drop()

    def add_drag_and_drop(self):
        for pawnId in self.list_of_pawn:
            game.can.tag_bind(pawnId, '<Button-1>', self.onPawnClick)
            game.can.tag_bind(pawnId, '<B1-Motion>', self.onPawnMoving)
            game.can.tag_bind(pawnId, '<ButtonRelease-1>', self.onPawnStopMoving)

class WhitePawn(Pawn):
    def init_color(self):
        for i in range(1, 10, 2):
            game.whitePawns.list_of_pawn.append(self.drawpawn(i, 6, game.WHITELIST[0]))
            game.whitePawns.list_of_pawn.append(self.drawpawn(i, 8, game.WHITELIST[0]))
            game.whitePawns.list_of_pawn.append(self.drawpawn(i - 1, 7, game.WHITELIST[0]))
            game.whitePawns.list_of_pawn.append(self.drawpawn(i - 1, 9, game.WHITELIST[0]))
        self.add_drag_and_drop()
    def add_drag_and_drop(self):
        for pawnId in self.list_of_pawn:
            game.can.tag_bind(pawnId, '<Button-1>', self.onPawnClick)
            game.can.tag_bind(pawnId, '<B1-Motion>', self.onPawnMoving)
            game.can.tag_bind(pawnId, '<ButtonRelease-1>', self.onPawnStopMoving)

class RedPawn(Pawn):
    def add_drag_and_drop(self):
        for pawnId in self.list_of_pawn:
            game.can.tag_bind(pawnId, '<Button-1>', self.onPawnClick)
            game.can.tag_bind(pawnId, '<B1-Motion>', self.onPawnMoving)
            game.can.tag_bind(pawnId, '<ButtonRelease-1>', self.onPawnStopMoving)

def start():
    """
    Start the game.
    :return: nothing
    """
    global currentPlayerColor

    game.blackPawns = PawnFactory.create_pawn("black")
    game.whitePawns = PawnFactory.create_pawn("white")

    game.blackPawns.init_color()
    game.whitePawns.init_color()

    # GUI setup
    game.initPawnsButton["state"] = DISABLED
    game.loadPawnsButton["state"] = DISABLED
    game.savePawnsButton["state"] = NORMAL
    game.blackLeftCounterLabel["text"] = len(game.blackPawns.list_of_pawn)
    game.whiteLeftCounterLabel["text"] = len(game.whitePawns.list_of_pawn)

    # add a drag-n-drop detection for each pawn

    # GUI setup
    currentPlayerColor = game.WHITELIST
    game.generalLabel["text"] = game.WHITE_TURN



import datetime

def save_game_state():
    """
    Save the state of the game in a text file.
    """

    board_state = [['-' for _ in range(10)] for _ in range(10)]  # Initialize the board state with empty spaces

    # Mark the positions of black pawns and queens on the board
    for pawnId in game.blackPawns.list_of_pawn:
        x1, y1, _, _ = game.can.coords(pawnId)
        col = int((x1 - 5) // 50)
        row = int((y1 - 5) // 50)
        color = game.can.itemcget(pawnId, "fill")
        if color == "black":
            board_state[row][col] = 'B'  # 'B' represents a black pawn
        elif color == "red":
            board_state[row][col] = 'R'  # 'R' represents a black queen

    # Mark the positions of white pawns and queens on the board
    for pawnId in game.whitePawns.list_of_pawn:
        x1, y1, _, _ = game.can.coords(pawnId)
        col = int((x1 - 5) // 50)
        row = int((y1 - 5) // 50)
        color = game.can.itemcget(pawnId, "fill")
        if color == "white":
            board_state[row][col] = 'W'  # 'W' represents a white pawn
        elif color == "yellow":
            board_state[row][col] = 'Y'  # 'Y' represents a white queen

    # Generate a unique filename based on current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    filename = f"Saved Games/game_state_{timestamp}.txt"

    # Write the board state to the text file
    with open(filename, "w") as file:
        if currentPlayerColor is not None:
            file.write(f"Current Player: {currentPlayerColor[0]}\n")
        else:
            file.write(f"Current Player: None\n")
        for row in board_state:
            file.write(' '.join(row) + '\n')

def load_game_state():
    """
    Load the state of the game from a text file.
    """
    filename = tkinter.filedialog.askopenfilename()
    if filename:
        with open(filename, "r") as file:
            content = file.readlines()

            # Remove whitespace characters like `\n` at the end of each line
            content = [line.strip() for line in content]
            if len(content) != 0:
                # Retrieve the current player color
                current_player_line = content[0]
                current_player_color = current_player_line.split(": ")[1]

                # Retrieve the board state
                board_state = [line.split() for line in content[1:]]

                # Clear the current board
                game.can.delete("all")

                # Initialize a new board
                game.initBoard()

                # Process board state
                for row_index, row in enumerate(board_state):
                    for col_index, cell in enumerate(row):
                        if cell == 'B' :
                            x1, y1, x2, y2 = col_index * 50 + 5, row_index * 50 + 5, col_index * 50 + 45, row_index * 50 + 45
                            game.blackPawns.list_of_pawn.append(game.blackPawns.drawpawn(col_index, row_index, "black"))
                        elif cell == 'R':
                            x1, y1, x2, y2 = col_index * 50 + 5, row_index * 50 + 5, col_index * 50 + 45, row_index * 50 + 45
                            game.blackPawns.list_of_pawn.append(game.blackPawns.drawpawn(col_index, row_index, "red"))
                        elif cell == 'W':
                            x1, y1, x2, y2 = col_index * 50 + 5, row_index * 50 + 5, col_index * 50 + 45, row_index * 50 + 45
                            game.whitePawns.list_of_pawn.append(game.whitePawns.drawpawn(col_index, row_index, "white"))
                        elif cell == 'Y':
                            x1, y1, x2, y2 = col_index * 50 + 5, row_index * 50 + 5, col_index * 50 + 45, row_index * 50 + 45
                            game.whitePawns.list_of_pawn.append(game.whitePawns.drawpawn(col_index, row_index, "yellow"))

                global currentPlayerColor
                # Set the current player color
                if current_player_color in game.WHITELIST:
                    currentPlayerColor = game.WHITELIST
                    game.generalLabel["text"] = game.WHITE_TURN
                else:
                    currentPlayerColor = game.BLACKLIST
                    game.generalLabel["text"] = game.BLACK_TURN

                # Re-bind the event handlers for pawn movement
                game.blackPawns.add_drag_and_drop()
                game.whitePawns.add_drag_and_drop()

                game.initPawnsButton["state"] = DISABLED
                game.loadPawnsButton["state"] = DISABLED
                game.savePawnsButton["state"] = NORMAL
                game.blackLeftCounterLabel["text"] = len(game.blackPawns.list_of_pawn)
                game.whiteLeftCounterLabel["text"] = len(game.whitePawns.list_of_pawn)



class Game:
    # Singleton instance
    _instance = None

    @staticmethod
    def get_instance():
        """Static method to get the singleton instance of Game."""
        if Game._instance is None:
            Game._instance = Game()
        return Game._instance
    # constants
    BLACKLIST = ["black","red"]
    WHITELIST = ["white","yellow"]
    BLACK_TURN = "BLACK TURN"
    WHITE_TURN = "WHITE TURN"
    BLACK_VICTORY = "BLACK WINS!"
    WHITE_VICTORY = "WHITE WINS!"

    # variables
    blackPawns = BlackPawn()

    whitePawns = WhitePawn()
    movingPawnOriginalCoordinates = None
    movingPawnColor = None
    currentPlayerColor = None

    # GUI
    fen = Tk()
    fen.title("Checkers")
    fen.resizable(False, False)
    can = Canvas(fen, width=500, height=500, bg="#DCCACA")

    initPawnsButton = Button(fen, text="New Game", command=start)
    loadPawnsButton = Button(fen, text="Load Game", command=load_game_state)
    savePawnsButton = Button(fen, text="Save Game", command=save_game_state)
    savePawnsButton["state"] = DISABLED
    blackLeftLabel = Label(fen, text="Black Alive:")
    blackLeftCounterLabel = Label(fen, text=0, font="Helvetica 16 bold")
    whiteLeftLabel = Label(fen, text="White Alive:")
    whiteLeftCounterLabel = Label(fen, text=0, font="Helvetica 16 bold")
    generalLabel = Label(fen, font="Helvetica 16 bold")

    can.pack()
    initPawnsButton.pack(side="bottom", padx=3, pady=3)
    loadPawnsButton.pack(side="top", padx=3, pady=3)
    savePawnsButton.pack(side="top", padx=3, pady=3)
    blackLeftLabel.pack(side="left")
    blackLeftCounterLabel.pack(side="left")
    whiteLeftCounterLabel.pack(side="right")
    whiteLeftLabel.pack(side="right")
    generalLabel.pack()

    def __init__(self):
        self.initBoard()
        if Game._instance is not None:
            raise Exception("Only one instance of Game is allowed.")
        else:
            Game._instance = self

    def initBoard(self):
        """
        Create the board on the canvas.
        :return: nothing
        """
        for lineNumber in range(0, 10):
            offset = 0 if lineNumber % 2 == 1 else 50
            for squareNumber in range(0, 5):
                x = (100 * squareNumber) + offset
                y = 50 * lineNumber
                x1 = x + 50
                y1 = y + 50
                self.can.create_rectangle(x, y, x1, y1, fill="#875921")


if __name__ == "__main__":
    game = Game()
    game.fen.mainloop()





