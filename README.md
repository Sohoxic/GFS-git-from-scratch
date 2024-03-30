# GFS: Git From Scratch

## Overview

GFS: Git From Scratch is a Python-based project aimed at recreating core functionalities of the Git version control system from the ground up. Designed for educational purposes, lightweight Git needs, or as a foundation for more complex Git-based tools, GFS provides a minimalist yet powerful interface for managing Git repositories. By leveraging Python's standard libraries such as `argparse` for command-line parsing, `hashlib` for cryptographic hashing, and `zlib` for data compression, GFS offers a unique blend of simplicity and efficiency in manipulating Git objects and automating version control processes.

## Key Features

- **Core Git Operations:** Supports essential operations such as commit, push, and status checks, tailored for direct interaction with GitHub repositories.
- **Git Object Handling:** Directly manipulate blobs, trees, and commits, offering a hands-on approach to understanding Git's internal mechanisms.
- **SHA-1 Object Storage:** Utilizes SHA-1 hashing to ensure the integrity and uniqueness of repository data, mirroring Git's own storage strategies.
- **Streamlined CLI:** Incorporates `argparse` for an intuitive command-line interface, enabling easy integration with scripts or automation tools.
- **Efficient Compression:** Employs `zlib` for compressing data, optimizing storage efficiency and facilitating faster network transfers.
- **Network Synchronization:** Implements network communication protocols for efficient synchronization between local and remote repositories.

## Getting Started

### Installation

Clone GFS: Git From Scratch to your local machine:

```
git clone https://github.com/Sohoxic/GFS-git-from-scratch.git
```

Change to the project directory:

```
cd GFS-git-from-scratch
```

GFS requires Python 3.6 or newer. Dependencies are minimal, relying on standard Python libraries.

### Basic Usage

**Initialize a Repository:**

```
python3 gfs.py init <repository_name>
```

**Stage Files for Commit:**

```
python3 gfs.py add <file1> <file2> ...
```

**Commit Changes:**

```
python3 gfs.py commit -m "Commit message" -a "Author Name <author@example.com>"
```

**Push to GitHub:**

```
python3 gfs.py push <GitHub_repo_url> -u <GitHub_username> -p <GitHub_password>
```

**Check Repository Status:**

```
python3 gfs.py status
```

<img src="https://github.com/Sohoxic/GFS-git-from-scratch/blob/main/assets/images/cli.png">

## License

This project is made available under the MIT License. For more details, see the LICENSE file.

## Contributing

I welcome contributions to GFS: Git From Scratch! If you have improvements or bug fixes, please fork the repository, make your changes, and submit a pull request. For significant changes or new features, open an issue first to discuss what you would like to contribute.

---
GFS: Git From Scratch provides a foundational toolkit for those looking to dive deeper into Git's core functionalities, develop Git-based applications, or simply require a lightweight tool for basic Git operations.
