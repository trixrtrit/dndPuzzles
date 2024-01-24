from PIL import Image


def process_image(image_path, grid_size=(3, 3), tile_size=(100, 100)):
    im = Image.open(image_path)
    image_width, image_height = im.size

    tile_width = (image_width // grid_size[0])
    tile_height = (image_height // grid_size[1])

    tiles = []

    for row in range(grid_size[0]):
        for col in range(grid_size[1]):
            left = col * tile_width
            upper = row * tile_height
            right = left + tile_width
            lower = upper + tile_height

            tile = im.crop((left, upper, right, lower))
            tiles.append(tile)

    resized_tiles = []
    for tile in tiles:
        resized_tile = tile.resize(tile_size)
        resized_tiles.append(resized_tile)
    return resized_tiles
