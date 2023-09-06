from ursina import *

app = Ursina(development_mode=True,)

player = Entity(model='cube', color=color.orange, scale_y=2)
player.collider = "mesh"

def update():
    camera.add_script(SmoothFollow(target=player, offset=(0,2,0)))

def playermovement() -> None:
    player.x -= held_keys["a"] * time.dt
    player.x += held_keys["d"] * time.dt
player.update = playermovement

app.run()