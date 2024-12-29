# BkMeUp

**BkMeUp** provides shell config file archive and backup functionality

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **bkmeup**.

```bash
pip install bkmeup
```

## CLI Utility

The following CLI is provided in this package.

```bash
╰─ bkmeup -h                                                                                                                             ─╯
usage: bkmeup [-h] [--version] {show.env.info,show.dflt.bkup.list,create.archive} ...

-.-.-. BkMeUp Shell Config archiver & bkup!

positional arguments:
  {show.env.info,show.dflt.bkup.list,create.archive}
    show.env.info       show system environment info
    show.dflt.bkup.list
                        show list of default items to archive/bkup
    create.archive      accumulate shell config files if they exist and archive them

options:
  -h, --help            show this help message and exit
  --version             top-level package version

-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
```


## License

[MIT](https://choosealicense.com/licenses/mit/)

