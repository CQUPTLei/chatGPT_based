import cv2
from PIL import Image
import numpy as np


def find_best_scale(original_image_path, scaled_image_path):
    # Load the images
    original_image = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)
    scaled_image = cv2.imread(scaled_image_path, cv2.IMREAD_GRAYSCALE)

    # Initialize the best scale and the best match value
    best_scale = 1.0
    best_match = 0.0

    # Try different scales
    for scale in np.linspace(0.1, 3.0, 100):
        # Resize the scaled image
        resized_image = cv2.resize(scaled_image, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

        # Compute the template matching
        result = cv2.matchTemplate(original_image, resized_image, cv2.TM_CCORR_NORMED)
        _, match, _, _ = cv2.minMaxLoc(result)

        # Update the best scale and the best match value
        if match > best_match:
            best_scale = scale
            best_match = match

    return best_scale


scale = find_best_scale('B.jpg', 'ss.jpg')
print('Best scale:', scale)

# Load the image
img = cv2.imread('ss.jpg')

# Calculate the new size of the image
new_size = (int(img.shape[1] * scale), int(img.shape[0] * scale))

# Resize the image
resized_img = cv2.resize(img, new_size)

# Load the original image
original_img = cv2.imread('B.jpg')

# Resize the image to match the original image size
resized_img = cv2.resize(resized_img, (original_img.shape[1], original_img.shape[0]), interpolation=cv2.INTER_CUBIC)

cv2.imwrite('sss.jpg', resized_img)
# Display the image
# cv2.imshow('d', resized_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
