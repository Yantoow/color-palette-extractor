"""
Author:     Yanto Christoffel
Project:    Color Palette Generator

Generates a color palette from an input image.
(img = PIL.Image.open("example.png"))
The user can:
    - provide an input image of any format
    - adjust the color palette length
    - change the degree to which colors in the palette match
"""


import numpy as np
import colorsys


def filter_colors(top_colors, k, tol):
    """Makes sure the top colors don't match too much."""
    palette = []

    for col in top_colors:
        # Disregard the alpha value in rgba
        col = col[:3]

        clashes_with_palette = False

        # Check if the new color doesn't match
        # too much with the current palette
        for c in palette:
            diff = np.sum(np.abs(col - np.array(c)))

            if diff < tol:
                clashes_with_palette = True
                break

        # Only add non-duplicates to the palette
        if not(clashes_with_palette):
            palette.append(col)

        if len(palette) == k:
            return palette, True


    return palette, False


def get_palette(img, k, tol=50):
    """Constructs a palette of the top k colors from an image."""
    print(f"{img.size}, {img.format}")

    # Scale images down based on their size for computational efficiency
    w_scale_factor = img.size[0]//1000 + 1
    h_scale_factor = img.size[1]//1000 + 1

    # Use double colons to use the scaling factors as the step size
    img = np.asarray(img)[::w_scale_factor, ::h_scale_factor]

    # Flatten the first two dimensions of the image (width and height)
    # Now it's just a list of RGB(A) values
    img = img.reshape(-1, img.shape[-1])

    # Get the unique colors and their counts
    unique, counts = np.unique(img, axis=0, return_counts=True)

    # Get the top colors by sorting by the counts
    idxs = np.argsort(-counts, axis=-1)
    top_colors = np.column_stack((unique, counts))[idxs]

    return filter_colors(top_colors, k, tol)


def sort_palette_by_hue(palette):
    """Sorts a palette by hue values."""
    hls = [colorsys.rgb_to_hls(*rgb / float(255)) for rgb in palette]
    indices_sorted = np.argsort(hls, axis=0)[:, 0]
    return [palette[i] for i in indices_sorted]
