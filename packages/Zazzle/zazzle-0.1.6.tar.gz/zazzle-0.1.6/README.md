# Zazzle

[![Documentation Status](https://readthedocs.org/projects/zazzle/badge/?version=latest)](https://zazzle.readthedocs.io/en/latest/?badge=latest)

Zazzle is a module designed to make the process of creating, managing, and reading log files easier. 

# Installation

There are two ways to install Zazzle.

### Pip installation

```bash
pip install zazzle
```

### Manual installation

- Clone the repositiory, or download and unzip it.
- CD to the cloned/downloaded directory.
```bash
$ cd path/to/downloaded/repository
```

- Once you're in the main folder, run the below command.
```bash
$ python setup.py install
```

# Quick start
```python
import zazzle

# This only needs to be run once, and should be run after running any configuration methods you need.
zazzle.configure_logger()

# zazzle.log(log_level(int), log_message(string))
zazzle.log(1, "Hello world!")
```

This two-liner will produce a log in the following directory with the current date as the file name. The log will contain a single 'INFO' level log message. Levels 0-4 can be used here.

```bash
"C:\Users\'current user'\Documents\Zazzle\Y-M-D.log"
```

```bash
| INFO     |    Hello world!
```

This file output can be further customized with the following methods. I recommend running these in the 'if __name__ == '__main__'' check of your top __init__ file. This way your entire program will have access to the directory/name combo you're using, and you won't have to set it at the start of all your functions.

```python
if __name__ == "__main__":
    zazzle.set_log_directory("directory/you/want/to/use")
    zazzle.set_log_file_name("name_of_log")

    # Run the rest of your program here
```