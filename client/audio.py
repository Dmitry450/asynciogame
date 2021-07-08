import pygame
from pygame.math import Vector2


class Sound:
    
    def __init__(self, manager, snd):
        self.manager = manager
        self.snd = snd
        
        self.ttl = snd.get_length()
        
        self.playing = True
        
        self.snd.play()
    
    def update(self, dtime):
        self.ttl -= dtime
        
        if self.ttl <= 0:
            self.playing = False


class AttachedSound(Sound):
    
    def __init__(self, manager, snd, position, fade_dist=1, min_volume=0.1):
        super().__init__(manager, snd)
        
        if not isinstance(position, Vector2):
            position = Vector2(position)
        
        self.position = position
        
        self.fade_dist = fade_dist
        self.min_volume = min_volume

    def update(self, dtime):
        super().update(dtime)
        
        if self.playing and self.manager.track_object is not None:
            dist = self.position.distance_to(self.manager.track_object.position)
            
            volume = elf.fade_dist/dist
            
            if volume > self.min_volume:
                self.snd.set_volume(volume)
            
            else:
                self.snd.set_volume(0)


class AudioManager:
    
    def __init__(self):
        self.loaded = {}
        self.sounds = []
        
        self.track_object = None
    
    def play_sound(self, d):
        name = d["name"]
        
        if self.loaded.get(name) is None:
            self.loaded[name] = pygame.mixer.Sound(name)
        
        if d["type"] == "normal":
            self.sounds.append(Sound(self, self.loaded[name]))
        
        # Actually sound can be "attached_to_position" and "attached_to_entity".
        # To avoid adding EntityManager reference into AudioManager, "position"
        # will be replaced by entity.position in Connection when sound event handled.
        # Anyway, d["type"] will be set to "attached"
        elif d["type"] == "attached":
            self.sounds.append(AttachedSound(self, self.loaded[name], d["position"],
                                             fade_dist=d.get("fade_dist", 1),
                                             min_volume=d.get("min_volume", 0.1)))
    
    def update(self, dtime):
        for sound in self.sounds:
            sound.update(dtime)
            
            if not sound.playing:
                self.sounds.remove(sound)
