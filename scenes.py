class SceneManager:
    def __init__(self):
        self.current = "start"

    def change(self, new_scene):
        self.current = new_scene

    def is_scene(self, scene):
        return self.current == scene