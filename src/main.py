import os, shutil
from textnode import TextType, TextNode

from copystatic import copy_directory_contents
from generate_page import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
generate_page_from_path = "./content/index.md"
generate_page_template_path = "./template.html"
generate_page_dest_path = "./public/index.html"
generate_pages_recursive_dir_path_content = "./content"
generate_pages_recursive_template_path = "./template.html"
generate_pages_recursive_dest_dir_path = "./public"

def main():
    print("Deleting public directory...")
    print("Copying static files to public directory...")
    # note that this function does the deleting AND the copying
    copy_directory_contents(dir_path_static, dir_path_public)

    # generate_page(
    #     generate_page_from_path, 
    #     generate_page_template_path, 
    #     generate_page_dest_path
    # )
    generate_pages_recursive(
        generate_pages_recursive_dir_path_content,
        generate_pages_recursive_template_path,
        generate_pages_recursive_dest_dir_path
    )


main() 