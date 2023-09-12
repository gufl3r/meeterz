from ursina import *
from ursina.shaders import lit_with_shadows_shader
from string import ascii_uppercase
import copy
import time
import numpy

app = Ursina(development_mode=True,vsync=False,borderless=False,title="Meeterz")

lastid = "0A"
def setobjectid():
    global lastid
    if lastid[0] != "9":
        lastid = str(int(lastid[0])+1)+lastid[1]
    else:
        lastid = "0"+ascii_uppercase[ascii_uppercase.index(lastid[1])+1]
    return lastid

class living:
    #inte = internal
    #visu = visual
    #pers = personal (only players can have)
    def querydefault(query):
        default = {
            "inte_entityupdate": None,
            "inte_entitytexture": None,
            "inte_entityworldpos": (0, 0, 0),
            "inte_entitycolor": color.white,
            "inte_entityshader": lit_with_shadows_shader,
            "inte_walkspeed": 1,
            "inte_jumpstrenght": 3,
            "inte_onground": True,
            "inte_tags": ["gravityaffected", "hascollision"],
            "inte_name": None,
            "inte_weight": 0.1,
            "inte_id": None,
            "inte_velocity": {"x": 0, "y": 0, "z": 0},
            "visu_cosmetics": [],
            "pers_mail": None
        }
        return copy.deepcopy(default[query])
    
    class player(Entity):
        def __init__(self,id_,name,mail,texture=None,worldpos=None,cosmetics=None,color_=None,shader=None) -> None:
            #entity setup
            super().__init__()
            self.model = "cube"
            self.collider = "box"
            self.scale_y=2
            self.texture=living.querydefault("inte_entitytexture") if texture == None else texture
            self.world_position=living.querydefault("inte_entityworldpos") if worldpos == None else worldpos
            self.shader=living.querydefault("inte_entityshader") if shader == None else shader
            self.color=living.querydefault("inte_entitycolor") if color_ == None else color_

            #custom
            self.inte_tags = living.querydefault("inte_tags")
            self.inte_name = name
            self.inte_weight = living.querydefault("inte_weight")
            self.inte_walkspeed = living.querydefault("inte_walkspeed")
            self.inte_jumpstrenght=living.querydefault("inte_jumpstrenght")
            self.inte_onground = living.querydefault("inte_onground")
            self.inte_velocity = living.querydefault("inte_velocity")
            self.inte_id = id_
            self.visu_nametag = Text(text=self.inte_name,background=True)
            self.visu_cosmetics = living.querydefault("visu_cosmetics") if cosmetics == None else cosmetics
            self.pers_mail = mail
        def update(self):
            nametagpos = tuple([self.world_position[0]]+[self.world_position[1]+self.scale_y]+[self.world_position[2]])
            self.visu_nametag.x = world_position_to_screen_position(nametagpos)[0]
            self.visu_nametag.y = world_position_to_screen_position(nametagpos)[1]
            if sessionplayermail == self.pers_mail:
                camera.look_at(self)
                camera.set_position((5,7,20),relative_to=self)
                self.x+=self.inte_velocity["x"] * time.dt
                self.y+=self.inte_velocity["y"] * time.dt
                self.z+=self.inte_velocity["z"] * time.dt
                self.inte_velocity["x"] *= 0.8 if abs(self.inte_velocity["x"]) > 1e-40 else 0
                self.inte_velocity["z"] *= 0.8 if abs(self.inte_velocity["z"]) > 1e-40 else 0
                #y velocity is calculated by gravity

                self.inte_velocity["x"] -= held_keys["d"]* self.inte_walkspeed
                self.inte_velocity["x"] += held_keys["a"]* self.inte_walkspeed
                if self.inte_onground and (held_keys["space"]) == 1:
                    self.inte_velocity["y"] += self.inte_jumpstrenght
                    self.inte_onground = False
                self.inte_velocity["z"] -= held_keys["w"]* self.inte_walkspeed
                self.inte_velocity["z"] += held_keys["s"]* self.inte_walkspeed
        def getinfo(self, info):
            if info == "name":
                return self.inte_name
            elif info == "mail":
                return self.pers_mail
            elif info == "tags":
                return self.inte_tags
            elif info == "weight":
                return self.inte_weight
            elif info == "id":
                return self.inte_id
            elif info == "class":
                return "living"
        def settexture(self,texture):
            self.texture = texture
        def reloadtags(self) -> None:
            pass
    class pig(Entity):
        def __init__(self,id_,texture=None,worldpos=None,cosmetics=None,color_=None,shader=None) -> None:
            #entity setup
            super().__init__()
            self.model = "cube"
            self.collider="box"
            self.texture="assets/textures/pigface.jpg" if texture == None else texture
            self.world_position=living.querydefault("inte_entityworldpos") if worldpos == None else worldpos
            self.shader=living.querydefault("inte_entityshader") if shader == None else shader
            self.color=living.querydefault("inte_entitycolor") if color_ == None else color_

            #custom
            self.inte_tags = living.querydefault("inte_tags")
            self.inte_name = "Pig"
            self.inte_weight = living.querydefault("inte_weight")
            self.inte_walkspeed = living.querydefault("inte_walkspeed")
            self.inte_jumpstrenght=living.querydefault("inte_jumpstrenght")
            self.inte_onground = living.querydefault("inte_onground")
            self.inte_velocity = living.querydefault("inte_velocity")
            self.inte_id = id_
            self.visu_nametag = Text(text=self.inte_name,background=True)
            self.visu_cosmetics = living.querydefault("visu_cosmetics") if cosmetics == None else cosmetics
            self.pers_mail = living.querydefault("pers_mail")
        def update(self):
            nametagpos = tuple([self.world_position[0]]+[self.world_position[1]+self.scale_y]+[self.world_position[2]])
            self.visu_nametag.x = world_position_to_screen_position(nametagpos)[0]
            self.visu_nametag.y = world_position_to_screen_position(nametagpos)[1]
            self.x+=self.inte_velocity["x"] * time.dt
            self.y+=self.inte_velocity["y"] * time.dt
            self.z+=self.inte_velocity["z"] * time.dt
            self.inte_velocity["x"] *= 0.8 if abs(self.inte_velocity["x"]) > 1e-40 else 0
            self.inte_velocity["z"] *= 0.8 if abs(self.inte_velocity["z"]) > 1e-40 else 0
        def getinfo(self, info):
            if info == "tags":
                return self.inte_tags
            elif info == "weight":
                return self.inte_weight
            elif info == "id":
                return self.inte_id
            elif info == "class":
                return "living"
        def settexture(self,texture):
            self.texture = texture
        def reloadtags(self) -> None:
            pass
    class horse(Entity):
        def __init__(self,id_,texture=None,worldpos:tuple=(0,0,0),cosmetics=None,color_=None,shader=None) -> None:
            #entity setup
            super().__init__()
            self.model = "cube"
            self.collider="box"
            self.scale_x=2
            self.texture=living.querydefault("inte_entitytexture") if texture == None else texture
            self.world_position=living.querydefault("inte_entityworldpos") if worldpos == None else worldpos
            self.shader=living.querydefault("inte_entityshader") if shader == None else shader
            self.color=living.querydefault("inte_entitycolor") if color_ == None else color_

            #custom
            self.inte_tags = living.querydefault("inte_tags")
            self.inte_name = "Horse"
            self.inte_weight = living.querydefault("inte_weight")
            self.inte_walkspeed = living.querydefault("inte_walkspeed")
            self.inte_jumpstrenght=living.querydefault("inte_jumpstrenght")
            self.inte_onground = living.querydefault("inte_onground")
            self.inte_velocity = living.querydefault("inte_velocity")
            self.inte_id = id_
            self.visu_cosmetics = living.querydefault("visu_cosmetics") if cosmetics == None else cosmetics
            self.pers_mail = living.querydefault("pers_mail")
        def update(self):
            pass
        def getinfo(self, info):
            if info == "tags":
                return self.inte_tags
            elif info == "weight":
                return self.inte_weight
            elif info == "id":
                return self.inte_id
            elif info == "class":
                return "living"
        def settexture(self,texture):
            self.texture = texture
        def reloadtags(self) -> None:
            pass

class notliving:
    def querydefault(query):
        default = {
            "inte_entityupdate": None,
            "inte_entitytexture": None,
            "inte_entityworldpos": (0, 0, 0),
            "inte_entityshader": lit_with_shadows_shader,
            "inte_tags": ["gravityaffected", "hascollision"],
            "inte_weight": 0.05,
            "inte_name": None,
            "inte_id": None,
        }
        return copy.deepcopy(default[query])
    
    class terrain(Entity):
        def __init__(self,id_,model,scale,texture=None,worldpos=None,shader=None) -> None:
            #entity setup
            super().__init__()
            self.model=model
            self.scale=scale
            self.collider="box"
            self.texture=notliving.querydefault("inte_entitytexture") if texture == None else texture
            self.world_position=notliving.querydefault("inte_entityworldpos") if worldpos == None else worldpos
            self.shader=notliving.querydefault("inte_entityshader") if shader == None else shader

            #custom
            self.inte_tags = ["hascollision"]
            self.inte_weight = inf
            self.inte_name = notliving.querydefault("inte_name")
            self.inte_id = id_
        def update(self):
            pass
        def getinfo(self, info):
            if info == "tags":
                return self.inte_tags
            elif info == "weight":
                return self.inte_weight
            elif info == "id":
                return self.inte_id
            elif info == "class":
                return "notliving"
        def settexture(self,texture):
            self.texture = texture
        def reloadtags(self) -> None:
            pass
    class big(Entity):
        def __init__(self,id_,model,scale:tuple,texture,worldpos:tuple=(0,0,0),shader=lit_with_shadows_shader) -> None:
            #entity setup
            super().__init__()
            self.model=model
            self.scale=scale
            self.collider="box"
            self.texture=notliving.querydefault("inte_entitytexture") if texture == None else texture
            self.world_position=notliving.querydefault("inte_entityworldpos") if worldpos == None else worldpos
            self.shader=notliving.querydefault("inte_entityshader") if shader == None else shader
            
            #custom
            self.inte_tags = notliving.querydefault("inte_tags")
            self.inte_weight = 0.2
            self.inte_name = notliving.querydefault("inte_name")
            self.inte_id = id_
        def update(self):
            pass
        def getinfo(self, info):
            if info == "tags":
                return self.inte_tags
            elif info == "weight":
                return self.inte_weight
            elif info == "id":
                return self.inte_id
            elif info == "class":
                return "notliving"
        def settexture(self,texture):
            self.texture = texture
        def reloadtags(self) -> None:
            pass
    class small(Entity):
        def __init__(self,id_,model,scale:tuple,texture=None,worldpos:tuple=(0,0,0),shader=lit_with_shadows_shader) -> None:
            #entity setup
            super().__init__()
            self.model=model
            self.collider="box"
            self.scale=scale
            self.collider="box"
            self.texture=notliving.querydefault("inte_entitytexture") if texture == None else texture
            self.world_position=notliving.querydefault("inte_entityworldpos") if worldpos == None else worldpos
            self.shader=notliving.querydefault("inte_entityshader") if shader == None else shader

            #custom
            self.inte_tags = notliving.querydefault("inte_tags")
            self.inte_weight = notliving.querydefault("inte_weight")
            self.inte_name = notliving.querydefault("inte_name")
            self.inte_id = id_
        def update(self):
            pass
        def getinfo(self, info):
            if info == "tags":
                return self.inte_tags
            elif info == "weight":
                return self.inte_weight
            elif info == "id":
                return self.inte_id
            elif info == "class":
                return "notliving"
        def settexture(self,texture):
            self.texture = texture
        def reloadtags(self) -> None:
            pass

objects = {"livingobjs":{},
           "notlivingobjs":{}}
class map:
    default_myliving = []
    default_mynotliving = []
    def l_loadinmap(object:tuple,player=False):
        id_=str(object[0]).split(".")[2][:-2]+setobjectid()
        if not player:
            objects["livingobjs"][id_] = object[0](texture=object[1],worldpos=object[2],cosmetics=object[3],color_=object[4],shader=object[5],id_=id_)
        else:
            objects["livingobjs"][id_] = object[0](name=object[1],mail=object[2],texture=object[3],worldpos=object[4],cosmetics=object[5],color_=object[6],shader=object[7],id_=id_)
    def nl_loadinmap(object:tuple):
        id_=str(object[0]).split(".")[2][:-2]+setobjectid()
        objects["notlivingobjs"][id_] = object[0](model=object[1],scale=object[2],texture=object[3],worldpos=object[4],shader=object[5],id_=id_)
    class plain:
        def __init__(self) -> None:
            self.myliving = [(living.pig,None,(0,10,2),None,None,None),(living.pig,None,(-2,10,0),None,None,None),(living.pig,None,(2,10,0),None,None,None)]
            self.mynotliving = [(notliving.terrain,"cube",(50,1,50),"assets/textures/grass.jpg",(0,-1.5,0),None)]
        def loadmap(self):
            pivot = Entity()
            DirectionalLight(parent=pivot, y=0, x=-10, shadows=True)
            Sky()
            for object in self.myliving:
                map.l_loadinmap(object)
            for object in self.mynotliving:
                map.nl_loadinmap(object)
    
def setsessionplayer(mail) -> None:
    global sessionplayermail
    sessionplayermail = mail
setsessionplayer("marlonfg2004@gmail.com")

def selectobject(by,multiple,filterargument):
    if multiple:
        returnlist = []
        if by == "specific":
            raise Exception("specific filter can only be used for one object")
        elif by == "class":
            for object in objects[filterargument[0]+"objs"]:
                returnlist.append(objects[filterargument[0]+"objs"][object])
        elif by == "subclass":
            for object in objects[filterargument[0]+"objs"]:
                if object.startswith(filterargument[1]):
                    returnlist.append(objects[filterargument[0]+"objs"][object])
        return returnlist
    else:
        if by == "specific":
            for object in objects[filterargument[0]+"objs"]:
                if object.endswith(filterargument[1][-2:]):
                    return objects[filterargument[0]+"objs"][object]
        elif by == "class":
            return objects[filterargument[0]+"objs"][list(objects[filterargument[0]+"objs"].keys())[0]]
        elif by == "subclass":
            for object in objects[filterargument[0]+"objs"]:
                if object.startswith(filterargument[1]):
                    return objects[filterargument[0]+"objs"][object]

plainmap = map.plain()
plainmap.loadmap()
map.l_loadinmap((living.player,"Gufler","marlonfg2004@gmail.com","assets/textures/player.png",None,None,None,None),True)

def update():
    allobjects = selectobject("class",True,("living",None))+selectobject("class",True,("notliving",None))
    for object in allobjects:
        objecttags = object.getinfo("tags")
        if "hascollision" in objecttags:
            hitinfo = object.intersects()
            if "gravityaffected" in objecttags:
                if not hitinfo.hit:
                    object.inte_onground = False
                else:
                    if not object.inte_onground:
                        object.y = hitinfo.entities[0].y+object.scale[1]*0.5+hitinfo.entities[0].scale[1]*0.5
                    object.inte_onground = True

                if not object.inte_onground:
                    object.inte_velocity["y"] -= 60/len(allobjects)*time.dt
                elif object.inte_velocity["y"] < 0:
                    object.inte_velocity["y"] = 0

            if not hitinfo.hit:
                object.inte_sidecollision = False
            else:
                object.inte_sidecollision = False
                for entitypos in [entity.position for entity in hitinfo.entities]:
                    if object.y-object.scale[1]*0.5-hitinfo.entities[0].scale[1]*0.5 != entitypos[1]:
                        object.inte_sidecollision = True
                        entitycoords = numpy.array(entitypos)
                        break
                if object.inte_sidecollision and object.getinfo("weight") != inf:
                    difference = tuple(numpy.array(object.world_position)-entitycoords)
                    object.inte_velocity["x"],object.inte_velocity["z"] = difference[0]*2,difference[2]*2
        else:
            object.inte_onground = False
            object.inte_sidecollision = False 

app.run()