import os, shutil
from textnode import TextType, TextNode

from copystatic import copy_directory_contents


dir_path_static = "./static"
dir_path_public = "./public"


def main():
    print("Deleting public directory...")
    print("Copying static files to public directory...")
    copy_directory_contents(dir_path_static, dir_path_public)


main() 