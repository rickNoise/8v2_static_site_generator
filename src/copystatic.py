import os, shutil

def copy_directory_contents(source_dir, dest_dir):
    """
    a recursive function that copies all the contents from 
    a source directory (source_dir: str, relative to the project root) 
    to a destination directory (dest_dir: str, relative to the project root)
    """
    # It should first delete all the contents of the destination directory (public) to ensure that the copy is clean.
    # First check that the source_dir exists
    # print(f"\nnew call to copy_directory_contents with {source_dir} and {dest_dir}")
    if not os.path.exists(source_dir):
        raise Exception("The source directory provided does not exist!")
    # print(f"source directory exists: {source_dir}")

    # Then check the dest_dir exists
    if os.path.exists(dest_dir):
        # if it does, delete all of its contents
        # print(f"destination directory exists: {dest_dir}")
        # print(f"deleting all contents within {dest_dir}...")
        for entry in os.listdir(dest_dir):
            entry_path = os.path.join(dest_dir, entry)
            if os.path.isdir(entry_path):
                # print(f"deleting dir {entry}...")
                shutil.rmtree(entry_path)
            else:
                # print(f"deleting file {entry}...")
                os.remove(entry_path)
    else:
        # if not, create it
        # print(f"destination directory does not exist; creating it at {dest_dir}")
        os.mkdir(dest_dir)

    # It should copy all files and subdirectories, nested files, etc.
    # print("now attempting to copy all contents from source to destination")
    for entry in os.listdir(source_dir):
        # print(f"processing {entry} from {source_dir}")
        entry_path = os.path.join(source_dir, entry)
        if os.path.isfile(entry_path):
            # print(f"{entry} is a file; copying to {dest_dir}")
            shutil.copy(entry_path, dest_dir)
        else: # assume its a dir otherwise
            # print(f"{entry} is a dir")
            # print(f"calling copy_to_directory recursively with dest_dir as {os.path.join(dest_dir, entry)}")
            copy_directory_contents(entry_path, os.path.join(dest_dir, entry))

    # print(f"finishing this call to copy_directory contents\n")

