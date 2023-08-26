"""
This module provides classes and functions for image conversion and manipulation.
"""

import numpy as np
from PIL import Image

class ImageConverter:
    def __init__(self):
        self.header = "IMAGE_BINARY_FILE"
        self.footer = "END_OF_IMAGE"
    
    def convert_to_binary(self, image_path, output_path):
        try:
            image = Image.open(image_path)
            image = image.convert("RGB")
            image_array = np.array(image)
            
            # Preprocess data if needed
            # ...

            # Save binary data to file
            with open(output_path, "wb") as binary_file:
                binary_file.write(self.header.encode())
                binary_file.write(image_array.tobytes())
                binary_file.write(self.footer.encode())
            
            print("Image converted to binary successfully.")
        except FileNotFoundError:
            print("Error: Image file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def reconstruct_image(self, binary_path, output_path):
        try:
            with open(binary_path, "rb") as binary_file:
                binary_data = binary_file.read()
                image_data = binary_data.split(self.header.encode())[-1].split(self.footer.encode())[0]
                image_array = np.frombuffer(image_data, dtype=np.uint8)
                image_array = image_array.reshape((-1, 3))

                # Reconstruct image and save
                reconstructed_image = Image.fromarray(image_array.reshape(image_array.shape[0], -1))
                reconstructed_image.save(output_path)
            
            print("Image reconstructed successfully.")
        except FileNotFoundError:
            print("Error: Binary file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

class BinaryShortener:
    def shorten_binary(self, binary_path, output_folder):
        try:
            with open(binary_path, "rb") as binary_file:
                binary_data = binary_file.read()
                chunk_size = 1000  # Adjust the chunk size as needed

                # Split binary data into smaller chunks and save as text files
                chunks = [binary_data[i:i+chunk_size] for i in range(0, len(binary_data), chunk_size)]
                for i, chunk in enumerate(chunks):
                    with open(f"{output_folder}/chunk_{i}.txt", "w") as text_file:
                        text_file.write(chunk.hex())
                
            print("Binary file shortened and saved as text files.")
        except FileNotFoundError:
            print("Error: Binary file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

# Usage
converter = ImageConverter()

# Convert image to binary
image_path = "/workspaces/sending_pic_msg/img/krishna2.jpg"
converter.convert_to_binary(image_path, "output_binary.bin")

# Reconstruct image from binary
converter.reconstruct_image("output_binary.bin", "reconstructed_image.jpg")

# Shorten binary file using BinaryShortener
shortener = BinaryShortener()
shortener.shorten_binary("output_binary.bin", "text_files")
