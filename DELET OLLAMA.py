import shutil

# Directory where the model and tokenizer are saved
directory = "./dolphin_llama3_8b"

try:
    # Remove the directory and its contents
    shutil.rmtree(directory)
    print(f"Successfully removed {directory}")
except FileNotFoundError:
    print(f"Directory {directory} not found")
except Exception as e:
    print(f"Error occurred while removing {directory}: {str(e)}")
