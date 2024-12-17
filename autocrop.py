from PIL import Image
import numpy as np


def mode(a):
    u, c = np.unique(a, return_counts=True)
    return u[c.argmax()]


def detect_row_boundaries(image):
    modes = np.apply_along_axis(mode, 1, image)
    previous_pixel = modes[0]
    row_boundaries = []
    for y, current_pixel in enumerate(modes):
        if previous_pixel != current_pixel:
            row_boundaries.append(y)
            previous_pixel = current_pixel

    return row_boundaries


image = Image.open("temp.png")
gray_image = image.convert("L")
np_image = np.asarray(gray_image)

row_boundaries = detect_row_boundaries(np_image)
row_boundaries += [image.height]
upper_boundaries = [
    x for _, x in sorted(zip(np.diff(row_boundaries), row_boundaries), reverse=True)
]
lower_boundaries = [
    x for _, x in sorted(zip(np.diff(row_boundaries), row_boundaries[1:]), reverse=True)
]

print("Monday to Friday:", sorted(zip(upper_boundaries[:5], lower_boundaries[:5])))

for i, (upper, lower) in enumerate(
    sorted(zip(upper_boundaries[:5], lower_boundaries[:5]))
):
    row_image = image.crop((0, upper, image.width, lower))
    row_image.save(f"row_{i}.png")
