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

# (name, health, dmg, velocity, is_poisonous, width, height)
ENEMY_TYPES = (
    ('zombie', 3, 25, 2, False, 100, 200),
    ('crimson_head', 3, 25, 3, False, 100, 200),
    ('cerberus', 2, 10, 5, False, 100, 50),
    ('adder', 1, 1, 5, True, 100, 20),
    ('hunter', 5, 40, 2, True, 200, 200),
    ('chimera', 2, 10, 5, False, 100, 200),
    ('lisa_trevor', 20, 40, 1, False, 200, 200)
)

# item_name, env_width, env_height, in_game_name
ITEM_TYPES = (
    None,
    ('first_aid_spray', 50, 80, 'First Aid Spray'),    # 1
    ('green_herb', 70, 100, 'Green Herb'),              # 2
    ('red_herb', 70, 100, 'Red Herb'),                  # 3
    ('blue_herb', 70, 100, 'Blue Herb'),                # 4
    ('dagger', 50, 50, 'Dagger'),                      # 5
    ('handgun_ammo', 50, 50, 'Handgun Ammo'),          # 6
    ('mixed_g_r', 50, 50, 'Mixed Herbs (G + R)'),      # 7
    ('mixed_g_b', 50, 50, 'Mixed Herbs (G + B)'),      # 8
    ('mixed_g_g', 50, 50, 'Mixed Herbs (G + G)'),      # 9
    ('mixed_all', 50, 50, 'Mixed Herbs (G + R + B)')   # 10
)
