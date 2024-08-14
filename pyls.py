import argparse
import os
from datetime import datetime


def getDescriptionsOfFilesInDir(dirname):
    """
    Lists the files and folders in the given directory and constructs a list of dicts with the required information.

    Args:
        dirname (str): The directory to list files from.

    Returns:
        list: A list of dictionaries containing file information.
    """
    assert isinstance(dirname, str), "dirname should be a string"

    if not os.path.exists(dirname):
        raise FileNotFoundError(f"Directory '{dirname}' does not exist.")

    file_descriptions = []
    with os.scandir(dirname) as entries:
        for entry in entries:
            file_info = {
                "filename": entry.name,
                "filetype": (
                    "d" if entry.is_dir()
                    else "x" if os.access(entry.path, os.X_OK) and not entry.is_dir()
                    else "f"
                ),
                "modtime": datetime.fromtimestamp(entry.stat().st_mtime),
                "filesize": entry.stat().st_size if entry.is_file() else 0,
            }
            file_descriptions.append(file_info)

    return file_descriptions


def formatResults(results, long_format, filetype):
    formatted_lines = []
    for result in results:
        line = result["filename"]

        if filetype:
            if result["filetype"] == "d":
                line += "/"
            elif result["filetype"] == "x":
                line += "*"
            else:
                print(line)

        if long_format:
            modtime_str = result["modtime"].strftime("%Y-%m-%d %H:%M:%S")
            line = f"{modtime_str}  {result['filesize']:>10}  {line}"

        formatted_lines.append(line)
    return formatted_lines

def main(args):
    file_descriptions = getDescriptionsOfFilesInDir(args.dirname)
    lines = formatResults(file_descriptions, args.long_format, args.filetype)

    for line in lines:
        print(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="pyls",
        description="Lists files in given or current directory",
        epilog="Poor man's ls",
    )

    parser.add_argument(
        "dirname",
        help="Name of directory to list the contents of",
        action="store",
        nargs="?",
        default=".",
    )

    parser.add_argument(
        "-l",
        "--long-format",
        help="Presents more details about files in columnar format",
        action="store_true",
    )

    parser.add_argument(
        "-F",
        "--filetype",
        help="Adds an extra character to the end of the printed filename that indicates its type.",
        action="store_true",
    )

    args = parser.parse_args()
    main(args)
