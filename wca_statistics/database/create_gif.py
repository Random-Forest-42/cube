import os
from PIL import Image


file_match_str = 'practice_vs_time'


# --- Configuration ---
# Set this to the folder path where your images are located
TARGET_FOLDER = "D:\\Documentos\\Coding\\Python\\cube\\wca_statistics\\results\\"
# Set the frame delay in milliseconds (e.g., 200ms = 0.2 seconds per frame)
FRAME_DURATION = 200
# Name of the output file
OUTPUT_GIF_NAME = f"{TARGET_FOLDER}\\gif_{file_match_str}.gif"

# Create a small dummy folder/files for testing if you want
# import pathlib
# pathlib.Path(TARGET_FOLDER).mkdir(exist_ok=True)
# print(f"Make sure your images are in the '{TARGET_FOLDER}' folder!")

# --- Run the function ---
# Ensure you change 'TARGET_FOLDER' to your actual folder path!

folder_path = TARGET_FOLDER
output_filename = OUTPUT_GIF_NAME
duration = 200

def create_gif_from_images(folder_path, output_filename="animated_output.gif", duration=200):
    """
    Creates an animated GIF from images in a folder, ordered by the number in their filename.

    Args:
        folder_path (str): The path to the folder containing the images.
        output_filename (str): The name for the resulting GIF file.
        duration (int): The duration (in milliseconds) for which each frame is shown.
    """
    pass
# 1. Get all image files in the specified folder
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')) and file_match_str in f]

if not image_files:
    print("No image files found in the folder.")
    pass

# 2. Define a sorting key to order the files by the number they contain
# This key extracts the first sequence of digits found in the filename.
import re
def get_file_order(filename):
    # Look for a sequence of one or more digits (\d+) in the filename
    match = re.search(r'(\d+)', filename)
    if match:
        # Convert the matched digits to an integer for numerical sorting
        return int(match.group(1))
    # If no number is found, return a very large number so they sort last
    return float('inf')

# 3. Sort the files
# The 'key' argument uses our custom function to ensure numerical order.
image_files.sort(key=get_file_order)

print(f"--- Processing {len(image_files)} images in this order: ---")
for filename in image_files:
    print(f"  > {filename}")
print("-------------------------------------------------")

# 4. Open and process the images
images = []
try:
    # Open the first image; this will be the base image for the GIF
    first_image = Image.open(os.path.join(folder_path, image_files[0]))
    images.append(first_image)

    # Open the remaining images
    for filename in image_files[1:]:
        filepath = os.path.join(folder_path, filename)
        img = Image.open(filepath)
        # Ensure all images are converted to RGB mode, which is necessary for some GIF writers
        images.append(img.convert('RGB'))

except Exception as e:
    print(f"An error occurred while opening or converting an image: {e}")

# 5. Save as an animated GIF
try:
    # Save the first image, and append the rest as frames
    # save_all=True: tells Pillow to create an animation
    # append_images: the list of subsequent frames
    # duration: the time in milliseconds for each frame
    # loop=0: tells the GIF to loop indefinitely
    first_image.save(
        output_filename,
        save_all=True,
        append_images=images[1:], # Append all images *after* the first one
        duration=duration,
        loop=0
    )
    print(f"\n✅ Successfully created GIF: {output_filename}")

except Exception as e:
    print(f"\n❌ An error occurred while saving the GIF: {e}")

# create_gif_from_images(TARGET_FOLDER, OUTPUT_GIF_NAME, FRAME_DURATION)