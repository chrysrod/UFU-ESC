// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(RESET) 
	@SCREEN
	D=A
	@cur_screen_word 
	M=D

(LOOP)	
	@KBD
	D=M
	
	@FILL 
	D; JGT
	
	@BLANK 
	0; JMP
	
(FILL)
	@cur_screen_word
	A=M
	M=-1
	
	@CHECK
	0; JMP
	
(BLANK)
	@cur_screen_word
	A=M
	M=0
	
	@CHECK
	0; JMP
	
(CHECK) 
	@cur_screen_word
	MD=M+1
	@KBD
	D=D-A
	
	@RESET 
	D; JEQ
	
	@LOOP 
	0; JMP