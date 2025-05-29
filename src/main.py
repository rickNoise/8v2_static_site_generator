import sys
from copystatic import copy_directory_contents
from generate_page import generate_pages_recursive

basepath = sys.argv[1] if (len(sys.argv) > 1) else "/"

print(f"basepath: {basepath}")

dir_path_static = "./static"
dir_path_public = "./docs"
generate_pages_recursive_dir_path_content = "./content"
generate_pages_recursive_template_path = "./template.html"
generate_pages_recursive_dest_dir_path = "./docs"

def main():
    print(f"Deleting {dir_path_public} directory...")
    print(f"Copying static files to {dir_path_public} directory...")
    # note that this function does the deleting AND the copying
    copy_directory_contents(dir_path_static, dir_path_public)

    print("Recursively generating all pages...")
    generate_pages_recursive(
        generate_pages_recursive_dir_path_content,
        generate_pages_recursive_template_path,
        generate_pages_recursive_dest_dir_path,
        basepath=basepath
    )


main() 