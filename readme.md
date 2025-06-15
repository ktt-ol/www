# Website of the Hackspace Oldenburg / Mainframe / Kreativität trifft Technik e.V.

# Todo

- Add Event Calendar
    - Upcoming Events on the sidebar
- Make taxonomy listings more easily accessible

# Potential Improvements

- Rename spacewalk to rooms
- Move space status to top on mobile

# Development

You'll need [zola](https://www.getzola.org/) for generating the static site and
Python for generating the photo albums. You may install the tools locally or use
the provided `nix` devshell.

Run `zola serve` to build the site and run a local server:

```sh
$ zola serve
Building site...
Checking all internal links with anchors.
> Successfully checked 1 internal link(s) with anchors.
-> Creating 114 pages (0 orphan) and 41 sections
Done in 789ms.

Listening for changes in /./{config.toml,content,sass,static,templates}
Press Ctrl+C to stop

Web server is available at http://127.0.0.1:1111 (bound to 127.0.0.1:1111)
```

The production site is built and deployed using GitHub Actions.

To generate the IFS pages and albums, run the following Python scripts:

```sh
python3 ifs.py
python3 albums.py
```
