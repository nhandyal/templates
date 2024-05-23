# Python Simple
A simple project structure to get started with a python project

Contains
- code quality utils (typecheckers, linters, etc)
- base project structure

## Getting Started
Use the script init_project to initialize a target folder with the python_simple template
```
rsync -v --progress --exclude='.git' ./ abs/path/to/target/project_root
```

## Using Poetry
- https://python-poetry.org/docs/basic-usage/
```
# activates the virtual env that poetry installs dependencies to
# this is a subshell
poetry shell

# exit the virtual env
exit
```