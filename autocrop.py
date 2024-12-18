from PIL import Image
import numpy as np


def mode(a):
    u, c = np.unique(a, return_counts=True)
    return u[c.argmax()]


def detect_boundaries(image, axis):
    modes = np.apply_along_axis(mode, axis, image)
    previous_pixel = modes[0]
    boundaries = []
    for i, current_pixel in enumerate(modes):
        if previous_pixel != current_pixel:
            boundaries.append(i)
            previous_pixel = current_pixel

    return [0] + boundaries + [len(modes)]


def get_biggest_boundaries(boundaries, n_cells):
    start = [x for _, x in sorted(zip(np.diff(boundaries), boundaries), reverse=True)]
    end = [x for _, x in sorted(zip(np.diff(boundaries), boundaries[1:]), reverse=True)]
    return [(start, end) for start, end in zip(start[:n_cells], end[:n_cells])]


pil_image = Image.open("temp.png").convert("L")
image = np.asarray(pil_image)
row_boundaries = detect_boundaries(image, 1)
biggest_rows = get_biggest_boundaries(row_boundaries, 5)
print("Monday to Friday:", sorted(biggest_rows))
weekday_crops = [
    pil_image.crop((0, upper, image.shape[1], lower))
    for (upper, lower) in sorted(biggest_rows)
]

pil_image = weekday_crops[0]
image = np.asarray(pil_image)
col_boundaries = detect_boundaries(image, 0)
biggest_cells = get_biggest_boundaries(col_boundaries, 4)
print("Left to Right:", sorted(biggest_cells))

for i, (left, right) in enumerate(sorted(biggest_cells)):
    col_image = pil_image.crop((left, 0, right, image.shape[0]))
    col_image.save(f"col_{i}.png")
