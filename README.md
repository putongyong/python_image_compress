# python_image_compress

## Image Compression Script

In real-world production scenarios, it's common to encounter situations where image files need to adhere to specific size limits when being uploaded. To address this need, our Python script offers an automated solution for efficiently reducing the size of multiple image files. This script facilitates image compression to minimize their file sizes while upholding their original quality. Images that surpass a designated size threshold are subjected to compression to ensure they fit within a specified file size limit (e.g., 1MB). Meanwhile, smaller images are left untouched and copied without undergoing any compression.

## Features

- Compress images to reduce file size while maintaining quality.
- Images exceeding a specified file size are compressed.
- Smaller images are copied without compression.
- Supports JPG, JPEG, and PNG image formats.
- Uses the Pillow library for image processing.

## Usage

1. Place the images you want to compress in the `inputphoto` folder.
2. Run the script `imagecompress.py`.

The compressed images will be saved in the `output_compressed_images` folder.

## Requirements

- Python 3.x
- Pillow library (`pip install Pillow`)

## Configuration

You can configure the following parameters in the script:

- `max_file_size`: Maximum file size in bytes for images to be compressed.
- `quality`: Image quality for compression (0-100).
- `width`: New width for resized images.
- `height`: New height for resized images.
- `to_jpg`: Convert images to JPG format.

## Note

The script uses the `Image.LANCZOS` resampling filter for resizing images, which provides high-quality results. Adjust the `new_size_ratio` in the `compress_img` function to achieve the desired level of compression.

## Author

Yong XIE

## License

This project is licensed under the MIT License
