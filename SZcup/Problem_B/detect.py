import cv2
import numpy as np

# LSB analysis function
def lsb_analysis(image):
    # Get the size of the image
    height, width = image.shape

    # Initialize the count of LSBs
    lsbs = 0

    # Iterate over the image
    for i in range(height):
        for j in range(width):
            # Get the LSB of the pixel
            lsb = int(image[i, j]) & 1

            # If the LSB is 1, increment the count
            if lsb == 1:
                lsbs += 1

    # Calculate the ratio of LSBs to the total number of pixels
    ratio = lsbs / (height * width)

    return ratio

# SPA analysis function
def spa_analysis(image):
    # Get the size of the image
    height, width = image.shape

    # Initialize the count of LSB pairs
    lsb_pairs = 0

    # Iterate over the image
    for i in range(height):
        for j in range(width - 1):
            # Get the LSB of the current pixel and the next pixel
            lsb1 = int(image[i, j]) & 1
            lsb2 = int(image[i, j + 1]) & 1

            # If the LSBs are different, increment the count
            if lsb1 != lsb2:
                lsb_pairs += 1

    # Calculate the ratio of LSB pairs to the total number of pixels
    ratio = lsb_pairs / (height * width)

    return ratio

# RS analysis function
def rs_analysis(image):
    # Get the size of the image
    height, width = image.shape

    # Initialize the count of regular and singular groups
    regular_groups = 0
    singular_groups = 0

    # Iterate over the image
    for i in range(height):
        for j in range(width - 1):
            # Get the current pixel and the next pixel
            pixel1 = int(image[i, j])
            pixel2 = int(image[i, j + 1])

            # If the pixels are in the same group, increment the count
            if (pixel1 % 2 == 0 and pixel2 % 2 == 0) or (pixel1 % 2 == 1 and pixel2 % 2 == 1):
                regular_groups += 1
            else:
                singular_groups += 1

    # Calculate the ratio of singular groups to the total number of groups
    ratio = singular_groups / (regular_groups + singular_groups)

    return ratio

# Load the image
image = cv2.imread('SPP.PNG', cv2.IMREAD_GRAYSCALE)

# Perform the analyses
lsb_ratio = lsb_analysis(image)
spa_ratio = spa_analysis(image)
rs_ratio = rs_analysis(image)

# Print the results
print('LSB ratio:', lsb_ratio)
print('SPA ratio:', spa_ratio)
print('RS ratio:', rs_ratio)
