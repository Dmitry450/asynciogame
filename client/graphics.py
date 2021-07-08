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
    
    def load_image(self, name):
        """Load image if it is not exists yet"""
        try:
            if self.surfaces.get(name) is None:
                self.surfaces[name] = pygame.image.load(name).convert_alpha()
        except Exception as e:
            self.surfaces[name] = self.surfaces["null"]
            print(f"Error while loading texture {name}: {str(e)}")
        
        return self.surfaces[name]
    
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
    
    def draw(self):
        """Draw sprites"""
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
