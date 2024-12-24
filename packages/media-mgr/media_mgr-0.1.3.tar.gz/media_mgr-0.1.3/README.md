# Media-Mgr

**Media-Mgr** helps organize and search for media files on specified servers. Focus is currently PLEX based and includes PLEX server upgrade support on Ubuntu installs.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **media-mgr**.

```bash
pip install media-mgr
```

## CLI Controls

The following CLI controls are provided in this package for keeping track of media server categories and media server coordinates.

* mm-mediacfg
* mm-srvcfg

The following CLI controls assist with media server contents for search, organization, PLEX upgrades and miscellaneous tools (EXIF renamer)

* mm-util
* mm-path
* mm-search
* mm-gather
* mm-exif
* mm-plex-upg

Finally, these next sets of CLI controls are task specific for media management

* mount-drives
* search-plex
* move-plex
* cons-plex
* upgrade-plex
* upgrade-plex-all

Each command has help syntax via CLI -h argument

For example:

```bash
╰─ mount-drives -h
usage: mount-drives [-h] [--ipv4 <ipv4.addr>]

-.-.-. Mount Drives on Server utility

options:
  -h, --help          show this help message and exit
  --ipv4 <ipv4.addr>  Server IPV4

-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
```

or

```bash
╰─ mm-gather -h
usage: mm-gather [-h] [-d] [--version]
                 {show.titles,show.all.titles,show.bundles,store.bundles,show.plex.n.worker.bundles,store.plex.n.worker.bundles}
                 ...

-.-.-. Gathering for media manager

positional arguments:
  {show.titles,show.all.titles,show.bundles,store.bundles,show.plex.n.worker.bundles,store.plex.n.worker.bundles}
    show.titles         Show retrieved titles
    show.all.titles     Show ALL retrieved titles
    show.bundles        Show title bundles
    store.bundles       Store title bundles
    show.plex.n.worker.bundles
                        Show title bundles for Plex and Worker servers
    store.plex.n.worker.bundles
                        Store title bundles for Plex and Worker servers

options:
  -h, --help            show this help message and exit
  -d, --debug           run with debug hooks enabled
  --version             top-level package version

-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
```


## License

[MIT](https://choosealicense.com/licenses/mit/)

