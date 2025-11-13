from app import config

class DotState:
    def __init__(self):
        self.x = config.WIDTH // 2
        self.y = config.HEIGHT // 2
        self.color = config.DOT_COLOR
        self.radius = config.DOT_RADIUS_START
    
class AppState:
    def __init__(self):
        self.running = True
        self.clock = None
        self.surface = None
        self.dot = DotState()