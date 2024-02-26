import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
def rgb_to_grayscale(rgb_image):
    # Convert RGB image to grayscale
    grayscale_image = rgb_image.convert('L')
    return grayscale_image

def load_image_to_numpy(file_path):
    # Open the image file
    image = Image.open(file_path)
    
    # Convert the image to grayscale
    grayscale_image = rgb_to_grayscale(image)
    
    # Convert grayscale image to numpy array
    grayscale_array = np.array(grayscale_image)
    
    # Apply threshold operation
    thresholded_array = np.where(grayscale_array > 0, 255, 0)
    
    return thresholded_array

# Replace 'image.png' with the path to your PNG image file
file_path = 'heart.png'

# Load image and convert it to numpy array
grayscale_array = load_image_to_numpy(file_path)

# Display the shape of the numpy array
plt.imshow(grayscale_array)
plt.show()

print(np.max(grayscale_array))
