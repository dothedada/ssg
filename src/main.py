from textnode import TextNode
from filehandler import static_files_handler
from pagemaker import generate_pages_recursive


def main():
    static_files_handler()
    generate_pages_recursive("content", "template.html", "public")


main()
