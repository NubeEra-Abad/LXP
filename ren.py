import os

# Specify the root directory
root_dir = r"D:\nubeera\LXP\templates\abc"

# Walk through all files in the root directory and its subdirectories
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        # Check if the filename starts with 'trainer_'
        if filename.startswith("trainer_"):
            # Construct the full file path
            old_file_path = os.path.join(dirpath, filename)
            
            # Create the new filename by replacing 'trainer_' with 'mentor_'
            new_filename = "abc_" + filename[len("trainer_"):]
            new_file_path = os.path.join(dirpath, new_filename)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f'Renamed: {old_file_path} -> {new_file_path}')
