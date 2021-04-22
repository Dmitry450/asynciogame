import pygame


class Graphics:
    """Main object to draw stuff"""
    
    def __init__(self, screen):
        self.images = {}
        
        self.track_object = None
        
        self.draw_offset = pygame.math.Vector2()
        
        self.camera = pygame.math.Vector2()
        
        self.screen = screen
    
    def load_image(self, name):
        """Load image"""
        try:
            self.images[name] = pygame.image.load(name).convert_alpha()
        except Exception as e:
            print("Error while loading texture:", str(e))
    
    def update_camera(self):
        """Update camera position with tracked object"""
        if self.track_object is not None:
            self.camera = self.track_object.position - self.draw_offset
    
    def draw(self, image, position):
        """Draw image at position"""
        image = self.images.get(image)
        
        if image is None:
            return
        
        info = pygame.display.Info()
        
        draw_position = position - self.camera
        
        if (-image.get_width() < draw_position.x < info.current_w
            and -image.get_height() < draw_position.y < info.current_h):
            self.screen.blit(image, draw_position)
