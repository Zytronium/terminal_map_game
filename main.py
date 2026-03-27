import random
import sys
from io import StringIO

from colors import set_background_color, reset_color, set_color

tiles = [
    {
        "type": "grassland",
        "movement_cost": 1,
        "color": "green",
        "chance": 6/10
    },
    # {
    #     "type": "hills",
    #     "movement_cost": 2,
    #     "color": "brown"
    # },
    {
        "type": "mountain",
        "movement_cost": 10,
        "color": "dark gray",
        "chance": 1/10
    },
    {
        "type": "water",
        "movement_cost": 3,
        "color": "blue",
        "chance": 3/10
    },
]

items = [
    {
        "name": "coin",
        "spawns_on": ["grassland", "water"],
        "collectable": True,
        "icon": "🪙",
        "color": "yellow"
    },
    {
        "name": "volcano",
        "spawns_on": ["mountain"],
        "collectable": False,
        "icon": "🌋",
        "color": "red"
    }
]

def main():
    map = generate_map(16, 16, (15, 8), 12)

def generate_map(x: int, y: int, player_pos: tuple, num_coins):
    # Capture content for display
    # content_buffer = StringIO()
    # old_stdout = sys.stdout
    # sys.stdout = content_buffer

    coins = []

    for i in range(num_coins):
        coins.append((random.randint(0, x - 1), random.randint(0, y - 1)))

    # generate and print a random map
    for i in range(x):
        for j in range(y):
            item_icon = " "
            player_here = False
            if (i, j) == player_pos:
                player_here = True
                item_icon = "⭐"

            tile_pool = []

            for t in tiles:
                num = int(t["chance"] * 10)
                for _ in range(num):
                    tile_pool.append(t)
            tile = tile_pool[random.randint(0, len(tile_pool) - 1)]

            # If player starts here, don't generate mountain here
            while player_here and tile["type"] == "mountain":
                tile = tile_pool[random.randint(0, len(tile_pool) - 1)]

            color = tile["color"]
            if not player_here:
                if len(coins) < num_coins and tile["type"] in items[0]["spawns_on"] and random.randint(0, 100) <= 10:
                    set_color(items[0]["color"])
                    item_icon = items[0]["icon"]
                    coins.append((i, j))
                elif tile["type"] in items[1]["spawns_on"] and random.randint(0, 100) <= 15:
                    set_color(items[1]["color"])
                    item_icon = items[1]["icon"]
            set_background_color(color)
            print(item_icon if item_icon != " " else "  ", end="")
            reset_color()
        print()

    # content = content_buffer.getvalue()
    # sys.stdout = old_stdout
    #
    # return content

if __name__ == "__main__":
    main()