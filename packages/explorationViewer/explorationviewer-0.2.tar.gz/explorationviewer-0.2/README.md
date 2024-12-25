# ExplorationViewer

## Overview

This program provides an interactive HTML visualization platform for data
produced by the `exploration` module, most notably
`exploration.core.Exploration` and `explortion.core.DecisionGraph`
objects. It is partially based on the `dewlight` visualizer for literary
character interaction graphs.

## Dependencies:

Just Python version 3.10+ (might work on lower versions; probably not below
3.6). You will also need the `exploration` library (although a static
copy of that library is included and used for the web stuff).

## Installing

Just run `pip install explorationViewer`. This will install several dozen
megabytes of `pyodide` support files since the viewer uses
Python-in-the-browser.

## Getting Started:

Running `python -m explorationViewer` should launch a web server and via
that open the viewer HTML file in your default web browser. It will load an
example exploration but you can use the in-page controls to load another
file of your choice.

TODO: Support providing a filename on the command line.

## Changelog

- v0.2 alpha version with extremely basic functionality.
- v0.1 Initial pre-alpha upload.
