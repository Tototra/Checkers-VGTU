# Checkers-VGTU
## What is your application ?
My application, is a game of checkers.

## How to run the program?
First download the Zip file.
Once the Zip file decompressed,
To run the program there are different possibilities.
+ First you can use your shell with the latest version of python installed.
  Make sure the library Tkinter is installed (use **pip install tk**)
  And then simply run the command **python3 project.py**
+ If you can't manage to run the program in the terminal (depending on the system running on your computer, it can sometimes not work.) Open your favourite IDE, and simply run the program.

## How to use the program ?
The progam I decided to implement, is a game of checkers:
Once you have launched it, you have multiple choices available.
You can :
+ Start a New Game
+ Load an Existing Game (if you want to test the loading functionality, you can take a look in the Project/Saved Games directory, there are examples of saved games.)

![Image Alt text](/images/begining.png "Optional title")    

Once you have chosen, either the New Game, or the Load Game, the rules of the game are exacly the same as a checkers game, you can just not kill multiple pawns at the same time. 
## Rules
### How to win
To Win there is only one possibility, the first one that was no Pawn left losses.
### Pawn movements 
+ A pawn can only move on the diagonal
<p align="center">
  <img src="/images/pawn_movement.png" alt="Image Alt text" title="Optional title" />
</p>

+ If thre is a enemy pawn on a touching diagonal square, and the the space behind this pawn in diagonal is free, you can jump over it, and this enemy pawn will disapear.
+ You can eat in every direction you want, it just has to be in diagonal.
+ Once any Pawn has reached the opposite side, it becomes a Queen

### Queens Movements
+ A Queen 
