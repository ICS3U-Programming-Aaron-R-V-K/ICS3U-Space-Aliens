# !/usr/bin/env python3
# Created By: Aaron Rivelino
# Date: May 28, 2025

import ugame
import stage


# Define the game_scene function
def game_scene():
    # images banks for CircuitPython
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # Set the background to image 0 in the image bank
    # And the size (10x8 tile of size 16x16)
    background = stage.Grid(image_bank_background, 10, 8)

    # A sprite that will be updated every frame
    ship = stage.Sprite(image_bank_sprites, 5, 75, 66)
    # Create a stage for the background to show up on
    # and set the framerate to 60fps
    game = stage.Stage(ugame.display, 60)
    # Set the layers of all sprites, items show up in order
    game.layers = [ship] + [background]
    # Render al sprites
    # most likely you will render the background once per game scene
    game.render_block()

    # Repeat forever loop
    while True:
        # Get user input

        # update game logic

        # redraw sprites
        game.render_sprites([ship])
        game.tick()


if __name__ == "__main__":
    game_scene()
