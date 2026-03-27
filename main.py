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
        "icon": "🪙",
        "color": "yellow"
    },
    {
        "name": "volcano",
        "spawns_on": ["mountain"],
        "icon": "🌋",
        "color": "red"
    }
]

def main():
    map = generate_map(16, 16, (15, 8), 12)

    print_map(map)

def generate_map(x: int, y: int, player_pos: tuple, num_coins):
    map = []

    for i in range(x):
        row = []
        for i in range(y):
            row.append(None)
        map.append(row)

    def set_terrain(x, y, tile):
        map[x][y] = tile.copy()

    def set_item(x, y, item):
        map[x][y]["item"] = item

    def set_item_color(x, y, color):
        map[x][y]["item_color"] = color

    # Capture content for display
    # content_buffer = StringIO()
    # old_stdout = sys.stdout
    # sys.stdout = content_buffer

    coins = []

    # generate and print a random map
    for i in range(x):
        for j in range(y):
            item_icon = " "
            icon_color = ""
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

            # Add items if player not here (excluding coins)
            if not player_here:
                # Add volcanoes
                if tile["type"] in items[1]["spawns_on"] and random.randint(0, 100) <= 15:
                    icon_color = items[1]["color"] # set foreground color to volcano color
                    item_icon = items[1]["icon"]
            # set terrain
            set_terrain(i, j, tile)

            # set item
            set_item(i, j, item_icon)
            set_item_color(i, j, icon_color)
            # end loop
        # end loop
    # Add coins
    # NOTE: If we add more items in the future, we will need to ensure that coins can't overwrite other items. We are safe for now since coins and volcanoes cannot spawn on the same tile types.
    for i in range(num_coins):
        pos = (random.randint(0, x - 1), random.randint(0, y - 1))
        while not (map[pos[0]][pos[1]]["item"] == " " or map[pos[0]][pos[1]]["type"] in items[0]["spawns_on"] or pos not in coins):
            pos = (random.randint(0, x - 1), random.randint(0, y - 1))

        coins.append(pos)
        set_item(pos[0], pos[1], items[0]["icon"])
        set_item_color(pos[0], pos[1], items[0]["color"])

    return map

    # content = content_buffer.getvalue()
    # sys.stdout = old_stdout
    #
    # return content


def print_map(map):
    for row in map:
        for tile in row:
            terrain_color = tile["color"]
            item_icon = tile["item"]

            # set terrain color
            set_background_color(terrain_color)
            # set icon color
            set_color(tile["item_color"])
            # print tile with terrain color and item icon
            print(item_icon if item_icon != " " else "  ", end="") # 2 spaces if no icon, else no spaces because emojis are 2 characters in length
            reset_color()
        print()


if __name__ == "__main__":
    main()