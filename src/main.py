from textnode import TextNode
from filehandler import static_files_handler


def main():
    test_node = TextNode("Entonces pendejo", "code", "https://mmejia.com")
    static_files_handler()
    print(test_node)


main()
