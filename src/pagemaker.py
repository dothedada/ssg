from blocks import markdown_to_html_node
import os


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()

    raise Exception("No title found in page")


def generate_page(from_path, template_path, dest_path):
    print(f"Making page {from_path} with {template_path} to {dest_path}...")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    content_html = markdown_to_html_node(markdown).to_html()
    page_title = extract_title(markdown)
    page_html = template.replace(
        "{{ Title }}",
        page_title,
        1,
    ).replace(
        "{{ Content }}",
        content_html,
        1,
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page_html)
