# getignore
A lightweight solution to retrieve gitignore templates from [Github's gitignore templates repo](https://github.com/github/gitignore)

## Installation
### Build from source
You can build the project from source by following these commands:

#### Linux & macOS
    git clone https://github.com/catneep/getignore.git
    cd getignore
    python3 -m venv venv
    source venv/bin/activate
    pip install requirements.txt

#### Windows (Powershell)
    git clone https://github.com/catneep/getignore.git
    Set-Location getignore
    py -m venv venv
    . venv/scripts/activate
    pip install requirements.txt

## Usage
#### Linux & macOS
    python3 getignore.py -{option} {name}
#### Windows
    py getignore.py -{option} {name}
Options:

- **h** or **--help**: Display help
- **r**: Retrieve from the root of the repo (Used by default)
- **c**: Retrieve from the *"community"* directory
- **g**: Retrieve from the *"Global"* directory
- **l**: Retrieve from local cache (Uses "root" as a remote fallback)

### Examples

- Python gitignore template

        python3 getignore.py python

- C# gitignore template

        python3 getignore.py c#

- Fortran gitignore template

        python3 getignore.py fortran

This will output the contents of the template, to save into a new file you can do the following:

    python3 getignore.py typescript > .gitignore

Or append to an existing gitignore:

    python3 getignore.py typescript >> .gitignore
