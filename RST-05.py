# !/usr/bin/env python3
# Created By: Aaron Rivelino
# Date: May 28, 2025

import ugame
import stage

import constants


# Define the game_scene function
def game_scene():
    # images banks for CircuitPython
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # Set the background to image 0 in the image bank
    # And the size (10x8 tile of size 16x16)
    background = stage.Grid(image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)

    # A sprite that will be updated every frame
    ship = stage.Sprite(image_bank_sprites, 5, 75, constants.SCREEN_Y - (2 * constants.SPRITE_SIZE))
    # Create a stage for the background to show up on
    # and set the framerate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # Set the layers of all sprites, items show up in order
    game.layers = [ship] + [background]
    # Render al sprites
    # most likely you will render the background once per game scene
    game.render_block()

    # Repeat forever loop
    while True:
        # Get user input
        keys = ugame.buttons.get_pressed()

        if keys & ugame.K_X:
            pass
        if keys & ugame.K_O:
            pass
        if keys & ugame.K_START:
            pass
        if keys & ugame.K_SELECT:
            pass
        if keys & ugame.K_RIGHT:
            if ship.x <= constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move(ship.x + 2, ship.y)
            else:
                ship.move(constants.SCREEN_X - constants.SPRITE_SIZE, ship.y)
        if keys & ugame.K_LEFT:
            if ship.x >= 0:
                ship.move(ship.x - 2, ship.y)
            else:
                ship.move(0,ship.y)
        if keys & ugame.K_UP:
            pass
        if keys & ugame.K_DOWN:
            pass

        # update game logic

        # redraw sprites
        game.render_sprites([ship])
        game.tick()


if __name__ == "__main__":
    game_scene()
