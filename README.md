# Easyconda: A Conda Environment Management Tool

## Overview
Easyconda is a Python-based command-line tool designed to simplify the management of Conda environments. It allows users to easily backup, restore, install, and remove Conda environments. The tool is especially useful for those who frequently switch between different projects requiring separate environments or for those who want to keep their environments backed up and easily transferable.

## Features
- **Environment Backup**: Save your Conda environments as `.yml` files for easy restoration.
- **Environment Restore**: Easily restore environments from backup files.
- **Install Environments**: Install environments directly from the backup `.yml` files.
- **Remove Environments**: Safely remove environments from your system.
- **Environment Listing**: View all installed and backed up environments, including their status and size.

## Requirements
- Python 3.x
- Conda package manager installed

## Installation
Clone the repository:

```
git clone https://github.com/alexanderkrauck/easyconda.git
cd easyconda
```

## Usage
Run the script:

```./easyconda.py```


You will be presented with a command-line interface where you can choose to backup (`b`), install (`i`), remove (`r`), or backup and remove (`br`) environments. 

## Commands
- `(q)uit`: Exit the program.
- `(i)nstall [env_name]`: Install a specific environment by name.
- `(r)emove [env_name]`: Remove a specific environment by name.
- `(b)ackup [env_name]`: Backup a specific environment by name.
- `(br)backupremove [env_name]`: Backup and then remove a specific environment by name.
- You can perform actions on multiple environments simultaneously by listing their names separated by space.

## Configuration
You can modify the `envs_dir` variable in the script to change the default backup directory.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes or improvements.

## License
This project is licensed under the MIT License.

## Support
If you encounter any issues or have suggestions, please open an issue in the GitHub repository. 

---

Enjoy managing your Conda environments with Easyconda! 🐍🔧
