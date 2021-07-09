import logging

import pygame

from .image import SurfaceImage, AnimatedImage, TileMap


class Graphics:
    """Main object to draw stuff"""
    
    def __init__(self, screen):
        self.surfaces = {
            "null": pygame.Surface((1, 1), pygame.SRCALPHA)
        }
        
        self.group = pygame.sprite.Group()
        
        self.track_object = None
        
        self.draw_offset = pygame.math.Vector2()
        
        self.camera = pygame.math.Vector2()
        
        self.screen = screen
        
        self.background = pygame.Surface(screen.get_size())
        self.background.fill('#4444FF')
        
        self.ground = None
        self.ground_position = None
    
    def load_image(self, name):
        """Load image if it is not exists yet"""
        try:
            if self.surfaces.get(name) is None:
                self.surfaces[name] = pygame.image.load(name).convert_alpha()
        except Exception as e:
            self.surfaces[name] = self.surfaces["null"]
            print(f"Error while loading texture {name}: {str(e)}")
        
        return self.surfaces[name]
    
    def set_bg_color(self, color):
        self.background.fill(color)
    
    def set_bg_image(self, name):
        self.background = self.load_image(name)
    
    def set_ground(self, surfdef=None, image_name=None, position=(0, 0)):
        """Set ground sprite from definition dict"""
        if surfdef is None and image_name is None:
            logging.warn("Graphics.set_ground: expected surfdef or image_name argument (both are None)")
            return
        
        if surfdef is not None:
            self.ground = pygame.Surface(surfdef["size"])
            self.ground.fill(surfdef["color"])
        
        else:
            self.ground = self.load_image(image_name)
        
        self.ground_position = position
    
    def create_sprite(self, d):
        """Create sprite from definition dict"""
        
        if d["type"] == "surface":
            surf = self.surfaces.get(d["id"])
            
            if surf is None:
                surf = pygame.Surface(*d["size"])
                surf.fill(d["color"])
                
                self.surfaces[d["id"]] = surf
            
            sprite = SurfaceImage(self.camera, surf)
        
        elif d["type"] == "image":
            sprite = SurfaceImage(self.camera, self.load_image(d["image"]))
        
        elif d["type"] == "animated_image":
            surf = self.load_image(d["image"])
            
            tilemap = TileMap(surf, d["tiles_x"], d["tiles_y"])
            
            sprite = AnimatedImage(self.camera, tilemap,
                                   d["animations"],
                                   d["initial_animation"])
        
        self.group.add(sprite)
        
        return sprite
    
    def update(self, dtime):
        """Update sprites"""
        if self.track_object is not None:
            self.camera.update(self.track_object.position - self.draw_offset)
        
        self.group.update(dtime)
    
    def draw_background(self):
        """Draw background to screen"""
        self.screen.blit(self.background, (0, 0))
        
        if self.ground is not None:
            draw_x = draw_y = 0
            
            surf_x, surf_y = self.camera - self.ground_position
            
            if surf_x < 0:
                draw_x = -surf_x
                surf_x = 0
            
            if surf_y < 0:
                draw_y = -surf_y
                surf_y = 0
            
            draw_width, draw_height = self.screen.get_size()
            
            if surf_x + draw_width > self.ground.get_width():
                draw_width = self.ground.get_width() - surf_x
            
            if surf_y + draw_height > self.ground.get_height():
                draw_height = self.ground.get_height() - surf_y
            
            self.screen.blit(self.ground.subsurface((surf_x, surf_y, draw_width, draw_height)), (draw_x, draw_y))
                
    
    def draw(self):
        """Draw sprites"""
        self.draw_background()
        
        sprites = self.group.sprites()
        sprites.sort()
        
        for sprite in sprites:
            image = sprite.image
            
            if image is None:
                continue
            
            info = pygame.display.Info()
            
            draw_position = sprite.rect.topleft
            
            if (-image.get_width() < draw_position[0] < info.current_w
                and -image.get_height() < draw_position[1] < info.current_h):
                self.screen.blit(image, draw_position)
