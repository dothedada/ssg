import sys
from filehandler import static_files_handler
from pagemaker import generate_pages_recursive

default_basepath = "/"
template_path = "./template.html"
dir_path_content = "./content/"
dir_path_public = "./docs/"


def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    static_files_handler(basepath)

    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
        basepath,
    )


main()
