from blocks import markdown_to_html_node
import os


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()

    raise Exception("No title found in page")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Making page {from_path} with {template_path} to {dest_path}...")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    content_html = markdown_to_html_node(markdown).to_html()
    page_title = extract_title(markdown)
    page_html = (
        template.replace(
            "{{ Title }}",
            page_title,
            1,
        )
        .replace(
            "{{ Content }}",
            content_html,
            1,
        )
        .replace('href="/', 'href="' + basepath)
        .replace('src="/', 'src="' + basepath)
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page_html)


def generate_pages_recursive(
    dir_path_content,
    template_path,
    dest_dir_path,
    basepath,
):
    dir_entries = os.listdir(dir_path_content)

    if len(dir_entries) == 0:
        return

    for entry in dir_entries:
        content_path = os.path.join(dir_path_content, entry)

        if os.path.isdir(content_path):
            print(f"Parsing {content_path}...")
            dest_path = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(
                content_path,
                template_path,
                dest_path,
                basepath,
            )
        else:
            file_type = entry.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, file_type)
            generate_page(content_path, template_path, dest_path, basepath)
