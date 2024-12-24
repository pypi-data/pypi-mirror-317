"""
Module:         fs2f
Description:    A tool to taking snapshots of a file structure into a single file.
Author:         Andrii Burkatskyi aka andr11b
Year:           2024
Version:        0.0.1.241223
License:        MIT License
Email:          4ndr116@gmail.com
Link:           https://github.com/codyverse/fs2f
"""

import os
import hashlib
import sys
import argparse


def hash(file_path):
    """
    Calculate the SHA-256 hash of a given file.

    This function opens the file in binary mode and reads it in chunks of 8 KB, updating the SHA-256 hash for each
    chunk. This is efficient for large files as it prevents loading the entire file into memory.

    Args:
        file_path (str): The path to the file whose hash is to be calculated.

    Returns:
        str: The SHA-256 hash of the file, represented as a hexadecimal string.
    """

    sha256 = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


def fs2f(input_dir, shapshot):
    """
    Create a snapshot of the file structure from the specified directory.

    This function walks through the directory recursively, collecting information about directories and files
    (permissions, size, hash), and writes this information to the snapshot file. It also stores the content of the
    files in the snapshot.

    Args:
        input_dir (str): The path to the directory whose file structure is to be snapshotted.
        shapshot (str): The path to the file where the snapshot will be saved.

    Returns:
        None
    """

    base_dir = os.path.abspath(input_dir)

    try:
        with open(shapshot, 'wb') as f:
            for root, dirs, files in os.walk(base_dir):
                relative_root = os.path.relpath(root, base_dir)

                if relative_root == '.':
                    relative_root = ''  # Clear './'

                # Store information about directories
                for dir_name in dirs:
                    dir_path = os.path.join(relative_root, dir_name)
                    dir_mode = oct(os.stat(os.path.join(root, dir_name)).st_mode)[-3:] if os.name != 'nt' else '777'
                    dir_info = f"{dir_path}|d|{dir_mode}|0|\n"

                    f.write(dir_info.encode('utf-8'))
                    print(dir_path)

                # Store information about files
                for file_name in files:
                    abs_file_path = os.path.join(root, file_name)

                    # Skip snapshot itself
                    if os.path.abspath(abs_file_path) == os.path.abspath(shapshot):
                        continue

                    # Skip scrypt itself
                    if os.path.abspath(abs_file_path) == os.path.abspath(__file__):
                        continue

                    file_path = os.path.join(relative_root, file_name)
                    file_size = os.path.getsize(abs_file_path)
                    file_permissions = oct(os.stat(abs_file_path).st_mode)[-3:] if os.name != 'nt' else '666'
                    file_hash = hash(abs_file_path)

                    file_info = f"{file_path}|f|{file_permissions}|{file_size}|{file_hash}\n"
                    f.write(file_info.encode('utf-8'))

                    # Write file content
                    with open(abs_file_path, 'rb') as file_content:
                        f.write(file_content.read())

                    print(file_path)

                    # New line for a nicer structure
                    f.write(b'\n')

        print(f"\n{os.path.getsize(os.path.abspath(shapshot))}")
    except Exception as e:
        print(f"Failed to create file structure snapshot: {e}")


def f2fs(shapshot, output_dir, strict_mode=True):
    """
    Restore the file structure from a snapshot file.

    This function reads the snapshot file, creating directories and restoring files to the specified output directory.
    It also checks the integrity of restored files by comparing their hash values with the ones stored in the snapshot.
    If hash mismatches are detected and strict mode is enabled, the restoration process is aborted.

    Args:
        shapshot (str): The path to the snapshot file to restore from.
        output_dir (str): The directory where the restored files and directories will be placed.
        strict_mode (bool): If True, the process will stop on any hash mismatch;
                            if False, mismatches are ignored (default is True).

    Returns:
        None
    """

    try:
        with open(shapshot, 'rb') as f:
            while True:
                line = f.readline().decode('utf-8').strip()

                if not line:
                    break

                # Parse metadata
                name, type_, permissions, size, file_hash = line.split('|')
                size = int(size)
                new_path = os.path.join(output_dir, name)

                if type_ == 'd':
                    os.makedirs(new_path, exist_ok=True)
                    print(new_path + '/')

                    if os.name != 'nt':
                        os.chmod(new_path, int(permissions, 8))
                elif type_ == 'f':
                    # Restore file content
                    with open(new_path, 'wb') as file_out:
                        file_out.write(f.read(size))

                    if hash(new_path) != file_hash:
                        print(f"{new_path} - Hash mismatch!")
                        os.remove(new_path)

                        # If strict mode is enabled, exit on hash mismatch
                        if strict_mode:
                            sys.exit(1)
                    else:
                        print(new_path)

                        if os.name != 'nt':
                            os.chmod(new_path, int(permissions, 8))

                # Skip any empty lines between files
                while True:
                    pos = f.tell()  # Save current position
                    next_line = f.readline().decode('utf-8').strip()

                    # Check whether the file end has been reached
                    if not next_line:  # Empty line
                        if f.tell() == os.fstat(f.fileno()).st_size:  # The end of the file
                            break
                    else:
                        f.seek(pos)  # Back to metadata
                        break
    except Exception as e:
        print(f"Failed to restore file structure snapshot: {e}")


def list(shapshot):
    """
    List the contents of a snapshot file.

    This function reads the snapshot file and prints the list of directories and files stored in it, including their
    paths, permissions, sizes, and hashes. It does not restore any files, just displays metadata about them.

    Args:
        shapshot (str): The path to the snapshot file to list contents from.

    Returns:
        None
    """

    try:
        with open(shapshot, 'rb') as f:
            while True:
                line = f.readline().decode('utf-8').strip()

                if not line:
                    break

                # Parse metadata
                name, type_, permissions, size, file_hash = line.split('|')
                size = int(size)

                # Print out the file or directory
                print(f"{name + '/' if type_ == 'd' else name + ' - ' + str(round(size / 1024, 2)) + 'kB'}")

                # Skip binary data of the file
                if type_ == 'f':
                    f.seek(f.tell() + size)  # Skip the file content

                # Skip any empty lines between files
                while True:
                    pos = f.tell()  # Save current position
                    next_line = f.readline().decode('utf-8').strip()

                    # Check whether the file end has been reached
                    if not next_line:  # Empty line
                        if f.tell() == os.fstat(f.fileno()).st_size:  # The end of the file
                            break
                    else:
                        f.seek(pos)  # Back to metadata
                        break

    except Exception as e:
        print(f"Error while snapshot listing: {e}")


def main():
    parser = argparse.ArgumentParser(description="A tool for taking snapshots of a file structure into a single file.")
    parser.add_argument('-m', action='store_true', help="Create a file structure snapshot in a file")
    parser.add_argument('-u', action='store_true', help="Restore a file structure snapshot from a file")
    parser.add_argument('-s', action='store_true', help="Disable strict mode (continue on file hash mismatch)")
    parser.add_argument('-l', metavar="shapshot", type=str, help="List files and directories stored in snapshot")
    parser.add_argument('-d', metavar="directory", type=str, required=False, help="Path to the directory")
    parser.add_argument('-f', metavar="shapshot", type=str, required=False, help="Path to the snapshot")
    args = parser.parse_args()

    if args.l:
        list(args.l)
        sys.exit(0)

    if not args.m and not args.u:
        parser.print_help()
        sys.exit(1)

    if args.m:
        if not args.d or not args.f:
            print("Error: Both -d (directory) and -f (file) parameters are required for snapshot creation.")
            sys.exit(1)

        fs2f(args.d, args.f)
    elif args.u:
        if not args.d or not args.f:
            print("Error: Both -d (directory) and -f (file) parameters are required for snapshot restoration.")
            sys.exit(1)

        f2fs(args.f, args.d, strict_mode=not args.s)


if __name__ == "__main__":
    main()
