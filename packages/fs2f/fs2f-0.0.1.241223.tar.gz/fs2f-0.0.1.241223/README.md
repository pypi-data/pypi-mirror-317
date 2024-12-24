# fs2f

## Description

The **fs2f** script is for taking snapshots of a file structure into a single file, similar to archiving without compression.

## Features

  - Create a snapshot file from a specified directory.
  - Restore the file structure from a snapshot file to a chosen directory.
  - Preserve information about the owner and access rights on UNIX-like systems.
  - List the files and directories stored in the snapshot file.
  - Verify file integrity using hash checks.
  - *Strict mode* aborts recovery in the event of a hash error.

## Installation

- from GitHub
  ```bash
  git clone https://github.com/codyverse/fs2f.git
  cd fs2f
  ```

- via PIP
  ```bash
  pip install fs2f
  ```

## Usage

Options:
```
  -h, --help        Show this help message and exit.
  -m                Create a file structure snapshot and save it to a file.
  -u                Restore a file structure snapshot from a file.
  -s                Disable strict mode (continue restoring despite file hash mismatches).
  -l snapshot_file  List files and directories stored in a file structure snapshot.
  -d directory      Path to the directory.
  -f snapshot_file  Path to the snapshot file.
```

### Examples

- Snapshot the entire file structure inside the `./folder/a` directory to the `file.fs` file:
  ```bash
  python3 fs2f.py -m -d ./folder/a -f file.fs
  ```
- Restore the file structure from the `file.fs` file to the `./folder/b` directory:
  ```bash
  python3 fs2f.py -u -d ./folder/b -f file.fs
  ```

- Display all files and directories saved within the `file.fs` file:
  ```bash
  python3 fs2f.py -l file.fs
  ```

## Contributing

Feel free to contribute by submitting issues or pull requests!
