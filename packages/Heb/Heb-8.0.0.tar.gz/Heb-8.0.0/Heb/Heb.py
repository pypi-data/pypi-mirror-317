class Heb:
    def p1(self):
        print('''
        1> Read an image using OpenCV and PIL. 

import cv2  # Importing the OpenCV library for image processing
from PIL import Image  # Importing the Image module from the PIL (Pillow) library for handling images
import numpy as np  # Importing NumPy, which is often used for handling image arrays and numerical operations

# Read an image using OpenCV
img_cv = cv2.imread('image1.tif')  # Use OpenCV's imread function to read the image from the file 'image1.tif'
# This returns the image as a NumPy array. If the image cannot be read, it will return None.

cv2.imshow('OpenCV Image', img_cv)  # Display the image using OpenCV's imshow function in a window titled 'OpenCV Image'
# The imshow function requires a window title and the image array to display.

cv2.waitKey(0)  # Wait indefinitely for any key press to proceed
# Without this line, the window may close immediately, so this ensures the image remains on screen until a key is pressed.

cv2.destroyAllWindows()  # Close all OpenCV windows
# This releases the resources used for displaying the window and ensures no window remains open after the key press.

# Read an image using PIL (Python Imaging Library)
img_pil = Image.open('image1.tif')  # Open the image using PIL's Image.open function
# This returns an Image object that can be used for various image manipulations.

img_pil.show()  # Display the image using the default image viewer of the operating system
# The show method opens the image in an external viewer, unlike OpenCV, which opens its own window.


2> Resize the image to different dimensions.

def resize_image(img_cv, img_pil, width, height):
    # Resize the OpenCV image using the cv2.resize function
    # Parameters: the original image (img_cv) and the desired size (width, height)
    resized_cv = cv2.resize(img_cv, (width, height))
    
    # Resize the PIL image using the resize method from PIL.Image
    # Parameters: the original image (img_pil) and the desired size (width, height)
    resized_pil = img_pil.resize((width, height))
    
    # Return the resized images for both OpenCV and PIL
    return resized_cv, resized_pil

# Set desired width and height for resizing
width, height = 200, 200

# Call the resize_image function with the OpenCV and PIL images and desired dimensions
# This function returns the resized OpenCV image (resized_cv) and the resized PIL image (resized_pil)
resized_cv, resized_pil = resize_image(img_cv, img_pil, width, height)

# Display the resized OpenCV image in a window titled 'Resized Image - OpenCV'
cv2.imshow('Resized Image - OpenCV', resized_cv)

# Display the resized PIL image using the default image viewer of the operating system
resized_pil.show()

# Wait indefinitely for a key press to close the OpenCV window
cv2.waitKey(0)

# Close all OpenCV windows after a key is pressed
cv2.destroyAllWindows()


3> Crop a specific region from the image. 

def crop_image(img_cv, img_pil, left, top, right, bottom):
    # Crop the OpenCV image using array slicing
    # Slicing format: img[y1:y2, x1:x2], where top-left is (left, top) and bottom-right is (right, bottom)
    cropped_cv = img_cv[top:bottom, left:right]
    
    # Crop the PIL image using the crop() method
    # The crop method takes a tuple (left, top, right, bottom), defining the box to be cropped
    cropped_pil = img_pil.crop((left, top, right, bottom))
    
    # Return both the cropped OpenCV and PIL images
    return cropped_cv, cropped_pil

# Set coordinates for the top-left (left, top) and bottom-right (right, bottom) corners of the crop box
left, top, right, bottom = 50, 50, 300, 300

# Call the crop_image function with the OpenCV and PIL images and the cropping coordinates
# The function returns the cropped images for both OpenCV and PIL
cropped_cv, cropped_pil = crop_image(img_cv, img_pil, left, top, right, bottom)

# Display the cropped OpenCV image in a window titled 'Cropped Image - OpenCV'
cv2.imshow('Cropped Image - OpenCV', cropped_cv)

# Display the cropped PIL image using the default image viewer of the operating system
cropped_pil.show()

# Wait indefinitely for a key press to close the OpenCV window
cv2.waitKey(0)

# Close all OpenCV windows after a key press
cv2.destroyAllWindows()
--------------------------------------------------------------

4> Rotate the image by a certain angle. 

def rotate_image(img_cv, img_pil, angle):
    # Get the height and width of the OpenCV image (img_cv)
    (h, w) = img_cv.shape[:2]
    
    # Calculate the center of the image for rotation
    center = (w / 2, h / 2)
    
    # Create a rotation matrix for the given angle using OpenCV's getRotationMatrix2D
    # The last parameter '1.0' is the scaling factor (1.0 means no scaling)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Rotate the image using OpenCV's warpAffine function, passing the image, 
    # rotation matrix, and output size (width, height)
    rotated_cv = cv2.warpAffine(img_cv, M, (w, h))
    
    # Rotate the PIL image (img_pil) using its built-in rotate method
    rotated_pil = img_pil.rotate(angle)
    
    # Return both the rotated OpenCV image and rotated PIL image
    return rotated_cv, rotated_pil

# Define the angle of rotation
angle = 45

# Rotate both the OpenCV and PIL images by the specified angle
rotated_cv, rotated_pil = rotate_image(img_cv, img_pil, angle)

# Display the rotated OpenCV image in a window
cv2.imshow('Rotated Image - OpenCV', rotated_cv)

# Display the rotated PIL image using its show method (opens a window with the image)
rotated_pil.show()

# Wait for any key press to close the OpenCV window
cv2.waitKey(0)

# Close all OpenCV windows after the key press
cv2.destroyAllWindows()


5> Zoom into the image by a certain factor

def zoom_image(img_cv, img_pil, zoom_factor):
    # Get the height and width of the OpenCV image (img_cv)
    (h, w) = img_cv.shape[:2]
    
    # Zoom the OpenCV image using the resize function. The 'fx' and 'fy' parameters
    # specify the scale factor for width and height respectively (both set to zoom_factor)
    zoomed_cv = cv2.resize(img_cv, None, fx=zoom_factor, fy=zoom_factor)
    
    # Zoom the PIL image by resizing it to the new dimensions
    # Multiply the width and height by the zoom_factor and convert them to integers
    zoomed_pil = img_pil.resize((int(w * zoom_factor), int(h * zoom_factor)))
    
    # Return both the zoomed OpenCV image and zoomed PIL image
    return zoomed_cv, zoomed_pil

# Define the zoom factor (1.5 means the image will be zoomed to 150% of the original size)
zoom_factor = 1.5

# Zoom both the OpenCV and PIL images by the specified zoom factor
zoomed_cv, zoomed_pil = zoom_image(img_cv, img_pil, zoom_factor)

# Display the zoomed OpenCV image in a window
cv2.imshow('Zoomed Image - OpenCV', zoomed_cv)

# Display the zoomed PIL image using its show method (opens a window with the image)
zoomed_pil.show()

# Wait for any key press to close the OpenCV window
cv2.waitKey(0)

# Close all OpenCV windows after the key press
cv2.destroyAllWindows()

6> Shrink the image by a certain factor:

def shrink_image(img_cv, img_pil, shrink_factor):
    # Get the height and width of the OpenCV image (img_cv)
    (h, w) = img_cv.shape[:2]
    
    # Shrink the OpenCV image by resizing it using the specified shrink factor.
    # The 'fx' and 'fy' parameters define the scale for the width and height respectively.
    # Since we are shrinking, the shrink_factor will be less than 1 (e.g., 0.5 for 50% size).
    shrunk_cv = cv2.resize(img_cv, None, fx=shrink_factor, fy=shrink_factor)
    
    # Shrink the PIL image by resizing it to the new dimensions.
    # Multiply the original width and height by the shrink_factor and convert them to integers.
    shrunk_pil = img_pil.resize((int(w * shrink_factor), int(h * shrink_factor)))
    
    # Return both the shrunk OpenCV image and the shrunk PIL image.
    return shrunk_cv, shrunk_pil

# Define the shrink factor (0.5 means the image will be shrunk to 50% of its original size).
shrink_factor = 0.5

# Shrink both the OpenCV and PIL images using the specified shrink factor.
shrunk_cv, shrunk_pil = shrink_image(img_cv, img_pil, shrink_factor)

# Display the shrunk OpenCV image in a window.
cv2.imshow('Shrunk Image - OpenCV', shrunk_cv)

# Display the shrunk PIL image using its built-in show method (opens a window with the image).
shrunk_pil.show()

# Wait for any key press to close the OpenCV window.
cv2.waitKey(0)

# Close all OpenCV windows after a key press.
cv2.destroyAllWindows()



 7> Flip the image horizontally and vertically.

def flip_image(img_cv, img_pil, flip_code):
    # Flip the OpenCV image using cv2.flip() function
    # flip_code: 0 = flip vertically, 1 = flip horizontally, -1 = flip both vertically and horizontally
    flipped_cv = cv2.flip(img_cv, flip_code)
    
    # Check the flip_code to determine how to flip the PIL image
    if flip_code == 0:
        # If flip_code is 0, flip the PIL image vertically (top-to-bottom)
        flipped_pil = img_pil.transpose(Image.FLIP_TOP_BOTTOM)
    elif flip_code == 1:
        # If flip_code is 1, flip the PIL image horizontally (left-to-right)
        flipped_pil = img_pil.transpose(Image.FLIP_LEFT_RIGHT)
    else:
        # If flip_code is -1 or anything else, rotate the image 180 degrees (equivalent to flipping both horizontally and vertically)
        flipped_pil = img_pil.transpose(Image.ROTATE_180)
    
    # Return both the flipped OpenCV and PIL images
    return flipped_cv, flipped_pil

# Flip the images horizontally by passing flip_code = 1 (horizontal flip)
flipped_hor_cv, flipped_hor_pil = flip_image(img_cv, img_pil, 1)

# Display the horizontally flipped OpenCV image in a window titled 'Flipped Horizontally - OpenCV'
cv2.imshow('Flipped Horizontally - OpenCV', flipped_hor_cv)

# Display the horizontally flipped PIL image using the default system image viewer
flipped_hor_pil.show()

# Flip the images vertically by passing flip_code = 0 (vertical flip)
flipped_ver_cv, flipped_ver_pil = flip_image(img_cv, img_pil, 0)

# Display the vertically flipped OpenCV image in a window titled 'Flipped Vertically - OpenCV'
cv2.imshow('Flipped Vertically - OpenCV', flipped_ver_cv)

# Display the vertically flipped PIL image using the default system image viewer
flipped_ver_pil.show()

# Wait indefinitely for a key press to keep both OpenCV windows open
cv2.waitKey(0)

# Close all OpenCV windows after a key press
cv2.destroyAllWindows()


''')
    def p2(self):
        print('''
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read the image
image_path = 'images/image2.tif'
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Read the image in grayscale

if img is None:
    print("Error: Could not read the image.")
else:
    # Compute the histogram of the original image
    hist_orig = cv2.calcHist([img], [0], None, [256], [0, 256])

    # Apply histogram equalization
    img_equalized = cv2.equalizeHist(img)

    # Compute the histogram of the equalized image
    hist_equalized = cv2.calcHist([img_equalized], [0], None, [256], [0, 256])

    # Plot the original and equalized images
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.plot(hist_orig)
    plt.title('Histogram of Original Image')

    plt.subplot(2, 2, 3)
    plt.imshow(img_equalized, cmap='gray')
    plt.title('Equalized Image')
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.plot(hist_equalized)
    plt.title('Histogram of Equalized Image')

    plt.tight_layout()
    plt.show()

    # Display the original and equalized images using OpenCV
    cv2.imshow('Original Image', img)
    cv2.imshow('Equalized Image', img_equalized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


''')
    def p3(self):
        print('''
# Averaging smoothing filter
    import cv2
import matplotlib.pyplot as plt

# Read the image (color image)
image_path = 'images/image3.tif'
img = cv2.imread(image_path)

if img is None:
    print("Error: Could not read the image.")
else:
    # Apply Averaging Smoothing Filter
    avg_kernel = (5, 5)
    img_avg = cv2.blur(img, avg_kernel)

    # Display the original and smoothed images
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(img_avg, cv2.COLOR_BGR2RGB))
    plt.title('Averaging Smoothing')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # Show the images using OpenCV
    cv2.imshow('Original Image', img)
    cv2.imshow('Averaging Smoothing', img_avg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
              

#Apply gaussian smoothing filter
              import cv2
import matplotlib.pyplot as plt

# Read the image (color image)
image_path = 'images/image3-1.jpg'
img = cv2.imread(image_path)

if img is None:
    print("Error: Could not read the image.")
else:
    # Apply Gaussian Smoothing Filter
    gauss_kernel = (5, 5)
    sigma = 1.0
    img_gauss = cv2.GaussianBlur(img, gauss_kernel, sigma)

    # Display the original and smoothed images
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(img_gauss, cv2.COLOR_BGR2RGB))
    plt.title('Gaussian Smoothing')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # Show the images using OpenCV
    cv2.imshow('Original Image', img)
    cv2.imshow('Gaussian Smoothing', img_gauss)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
              
Apply sharpening filter using kernel
              
    import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read the image (color image)
image_path = 'images/image1.tif'
img = cv2.imread(image_path)

if img is None:
    print("Error: Could not read the image.")
else:
    # Apply Sharpening Filter Using Kernels
    kernel_sharpen = np.array([
        [-1, -1, -1],
        [-1,  9, -1],
        [-1, -1, -1]
    ])
    img_sharpen = cv2.filter2D(img, -1, kernel_sharpen)

    # Display the original and sharpened images
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(img_sharpen, cv2.COLOR_BGR2RGB))
    plt.title('Sharpened Image')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # Show the images using OpenCV
    cv2.imshow('Original Image', img)
    cv2.imshow('Sharpened Image', img_sharpen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




''')
    def p4(self):
        print('''
Add noise to an image 
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read the image
image_path = 'images/image4.tif'
img = cv2.imread(image_path)

if img is None:
    print("Error: Could not read the image.")
else:
    # Convert to grayscale if needed
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Add Gaussian noise
    noise_sigma = 25  # Standard deviation of noise
    noise = np.random.normal(0, noise_sigma, img_gray.shape).astype(np.uint8)
    img_noisy = cv2.add(img_gray, noise)

    # Save the noisy image
    noisy_image_path = 'images/noisy_image.jpg'
    cv2.imwrite(noisy_image_path, img_noisy)

    # Display the original and noisy images
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(img_gray, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(img_noisy, cmap='gray')
    plt.title('Noisy Image')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    print(f"Noisy image saved at: {noisy_image_path}")

# Apply spatial filtering to reduce noise
              import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read the noisy image
image_path = 'images/noisy_image.jpg'
img = cv2.imread(image_path)
img_noisy = cv2.add(img, np.random.normal(0, 25, img.shape).astype(np.uint8))

if img_noisy is None:
    print("Error: Could not read the noisy image.")
else:
    # Apply Gaussian Blur
    img_gaussian_blur = cv2.GaussianBlur(img_noisy, (5, 5), 0)
    
    # Apply Median Filtering
    img_median_blur = cv2.medianBlur(img_noisy, 5)

    # Display the noisy and filtered images
    plt.figure(figsize=(18, 6))
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(img_noisy, cv2.COLOR_BGR2RGB))
    plt.title('Noisy Image')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(cv2.cvtColor(img_gaussian_blur, cv2.COLOR_BGR2RGB))
    plt.title('Gaussian Blur')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(img_median_blur, cv2.COLOR_BGR2RGB))
    plt.title('Median Filter')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # Show the images using OpenCV
    cv2.imshow('Noisy Image', img_noisy)
    cv2.imshow('Gaussian Blur', img_gaussian_blur)
    cv2.imshow('Median Filter', img_median_blur)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
# Apply frequency domain filtering to reduce noise
              
              import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read the noisy grayscale image
image_path = 'images/noisy_image.jpg'
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
img_noisy = cv2.add(img, np.random.normal(0, 25, img.shape).astype(np.uint8))

if img_noisy is None:
    print("Error: Could not read the noisy image.")
else:
    # Perform Fourier Transform
    dft = cv2.dft(np.float32(img_noisy), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    # Create a mask with a circular high-pass filter
    rows, cols = img_noisy.shape
    crow, ccol = rows // 2, cols // 2
    radius = 30
    mask = np.ones((rows, cols, 2), np.uint8)
    center = [crow, ccol]
    cv2.circle(mask, center, radius, 0, thickness=-1)

    # Apply mask and inverse DFT
    fshift = dft_shift * mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])
    img_back = np.uint8(img_back)

    # Display the noisy and filtered images
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(img_noisy, cmap='gray')
    plt.title('Noisy Image')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(img_back, cmap='gray')
    plt.title('Frequency Domain Filtered Image')
    plt.axis('off')

    plt.tight_layout()
    plt.show()



''')
    def p5(self):
        print('''
# Apply edge detection using Canny
              import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read the image
image_path = 'images/image5.tif'
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    print("Error: Could not read the image.")
else:
    # Apply Canny Edge Detection
    edges = cv2.Canny(img, 100, 200)

    # Display the result
    plt.figure(figsize=(6, 6))
    plt.imshow(edges, cmap='gray')
    plt.title('Canny Edge Detection')
    plt.axis('off')
    plt.show()

    # Save the result
    cv2.imwrite('images/canny_edges.jpg', edges)
# Perform global and adaptive thresholding
              
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read the image
image_path = 'images/image5.tif'
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    print("Error: Could not read the image.")
else:
    # Global Thresholding
    _, global_thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Adaptive Thresholding
    adaptive_thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 11, 2)

    # Display the results
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(global_thresh, cmap='gray')
    plt.title('Global Thresholding')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(adaptive_thresh, cmap='gray')
    plt.title('Adaptive Thresholding')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # Save the results
    cv2.imwrite('images/global_thresh.jpg', global_thresh)
    cv2.imwrite('images/adaptive_thresh.jpg', adaptive_thresh)



''')
    def p6(self):
        print('''
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load a binary image (ensure the image is in binary format, or convert it)
image = cv2.imread('images/image6-1.png', 0)  # 0 loads the image in grayscale

# Create structuring elements
kernel = np.ones((5,5), np.uint8)  # You can change the size and shape

# 1. Apply Erosion to a Binary Image
erosion = cv2.erode(image, kernel, iterations=1)

# 2. Apply Dilation to a Binary Image
dilation = cv2.dilate(image, kernel, iterations=1)

# 3. Apply Opening Operation (Erosion followed by Dilation)
opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

# 4. Apply Closing Operation (Dilation followed by Erosion)
closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

# 5. Implement Morphological Gradient (Dilation minus Erosion)
gradient = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)

# Plot all the transformations for comparison
plt.figure(figsize=(10, 10))

plt.subplot(2, 3, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(2, 3, 2)
plt.imshow(erosion, cmap='gray')
plt.title('Erosion')
plt.axis('off')

plt.subplot(2, 3, 3)
plt.imshow(dilation, cmap='gray')
plt.title('Dilation')
plt.axis('off')

plt.subplot(2, 3, 4)
plt.imshow(opening, cmap='gray')
plt.title('Opening')
plt.axis('off')

plt.subplot(2, 3, 5)
plt.imshow(closing, cmap='gray')
plt.title('Closing')
plt.axis('off')

plt.subplot(2, 3, 6)
plt.imshow(gradient, cmap='gray')
plt.title('Morphological Gradient')
plt.axis('off')

plt.show()

# To compare effects of different structuring elements, you can modify the kernel and repeat the above operations.
# Example: Try a different shape or size of the structuring element
kernel_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
dilation_cross = cv2.dilate(image, kernel_cross, iterations=1)

# Display result of dilation with different structuring element
plt.imshow(dilation_cross, cmap='gray')
plt.title('Dilation with Cross-shaped Kernel')
plt.axis('off')
plt.show()



''')
    def p7(self):
        print('''
import cv2
import numpy as np
import heapq
import os
from collections import defaultdict
from PIL import Image
import matplotlib.pyplot as plt


# ------------------------------------------------------
# Huffman Coding Implementation (Lossless Compression)
# ------------------------------------------------------

class Node:
    def __init__(self, value, frequency):
        self.value = value
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def build_huffman_tree(data):
    heap = [Node(value, freq) for value, freq in data.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.frequency + right.frequency)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def generate_huffman_codes(node, current_code="", codes={}):
    if node is not None:
        if node.value is not None:
            codes[node.value] = current_code
        generate_huffman_codes(node.left, current_code + "0", codes)
        generate_huffman_codes(node.right, current_code + "1", codes)
    return codes

def huffman_compress(image):
    # Convert the image to grayscale and flatten it
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    flat_image = gray_image.flatten()

    # Count frequency of each pixel value
    frequency = defaultdict(int)
    for pixel in flat_image:
        frequency[pixel] += 1

    # Build Huffman Tree and generate codes
    huffman_tree = build_huffman_tree(frequency)
    codes = generate_huffman_codes(huffman_tree)

    # Compress the image using the Huffman codes
    compressed = "".join(codes[pixel] for pixel in flat_image)
    return compressed, codes, gray_image

# ------------------------------------------------------
# Run-Length Encoding Implementation (Lossless Compression)
# ------------------------------------------------------

def run_length_encode(image):
    # Convert the image to grayscale and flatten it
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    flat_image = gray_image.flatten()

    # Run-Length Encoding
    encoding = []
    prev_pixel = flat_image[0]
    count = 1
    for pixel in flat_image[1:]:
        if pixel == prev_pixel:
            count += 1
        else:
            encoding.append((prev_pixel, count))
            prev_pixel = pixel
            count = 1
    encoding.append((prev_pixel, count))  # For the last run
    return encoding, gray_image

# ------------------------------------------------------
# JPEG Compression (Lossy Compression)
# ------------------------------------------------------

def jpeg_compress(image, quality=90):
    # Convert image to JPEG format using PIL (quality can be adjusted)
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    pil_image.save("compressed_image.jpg", "JPEG", quality=quality)
    return "compressed_image.jpg"

# ------------------------------------------------------
# Testing the Compression Methods
# ------------------------------------------------------

# Load an example image (you can change this to any image)
image = cv2.imread('images/image7.tif')

# Huffman Compression
compressed_huffman, huffman_codes, _ = huffman_compress(image)
print("Huffman Compressed Size: ", len(compressed_huffman))

# Run-Length Encoding Compression
encoded_rle, _ = run_length_encode(image)
print("Run-Length Encoded Size: ", len(str(encoded_rle)))

# JPEG Compression (Lossy)
jpeg_file = jpeg_compress(image, quality=80)  # Example quality = 80
print(f"JPEG Compressed File: {jpeg_file}")

# ------------------------------------------------------
# Visualization for Comparison
# ------------------------------------------------------

# Show the original image and the result of JPEG compression
compressed_image = cv2.imread(jpeg_file)

# Plot the images
plt.figure(figsize=(10, 10))

plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(cv2.cvtColor(compressed_image, cv2.COLOR_BGR2RGB))
plt.title("JPEG Compressed Image")
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(cv2.cvtColor(cv2.imread('images/image7.tif'), cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis('off')

plt.show()



''')
    def p8(self):
        print('''
import cv2 as cv

import matplotlib.pyplot as plt

import numpy as n

def convertToRGB(img):

    return cv.cvtColor(img, cv.COLOR_BGR2RGB)

face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

image=cv.imread('images/image8.jfif')

grayimage=cv.cvtColor(image,cv.COLOR_BGR2GRAY)

faces=face_cascade.detectMultiScale(grayimage,scaleFactor=1.11,minNeighbors=5)

for (x, y, w, h) in faces:

    cv.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 1)

    plt.imshow(convertToRGB(image))

    print('no of faces:'),print(len(faces))`


''')
    def go1(self):
        print('''
Variant 2
package main
import (
"fmt"
"math/big"
)
// Iterative approach to calculate factorial
func factorialIterative(n int64) *big.Int {
result := big.NewInt(1)
for i := int64(2); i <= n; i++ {
result.Mul(result, big.NewInt(i))
}
return result
}
// Recursive approach with an early base case
func factorialRecursive(n int64) *big.Int {
result := big.NewInt(1)
if n > 1 {
result.Mul(big.NewInt(n), factorialRecursive(n-1))
}
return result
}
func main() {
var num int64
fmt.Print("Enter a number: ")
fmt.Scan(&num)
// Iterative factorial
fmt.Printf("Factorial of %d (Iterative): %v\n", num, factorialIterative(num))
// Recursive factorial
fmt.Printf("Factorial of %d (Recursive): %v\n", num, factorialRecursive(num))
}

''')
    def go2(self):
        print('''
package main
import "fmt"
// Define a struct to represent a BankAccount
type BankAccount struct {
accountHolder string
balance float64
}
// Method to deposit money into the account
func (b *BankAccount) Deposit(amount float64) {
b.balance += amount
fmt.Printf("Deposited: %.2f\n", amount)
}
// Method to withdraw money from the account
func (b *BankAccount) Withdraw(amount float64) {
if amount > b.balance {
fmt.Println("Insufficient funds!")
} else {
b.balance -= amount
fmt.Printf("Withdrawn: %.2f\n", amount)
}
}
// Method to check the current balance
func (b *BankAccount) CheckBalance() float64 {
return b.balance
}
func main() {
// Create a new bank account
account := BankAccount{accountHolder: "John Doe", balance: 1000.0}
// Deposit money into the account
account.Deposit(500)
// Try to withdraw money
account.Withdraw(300)
// Check the current balance
fmt.Printf("Current balance: %.2f\n", account.CheckBalance())
// Try to withdraw more than the available balance
account.Withdraw(1500)
// Check the balance again
fmt.Printf("Balance after withdrawal: %.2f\n", account.CheckBalance())
}

''')
    def go3(self):
        print('''
package main
import "fmt"
// Function to check if a matrix is symmetric
func isSymmetric(matrix *[][]int, size int) bool {
for i := 0; i < size; i++ {
for j := 0; j < size; j++ {
if (*matrix)[i][j] != (*matrix)[j][i] {
return false
}
}
}
return true
}
func main() {
var size int
fmt.Print("Enter the size of the square matrix: ")
fmt.Scan(&size)
// Initialize a 2D slice for the matrix
matrix := make([][]int, size)
for i := range matrix {
matrix[i] = make([]int, size)
}
// Read matrix input from the user
fmt.Println("Enter the matrix elements row by row:")
              
for i := 0; i < size; i++ {
for j := 0; j < size; j++ {
fmt.Scan(&matrix[i][j])
}
}
// Check if the matrix is symmetric
if isSymmetric(&matrix, size) {
fmt.Println("The matrix is symmetric.")
} else {
fmt.Println("The matrix is not symmetric.")
}
}



''')
    def go4(self):
        print('''
package main
import "fmt"
// Function to swap two integers using pointers
func swap(a, b *int) {
temp := *a
*a = *b
*b = temp
}
func main() {
var x, y int
fmt.Print("Enter two integers: ")
fmt.Scan(&x, &y)
fmt.Printf("Before swap: x = %d, y = %d\n", x, y)
swap(&x, &y)
fmt.Printf("After swap: x = %d, y = %d\n", x, y)
}

''')
    def go5(self):
        print('''
package main
import "fmt"
// Recursive function to compute Fibonacci number
func fibonacci(n int) int {
if n <= 0 {
return 0
} else if n == 1 {
return 1
}
              return fibonacci(n-1) + fibonacci(n-2)
}
func main() {
var num int
fmt.Print("Enter the number of Fibonacci terms to compute: ")
fmt.Scan(&num)
fmt.Printf("Fibonacci sequence up to %d terms:\n", num)
for i := 0; i < num; i++ {
fmt.Printf("%d ", fibonacci(i))
}
fmt.Println()
}




''')
    def go6(self):
        print('''

package main
import "fmt"
// Struct to represent a Book
type Book struct {
title string
available bool
}
// Method to borrow a book
func (b *Book) borrow() {
if b.available {
b.available = false
fmt.Println(b.title, "has been borrowed.")
} else {
fmt.Println(b.title, "is not available.")
}
}
              // Method to return a book
func (b *Book) returnBook() {
if !b.available {
b.available = true
fmt.Println(b.title, "has been returned.")
} else {
fmt.Println(b.title, "was not borrowed.")
}
}
// Method to check availability
func (b *Book) checkAvailability() {
if b.available {
fmt.Println(b.title, "is available.")
} else {
fmt.Println(b.title, "is not available.")
}
}
func main() {
// Create a new book
book1 := Book{title: "Go Programming", available: true}
// Borrow and return the book
book1.checkAvailability()
book1.borrow()
book1.checkAvailability()
              
book1.returnBook()
book1.checkAvailability()
}


''')
    def go7(self):
        print('''

package main
import "fmt"
// Define the LibraryItem interface
type LibraryItem interface {
borrow()
returnItem()
checkAvailability()
}
// Book struct implementing LibraryItem interface
type Book struct {
title string
available bool
}
func (b *Book) borrow() {
if b.available {
b.available = false
fmt.Println(b.title, "has been borrowed.")
} else {
fmt.Println(b.title, "is not available.")
}
}
func (b *Book) returnItem() {
if !b.available {
b.available = true
fmt.Println(b.title, "has been returned.")
} else {
fmt.Println(b.title, "was not borrowed.")
}
}
func (b *Book) checkAvailability() {
if b.available {
fmt.Println(b.title, "is available.")
} else {
fmt.Println(b.title, "is not available.")
}
}
func main() {
// Create a new book
var item LibraryItem = &Book{title: "Go Programming", available: true}
// Borrow, check availability, and return the book
item.checkAvailability()
item.borrow()
item.checkAvailability()
item.returnItem()
}


''')
    def go8(self):
        print('''
 package main
import (
"fmt"
"math"
)
// Define the Shape interface
type Shape interface {
area() float64
perimeter() float64
}
// Square struct implementing Shape interface
type Square struct {
side float64
}
func (s Square) area() float64 {
return s.side * s.side
}
func (s Square) perimeter() float64 {
return 4 * s.side
}
// Circle struct implementing Shape interface
type Circle struct {
radius float64
}
func (c Circle) area() float64 {
return math.Pi * c.radius * c.radius
}
func (c Circle) perimeter() float64 {
return 2 * math.Pi * c.radius
}
func main() {
// Create a square and circle
s := Square{side: 5}
c := Circle{radius: 3}
// Calculate and display area and perimeter for both shapes
fmt.Printf("Square: Area = %.2f, Perimeter = %.2f\n", s.area(), s.perimeter())
fmt.Printf("Circle: Area = %.2f, Perimeter = %.2f\n", c.area(), c.perimeter())
}

              


''')