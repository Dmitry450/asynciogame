import time
import asyncio


class AsyncClock:
    """Asynchronous pygame.Clock implementation"""
    
    def __init__(self):
        self.last_call_time = time.time()
        self.time_passed = 0
        self.frames = 0
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f'<AsyncClock fps={self.get_fps():.1}>'

    def get_fps(self):
        """Returns average fps using count of all tick() calls and total time since start"""
        if self.time_passed != 0:
            return self.frames/self.time_passed
        return 0

    async def tick(self, framerate=60):
        """Update the clock"""
        dtime = time.time() - self.last_call_time
        
        time_to_sleep = 1/framerate - dtime
        
        self.last_call_time += dtime
        
        self.time_passed += dtime
        
        self.frames += 1
        
        if self.time_passed > 1:
            self.time_passed = 0
            self.frames = 0
        
        await asyncio.sleep(time_to_sleep)
        
        return dtime
