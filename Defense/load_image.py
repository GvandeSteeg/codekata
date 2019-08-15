import constants

from PIL import Image, ImageDraw

land_color = dict(F=(37, 93, 22), W=(18, 65, 142), M=(71, 71, 71), G=(158, 182, 93), V=(145, 27, 17))


def get_initial_map() -> Image:
    mode = 'RGB'
    size = (50, 50)
    color = 'black'
    img = Image.new(mode, size, color)
    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i, j] = land_color[constants.land[j][i]]

    return img


def find_village(img):
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if constants.land[j][i] == 'V':
                return j, i


def draw_square_on_village(img: Image, length: int):
    j, i = find_village(img)

    x0, y0, x1, y1 = j - length / 2, i - length / 2, j + length / 2, i + length / 2
    ImageDraw.Draw(img).rectangle([x0, y0, x1, y1], outline='red', width=1)
    return img


if __name__ == '__main__':
    i = get_initial_map()
    i = draw_square_on_village(i, 14)
    i.show()
