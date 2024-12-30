import os
import argparse
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_binary_file(file_path):
    """Check if a file is binary."""
    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(1024)
            if b'\x00' in chunk:
                return True
            text_characters = bytes(range(32, 127)) + b'\n\r\t\f\b'
            if bool(chunk.translate(None, text_characters)):
                return True
        return False
    except Exception as e:
        logging.error(f"Error determining if file is binary {file_path}: {e}")
        return True

def clean_content(file_path):
    """Cleans up the content of a file by removing unnecessary whitespace."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        return '\n'.join(cleaned_lines)

def generate_tree(directories, extensions=None, include_all=False, include_hidden=False,ignore_dirs=None):
    """Generates a tree structure for multiple directories."""
    tree_structure = ''
    for directory in directories:
        directory_path = Path(directory).resolve()

        for root, dirs, files in os.walk(directory_path):
            root_path = Path(root).resolve()
            relative_root = root_path.relative_to(directory_path)

           # Check if the current directory should be ignored
            if ignore_dirs and any(str(root_path).startswith(str(ignore_dir)) or str(relative_root).startswith(str(ignore_dir)) for ignore_dir in ignore_dirs):
#            if ignore_dirs and any(root_path.is_relative_to(ignore_dir) or str(relative_root).startswith(str(ignore_dir)) for ignore_dir in ignore_dirs):
                # Skip this directory and its contents
                dirs[:] = []  # Stop os.walk from descending into this directory
                continue

            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                files = [f for f in files if not f.startswith('.')]
            
            if include_all:
                included_files = files
            elif extensions:
                included_files = [f for f in files if Path(f).suffix in extensions]
            else:
                dirs[:] = []  # Skip all directories
                included_files = []  # Skip all files

            included_files = [f for f in included_files if not is_binary_file(os.path.join(root, f))]
            if included_files or (dirs and include_all):
                level = len(root_path.relative_to(directory_path).parts)
                indent = '|   ' * level + '|-- '
                sub_indent = '|   ' * (level + 1) + '|-- '
                tree_structure += f"{indent}{root_path.name}/\n"
                for file in included_files:
                    tree_structure += f"{sub_indent}{file}\n"
    return tree_structure

def list_files(directories=None,  extensions=None, include_all=False, include_hidden=False,ignore_dirs=None):
        """Lists files in multiple directories."""
    #try:
        files_info = []
        num_files = 0
        if None==directories:
            return
        total_files=0
        for directory in directories:
            directory_path = Path(directory)
            if not directory_path.is_dir():
                logging.error(f"The path {directory} is not a valid directory.")
                continue

            logging.info(f"Processing directory: {directory_path}")

            for file_path in directory_path.rglob('*'):
                absolute_path = file_path.resolve()

                # Check if the file's directory or its parent directories should be ignored
#                if ignore_dirs and any(absolute_path.is_relative_to(ignore_dir) for ignore_dir in ignore_dirs):
                if ignore_dirs and any(str(absolute_path).startswith(str(ignore_dir)) for ignore_dir in ignore_dirs):

                    continue
                total_files+=1

                if file_path.is_file() and '.git' not in file_path.parts:
                    if not include_hidden and file_path.name.startswith('.'):
                        continue
                    #if is_binary_file(file_path):
                     #   print("binary .")
                     #   continue
                    if include_all or (extensions and file_path.suffix.lower() in extensions):
                        num_files += 1
                        file_info = [f"Path: {file_path}", f"File: {file_path.name}", "-------"]

                        try:
                            with open(file_path, 'r') as f:
                                file_info.append(f.read())
                        except Exception as e:
                            logging.error(f"Error reading file {file_path}: {e}")
                        
                        files_info.append('\n'.join(file_info))

        logging.info(f"Files processed: {num_files} of {total_files}")
        return '\n'.join(files_info)
    #except Exception as e:
    #    logging.error(f"Error processing directories: {e}")
    #    return ""
    
def write_file(file_path, data):
    """Writes data to the specified file."""
    try:
        with open(file_path, 'w') as file:
            file.write(data)
        logging.info(f"Output written to: {file_path}.")
    except IOError as e:
        logging.error(f"Failed to write to {file_path}: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while writing to {file_path}: {e}")

def print_configuration(directories, extensions, include_all, include_hidden,ignore_dirs=None):
    """Prints the directories and extensions being processed."""
    logging.info(f"Processing:  {', '.join(directories)}")
    logging.info(f"Types: {', '.join(extensions)}")
    logging.info(f"All files: {include_all}")
    logging.info(f"Hidden files: {include_hidden}")
    if ignore_dirs:

        for dir in ignore_dirs:
            logging.info(f"Omitting: {dir}")

def main():
    """Main function to parse arguments and execute operations."""
    output_file = f"{os.path.basename(os.getcwd())}.flort"
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  
    parser = argparse.ArgumentParser(description="flort: create a single file of all given extensions, ecursivly for all dirictories given. Ignores binary files.", prog='flort',add_help=False,prefix_chars='-',allow_abbrev=False)
    parser.add_argument('directories', metavar='DIRECTORY',default=".", type=str, nargs='*', help='Directories to list files from, defaults to the curent working directory.')
    parser.add_argument('--ignore-dirs', type=str, help='Directories to ignore (comma-separated list).')
    parser.add_argument('-h', '--help', action='help', help='show this help message and exit')
    parser.add_argument('--output', type=str, default=output_file, help='Output file path. Defaults to the basename of the current directory if not specified. stdio will ouput to console')
    parser.add_argument('--no-tree', action='store_true', help='Do not print the tree at the beginning.')
    parser.add_argument('--all', action='store_true', help='Include all files regardless of extensions.')
    parser.add_argument('--hidden', action='store_true', help='Include hidden files.')
    args, unknown_args = parser.parse_known_args()

    # Handle ignore_dirs argument
    if args.ignore_dirs:
        ignore_dirs = [Path(ignore_dir).resolve() for ignore_dir in args.ignore_dirs.split(',')]
    else:
        ignore_dirs = []

    # Treat unknown args as extensions that start with '--'
    extensions = [f".{ext.lstrip('-')}" for ext in unknown_args if ext.startswith('--')]

    # Print configuration
    print_configuration(args.directories, extensions, args.all, args.hidden,ignore_dirs)

    if not extensions and not args.all:
        logging.error("No extensions provided and --all flag not set. No files to process.")
        return

    output_content = [f"Florted: {current_datetime}"]
    if not args.no_tree:
        output_content.append(generate_tree(args.directories, extensions=extensions, include_all=args.all, include_hidden=args.hidden,ignore_dirs=ignore_dirs))

    output_content.append(list_files(args.directories, extensions=extensions, include_all=args.all, include_hidden=args.hidden,ignore_dirs=ignore_dirs))

    if args.output != "stdio":
        write_file(args.output, "\n".join(output_content))
    else:
        print("\n".join(output_content))

if __name__ == "__main__":
    main()
