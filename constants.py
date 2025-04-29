WIDTH = 1280
HEIGHT = 720
FPS = 60
FLOOR_HEIGHT = 70
ACTUAL_HEIGHT = HEIGHT - FLOOR_HEIGHT
GRAVITY_ACCELERATION = 9.8
INVENTORY_SLOT_WIDTH = INVENTORY_SLOT_HEIGHT = 80
ITEM_WIDTH = ITEM_HEIGHT = 54
DEFAULT_AMMO_LOADED = 15
DEFAULT_AMMO_STORED = 30
DOOR_TYPES = (
    'walk through the door',
    'go up the stairs',
    'go down the stairs'
)
# (name, health, dmg, velocity, is_poisonous, width, height)
ENEMY_TYPES = (
    ('zombie', 3, 25, 2, False, 100, 200),
    ('crimson_head', 3, 25, 3, False, 100, 200),
    ('cerberus', 2, 10, 5, False, 100, 50),
    ('adder', 1, 1, 5, True, 100, 20),
    ('hunter', 5, 40, 2, True, 200, 200),
    ('chimera', 2, 10, 5, False, 100, 200),
    ('lisa_trevor', 20, 20, 1, False, 150, 200)
)
