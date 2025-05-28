import os, shutil
from textnode import TextType, TextNode

from copystatic import copy_directory_contents
from generate_page import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
generate_page_from_path = "./content/index.md"
generate_page_template_path = "./template.html"
generate_page_dest_path = "./public/index.html"


def main():
    print("Deleting public directory...")
    print("Copying static files to public directory...")
    copy_directory_contents(dir_path_static, dir_path_public)

    generate_page(
        generate_page_from_path, 
        generate_page_template_path, 
        generate_page_dest_path
    )


main() 