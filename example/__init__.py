if __name__ == "__main__":
    api_key = "your_openai_api_key_here"
    processor = ImageProcessor(api_key)
    processor.process_images("path_to_directory_or_zip_file")