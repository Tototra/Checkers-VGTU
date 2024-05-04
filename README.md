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

+ If thre is a enemy pawn on a touching diagonal square, and the the space behind this pawn in diagonal is free, you can jump over it, and this ennemy pawn will disapear.
  <p align="center">
  <img src="/images/kill.png" alt="Image Alt text" title="Optional title" />
</p>

+ You can eat in every direction you want, it just has to be in diagonal.
+ Once any Pawn has reached the opposite side, it becomes a Queen

### Queens Movements
+ A Queen still only move in diagonal, but she can move multiple squares.
+ If an ennemy Pawn is on the same diagonal as here, she can jump over it, add finish her movement where she wants on the same diagonal, and the ennemy will desapear.
    <p align="center">
  <img src="/images/queen.png" alt="Image Alt text" title="Optional title" />
</p>

## Body/Analysis
### Polymorphism
If you look at the code, there is a principal class wich is class **Pawn**. This class has all of the methodes of the black and white pawns. 
That means, that in each class, Blackpawn and Whitepawn, we can access the same method, without copying them twice.

### Abstraction
In the class Pawn I have implemented the two abstract methodes that will be used in the BlacPawn and the WhitePawn class.
    <p align="center">
  <img src="/images/Abstraction.png" alt="Image Alt text" title="Optional title" />
</p>

### Inheritance
Both BlackPawn and WhitePawn inherit from the Pawn class. 
They are define like: **BlackPawn(Pawn)**, **WhitePawn(Pawn)**, this is reaaly useful, when we want to use a method that does the same thing for different objects.

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
