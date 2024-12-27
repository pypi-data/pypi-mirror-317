# F2 Commander

F2 Commander is an orthodox file manager for the modern world.

![F2 Commander Showcase](docs/img/f2.png "F2 Commander Showcase")

## Installation

From PyPI:

    pipx install f2-commander

From source:

    poetry build
    pipx install [--force] dist/f2_commander-0.4.1.tar.gz

This software is designed to work in Linux and macOS. It should also work in
WSL (Windows Subsystem for Linux).

## Usage

 - Start by running `f2` in your terminal emulator
 - Hit `?` to see the built-in help
 - Hit `q` to quit

## About

F2 Commander exists to bring the experience of an orthodox file manager into
the world of modern computing.

A "file system" can be anything that can seem to contain files and directories,
(a local disk, a BLOB storage, a Cloud drive, a compressed file, etc.).

Finally, it is designed to be discoverable: making file systems easy to
navigate, and making the F2 Commander itself obvious to use.

F2 Commander is an overgrown personal project, may contain bugs, and is
provided "as is", without warranty of any kind.

## Features

Below is a short summary. For a complete list of features, existing and
planned, see the [complete feature list](docs/features.md). Some features are a
work-in-progress as indicated below.

 - [x] Works in Linux, macOS
 - [ ] Works in WSL (should work, but to be extensively tested)
 - [x] An orthodox two-panel interface with a footer menu
 - [x] Vi-like key bindings
 - [ ] Classic Fn key bindings, and configurable key bindings
 - [x] Command Palette (Ctrl-P)
 - [x] Rich and flexible file listing (file attributes, ordering options,
       filtering with glob, hidden files toggle, compute directory size,
       and more)
 - [x] Incremental search (type to search, fuzzy matching)
 - [ ] Recursive file search. Find in (text) files.
 - [x] Integration with native OS applications (open a directory in a file
       manager, open a file with a default program)
 - [x] File and directory manipulation (copy, move, move to trash,
   etc.)
 - [x] Multiple file selection
 - [x] View and edit files
 - [x] Configurable bookmarks. Quick "Go to path".
 - [x] Preview panel
 - [x] Drop to shell
 - [x] User-level configuration file
 - [x] Extensive "Remote File systems" support. A non-extensive list
       includes: AWS S3, GCP GCS, Azure ADLS, OCI, OSS, DVC, LakeFS, HDFS,
       Dropbox, Google Drive, FTP/FTPS, SFTP, SMB, WebDAV, and many more.
       Custom implementations are possible through other
       [fsspec](https://github.com/fsspec/filesystem_spec) implementations and
       plugins. \*\*See also the note below.
 - [x] Read and extract ZIP files
 - [ ] Create and update ZIP files
 - [ ] Read and extract other archives and compressed files. A non-exhaustive
       list includes: ZIP, TAR, XAR, LHA/LZH, ISO 0660 (optical disc files),
       cpio, mtree, shar, ar, pax, RAR, MS CAB, 7-Zip, WARC, and more are
       supported in **read-only** mode (can be listed, viewed, extracted) -
       everything supported by [libarchive](https://github.com/libarchive/libarchive).
 - [x] Multiple color themes
 - [x] Built-in help

> \*\*Note: Remote file systems are in *preview*. All features are available,
> but not extensively tested. Connection configurations are not persisted,
> connection dialog is rough on the edges, but functional.

And, hopefully, a polished up user experience that you'd normally expect from
a robust file manager. Feel free to submit any issues to make F2 Commander
even better!

See also a [list of known bugs](docs/testing.md).

## Development environment

This project uses Poetry for dependency management and as a build tool. The
configuration is conventional, use as usual:

    poetry install --with dev

It also uses black, flake8, isort, mypy and pytest. An IDE or an LSP should
pick up their configuration, or they can be executed with poetry. For example:

    poetry run pytest

To run all code quality controls and linters:

    ./check

To run the application from source code:

    poetry run f2

To run the application with dev tools:

    poetry run textual console [-v -x SYSTEM -x EVENT -x DEBUG -x INFO]  # this first!
    poetry run textual run --dev f2.app:F2Commander

To run tests in all target Python versions (typically before a release):

    pipx install nox
    nox [-r]  # -r == --reuse-existing-virtualenvs

## About (continued)

"F2" is a loose interpretation of "a **F**ile manager with **2** side-by-side
panels", and "Commander" is an homage to the old-school orthodox file managers.

"F2 Commander" is a personal project that has grown into a full-fledged file
manager and is now open-sourced. Being a personal project means that:
a) my intent is to continue the development of the features outlined above, but
   the development and bug fixing may be irregularly-paced and priorities may
   shift;
b) my intent is to keep F2 Commander stable, but future versions may include
   backward-incompatible changes where that would seem pragmatic.

## Special Thanks

F2 Commander is made with [Textual](https://github.com/textualize/textual/)
framework, [fsspec](https://github.com/fsspec/filesystem_spec) and other great
packages. Many features are made possible or stem directly from these, and I
encourage F2 Commander users to support them.

## Contributions

Bug reports, feature requests and pull requests are welcome.

If you plan to contribute to the source code, see the "Development environment"
above and, please, note that:

 - contributed source code must pass the `./check`,
 - in this repository, contributed source code is only accepted under Mozilla
   Public License 2.0 and should include according file headers.

## License

This application is provided "as is", without warranty of any kind.

Mozilla Public License, v. 2.0.
