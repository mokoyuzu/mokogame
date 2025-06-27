import random

def get_enemy_type_by_stage(stage):
    if stage == 1:
        return "normal"
    elif stage == 2:
        return random.choice(["normal", "fast"])
    elif stage >= 3:
        return random.choice(["normal", "fast", "zig"])