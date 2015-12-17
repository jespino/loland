from pyglet.window import Window
from pyglet.window import key
from pyglet import app
from pyglet import clock

from loland.screens import Menu, Playing

window = Window(fullscreen=True)
window.section = "menu"

menu = Menu(window)
playing = Playing(window)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.F:
        if window.fullscreen:
            window.set_fullscreen(False)
        else:
            window.set_fullscreen(True)
    elif window.section == "menu":
        if symbol == key.Q:
            app.exit()

        elif symbol == key.DOWN:
            menu.selected_option = 1

        elif symbol == key.UP:
            menu.selected_option = 0

        elif symbol == key.ENTER:
            if menu.selected_option == 0:
                window.section = "playing"
            elif menu.selected_option == 1:
                app.exit()
    elif window.section == "playing":
        if symbol == key.Q:
            window.section = "menu"


@window.event
def on_draw():
    window.clear()
    if window.section == "menu":
        menu.draw()
    elif window.section == "playing":
        playing.draw()

clock.set_fps_limit(60)

while not app.event_loop._has_exit:
    clock.tick()

    for window in app.windows:
        window.switch_to()
        window.dispatch_events()
        window.dispatch_event('on_draw')
        window.flip()
