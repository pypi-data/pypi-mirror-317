"""
This code is requested by the viewer index.html file and then run
directly in pyodide to set up and control the visualizer.

It both contains the initialization code and related support functions
for interfacing between the `exploration.viewer` module and the
javascript in the viewer page.
"""

import time

# Get start time so we can measure how long it takes to load pyodide T_T
start = time.time()

# Import pyodide stuff
import js  # type: ignore
import pyodide_js  # type: ignore
import micropip  # type: ignore

js.console.log("Python setup running...")

# We'll load this module during setup & replace this None.
exploration = None

# Global variable to hold the current exploration. Accessible in
# Javascript via pyodide.globals.EXPLORATION
EXPLORATION = None;

def receiveData(dataStr):
    """
    Function to call when we are loading a new exploration. Gets the raw
    JSON string for the exploration file.
    """
    global EXPLORATION
    # Parse data
    js.notifyWait("parsing");
    js.console.log("Receiving new data...")
    parsed = exploration.parsing.fromJSON(dataStr)
    js.notifyWaitDone("parsing");
    # If we got a DecisionGraph, make that into a 1-step exploration
    if isinstance(parsed, exploration.DecisionGraph):
        exp = exploration.DiscreteExploration.fromGraph(parsed)
    elif isinstance(parsed, exploration.DiscreteExploration):
        exp = parsed
    else:
        # TODO: Journal parsing option here?
        # Note: could check for initial '{' above... ?
        raise ValueError(
            f"Loaded a {type(parsed)} from incoming data, but we don't"
            f" know how to convert that into a DiscreteExploration."
        )

    # Load into global variable
    EXPLORATION = exp
    js.console.log("Loaded exploration object.");

    # Perform setup to add extra info to exploration

    # Attach full analysis results to the exploration object
    js.notifyWait("analyzing");
    exp.analysis = exploration.analysis.runFullAnalysis(exp)

    # Set final & path positions on the exploration object
    exploration.display.setFinalPositions(exp)
    exploration.display.setPathPositions(exp)
    exploration.display.setBaryeccentricPositions(exp)
    js.notifyWaitDone("analyzing");

    # Let javascript know it has changed
    js.newExploration(exp)


async def setupExploration():
    """
    Setup function which loads initial data and gets things started.
    May take multiple *seconds* as it has to install the exploration
    module from its wheel.
    """
    # Ensure module is available throughout file when we import it
    global exploration
    js.console.log("Setting up exploration support...")
    await micropip.install("pyodide/exploration-0.7.5-py3-none-any.whl")
    # await pyodide_js.loadPackage("exploration")
    import exploration
    js.console.log(
        f"Installed exploration module version"
        f" {exploration.__version__}..."
    )
    elapsed = (time.time() - start)
    js.console.log("Done loading exploration module.")
    js.console.log("Python setup took " + str(elapsed) + " seconds.");
    js.notifyWaitDone("loading")
    js.PYODIDE_READY = True

    # Default target: example file
    dataFile = "example.exp"
    # dataFile = "diwl_Peter.dcg"
    # dataFile = "htr_Peter.dcg"

    # If there's a ?t= search param, use that instead
    url = js.URL.new(js.window.location.href)
    target = url.searchParams.get('t')
    if target:
        dataFile = target

    # If inline data is defined in the file and there's no specified
    # target, use the inline data
    if not target and js.inlineData:
        js.console.log("Loading inline data by default...")
        receiveData(js.inlineData)

    else:
        # Otherwise load the default or specified target data file
        js.console.log(f"Loading data from {dataFile!r}...")

        # This is also async: fetch file & load data when it's fetched
        # TODO: Update example.exp datafile to current format!!!
        receiveData(await js.d3.text(dataFile))

# Actually call our setup function to kick things off
setupExploration()
