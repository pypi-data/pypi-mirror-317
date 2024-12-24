"""
- Authors: Peter Mawhorter
- Consulted:
- Date: 2023-7-14
- Purpose: Serve HTML pages that can be used to analyze Exploration
    objects, including visualizing the graphs & filtering/searching for
    stuff.

This is based on the `dewlight` library for visualizing conversation
graphs, but tweaks things to work better for exploration graphs, and to
include a lot of exploration-graph-specific features. Also uses pyiodide to
invoke the exploration library within the browser, instead of just using it
for preprocessing. This module mainly deals with launching a webserver
and opening a browser tab; the core functionality is in the
`explorationViewer.viewer` module, and in the `viewer/index.html` file.

When you run this file, (e.g., by running `python -m explorationViewer`)
it will write 'redirect.html' and 'explorationViewer.html' files in the
current directory, and launch a web server serving files from the current
directory, plus it will open a browser tab that follows the redirect to
show you the viewer file. Use control-C to stop the server when you're
done.
"""

from typing import (
    Tuple, TextIO, Literal, TypeAlias
)

import importlib.resources

import os, webbrowser, http.server

FileSpec: 'TypeAlias' = Tuple[Literal["file"], str]
"""
Specifies a file to load, relative to current working directory unless an
absolute path is used.
"""
ResourceSpec: 'TypeAlias' = Tuple[Literal["resource"], str, str]
"""
Specifies a resource to load using importlib.resources. Includes the
module name and then the file within that module. The resource will be
loaded as text using:

```py
importlib.resources.files(<module>).joinpath(<file>).read_text()
```
"""

AnySource: 'TypeAlias' = FileSpec | ResourceSpec | TextIO
"""
Either a file-on-disk or a package-relative resource to load or write to
(can only write to files).
"""


def loadSource(source: AnySource) -> str:
    """
    Loads the content of an `AnySource` as a string.
    """
    if isinstance(source, tuple):
        if source[0] == "resource":
            # Must be a ResourceSpec
            return importlib.resources.files(
                source[1]
            ).joinpath(source[2]).read_text()
        elif source[0] == "file":
            # Must be a FileSpec
            with open(source[1], 'r') as fileInput:
                return fileInput.read()
        else:
            raise TypeError(
                f"Source tuple started with invalid type specifier"
                f" {repr(source[0])}"
            )
    else:
        return source.read()


def escapeHTML(help):
    """
    Custom escaper for the help HTML.
    """
    # TODO: Worry about escaped double quotes in help string?
    return help.replace('"', '\\"').replace('\n', ' ')


def bundleViewer(
    outStream: TextIO,
    html: AnySource = ("resource", "explorationViewer.viewer", "index.html"),
    helpText: AnySource = ("resource", "explorationViewer.viewer", "help.html"),
    data: AnySource = ("resource", "explorationViewer.viewer", "example.exp"),
    d3: AnySource = ("resource", "explorationViewer.viewer", "d3.v7.min.js"),
    title: str = "Exploration Viewer"
):
    """
    Given an output stream (e.g., an open file), and a few pieces to
    assemble together, this function bundles things up and writes a single
    standalone HTML+CSS+JS file to the given output stream. Defaults are
    available, but it accepts:

    - a base HTML source (default 'viewer/index.html'),
    - a data file in '.exp'/JSON format (e.g., as produced by using
        `core.exploration.save`; default 'viewer/example.exp'),
    - a copy of JS code for the `d3` visualization library (possibly
        minified, default 'viewer/d3.v7.min.js'),
    - a custom title for the page (default is 'Exploration Viewer')
    """
    htmlSource = loadSource(html)
    helpSource = loadSource(helpText)
    dataSource = loadSource(data)
    d3Source = loadSource(d3)

    result = ''
    for line in htmlSource.split('\n'):
        if line == '    <title>Exploration Viewer</title>':
            result += f'    <title>{title}</title>\n'
        elif line == 'inlineHelp = undefined;':
            result += f'inlineHelp = "{escapeHTML(helpSource)}";\n'
        elif line == 'inlineData = undefined;':
            result += f'inlineData = {dataSource};\n'
        elif line == '    <script src="d3.v7.min.js"></script>':
            result += f"<script type='text/javascript'>\n{d3Source}\n</script>"
        else:
            result += line + '\n'

    outStream.write(result)


def fileURL(path):
    """
    Returns the file:// URL for the path or pathlib.Path object `path`.
    """
    abs = os.path.abspath(str(path))
    drive, tail = os.path.splitdrive(abs)
    tail = tail.lstrip('/').lstrip('\\')
    return 'file:///' + '/'.join(os.path.split(tail))


if __name__ == "__main__":
    # TODO: More CLI interface here

    # Figure out server address & url for file on server
    port = 8456
    # Note: it's important not to serve outside localhost
    serverAddress = ('127.0.0.1', port)
    url = f'http://127.0.0.1:{port}/'

    # Abstract traversable for viewer dir
    viewerDirAbs = importlib.resources.files('explorationViewer') / 'viewer'
    # Use 'as_file' to ensure it's a directory, possibly creating a temp
    # dir from unizpped resources:
    with importlib.resources.as_file(viewerDirAbs) as viewerDir:
        # Get file:// url for redirect file (we're opening it *before*
        # launching the HTTP server)
        redirURL = fileURL(viewerDir / "redirect.html")
        print(redirURL)

        # Change into the viewer directory & back afterwards
        here = os.getcwd()
        try:
            os.chdir(viewerDir)

            # Start to open the browser tab for the redirect file, giving us ~2
            # seconds to get the server online
            webbrowser.open(redirURL)

            # Now launch the server & serve forever
            print("Launching web server. Press control-C to shut it down...")
            httpd = http.server.HTTPServer(
                serverAddress,
                http.server.SimpleHTTPRequestHandler
            )
            httpd.serve_forever()

        finally:
            os.chdir(here)
