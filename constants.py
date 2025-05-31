WIDTH = 1280
HEIGHT = 720
FPS = 60
FLOOR_HEIGHT = 70
ACTUAL_HEIGHT = HEIGHT - FLOOR_HEIGHT
GRAVITY_ACCELERATION = 9.8
INVENTORY_SLOT_WIDTH = INVENTORY_SLOT_HEIGHT = 80
ITEM_WIDTH = ITEM_HEIGHT = 54
DEFAULT_AMMO_LOADED = 15
DEFAULT_AMMO_STORED = 15

# (name, health, dmg, velocity, is_poisonous, width, height)
ENEMY_TYPES = (
    ('zombie', 5, 25, 2, False, 125, 250),             # 0
    ('cerberus', 3, 20, 5, False, 200, 100),           # 1
    ('adder', 1, 1, 5, True, 100, 20),                 # 2
    ('hunter', 6, 35, 2, False, 250, 250),             # 3
    ('lisa_trevor', 20, 35, 1, False, 200, 200)        # 4
)

# item_name, env_width, env_height, in_game_name
ITEM_TYPES = (
    None,
    ('first_aid_spray', 50, 80, 'First Aid Spray'),    # 1
    ('green_herb', 70, 100, 'Green Herb'),             # 2
    ('red_herb', 70, 100, 'Red Herb'),                 # 3
    ('blue_herb', 70, 100, 'Blue Herb'),               # 4
    ('dagger', 70, 20, 'Dagger'),                      # 5
    ('handgun_ammo', 50, 50, 'Handgun Ammo'),          # 6
    ('mixed_g_r', 50, 50, 'Mixed Herbs (G + R)'),      # 7
    ('mixed_g_b', 50, 50, 'Mixed Herbs (G + B)'),      # 8
    ('mixed_g_g', 50, 50, 'Mixed Herbs (G + G)'),      # 9
    ('mixed_all', 50, 50, 'Mixed Herbs (G + R + B)')   # 10
)
