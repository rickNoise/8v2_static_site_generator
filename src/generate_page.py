from markdown_to_html import (
    markdown_to_html_node, 
    extract_title,
)
from htmlnode import HTMLNode
import os


def generate_page(from_path, template_path, dest_path):
    # print(f"Generating page from {from_path} to {dest_path} using {template_path}...")

    # Read the markdown file at from_path and store the contents in a variable.
    from_path_file = open(from_path)
    from_path_contents = from_path_file.read()
    from_path_file.close()

    # Read the template file at template_path and store the contents in a variable.
    template_path_file = open(template_path)
    template_path_contents = template_path_file.read()
    template_path_file.close()

    from_path_contents_as_html = markdown_to_html_node(from_path_contents).to_html()
    from_path_contents_title = extract_title(from_path_contents)
    
    # Replace the {{ Title }} and {{ Content }} placeholders 
    # in the template with the HTML and title you generated.
    final_html_with_title = from_path_contents_title.join(
        template_path_contents.split("{{ Title }}", 1)
    )
    final_html_with_title_and_content = from_path_contents_as_html.join(
        final_html_with_title.split("{{ Content }}", 1)
    )

    with open(dest_path, "w") as f:
        f.write(final_html_with_title_and_content)
    
    if not f.closed:
        raise Exception("dest_path file did not close successfully!")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, dest_file_ext=".html"):
    """
    Crawl every entry in the content directory.
    For each markdown file found, generate a new .html file using the same template.html. 
    The generated pages should be written to the public directory in the 
    same directory structure.
    """

    # check that dir_path_content exists and is a directory
    if not os.path.exists(dir_path_content):
        raise ValueError("Provided dir_path_content does not exist!")
    if not os.path.isdir(dir_path_content):
        raise ValueError("Provided dir_path_content is not a directory!")
    
    # print(f"Recursively generating pages from {dir_path_content} to {dest_dir_path} using {template_path}...")

    # crawl every entry in the content directory
    # print(f"Crawling all entries in {dir_path_content}...")
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        # print(f"processing entry {entry} at path {entry_path}")
        if os.path.isfile(entry_path):
            file_name, file_extension = os.path.splitext(entry)
            if file_extension == ".md":
                # print(f"{entry} is a markdown file. Running generate_page using template path {template_path}...")
                generate_page(
                    entry_path, 
                    template_path, 
                    os.path.join(dest_dir_path, file_name + dest_file_ext)
                )
        if os.path.isdir(entry_path):
            # print(f"{entry} is a directory. Recursively running generate_pages_recursive with dir_path_content: {dir_path_content}, template_path: {os.path.abspath(template_path)}, and dest_dir_path: {dest_dir_path}...")

            # create the directory first if it doesn't exist
            new_dest_dir_path = os.path.join(dest_dir_path, entry)
            if not os.path.exists(new_dest_dir_path):
                try:
                    os.mkdir(new_dest_dir_path)
                    # print(f"Directory '{new_dest_dir_path}' created successfully.")
                except PermissionError:
                    print(f"Permission denied: Unable to create '{new_dest_dir_path}'.")
                except Exception as e:
                    print(f"An error occurred: {e}")

            generate_pages_recursive(
                os.path.join(dir_path_content, entry),
                os.path.abspath(template_path),
                new_dest_dir_path
            )
    
    # print("COMPLETED running generate_pages_recursive.")


