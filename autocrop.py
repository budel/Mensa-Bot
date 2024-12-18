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

    return boundaries


pil_image = Image.open("temp.png").convert("L")
image = np.asarray(Image.open("temp.png").convert("L"))

row_boundaries = detect_boundaries(image, 1)
row_boundaries = [0] + row_boundaries
row_boundaries += [image.shape[0]]
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
    row_image = pil_image.crop((0, upper, image.shape[1], lower))
    row_image.save(f"row_{i}.png")

n_cells = 4
pil_image = Image.open("row_0.png")
image = np.asarray(Image.open("row_0.png"))
col_boundaries = detect_boundaries(image, 0)
col_boundaries = [0] + col_boundaries
col_boundaries += [image.shape[1]]
print(f"{col_boundaries=}")
print(f"{np.diff(col_boundaries)=}")
left_boundaries = [
    x for _, x in sorted(zip(np.diff(col_boundaries), col_boundaries), reverse=True)
]
right_boundaries = [
    x for _, x in sorted(zip(np.diff(col_boundaries), col_boundaries[1:]), reverse=True)
]
print(
    "Left to Right:", sorted(zip(left_boundaries[:n_cells], right_boundaries[:n_cells]))
)

for i, (left, right) in enumerate(
    sorted(zip(left_boundaries[:n_cells], right_boundaries[:n_cells]))
):
    # (left upper right lower)
    col_image = pil_image.crop((left, 0, right, image.shape[0]))
    col_image.save(f"col_{i}.png")
