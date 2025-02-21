import os
import json

def generate_image_list(directory):
    # List to hold image filenames
    image_list = []

    # Loop through the directory and add image files to the list
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):  # Add more extensions if needed
            image_list.append(filename)

    # Write the image list to a JSON file
    with open('image_list.json', 'w') as json_file:
        json.dump(image_list, json_file)

if __name__ == "__main__":
    # Specify the directory containing images
    images_directory = 'uploads'  # Change this to your images directory
    generate_image_list(images_directory)
