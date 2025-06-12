# !/usr/bin/env python3
# Created By: Aaron Rivelino
# Date: May 28, 2025
# Donut Invaders Game, is a space shooting alien game where you have to shoot at aliens
# to get the highest score possible

import ugame
import stage
import time
import random

# library to reboot the pybadge, making the game start over, and reload the game
import supervisor

import constants


# define the splash scene
def splash_scene():
    # images banks for CircuitPython
    image_bank_mt_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # get sound of the coin
    # Open the folder sound and store it on a variable
    coin_sound = open("coin.wav", "rb")
    # Get the audio
    sound = ugame.audio
    # stop the audio in case any other audio is running
    sound.stop()
    sound.mute(False)
    # play the sound
    sound.play(coin_sound)

    # Set the background to image 0 in the image bank
    background = stage.Grid(
        image_bank_mt_background, constants.SCREEN_X, constants.SCREEN_Y
    )

    # used this program to split the image into tile:
    #   https://ezgif.com/sprite-cutter/ezgif-5-818cdbcc3f66.png
    background.tile(2, 2, 0)  # blank white
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)
    background.tile(7, 2, 0)  # blank white

    background.tile(2, 3, 0)  # blank white
    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)
    background.tile(7, 3, 0)  # blank white

    background.tile(2, 4, 0)  # blank white
    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)
    background.tile(7, 4, 0)  # blank white

    background.tile(2, 5, 0)  # blank white
    background.tile(3, 5, 0)
    background.tile(4, 5, 13)
    background.tile(5, 5, 14)
    background.tile(6, 5, 0)
    background.tile(7, 5, 0)  # blank white

    # Create a stage for the background to show up on
    # and set the framerate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # Set the layers of all sprites, items show up in order
    game.layers = [background]
    # Render all sprites
    # most likely you will render the background once per game scene
    game.render_block()

    # Repeat forever loop
    while True:
        # Wait for 2 seconds
        time.sleep(2.0)
        menu_scene()


# Define the game_scene function
def menu_scene():
    # images banks for CircuitPython
    image_bank_mt_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # Text variable, list
    text = []
    # Add the first text. with its measures, font and color
    text1 = stage.Text(
        width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None
    )
    # Set where the text is going to be, in pixels
    text1.move(20, 10)
    text1.text("Mt Game Studios")
    # Add the text to the list
    text.append(text1)

    # Add the second text the same way
    text2 = stage.Text(
        width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None
    )
    text2.move(40, 110)
    text2.text("PRESS START")
    text.append(text2)

    # Set the background to image 0 in the image bank
    # And the size (10x8 tile of size 16x16)
    background = stage.Grid(
        image_bank_mt_background, constants.SCREEN_X, constants.SCREEN_Y
    )

    # Create a stage for the background to show up on
    # and set the framerate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # Set the layers of all sprites, items show up in order
    game.layers = text + [background]
    # Render all sprites
    # most likely you will render the background once per game scene
    game.render_block()

    # Repeat forever loop
    while True:
        # Get user input
        keys = ugame.buttons.get_pressed()

        # If user presses start
        if keys & ugame.K_START != 0:
            # It will go to the game scene
            game_scene()

        # redraw sprites
        game.tick()

# High Score Functions
# Loads the high score from a file. If the file dosen't exist or its content is invalid it returns 0
def load_high_score(filename="highscore.txt"):
    try:
        with open(filename, "r") as file:
            return int(file.read())
    # OSError covers FileNotFoundError and other potential file system errors
    # ValueError covers cases where file content is not a valid integer 
    except (OSError, ValueError):
        return 0

# Saves the new score to the high score file if it is greater than the currently saved high score
# The w mode will create the fille if it doesn't exist or overwrite it
def save_high_score(score, filename="highscore.txt"):
    # load the function to get the existing score
    current_high_score = load_high_score(filename)
    if score > current_high_score:
        try:
            with open(filename, "w") as file: # Use "w" to create/overwrite
                file.write(str(score))
        except OSError:
            # Handle potential errors during writing (e.g., full disk, permissions)
            print("Could not save high score.")
            # If the new score is not higher, nothing will happend

# Define the game_scene function
def game_scene():
    high_score = load_high_score()
    # Set score to 0
    score = 0
    # Display the score
    score_text = stage.Text(width=29, height=14)
    score_text.clear()
    score_text.cursor(0, 0)
    score_text.move(1, 1)
    score_text.text("Score: {0}".format(score))
    
    lives = 3
    lives_text = stage.Text(width=29, height=14)
    score_text.cursor(0, 0)
    lives_text.move(90, 0)
    lives_text.text("Lives: {0}".format(lives))

    
    # Define the alien function
    def show_alien():
        # This function takes an alien from off the screen and moves it on screen
        for alien_number in range(len(aliens)):
            # if the alien position is less than 0(side of the screen)
            if aliens[alien_number].x < 0:
                # Then it would take it and place in a random x axis, and on the y axis would be at the top of the screen
                aliens[alien_number].move(
                    random.randint(
                        0 + constants.SPRITE_SIZE,
                        constants.SCREEN_X - constants.SPRITE_SIZE,
                    ),
                    constants.OFF_TOP_SCREEN,
                )
                break

    # images banks for CircuitPython
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # buttons that you want to keep state information on
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # get sound ready
    # open the sound for pew
    pew_sound = open("pew.wav", "rb")
    # open the sound for boom
    boom_sound = open("boom.wav", "rb")
    # open crash sound
    crash_sound = open("crash.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # Set the background to image 0 in the image bank
    # And the size (10x8 tile of size 16x16)
    background = stage.Grid(
        image_bank_background, constants.SCREEN_X, constants.SCREEN_Y
    )
    # For loop to randomize the background
    # For the x axis
    for x_location in range(constants.SCREEN_GRID_X):
        # For the Y axis
        for y_location in range(constants.SCREEN_GRID_Y):
            # Generates a random number which represent the tile number
            tile_picked = random.randint(1, 3)
            background.tile(x_location, y_location, tile_picked)
            # It creates a random background each time

    # A sprite that will be updated every frame
    ship = stage.Sprite(
        image_bank_sprites, 5, 75, constants.SCREEN_Y - (2 * constants.SPRITE_SIZE)
    )

    # Alien sprite
    # Create a list of aliens
    aliens = []
    for alien_number in range(constants.TOTAL_NUMBER_OF_ALIENS):
        a_single_alien = stage.Sprite(
            image_bank_sprites, 9, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
        )
        # append the single laser
        aliens.append(a_single_alien)
    # Place one alien on the screen
    show_alien()

    # Create a list of laser when shoot
    # for loop going from 0 to 4
    # Create a single sprite
    lasers = []
    for laser_number in range(constants.TOTAL_NUMBER_OF_LASERS):
        a_single_laser = stage.Sprite(
            image_bank_sprites, 10, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
        )
        # append the single laser
        lasers.append(a_single_laser)

    # Create a stage for the background to show up on
    # and set the framerate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # Set the layers of all sprites, items show up in order
    game.layers = [score_text, lives_text] + aliens + lasers + [ship] + [background]
    # Render al sprites
    # most likely you will render the background once per game scene
    game.render_block()

    # Repeat forever loop
    while True:
        # Get user input
        keys = ugame.buttons.get_pressed()

        # A button to fire
        if keys & ugame.K_X != 0:
            # If the A button was previously up and now is being pressed
            if a_button == constants.button_state["button_up"]:
                # and set button as just pressed(just once)
                a_button = constants.button_state["button_just_pressed"]
            # elif the button is still being pressed instead of just once
            elif a_button == constants.button_state["button_just_pressed"]:
                # It will set a button as button still pressed
                a_button = constants.button_state["button_still_pressed"]
        # else if the button is not being pressed anymore or at all
        else:
            # If the button was being pressed, it will set the button from still pressed to button released
            if a_button == constants.button_state["button_still_pressed"]:
                # change it to released
                a_button = constants.button_state["button_released"]
            # Else the button was never pressed so is up
            else:
                a_button = constants.button_state["button_up"]
        # B button
        if keys & ugame.K_O != 0:
            pass

        if keys & ugame.K_START != 0:
            pass
        if keys & ugame.K_SELECT != 0:
            pass
        # If keys is pressed right
        if keys & ugame.K_RIGHT != 0:
            # if the ships is inside the grid it can move
            if ship.x <= constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move((ship.x + constants.SPRITE_MOVEMENT_SPEED), ship.y)
            else:
                # It will bounce off the limit of the right part
                ship.move(constants.SCREEN_X - constants.SPRITE_SIZE, ship.y)
        # If keys pressed is left
        if keys & ugame.K_LEFT != 0:
            # if the ship is inside the grid it can move
            if ship.x >= 0:
                ship.move((ship.x - constants.SPRITE_MOVEMENT_SPEED), ship.y)
            # Else it will bounce off the left limit
            else:
                ship.move(0, ship.y)
        if keys & ugame.K_UP != 0:
            pass
        if keys & ugame.K_DOWN != 0:
            pass

        # update game logic
        if a_button == constants.button_state["button_just_pressed"]:
            # fire a laser, if we have enough power( have not used all lasers)
            # check for each individual laser an check if it less than 0
            for laser_number in range(len(lasers)):
                if lasers[laser_number].x < 0:
                    # If there is one laser that is off the screen, move it to where the ship is
                    lasers[laser_number].move(ship.x, ship.y)
                    # play the sound when you find one
                    sound.play(pew_sound)
                    break

        # Check if there is a laser on the screen, so it moves
        for laser_number in range(len(lasers)):
            # if the laser is on the screen, move the laser up 1
            if lasers[laser_number].x > 0:
                lasers[laser_number].move(
                    lasers[laser_number].x,
                    lasers[laser_number].y - constants.LASER_SPEED,
                )
                # Then check its y location, so it is not off the screen
                if lasers[laser_number].y < constants.OFF_TOP_SCREEN:
                    # if it goes off top of the screen move it to the holding pattern
                    lasers[laser_number].move(
                        constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
                    )

            for alien_number in range(len(aliens)):
                # if the alien is on the screen, move the laser down by 1 pixel
                if aliens[alien_number].x > 0:
                    aliens[alien_number].move(
                        aliens[alien_number].x,
                        aliens[alien_number].y + constants.ALIEN_SPEED,
                    )
                    # Then check its y location is off the screen
                    if aliens[alien_number].y > constants.SCREEN_Y:
                        # if it goes off then it moves back to its holding area
                        aliens[alien_number].move(
                            constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
                        )
                        # Then call the function to show another alien
                        show_alien()
                        # Then subtract - 1 to the global score
                        score -= 1
                        # if the score is less than 0 don't subtract nothing
                        if score < 0:
                            score = 0
                        # Then display the new score
                        score_text.clear()
                        score_text.cursor(0, 0)
                        score_text.move(1, 1)
                        score_text.text("Score: {0}".format(score))

            # Each frame checks if the lasers are touching the aliens
            # Loop for every laser but only the ones that are on the screen
            for laser_number in range(len(lasers)):
                # if, to check if they are on the screen
                if lasers[laser_number].x > 0:
                    # the same for aliens
                    for alien_number in range(len(aliens)):
                        if aliens[alien_number].x > 0:
                            # Add the specific collisions for the aliens and lasers
                            if stage.collide(
                                lasers[laser_number].x + 6,
                                lasers[laser_number].y + 2,
                                lasers[laser_number].x + 11,
                                lasers[laser_number].y + 12,
                                aliens[alien_number].x + 1,
                                aliens[alien_number].y,
                                aliens[alien_number].x + 15,
                                aliens[alien_number].y + 15,
                            ):
                                # You hit an alien
                                aliens[alien_number].move(
                                    constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
                                )
                                lasers[laser_number].move(
                                    constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
                                )
                                sound.stop()
                                sound.play(boom_sound)
                                show_alien()
                                show_alien()
                                # When a laser touches add 1 to the score and re-draw the screen
                                score = score + 1
                                score_text.clear()
                                score_text.cursor(0, 0)
                                score_text.move(1, 1)
                                score_text.text("Score: {0}".format(score))

            # When an alien touches the ship
            # Each frame check if any alien is touching the ship
            # Check for collision between alien and ship
            for alien_number in range(len(aliens)):
                if aliens[alien_number].x > 0:
                    if stage.collide(
                        aliens[alien_number].x + 1,
                        aliens[alien_number].y,
                        aliens[alien_number].x + 15,
                        aliens[alien_number].y + 15,
                        ship.x,
                        ship.y,
                        ship.x + 15,
                        ship.y + 15,
                    ):
                        # Play crash sound
                        sound.stop()
                        sound.play(crash_sound)
            
                        # Subtract one life
                        lives -= 1
            
                        # Move alien off screen to avoid instant repeated collision
                        aliens[alien_number].move(
                            random.randint(
                                0 + constants.SPRITE_SIZE,
                                constants.SCREEN_X - constants.SPRITE_SIZE
                            ),
                            constants.OFF_TOP_SCREEN
                        )
                        score_text.cursor(0, 0)
                        lives_text.move(90, 0)
                        lives_text.text("Lives: {0}".format(lives))

                        # Pause briefly to show effect
                        time.sleep(1.0)
            
                        # If no lives left, game over
                        if lives <= 0:
                            save_high_score(score)
                            game_over_scene(score)
            


        # redraw sprites
        game.render_sprites(aliens + lasers + [ship])
        # wait until refresh rate finishes
        game.tick()


# this function is the game over scene
def game_over_scene(final_score):

    # turn off sound from last scene
    sound = ugame.audio
    sound.stop()

    # image banks
    # grabs the empty image bank and
    image_bank_2 = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # sets the background to image 0 in the image bank
    # to print a blanc background
    background = stage.Grid(
        image_bank_2, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )
    
    high_score = load_high_score()
    # Add a list for text
    text = []
    # Text object for displaying the final score
    text1 = stage.Text(
        width=29, height=14, font=None, palette=constants.RED_PALETTE, buffer = None)
    text1.move(22, 20)
    text1.text("Final Score: {:0>2d}".format(final_score))
    text.append(text1)

    # Text object for "GAME OVER" message
    text2 = stage.Text(
        width=29, height=14, font=None, palette=constants.RED_PALETTE, buffer = None)
    text2.move(43, 60)
    text2.text("GAME OVER")
    text.append(text2)

    # Text object for "PRESS SELECT" instruction
    text3 = stage.Text(
        width=29, height=14, font=None, palette=constants.RED_PALETTE, buffer = None
    )
    text3.move(32, 110)
    text3.text("PRESS SELECT")
    text.append(text3)

    # Text object for displaying the high score
    text4 = stage.Text(
        width=29, height=14, font=None, palette=constants.RED_PALETTE, buffer = None
    )
    text4.move(22, 40)
    text4.text("High Score: {:0>2d}".format(high_score))
    text.append(text4)
    
    # create a stage for the background to show up on
    # Set the frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # set the layers, they show up in order
    game.layers = text + [background]

    # render the background and initial location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()

        # Start button
        # if it is pressed it will reboot the game
        if keys & ugame.K_SELECT != 0:
            supervisor.reload()

        # update game logic
        game.tick()  # wait until refresh rate finishes


if __name__ == "__main__":
    splash_scene()

