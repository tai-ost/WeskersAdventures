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
    'walk through the door',  # 0 - door
    '  go up the stairs',     # 1 - stairs up
    ' go down the stairs'     # 2 - stairs down
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

# item_name, env_width, env_height, in_game_name
ITEM_TYPES = (
    None,
    ('first_aid_spray', 50, 80, 'First Aid Spray'),
    ('green_herb', 50, 50, 'Green Herb'),
    ('red_herb', 50, 50, 'Red Herb'),
    ('blue_herb', 50, 50, 'Blue Herb'),
    ('dagger', 50, 50, 'Dagger'),
    ('handgun_ammo', 50, 50, 'Handgun Ammo')
)
