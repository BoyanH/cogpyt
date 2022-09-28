from typing import Tuple, List
from PIL import Image  # requires pillow
from IPython.display import display
import numpy as np  # requires numpy
import cogpyt


def show_image_from_destination(data: np.ndarray, width, height):
    display(get_image_from_destination(data, width, height))


def get_image_from_destination(data: np.ndarray, width, height):
    image_np = np.array(data, dtype=np.uint8).reshape(height, width)
    return Image.fromarray(image_np)


def get_lena() -> Tuple[List[int], int, int]:
    lena_rgb = Image.open('img/lena.jpg')
    lena_grayscale = lena_rgb.convert('L')
    return lena_grayscale


def pad_and_flatten_image(image: Image.Image, padding: Tuple):
    image_np = np.array(image)
    vertical_padding, horizontal_padding = padding
    image_padded = np.pad(
        image_np, (
            (vertical_padding, vertical_padding),
            (horizontal_padding, horizontal_padding)
        )
    )
    return image_padded.flatten()


def get_destination_for_image(image: Image.Image):
    width, height = image.size
    return [0] * (width * height)


def get_sobel() -> Tuple[List[int], int, int]:
    return np.array([
        [1, 0, -1],
        [2, 0, -2],
        [1, 0, -1]
    ])


def convolve_naive(source, destination, kernel, image_width, kernel_width):
    destination_size = len(destination)
    padded_image_width = image_width + (kernel_width - 1)

    for destination_index in range(destination_size):
        acc = 0

        for kernel_idx, kernel_center in enumerate(kernel):
            kernel_y = kernel_idx // kernel_width
            kernel_x = kernel_idx % kernel_width

            destination_y = destination_index // image_width
            destination_x = destination_index % image_width
            corresponding_index_in_source = destination_y * padded_image_width + destination_x
            source_index = corresponding_index_in_source + padded_image_width * kernel_y + kernel_x

            acc += source[source_index] * kernel_center

        destination[destination_index] = min(max(acc, 0), 255)


@cogpyt.GeneratedFunction
def convolve_cogpyt(
        generated_code_block: cogpyt.GeneratedCodeBlock,
        source, destination, kernel, image_width, kernel_width
):
    destination_size = len(destination)
    padded_image_width = image_width + (kernel_width - 1)

    with generated_code_block:
        for destination_index in range(destination_size):
            acc = 0

            destination_y = destination_index // image_width
            destination_x = destination_index % image_width
            corresponding_index_in_source = destination_y * padded_image_width + destination_x
    generated_code_block.indent()

    for kernel_idx, kernel_center in enumerate(kernel):
        kernel_y = kernel_idx // kernel_width
        kernel_x = kernel_idx % kernel_width
        if kernel_center == 0:
            continue

        kernel_offset = padded_image_width * kernel_y + kernel_x

        if kernel_center == 1:
            with generated_code_block:
                acc += source[corresponding_index_in_source + kernel_offset]
        elif kernel_center == -1:
            with generated_code_block:
                acc -= source[corresponding_index_in_source + kernel_offset]
        else:
            with generated_code_block:
                acc += source[corresponding_index_in_source + kernel_offset] * kernel_center

    with generated_code_block:
        destination[destination_index] = min(max(acc, 0), 255)
