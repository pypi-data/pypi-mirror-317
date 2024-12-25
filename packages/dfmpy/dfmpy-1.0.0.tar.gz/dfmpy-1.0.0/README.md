# dfm

[![pipeline](https://gitlab.com/deliberist/dfmpy/badges/main/pipeline.svg)](https://gitlab.com/deliberist/dfmpy/-/commits/main)
[![Build status](https://ci.appveyor.com/api/projects/status/gie9q4210vr7usf0?svg=true)](https://ci.appveyor.com/project/rbprogrammer/dfmpy)
[![codecov](https://codecov.io/gl/deliberist/dfmpy/branch/main/graph/badge.svg?token=8zT6EYk0if)](https://codecov.io/gl/deliberist/dfmpy)
[![pypi](https://img.shields.io/pypi/v/dfmpy.svg)](https://pypi.org/project/dfmpy)

Sometimes pronounced "_diff-em-py_" and is a small play on words.  dfm is yet
another Dot-Files Manager, but with robust features that can essentially
"_diff_" the dotfiles actually installed versus the expected installed files.
Hence the "_diff-em_".

dfm is not just another dotfiles manager, it supports multiple environments
based on hostname, system type, or a combination of the two.  It also ignores
files/directories based on user defined globs which can be particularly useful
if dfm has to traverse directories that have large I/O latencies (large
directory inodes, too many files to stat, or even just network mounted
directories, etc.).

## Installation

Since dfm is [registered on Pypi](https://pypi.org/project/dfm), you can install
dfm through standard `pip` methods.

```bash
python3 -m pip install --user --upgrade dfmpy
```

For more installation details, see
[INSTALLATION.md](https://gitlab.com/deliberist/dfmpy/blob/main/INSTALLATION.md).

## Config Files

To use dfm you must first `dfm init` which will create two files config
files:

1. `${XDG_CONFIG_HOME}/dfm/config.ini`
1. `${XDG_CONFIG_HOME}/dfm/ignore.globs`

where `${XDG_CONFIG_HOME}` is usually `~/.config`.  dfm uses
[xdgenvpy](https://pypi.org/project/xdgenvpy) to get a handle on the dfm config
directory.

`config.ini` is the main config file that tells it, among other things, where to
find your dotfiles repository, where to install symlinks, and even how to manage
identical filenames for different systems.

`ignore.globs` is a set of commonly ignored files and directories that one might
never want synced with their dotfiles repository.  For example, if you manage
your dotfiles repository with Git then you would never want the `.git` directory
symlinked to your destination directory.  And vice versa, you should never add
SSH keys (`~/.ssh/id_*`) to your dotfiles repo.  The globs in this file tell
dfm to just skip over the files or directories.

## Usage

dfm makes use of Python's
[argparse](https://docs.python.org/3/library/argparse.html) library sub-command
feature.  This gives dfm multiple independent commands with their own set of
CLI arguments.

### File suffixes

To maintain dotfiles across multiple systems there needs to be a mechanism that
allows for all the files to have the same name when install but not collide when
they reside in the repository.  To get around this dfm makes use of the system's
hostname and system type appended to the file name.

For example, developers may want a `~/.vimrc` in their home directory.  But in
the dotfiles repository we may want all vimrc files next to each other, i.e. in
the same directory.  dfm searches for a `##` marker in a file to determine if
the file has a system specific variant.  Suppose our dotfiles repo looks like
this:

```bash
cd ~/.files
tree
.
|-- .vimrc
|-- .vimrc##host1.Linux
|-- .vimrc##host2.Linux
|-- .vimrc##host2.Windows
|-- .vimrc##host3
`-- .vimrc##Windows

0 directories, 6 files
```

- `.vimrc` is the default vimrc file and will be the symlinked file if no other
    system specific file exists.

- `.vimrc##host1.Linux` is a system specific file that will only be symlinked if
    the hostname is "host1" and the system type is Linux.

- `.vimrc##host2.Linux` is a system specific file that will only be symlinked if
    the hostname is "host2" and the system type is Linux.

- `.vimrc##host2.Windows` is a system specific file that will only be symlinked
    if the hostname is "host2" and the system type is Windows.

- `.vimrc##host3` is a system specific file that will only be symlinked if the
    hostname is "host3".

- `.vimrc##Windows` is a system specific file that will only be symlinked if the
    system type is Windows.

The hostname is determined by the return value from
[socket.gethostname()](https://docs.python.org/3/library/socket.html#socket.gethostname),
and the system type is determined by the return value from
[platform.system()](https://docs.python.org/3/library/platform.html#platform.system).

### Common arguments

```bash
dfm --help
```

`-v` is the verbose flag, which can be used multiple times.  This flag controls
which log level gets printed.  The default log level is set to ERROR, which is
lowered to WARNING when one `-v` flag is set.  Multiple `-v` flags will lower
the log level even further.

`-i` turns on interactive mode.  dfm strives to be as filesystem safe as
possible.  By default it will not attempt to overwrite files.  The interactive
flag tells dfm to ask for permission when it performs a potentially dangerous
operation.

`-f` turns on force mode.  Again, dfm strives to be filesystem safe.  The
default commands will not overwrite files nor delete files without explicit user
direction.  While interactive mode can help with this, sometimes developers want
to just force an operation and live with the consequences.  Effectively, force
mode short circuits interactive mode and assumes the developers accepts the
operation that dfm is trying to perform (e.g. overwriting a file).

### Install dfm

```bash
dfm init --help
```

Currently, dfm requires initialization after installation.  We merely need to
run the `init` command.

```bash
python3 -m pip install --user --upgrade dfmpy
dfm init
```

Next, if you don't want to have your dotfiles repository under `~/.files/` then
you have one of two options:

1. Create a symlink, something like:
   `ln -s /home/user/.local/git/dotfiles/source/ ~/.files`.  Or
1. Update `~/.config/dfm/config.ini` and change the `repository_dir` property to
    point to your actual dotfiles repo.

### Sync your dotfiles

```bash
dfm sync --help
```

Once installed and initialized, dfm will utilize the
`${XDG_CONFIG_HOME}/dfm/config.ini` config file when it needs to (re)sync your
dotfiles.  Per the default `config.ini` file, dfm assumes your dotfiles repo is
initially located at `~/.local/share/dotfiles`.  If this is not the case, you
need to modify your `config.ini` accordingly.

```bash
dfm sync -f
```

The sync command will use the `dfm/config.ini` file to determine where the
dotfiles are installed and where the dotfiles repository is.  It will then
calculate a set of expected symlinks to files.  dfm uses this set to traverse
the installed dotfiles to determine what needs updating.

The sync command will create new symlinks to the expected files in the dotfiles
repository.  However, being filesystem safe, the sync command will not unlink
existing symlinks, nor overwrite existing symlinks.  Either interactive or force
mode is required to make such changes.

### Adding individual files

```bash
dfm add --help
```

Sometimes developers want to add a single file to their dotfiles repository.
dfm has an option to add the file from their home directory directly into their
dotfiles repository, then automatically symlink so a system specific file.

For example, let's say we needed to add our `~/.vimrc` file to our dotfiles.
The `$HOME` directory may look roughly like this:

```bash
ls -al ~
drwxr-xr-x 22 user user  4096 Nov 10 11:47 .
drwxr-xr-x  3 root root  4096 Apr 25  2019 ..
...
drwxr-xr-x 13 user user  4096 Jul  9 04:54 .cache
drwxr-xr-x 30 user user  4096 Nov 10 11:47 .config
drwx------  6 user user  4096 Nov 10 11:47 .local
-rw-------  1 user user    57 Oct 23 19:13 .vimrc
...
```

We can simply add the `~/.vimrc` file, and the developer's home directory will
look like this:

```bash
dfm add ~/.vimrc
ls -al ~
drwxr-xr-x 22 user user  4096 Nov 10 11:47 .
drwxr-xr-x  3 root root 4096 Apr 25  2019 ..
...
drwxr-xr-x 13 user user  4096 Jul  9 04:54 .cache
drwxr-xr-x 30 user user  4096 Nov 10 11:47 .config
drwx------  6 user user  4096 Nov 10 11:47 .local
lrwxrwxrwx  1 user user    28 Nov 10 11:47 .vimrc -> /home/user/.files/.vimrc##hostname.Linux
...
```

Under the hood, dfm is simply moving the file into the dotfiles repository with
the most restrictive system specific name.  Then it will create the symlink so
that `~/.vimrc` points to the repository file.

### Listing the installed (eg synced) files

```bash
dfm list --help
```

dfm has a unique insight into your dotfiles.  It knows how to ignore certain
files, it knows what files should be symlinked to others, and it knows when
there is a discrepancy with the installed files versus the dotfiles repo.  As
such, simple Bash `ls -R` or `tree` commands will not print just the dotfiles
managed by dfm.

dfm has a `list` command that prints only the files dfm manages, the files it
expects, and the files that might have broken symlinks.  The file listing also
adheres to dfm's log level conventions:

- **broken symlinks** (links to non-existent files) are logged at the CRITICAL
    level.
- **stale symlinks** (links to the wrong files) are logged at the ERROR level.
- **not installed symlinks** are logged at the WARNING level.
- and **proper symlinks** (links to the correct files) are logged at the INFO
    level.

Additionally, the list command has a `--tree` mode that changes the output into
a directory tree structure, rather than a strict list.
