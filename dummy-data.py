import os

def create_dummy_files(folder_path):
    os.makedirs(folder_path, exist_ok=True)
    
    prefixes = ["cat", "dog", "pet"]
    keywords = {
        "cat": ["whiskers", "meow", "fur"],
        "dog": ["bark", "paws", "bone"],
        "pet": ["feed", "walk", "cuddle"]
    }
    
    for prefix in prefixes:
        for i in range(1, 4):  # Create 3 files for each prefix
            file_path = os.path.join(folder_path, f"{prefix}_file{i}.txt")
            with open(file_path, 'w') as f:
                for keyword in keywords[prefix]:
                    f.write(f"This is a line with the keyword {keyword}\n")
                    
if __name__ == "__main__":
    folder_path = "your_folder_path_here"  # Replace with the folder where you want the dummy files to be created
    create_dummy_files(folder_path)
