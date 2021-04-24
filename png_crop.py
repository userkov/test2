from PIL import Image

def crop(location_table, size_table, location_group, size_group):
    png = Image.open("table.png")
    x = location_group["x"] - location_table["x"]
    y = 0
    width = size_group["width"]
    height = size_table["height"]
    print(x, y, width, height)
    png_ready = png.crop( (x, y, width + x, height))
    png_ready.save("group.png")