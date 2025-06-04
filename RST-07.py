# !/usr/bin/env python3
# Created By: Aaron Rivelino
# Date: May 28, 2025

import ugame
import stage

import constants


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
    text1.text("Mega Donut Studios")
    # Add the text to the list
    text.append(text1)

    # Add the second text the same way
    text2 = stage.Text(
        width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None
    )
    text2.move(48, 118)
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


# Define the game_scene function
def game_scene():
    # images banks for CircuitPython
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # buttons that you want to keep state information on
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # get sound ready
    pew_sound = open("pew.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # Set the background to image 0 in the image bank
    # And the size (10x8 tile of size 16x16)
    background = stage.Grid(
        image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    # A sprite that will be updated every frame
    ship = stage.Sprite(
        image_bank_sprites, 5, 75, constants.SCREEN_Y - (2 * constants.SPRITE_SIZE)
    )

    # Alien sprite
    alien = stage.Sprite(
        image_bank_sprites,
        9,
        int(constants.SCREEN_X / 2 - constants.SPRITE_SIZE / 2),
        16,
    )

    # Create a stage for the background to show up on
    # and set the framerate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # Set the layers of all sprites, items show up in order
    game.layers = [ship] + [alien] + [background]
    # Render al sprites
    # most likely you will render the background once per game scene
    game.render_block()

    # Repeat forever loop
    while True:
        # Get user input
        keys = ugame.buttons.get_pressed()

        # A button to fire
        if keys & ugame.K_O != 0:
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
        if keys & ugame.K_X != 0:
            pass
        #
        if keys & ugame.K_START != 0:
            pass
        if keys & ugame.K_SELECT != 0:
            pass
        if keys & ugame.K_RIGHT != 0:
            if ship.x <= constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move(ship.x + 2, ship.y)
            else:
                ship.move(constants.SCREEN_X - constants.SPRITE_SIZE, ship.y)
        if keys & ugame.K_LEFT != 0:
            if ship.x >= 0:
                ship.move(ship.x - 2, ship.y)
            else:
                ship.move(0, ship.y)
        if keys & ugame.K_UP != 0:
            pass
        if keys & ugame.K_DOWN != 0:
            pass

        # update game logic
        if a_button == constants.button_state["button_just_pressed"]:
            sound.play(pew_sound)
        # redraw sprites
        game.render_sprites([ship] + [alien])
        game.tick()


if __name__ == "__main__":
    menu_scene()
