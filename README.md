# Checkers-VGTU
## What is your application ?
My application, is a game of checkers.

## How to run the program?
First download the Zip file.
Once the Zip file decompressed,
To run the program there are different possibilities.
+ First, you can use your shell with the latest version of python installed.
  Make sure the library Tkinter is installed (use **pip install tk**)
  And then simply run the command **python3 project.py**
+ If you can't manage to run the program in the terminal (depending on the system running on your computer, it can sometimes not work.) Open your favorite IDE, and simply run the program.

## How to use the program ?
The program, I decided to implement, is a game of checkers:
Once you have launched it, you have multiple choices available.
You can :
+ Start a New Game
+ Load an Existing Game (if you want to test the loading functionality, you can take a look in the Project/Saved Games directory, there are examples of saved games.)

![Image Alt text](/images/begining.png "Optional title")    

Once you have chosen, either the New Game, or the Load Game, the rules of the game are exactly the same as a checkers game, you can just not kill multiple pawns at the same time. 
## Rules
### How to win
To Win there is only one possibility, the first one that was no Pawn left losses.
### Pawn movements 
+ A pawn can only move on the diagonal
<p align="center">
  <img src="/images/pawn_movement.png" alt="Image Alt text" title="Optional title" />
</p>

+ If there is an enemy pawn on a touching diagonal square, and the space behind this pawn in diagonal is free, you can jump over it, and this enemy pawn will disappear.
  <p align="center">
  <img src="/images/kill.png" alt="Image Alt text" title="Optional title" />
</p>

+ You can eat in every direction you want, it just has to be in diagonal.
+ Once any Pawn has reached the opposite side, it becomes a Queen

### Queens Movements
+ A Queen still only move in diagonal, but she can move multiple squares.
+ If an enemy Pawn is on the same diagonal as here, she can jump over it, add finish her movement where she wants on the same diagonal, and the enemy will despair.
    <p align="center">
  <img src="/images/queen.png" alt="Image Alt text" title="Optional title" />
</p>

## Body/Analysis
### Polymorphism
If you look at the code, there is a principal class which is class **Pawn**. This class has all the methods of the black and white pawns. 
That means, that in each class, Blackpawn and Whitepawn, we can access the same method, without copying them twice.

### Abstraction
In the class Pawn I have implemented the two abstract methods that will be used in the BlacPawn and the WhitePawn class.
    <p align="center">
  <img src="/images/Abstraction.png" alt="Image Alt text" title="Optional title" />
</p>

### Inheritance
Both BlackPawn and WhitePawn inherit from the Pawn class. 
They are defined like: **BlackPawn(Pawn)**, **WhitePawn(Pawn)**, this is really useful, when we want to use a method that does the same thing for different objects.

### Encapsulation
Encapsulation is the fundamental implementation in POO, so all the code has encapsulation.

## 2 design patterns
### Singleton
I used Singleton in the Game Class, to be sure that we could only create one instance at a time. This means that whenever an object of the class is instantiated, the same instance is returned every time, rather than creating a new instance.
    <p align="center">
  <img src="/images/singleton1.png" alt="Image Alt text" title="Optional title" />
</p>

  <p align="center">
  <img src="/images/singleton2.png" alt="Image Alt text" title="Optional title" />
</p>

### Factory Methods
Factory methods are used for creating objects without specifying the exact class of object that will be created. In this code, the PawnFactory class has a **create_pawn** static method that takes a color as input and returns an instance of a Pawn subclass based on that color.
<p align="center">
  <img src="/images/factory.png" alt="Image Alt text" title="Optional title" />
</p>

### Overall code explanation

1. **Entry Point**: When you launch the app, the first thing python will run is `if __name__ == "__main__":`.

2. **Game Initialization**: Inside the `main` function, create an instance of the `Game` class using the line `game = Game()`. This initializes the game environment, including the game board and the graphical user interface.

3. **Game Board Setup**: The `Game` class's `initBoard` method sets up the game board on the canvas. This method creates a checkered pattern using rectangles on the Tkinter canvas.

4. **Game Start**: Call the `start` function to begin the game. This function initializes the game state, including creating pawn objects for both black and white players and setting up the initial positions of the pawns on the board.

5. **Player Interaction**: Interact with the game by clicking and dragging the pawns on the board. Event handlers defined in the `Pawn` class, such as `onPawnClick`, `onPawnMoving`, and `onPawnStopMoving`, facilitate this interaction.

6. **Game Logic**: The game logic handles pawn movement, turn switching, and win conditions. For example, the `isValidMove` method in the `Pawn` class determines whether a move is valid according to the rules of checkers.

7. **Save and Load Game State**: Players can save the current game state or load a previously saved state using the `save_game_state` and `load_game_state` functions, respectively. These functions serialize the game state to a text file and deserialize it back into the game environment.

8. **GUI Controls**: The graphical user interface includes buttons for starting a new game, loading a saved game, and saving the current game state. These buttons are created and configured in the `Game` class.

## Results and Summary
### Results
1. **Successful Game Implementation:** The implementation of the checkers game provides a functional environment where players can interact with the graphical interface to play the game according to the rules.
2. **Challenges with Pawn Movement Logic:** One challenge encountered was implementing the logic for pawn movement, especially considering the rules of checkers, such as diagonal movement and capturing opponent pawns.
3. **GUI Integration and Event Handling:** Integrating the graphical user interface (GUI) with the game logic posed some challenges, particularly in managing event handling for pawn movement and ensuring smooth interaction between the player's actions and the game state.


### Conclusions
**Key Findings and Outcomes:** This coursework has successfully implemented a checkers game using Python and Tkinter. The program demonstrates the integration of game logic with a graphical user interface, allowing for intuitive gameplay.\
**Achievements:** The result of this work is a functional checkers game with features such as pawn movement, turn-based gameplay, and save/load functionality. The program fulfills every functional requirements. \
**Future Prospects:** Moving forward, there are several avenues for enhancing the program, including improving the user interface design, implementing additional game features such as multiplayer support, and optimizing the code for better performance. 

### Extension of the Application
1. **Multiplayer Support:** Implement online multiplayer functionality to allow players to compete against each other over the internet. This would involve integrating networking capabilities to facilitate communication between players' devices.
2. **AI Opponent:** Develop an artificial intelligence (AI) opponent to enable single-player mode. The AI would provide challenging gameplay by making strategic moves based on game rules and board evaluation algorithms.
3. **Enhanced User Interface:** Improve the user interface with more intuitive controls, interactive animations, and visually appealing graphics. Customizable themes and sound effects can also enhance the overall gaming experience.
4. **Additional Game Modes:** Introduce new game modes such as timed matches, tournament modes, or custom rule sets. This allows players to explore different challenges and gameplay variations.
5. **Statistics and Leaderboards:** Implement features to track players' game statistics, including win-loss records, average game duration, and highest score. Leaderboards can be added to showcase top-performing players.
