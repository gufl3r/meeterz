from ursina import *

app = Ursina(development_mode=True,)

class living:
    #inte = internal
    #visu = visual
    #pers = personal (only players can have)
    default_inte_entity = None
    default_inte_entityupdate = None
    default_inte_tags = ["gravityaffected","hascollision"]
    default_inte_name = None
    default_inte_weight = 0.1
    default_visu_cosmetics = []
    default_pers_mail = None
    
    class player:
        def __init__(self,name,mail) -> None:
            self.inte_entity = Entity(model='cube', collider="mesh", scale_y=2)
            self.inte_entity.update = self.update
            self.inte_tags = living.default_inte_tags
            self.inte_name = name
            self.inte_weight = living.default_inte_weight
            self.visu_cosmetics = living.default_visu_cosmetics
            self.pers_mail = mail

            camera.parent = self.inte_entity
            camera.set_position((0,-20,-20))
            camera.look_at(self.inte_entity)
        def update(self):
            if sessionplayermail == self.pers_mail:
                self.inte_entity.z += held_keys["w"] * time.dt
                self.inte_entity.z -= held_keys["s"] * time.dt
                self.inte_entity.x -= held_keys["a"] * time.dt
                self.inte_entity.x += held_keys["d"] * time.dt
                self.inte_entity.y += held_keys["space"] * time.dt
        def getinfo(self, info):
            if info == "entity":
                return self.inte_entity
            elif info == "name":
                return self.inte_name
            elif info == "mail":
                return self.pers_mail
            elif info == "tags":
                return self.inte_tags
            elif info == "weight":
                return self.inte_weight
        def settexture(self,texture):
            self.inte_entity.texture = texture
    class pig:
        def __init__(self) -> None:
            self.inte_entity = living.default_inte_entity
            self.inte_entity.update = self.update
            self.inte_tags = living.default_inte_tags
            self.inte_name = "Pig"
            self.inte_weight = living.default_inte_weight
            self.visu_cosmetics = living.default_visu_cosmetics
            self.pers_mail = living.default_pers_mail
        def update(self):
            pass
        def getinfo(self, info):
            if info == "entity":
                return self.inte_entity
            elif info == "tags":
                return self.inte_tags
            elif info == "weight":
                return self.inte_weight
        def settexture(self,texture):
            self.inte_entity.texture = texture
    class horse:
        def __init__(self) -> None:
            self.inte_entity = living.default_inte_entity
            self.inte_entity.update = self.update
            self.inte_tags = living.default_inte_tags
            self.inte_name = "Horse"
            self.inte_weight = living.default_inte_weight
            self.visu_cosmetics = living.default_visu_cosmetics
            self.pers_mail = living.default_pers_mail
        def update(self):
            pass
        def getinfo(self, info):
            if info == "entity":
                return self.inte_entity
            elif info == "tags":
                return self.inte_tags
            elif info == "weight":
                return self.inte_weight
        def settexture(self,texture):
            self.inte_entity.texture = texture

class notliving:
    default_inte_entity = None
    default_inte_tags = ["moves","hascollision"]
    default_inte_weight = 0.05
    default_inte_name = None
    class terrain:
        def __init__(self) -> None:
            self.inte_entity = Entity()
            self.inte_tags = ["hascollision"]
            self.inte_weight = inf
            self.inte_name = notliving.default_inte_name
        def update(self):
            pass
        def settexture(self,texture):
            self.inte_entity.texture = texture
    class bigobject:
        def __init__(self) -> None:
            self.inte_entity = Entity()
            self.inte_tags = notliving.default_inte_tags
            self.inte_weight = 0.2
            self.inte_name = notliving.default_inte_name
        def update(self):
            pass
        def settexture(self,texture):
            self.inte_entity.texture = texture
    class smallobject:
        def __init__(self) -> None:
            self.inte_entity = Entity()
            self.inte_tags = notliving.default_inte_tags
            self.inte_weight = notliving.default_inte_weight
            self.inte_name = notliving.default_inte_name
        def update(self):
            pass
        def settexture(self,texture):
            self.inte_entity.texture = texture
        
            
def setsessionplayer(mail):
    global sessionplayermail
    sessionplayermail = mail

setsessionplayer("marlonfg2004@gmail.com")
devplayer = living.player("Gufler","marlonfg2004@gmail.com")
devplayer.settexture("assets/textures/amonga.png")

def update():
    pass

app.run()