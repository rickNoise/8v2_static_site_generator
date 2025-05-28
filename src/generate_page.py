from markdown_to_html import (
    markdown_to_html_node, 
    extract_title,
)
from htmlnode import HTMLNode
import os


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")

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