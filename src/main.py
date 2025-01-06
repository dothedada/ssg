from textnode import TextNode
from filehandler import static_files_handler
from pagemaker import generate_page


def main():
    static_files_handler()
    generate_page("content/index.md", "template.html", "public/index.html")


main()
