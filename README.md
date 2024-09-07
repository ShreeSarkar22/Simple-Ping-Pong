# Simple-Ping-Pong

This is a Ping Pong game on screen, made in Python using the following Modules :
                1. OpenCV
                2. Mediapipe
                3. Time

It works by tracking position of index finger tip.
When you run the program, your camera should start and a window will be displayed showing the option to choose between Human vs Human and Human vs Ai.

If you want to choose Human vs Human, hover your index finger tip on the letter "n" of the first "Human" for about 2 seconds.
If you want to choose Human vs Ai, hover your index finger tip on the letter "m" for about 2 seconds.

The first to score 3 points wins. A point is scored if you cannot hit the ball.
With each collision of the ball with paddle, the paddle will get shorter and thinner till a set dimension. Similarly, the ball will get smaller and faster till a set radius and speed.

In case of Human vs Human, Player 1 controls the paddle with the index finget tip by hovering it over the left side of screen, while Player 2 controls the paddle by hovering over right side of screen. Make sure the hand is clearly and fully visible on screen , else the hand may not be detected. 

For Human vs Ai, you will be controlling the right paddle by hovering over right side of screen. You cannot control the left paddle and hovering over left side of screen will have no effect.
The left paddle is  controlled by Ai, with a simple algorithm, it checks the y-coordinate of the centre of the ball and moves towards it at a fixed speed.

When the winning score is reached , it will display a message, indicating who won.
