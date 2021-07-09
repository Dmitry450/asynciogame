import pygame as pg


class TileMap:
    """Wrapper for pg.Surface that can be used for easier access to
    different tile map sprites. Note that all tile map sprites should
    have same size."""

    def __init__(self, surf, tiles_x, tiles_y):
        self.surf = surf

        self.tiles_x = tiles_x
        self.tiles_y = tiles_y

        self.width = surf.get_width()
        self.height = surf.get_height()

        self.tile_width = self.width//self.tiles_x
        self.tile_height = self.height//self.tiles_y
        
        self.current_x = self.current_y = 0
        
    def select(self, x=None, y=None):
        """Select default tile"""
        x = x if x is not None else self.current_x
        y = y if y is not None else self.current_y
        
        self.current_x = x
        self.current_y = y

    def get(self, x=None, y=None):
        """Get tile at given or default position"""
        x = x if x is not None else self.current_x
        y = y if y is not None else self.current_y
        
        if (x < 0 or x > self.tiles_x) or (y < 0 or y > self.tiles_y):
            raise IndexError(
                "invalid position on tile map (tile map: "
                f"x: 0-{self.tiles_x-1}, y: 0-{self.tiles_y-1}, "
                f"position: x: {x}, y: {y})")

        return self.surf.subsurface(
                    (x*self.tile_width,
                     y*self.tile_height,
                     min(self.tile_width, self.width-x*self.tile_width),
                     min(self.tile_height, self.height-y*self.tile_height)))


class SurfaceImage(pg.sprite.Sprite):
    """pygame.Surafce wrapper"""
    
    def __init__(self, camera, surf):
        super().__init__()
        
        self.image = surf
        
        self.rect = surf.get_rect()
        
        self.camera = camera
    
    def set_pos(self, position):
        self.rect.center = position - self.camera
    
    def __gt__(self, other):
        return self.rect.bottom > other.rect.bottom
    
    def __lt__(self, other):
        return other > self


class AnimatedImage(SurfaceImage):
    """TileMap wrapper"""
    
    def __init__(self, camera, tile_map, animations, current_animation):
        self.tile_map = tile_map
        
        self.animations = animations
        
        self.animname = current_animation
        
        self.frameno = 0
        
        self.timer = animations[current_animation]['time_per_frame']
        
        super().__init__(camera, self.get_image())
    
    def get_image(self):
        return self.tile_map.get(*self.animations[self.animname]['frames'][self.frameno])
    
    def update_image(self):
        self.image = self.get_image()
    
    def set_animation(self, name, frameno=None):
        self.animname = name
        
        if frameno is not None:
            self.frameno = frameno
            self.timer = self.animations[name]['time_per_frame']

        self.update_image()
    
    def next_frame(self):
        self.frameno += 1
        
        name = self.animname
        frameno = self.frameno
        
        if self.frameno == len(self.animations[self.animname]['frames']):
            frameno = 0
            
            if self.animations[self.animname].get('on_end_animname'):
                name = self.animations[self.animname]['on_end_animname']
            
            if self.animations[self.animname].get('on_end_frameno'):
                frameno = self.animations[self.animname]['on_end_frameno']
        
        self.set_animation(name, frameno)

    def update(self, dtime):
        self.timer -= dtime
        
        if self.timer < 0:
            self.next_frame()
