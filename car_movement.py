from pyglet import *
import numpy as np
from pyglet.window import key

WINDOW_SIZE = (1280, 720)
TITLE = 'Car Movement'
TURNING_SPEED = 3 * np.pi / 180
MAX_SPEED = 10
DRAG = 0.05
START_POS = [83., 357.]
MAP_IMAGE = image.load('map2.png')
CAR_IMAGE = image.load('car.png')

#Sets the window size etc.
window = window.Window(*WINDOW_SIZE, TITLE)

position = START_POS
velocity = [0., np.pi / 2]
braking_speed = 0.15
accelerating = 0
turning = 0


@window.event
def on_key_press(symbol, modifiers):
    global velocity, turning, accelerating, position
    if symbol == key.A:
        turning = 1
    if symbol == key.D:
        turning = -1
    if symbol == key.W:
        accelerating = 1
    if symbol == key.S:
        accelerating = -1


@window.event
def on_key_release(symbol, modifiers):
    global turning, accelerating
    if symbol == key.A:
        turning = 0
    if symbol == key.D:
        turning = 0
    if symbol == key.W:
        accelerating = 0
    if symbol == key.S:
        accelerating = 0


def calc_position():
    global position
    position[0] += velocity[0] * np.cos(velocity[1])
    position[1] += velocity[0] * np.sin(velocity[1])


@window.event
def on_draw():
    window.clear()
    background = MAP_IMAGE
    background.blit(0, 0)
    player_image = CAR_IMAGE
    player_image.anchor_x = player_image.width // 2
    player_image.anchor_y = player_image.height // 4
    player = sprite.Sprite(player_image, position[0], position[1])
    player.scale = 0.07
    player.rotation =  - velocity[1] / np.pi * 180 - 90
    player.draw()


def update(dt):
    global position, velocity
    velocity[1] += TURNING_SPEED * turning # Changes angle of the car when turning.
    accel_rate = velocity[0] / MAX_SPEED * 10 # Acceleration curve.
    acceleration_speed = 1 / (2 * (accel_rate + 1.5)) # Decreases acceleration as speed increases.
    if velocity[0] < MAX_SPEED - acceleration_speed and accelerating == 1: # Accelerates car.
        velocity[0] += acceleration_speed * accelerating
    elif velocity[0] > 0 and accelerating == -1: # Controls braking.
        if velocity[0] < acceleration_speed:
            velocity[0] = 0.
        else:
            velocity[0] -= braking_speed
    if velocity[0] > 0 and accelerating == 0: # Decreases speed if no accel is provided.
        velocity[0] -= DRAG
    if velocity[0] < 0:
        velocity[0] = 0.
    calc_position()
    print(f"| x: {position[0]:.4f} | y: {position[1]:.4f} | speed: {velocity[0]:.4f} | acceleration rate: {acceleration_speed:.4f} | angle: {(velocity[1] * 180 / np.pi) % 360:.0f} |")


def main():
    clock.schedule_interval(update, 1/60.0)
    app.run()


main()