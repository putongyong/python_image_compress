import os
from PIL import Image
import shutil
import io

def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

def compress_img(image_name, output_folder, max_file_size=1 * 1024 * 1024, quality=90, width=None, height=None, to_jpg=True):
    # Load the image to memory
    img = Image.open(image_name)
    # Print the original image shape
    print("[*] Image shape:", img.size)
    # Get the original image size in bytes
    original_image_size = os.path.getsize(image_name)
    # Print the size before compression/resizing
    print("[*] Size before compression:", get_size_format(original_image_size))
    
    if original_image_size <= max_file_size:
        print("Image is already under 1MB, skipping compression.")
        new_filename = os.path.join(output_folder, os.path.basename(image_name))
        shutil.copy(image_name, new_filename)
    else:
        new_size_ratio = (max_file_size / original_image_size) ** 0.5  # Adjust this ratio as needed
        
        # Perform compression to keep the image size under 1MB
        compressed_image = img.copy()
        new_image_size = original_image_size

        while new_image_size > max_file_size:
            if new_size_ratio < 1.0:
                compressed_image = compressed_image.resize((int(compressed_image.size[0] * new_size_ratio), int(compressed_image.size[1] * new_size_ratio)), Image.Resampling.LANCZOS)
            elif width and height:
                compressed_image = compressed_image.resize((width, height), Image.Resampling.LANCZOS)

            buffer = io.BytesIO()
            compressed_image.save(buffer, format="JPEG", quality=quality, optimize=True)
            new_image_size = len(buffer.getvalue())
            buffer.close()

        # Construct the new filename
        filename, ext = os.path.splitext(image_name)
        if to_jpg:
            new_filename = f"{filename}_compressed.jpg"
        else:
            new_filename = f"{filename}_compressed{ext}"
        new_filename = os.path.join(output_folder, os.path.basename(new_filename))

        # Save the compressed image
        compressed_image.save(new_filename, format="JPEG", quality=quality, optimize=True)

        print("[+] New file saved:", new_filename)
        # Print the new size in a good format
        print("[+] Size after compression:", get_size_format(new_image_size))
        # Calculate the saving bytes
        saving_diff = original_image_size - new_image_size
        # Print the saving percentage
        print(f"[+] Image size change: {saving_diff/original_image_size*100:.2f}% of the original image size.")

def main():
    source_folder = "inputphoto"
    compressed_output_folder = "output_compressed_images"

    if not os.path.exists(compressed_output_folder):
        os.makedirs(compressed_output_folder)

    max_file_size = 1 * 1024 * 1024  # 1 MB in bytes

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Add more image formats if needed
            input_path = os.path.join(source_folder, filename)

            # Get the size of the image
            image_size = os.path.getsize(input_path)

            # Construct the output path in the compressed output folder
            output_path = os.path.join(compressed_output_folder, filename)

            # If the compressed image doesn't exist and the image size is greater than 1MB, compress it
            if not os.path.exists(output_path) and image_size > max_file_size:
                compress_img(input_path, output_folder=compressed_output_folder, max_file_size=max_file_size, to_jpg=True)
            else:
                # Otherwise, copy the original image to the output folder
                shutil.copy(input_path, output_path)

if __name__ == "__main__":
    main()

