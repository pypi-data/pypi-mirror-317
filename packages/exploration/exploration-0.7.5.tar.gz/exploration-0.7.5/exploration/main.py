"""
- Authors: Peter Mawhorter
- Consulted:
- Date: 2022-10-15
- Purpose: Main API entry points to support the `__main__.py` script.
"""

from __future__ import annotations

import argparse
import pathlib
import textwrap
import sys
import csv
import json
import time

# Resource module not available in Pyodide
try:
    import resource
except Exception:
    resource = None  # type: ignore

import networkx as nx  # type: ignore

from typing import (
    Literal, Optional, Union, get_args, TypeAlias, List, Callable, Dict,
    Sequence, Any, cast, Tuple, Set, Collection
)

from . import journal
from . import core
from . import base
from . import analysis
from . import parsing


#------------#
# File input #
#------------#

SourceType: TypeAlias = Literal[
    "graph",
    "dot",
    "exploration",
    "journal",
]
"""
The file types we recognize.
"""


def determineFileType(filename: str) -> SourceType:
    if filename.endswith('.dcg'):
        return 'graph'
    elif filename.endswith('.dot'):
        return 'dot'
    elif filename.endswith('.exp'):
        return 'exploration'
    elif filename.endswith('.exj'):
        return 'journal'
    else:
        raise ValueError(
            f"Could not determine the file type of file '{filename}':"
            f" it does not end with '.dcg', '.dot', '.exp', or '.exj'."
        )


def loadDecisionGraph(path: pathlib.Path) -> core.DecisionGraph:
    """
    Loads a JSON-encoded decision graph from a file. The extension
    should normally be '.dcg'.
    """
    with path.open('r', encoding='utf-8-sig') as fInput:
        return parsing.loadCustom(fInput, core.DecisionGraph)


def saveDecisionGraph(
    path: pathlib.Path,
    graph: core.DecisionGraph
) -> None:
    """
    Saves a decision graph encoded as JSON in the specified file. The
    file should normally have a '.dcg' extension.
    """
    with path.open('w', encoding='utf-8') as fOutput:
        parsing.saveCustom(graph, fOutput)


def loadDotFile(path: pathlib.Path) -> core.DecisionGraph:
    """
    Loads a `core.DecisionGraph` form the file at the specified path
    (whose extension should normally be '.dot'). The file format is the
    GraphViz "dot" format.
    """
    with path.open('r', encoding='utf-8-sig') as fInput:
        dot = fInput.read()
        try:
            return parsing.parseDot(dot)
        except parsing.DotParseError:
            raise parsing.DotParseError(
                "Failed to parse Dot file contents:\n\n"
              + dot
              + "\n\n(See error above for specific parsing issue.)"
            )


def saveDotFile(path: pathlib.Path, graph: core.DecisionGraph) -> None:
    """
    Saves a `core.DecisionGraph` as a GraphViz "dot" file. The file
    extension should normally be ".dot".
    """
    dotStr = parsing.toDot(graph, clusterLevels=[])
    with path.open('w', encoding='utf-8') as fOutput:
        fOutput.write(dotStr)


def loadExploration(path: pathlib.Path) -> core.DiscreteExploration:
    """
    Loads a JSON-encoded `core.DiscreteExploration` object from the file
    at the specified path. The extension should normally be '.exp'.
    """
    with path.open('r', encoding='utf-8-sig') as fInput:
        return parsing.loadCustom(fInput, core.DiscreteExploration)


def saveExploration(
    path: pathlib.Path,
    exploration: core.DiscreteExploration
) -> None:
    """
    Saves a `core.DiscreteExploration` object as JSON in the specified
    file. The file extension should normally be '.exp'.
    """
    with path.open('w', encoding='utf-8') as fOutput:
        parsing.saveCustom(exploration, fOutput)


def loadJournal(path: pathlib.Path) -> core.DiscreteExploration:
    """
    Loads a `core.DiscreteExploration` object from a journal file
    (extension should normally be '.exj'). Uses the
    `journal.convertJournal` function.
    """
    with path.open('r', encoding='utf-8-sig') as fInput:
        return journal.convertJournal(fInput.read())


def saveAsJournal(
    path: pathlib.Path,
    exploration: core.DiscreteExploration
) -> None:
    """
    Saves a `core.DiscreteExploration` object as a text journal in the
    specified file. The file extension should normally be '.exj'.

    TODO: This?!
    """
    raise NotImplementedError(
        "DiscreteExploration-to-journal conversion is not implemented"
        " yet."
    )


def loadSource(
    path: pathlib.Path,
    formatOverride: Optional[SourceType] = None
) -> Union[core.DecisionGraph, core.DiscreteExploration]:
    """
    Loads either a `core.DecisionGraph` or a `core.DiscreteExploration`
    from the specified file, depending on its file extension (or the
    specified format given as `formatOverride` if there is one).
    """
    if formatOverride is not None:
        format = formatOverride
    else:
        format = determineFileType(str(path))

    if format == "graph":
        return loadDecisionGraph(path)
    if format == "dot":
        return loadDotFile(path)
    elif format == "exploration":
        return loadExploration(path)
    elif format == "journal":
        return loadJournal(path)
    else:
        raise ValueError(
            f"Unrecognized file format '{format}' (recognized formats"
            f" are 'graph', 'exploration', and 'journal')."
        )


#---------------------#
# Analysis tool lists #
#---------------------#

CSVEmbeddable: TypeAlias = Union[None, bool, str, int, float, complex]
"""
A type alias for values we're willing to store in a CSV file without
coercing them to a string.
"""


def coerceToCSVValue(result: Any) -> CSVEmbeddable:
    """
    Coerces any value to one that's embeddable in a CSV file. The
    `CSVEmbeddable` types are unchanged, but all other types are
    converted to strings via `json.dumps` if possible or `repr` if not.
    """
    if isinstance(result, get_args(CSVEmbeddable)):
        return result
    else:
        try:
            return json.dumps(result)
        except Exception:
            return repr(result)


#---------------#
# API Functions #
#---------------#

def show(
    source: pathlib.Path,
    formatOverride: Optional[SourceType] = None,
    step: int = -1
) -> None:
    """
    Shows the graph or exploration stored in the `source` file. You will
    need to have the `matplotlib` library installed. Consider using the
    interactive interface provided by the `explorationViewer` module
    instead. The file extension is used to determine how to load the data,
    although the `--format` option may override this. '.dcg' files are
    assumed to be decision graphs in JSON format, '.exp' files are assumed
    to be exploration objects in JSON format, and '.exj' files are assumed
    to be exploration journals in the default journal format. If the object
    that gets loaded is an exploration, the final graph for that
    exploration will be displayed, or a specific graph may be selected
    using `--step`.
    """
    obj = loadSource(source, formatOverride)
    if isinstance(obj, core.DiscreteExploration):
        obj = obj.getSituation(step).graph

    import matplotlib.pyplot # type: ignore

    # This draws the graph in a new window that pops up. You have to close
    # the window to end the program.
    nx.draw(obj)
    matplotlib.pyplot.show()


def transitionStr(
    exploration: core.DiscreteExploration,
    src: base.DecisionID,
    transition: base.Transition,
    dst: base.DecisionID
) -> str:
    """
    Given an exploration object, returns a string identifying a
    transition, incorporating the final identity strings for the source
    and destination.
    """
    srcId = analysis.finalIdentity(exploration, src)
    dstId = analysis.finalIdentity(exploration, dst)
    return f"{srcId} → {transition} → {dstId}"


def printPerf(analyzerName: str) -> None:
    """
    Prints performance for the given analyzer to stderr.
    """
    perf = analysis.ANALYSIS_TIME_SPENT.get(analyzerName)
    if perf is None:
        raise RuntimeError(
            f"Missing analysis perf for {analyzerName!r}."
        )
    unit = analysis.ALL_ANALYZERS[analyzerName]._unit
    call, noC, tc, tw = perf.values()
    print(
        f"{analyzerName} ({unit}): {call} / {noC} / {tc:.6f} / {tw:.6f}",
        file=sys.stderr
    )


def printMem() -> None:
    """
    Prints (to stderr) a message about how much memory Python is
    currently using overall.
    """
    if resource is not None:
        used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print(f"Using {used} memory (bytes or kilobytes, depending on OS)")
    else:
        print(
            f"Can't get memory usage because the resource module is not"
            f" available."
        )
    # TODO: This is apparently kilobytes on linux but bytes on mac?


def analyze(
    source: pathlib.Path,
    destination: Optional[pathlib.Path] = None,
    formatOverride: Optional[SourceType] = None,
    applyTools: Optional[Collection[str]] = None,
    finalOnly: Optional[Collection[str]] = None,
    includeAll: bool = False,
    profile: bool = False
) -> None:
    """
    Analyzes the exploration stored in the `source` file. The file
    extension is used to determine how to load the data, although this
    may be overridden by the `--format` option. Normally, '.exp' files
    are treated as JSON-encoded exploration objects, while '.exj' files
    are treated as journals using the default journal format.

    This applies a number of analysis functions to produce a CSV file
    showing per-decision-per-step, per-decision, per-step, and
    per-exploration metrics. A subset of the available metrics may be
    selected by passing a list of strings for the `applyTools` argument.
    These strings should be the names of functions in `analysis.py` that
    are decorated with `analysis.analyze`. By default, only those not
    marked with `analysis.elide` will be included. You can set
    `includeAll` to `True` to include all tools, although this is ignored
    when `applyTools` is not `None`. `finalOnly` specifies one or more
    tools to only run on the final step of the exploration rather than
    every step. This only applies to tools whose unit of analysis is
    'step', 'stepDecision', or 'stepTransition'. By default those marked
    as `finalOnly` in `analysis.py` will be run this way. Tools excluded
    via `applyTools` or by default when `includeAll` is false won't be
    run even if specified in `finalOnly`. Set `finalOnly` to `False` to
    run all selected tools on all steps without having to explicitly
    list the tools that would otherwise be restricted by default.

    Set `profile` to `True` to gather and report analysis time spent
    results (they'll be printed to stdout).

    If no output file is specified, the output will be printed out.
    """
    if profile:
        print("Starting analysis with profiling...", file=sys.stderr)
        parseStart = time.perf_counter()
        printMem()
    # Load our source exploration object:
    obj = loadSource(source, formatOverride)
    if isinstance(obj, core.DecisionGraph):
        obj = core.DiscreteExploration.fromGraph(obj)
    if profile:
        elapsed = time.perf_counter() - parseStart
        print(f"Parsed input in {elapsed:.6f}s...", file=sys.stderr)
        printMem()

    exploration: core.DiscreteExploration = obj

    # Set up for profiling
    if profile:
        analysis.RECORD_PROFILE = True
    else:
        analysis.RECORD_PROFILE = False

    # Figure out which to apply
    if applyTools is not None:
        toApply: Set[str] = set(applyTools)
    else:
        toApply = set(analysis.ALL_ANALYZERS.keys())
        if not includeAll:
            print("ELIDING:", analysis.ELIDE, file=sys.stderr)
            toApply -= analysis.ELIDE

    if finalOnly is False:
        finalOnly = set()
    elif finalOnly is None:
        finalOnly = analysis.FINAL_ONLY

    # Group analyzers by unit
    byUnit = analysis.analyzersByUnit(toApply)

    # Apply all of the analysis functions (or only just those that are
    # selected using applyTools):

    wholeRows: List[List[CSVEmbeddable]] = [['Whole exploration metrics:']]
    if profile:
        print(
            "name (unit): calls / non-cached / time (lookups) / time (work)",
            file=sys.stderr
        )
    # One row per analyzer
    for ea in byUnit["exploration"]:
        wholeRows.append([ea.__name__, coerceToCSVValue(ea(exploration))])
        if profile:
            printPerf(ea.__name__)

    # A few variables for holding pieces we'll assemble
    row: List[CSVEmbeddable]
    columns: List[CSVEmbeddable]

    decisionRows: List[Sequence[CSVEmbeddable]] = [
        ['Per-decision metrics:']
    ]
    # One row per tool; one column per decision
    decisionList: List[base.DecisionID] = exploration.allDecisions()
    columns = (
        cast(List[CSVEmbeddable], ['Metric ↓/Decision →'])
      + cast(List[CSVEmbeddable], decisionList)
    )

    decisionRows.append(columns)
    for da in byUnit["decision"]:
        row = [da.__name__]
        decisionRows.append(row)
        for decision in decisionList:
            row.append(coerceToCSVValue(da(exploration, decision)))
        if profile:
            printPerf(da.__name__)

    transitionRows: List[Sequence[CSVEmbeddable]] = [
        ['Per-transition metrics:']
    ]
    # One row per tool; one column per decision
    transitionList: List[
        Tuple[base.DecisionID, base.Transition, base.DecisionID]
    ] = exploration.allTransitions()
    transitionStrings: List[CSVEmbeddable] = [
        transitionStr(exploration, *trans)
        for trans in transitionList
    ]
    columns = (
        cast(List[CSVEmbeddable], ['Metric ↓/Transition →'])
      + transitionStrings
    )
    transitionRows.append(columns)
    for ta in byUnit["transition"]:
        row = [ta.__name__]
        transitionRows.append(row)
        for transition in transitionList:
            row.append(
                coerceToCSVValue(ta(exploration, *transition))
            )
        if profile:
            printPerf(ta.__name__)

    stepRows: List[Sequence[CSVEmbeddable]] = [
        ['Per-step metrics:']
    ]
    # One row per exploration step; one column per tool
    columns = ['Step ↓/Metric →']
    stepRows.append(columns)
    for step in range(len(exploration)):
        row = [step]
        stepRows.append(row)
        for sa in byUnit["step"]:
            if step == 0:
                columns.append(sa.__name__)
            if sa.__name__ in finalOnly and step != len(exploration) - 1:
                row.append("")
            else:
                row.append(coerceToCSVValue(sa(exploration, step)))

    # Print profile results just once after all steps have been analyzed
    if profile:
        for sa in byUnit["step"]:
            printPerf(sa.__name__)

    stepwiseRows: List[Sequence[CSVEmbeddable]] = [
        ['Per-decision-per-step metrics (one table per metric):']
    ]

    # For each per-step decision tool; one row per exploration step and
    # one column per decision
    columns = (
        cast(List[CSVEmbeddable], ['Step ↓/Decision →'])
      + cast(List[CSVEmbeddable], decisionList)
    )
    identities = ['Decision names:'] + [
        analysis.finalIdentity(exploration, d)
        for d in decisionList
    ]
    for sda in byUnit["stepDecision"]:
        stepwiseRows.append([sda.__name__])
        stepwiseRows.append(columns)
        stepwiseRows.append(identities)
        if sda.__name__ in finalOnly:
            step = len(exploration) - 1
            row = [step]
            stepwiseRows.append(row)
            for decision in decisionList:
                row.append(coerceToCSVValue(sda(exploration, step, decision)))
        else:
            for step in range(len(exploration)):
                row = [step]
                stepwiseRows.append(row)
                for decision in decisionList:
                    row.append(
                        coerceToCSVValue(sda(exploration, step, decision))
                    )
        if profile:
            printPerf(sda.__name__)

    stepwiseTransitionRows: List[Sequence[CSVEmbeddable]] = [
        ['Per-transition-per-step metrics (one table per metric):']
    ]

    # For each per-step transition tool; one row per exploration step and
    # one column per transition
    columns = (
        cast(List[CSVEmbeddable], ['Step ↓/Transition →'])
      + cast(List[CSVEmbeddable], transitionStrings)
    )
    for sta in byUnit["stepTransition"]:
        stepwiseTransitionRows.append([sta.__name__])
        stepwiseTransitionRows.append(columns)
        if sta.__name__ in finalOnly:
            step = len(exploration) - 1
            row = [step]
            stepwiseTransitionRows.append(row)
            for (src, trans, dst) in transitionList:
                row.append(
                    coerceToCSVValue(sta(exploration, step, src, trans, dst))
                )
        else:
            for step in range(len(exploration)):
                row = [step]
                stepwiseTransitionRows.append(row)
                for (src, trans, dst) in transitionList:
                    row.append(
                        coerceToCSVValue(
                            sta(exploration, step, src, trans, dst)
                        )
                    )
        if profile:
            printPerf(sta.__name__)

    # Build a grid containing just the non-empty analysis categories, so
    # that if you deselect some tools you get a smaller CSV file:
    grid: List[Sequence[CSVEmbeddable]] = []
    if len(wholeRows) > 1:
        grid.extend(wholeRows)
    for block in (
        decisionRows,
        transitionRows,
        stepRows,
        stepwiseRows,
        stepwiseTransitionRows
    ):
        if len(block) > 1:
            if grid:
                grid.append([])  # spacer
            grid.extend(block)

    # Print all profile results at the end
    if profile:
        print("-"*80, file=sys.stderr)
        print("Done with analysis. Time taken:", file=sys.stderr)
        print("-"*80, file=sys.stderr)
        for aname in analysis.ANALYSIS_TIME_SPENT:
            printPerf(aname)
        print("-"*80, file=sys.stderr)
        printMem()

    # Figure out our destination stream:
    if destination is None:
        outStream = sys.stdout
        closeIt = False
    else:
        outStream = open(destination, 'w')
        closeIt = True

    # Create a CSV writer for our stream
    writer = csv.writer(outStream)

    # Write out our grid to the file
    try:
        writer.writerows(grid)
    finally:
        if closeIt:
            outStream.close()


def convert(
    source: pathlib.Path,
    destination: pathlib.Path,
    inputFormatOverride: Optional[SourceType] = None,
    outputFormatOverride: Optional[SourceType] = None,
    step: int = -1
) -> None:
    """
    Converts between exploration and graph formats. By default, formats
    are determined by file extensions, but using the `--format` and
    `--output-format` options can override this. The available formats
    are:

    - '.dcg' A `core.DecisionGraph` stored in JSON format.
    - '.dot' A `core.DecisionGraph` stored as a GraphViz DOT file.
    - '.exp' A `core.DiscreteExploration` stored in JSON format.
    - '.exj' A `core.DiscreteExploration` stored as a journal (see
        `journal.JournalObserver`; TODO: writing this format).

    When converting a decision graph into an exploration format, the
    resulting exploration will have a single starting step containing
    the entire specified graph. When converting an exploration into a
    decision graph format, only the current graph will be saved, unless
    `--step` is used to specify a different step index to save.
    """
    # TODO journal writing
    obj = loadSource(source, inputFormatOverride)

    if outputFormatOverride is None:
        outputFormat = determineFileType(str(destination))
    else:
        outputFormat = outputFormatOverride

    if outputFormat in ("graph", "dot"):
        if isinstance(obj, core.DiscreteExploration):
            graph = obj.getSituation(step).graph
        else:
            graph = obj
        if outputFormat == "graph":
            saveDecisionGraph(destination, graph)
        else:
            saveDotFile(destination, graph)
    else:
        if isinstance(obj, core.DecisionGraph):
            exploration = core.DiscreteExploration.fromGraph(obj)
        else:
            exploration = obj
        if outputFormat == "exploration":
            saveExploration(destination, exploration)
        else:
            saveAsJournal(destination, exploration)


INSPECTOR_HELP = """
Available commands:

- 'help' or '?': List commands.
- 'done', 'quit', 'q', or 'exit': Quit the inspector.
- 'f' or 'follow': Follow the primary decision when changing steps. Also
    changes to that decision immediately. Toggles off if on.
- 'cd' or 'goto': Change focus decision to the named decision. Cancels
    follow mode.
- 'ls' or 'list' or 'destinations': Lists transitions at this decision
    and their destinations, as well as any mechanisms at this decision.
- 'lst' or 'steps': Lists each step of the exploration along with the
    primary decision at each step.
- 'st' or 'step': Switches to the specified step (an index)
- 'n' or 'next': Switches to the next step.
- 'p' or 'prev' or 'previous': Switches to the previous step.
- 't' or 'take': Change focus decision to the decision which is the
    destination of the specified transition at the current focused
    decision.
- 'prm' or 'primary': Displays the current primary decision.
- 'a' or 'active': Lists all currently active decisions
- 'u' or 'unexplored': Lists all unexplored transitions at the current
    step.
- 'x' or 'explorable': Lists all unexplored transitions at the current
    step which are traversable based on the current state. (TODO:
    make this more accurate).
- 'r' or 'reachable': TODO
- 'A' or 'all': Lists all decisions at the current step.
- 'M' or 'mechanisms': Lists all mechanisms at the current step.
"""


def inspect(
    source: pathlib.Path,
    formatOverride: Optional[SourceType] = None
) -> None:
    """
    Inspects the graph or exploration stored in the `source` file,
    launching an interactive command line for inspecting properties of
    decisions, transitions, and situations. The file extension is used
    to determine how to load the data, although the `--format` option
    may override this. '.dcg' files are assumed to be decision graphs in
    JSON format, '.exp' files are assumed to be exploration objects in
    JSON format, and '.exj' files are assumed to be exploration journals
    in the default journal format. If the object that gets loaded is a
    graph, a 1-step exploration containing just that graph will be
    created to inspect. Inspector commands are listed in the
    `INSPECTOR_HELP` variable.
    """
    print(f"Loading exploration from {source!r}...")
    # Load our exploration
    exploration = loadSource(source, formatOverride)
    if isinstance(exploration, core.DecisionGraph):
        exploration = core.DiscreteExploration.fromGraph(exploration)

    print(
        f"Inspecting exploration with {len(exploration)} step(s) and"
        f" {len(exploration.allDecisions())} decision(s):"
    )
    print("('h' for help)")

    # Set up tracking variables:
    step = len(exploration) - 1
    here: Optional[base.DecisionID] = exploration.primaryDecision(step)
    graph = exploration.getSituation(step).graph
    follow = True

    pf = parsing.ParseFormat()

    if here is None:
        print("Note: There are no decisions in the final graph.")

    while True:
        # Re-establish the prompt
        prompt = "> "
        if here is not None and here in graph:
            prompt = graph.identityOf(here) + "> "
        elif here is not None:
            prompt = f"{here} (?)> "

        # Prompt for the next command
        fullCommand = input(prompt).split()

        # Track number of invalid commands so we can quit after 10 in a row
        invalidCommands = 0

        if len(fullCommand) == 0:
            cmd = ''
            args = ''
        else:
            cmd = fullCommand[0]
            args = ' '.join(fullCommand[1:])

        # Do what the command says
        invalid = False
        if cmd in ("help", '?'):
            # Displays help message
            if len(args.strip()) > 0:
                print("(help does not accept any arguments)")
            print(INSPECTOR_HELP)
        elif cmd in ("done", "exit", "quit", "q"):
            # Exits the inspector
            if len(args.strip()) > 0:
                print("(quit does not accept any arguments)")
            print("Bye.")
            break
        elif cmd in ("f", "follow"):
            if follow:
                follow = False
                print("Stopped following")
            else:
                follow = True
                here = exploration.primaryDecision(step)
                print(f"Now following at: {graph.identityOf(here)}")
        elif cmd in ("cd", "goto"):
            # Changes focus to a specific decision
            try:
                target = pf.parseDecisionSpecifier(args)
                target = graph.resolveDecision(target)
                here = target
                follow = False
                print(f"now at: {graph.identityOf(target)}")
            except Exception:
                print("(invalid decision specifier)")
        elif cmd in ("ls", "list", "destinations"):
            fromID: Optional[base.AnyDecisionSpecifier] = None
            if args.strip():
                fromID = pf.parseDecisionSpecifier(args)
                fromID = graph.resolveDecision(fromID)
            else:
                fromID = here

            if fromID is None:
                print(
                    "(no focus decision and no decision specified;"
                    " nothing to list; use 'cd' to specify a decision,"
                    " or 'all' to list all decisions)"
                )
            else:
                outgoing = graph.destinationsFrom(fromID)
                info = graph.identityOf(fromID)
                if len(outgoing) > 0:
                    print(f"Destinations from {info}:")
                    print(graph.destinationsListing(outgoing))
                else:
                    print("No outgoing transitions from {info}.")
        elif cmd in ("lst", "steps"):
            total = len(exploration)
            print(f"{total} step(s):")
            for step in range(total):
                pr = exploration.primaryDecision(step)
                situ = exploration.getSituation(step)
                stGraph = situ.graph
                identity = stGraph.identityOf(pr)
                print(f"  {step} at {identity}")
            print(f"({total} total step(s))")
        elif cmd in ("st", "step"):
            stepTo = int(args.strip())
            if stepTo < 0:
                stepTo += len(exploration)
            if stepTo < 0:
                print(
                    f"Invalid step {args!r} (too negative; min is"
                    f" {-len(exploration)})"
                )
            if stepTo >= len(exploration):
                print(
                    f"Invalid step {args!r} (too large; max is"
                    f" {len(exploration) - 1})"
                )

            step = stepTo
            graph = exploration.getSituation(step).graph
            if follow:
                here = exploration.primaryDecision(step)
                print(f"Followed to: {graph.identityOf(here)}")
        elif cmd in ("n", "next"):
            if step == -1 or step >= len(exploration) - 2:
                print("Can't step beyond the last step.")
            else:
                step += 1
                graph = exploration.getSituation(step).graph
                if here not in graph:
                    here = None
            print(f"At step {step}")
            if follow:
                here = exploration.primaryDecision(step)
                print(f"Followed to: {graph.identityOf(here)}")
        elif cmd in ("p", "prev"):
            if step == 0 or step <= -len(exploration) + 2:
                print("Can't step before the first step.")
            else:
                step -= 1
                graph = exploration.getSituation(step).graph
                if here not in graph:
                    here = None
            print(f"At step {step}")
            if follow:
                here = exploration.primaryDecision(step)
                print(f"Followed to: {graph.identityOf(here)}")
        elif cmd in ("t", "take"):
            if here is None:
                print(
                    "(no focus decision, so can't take transitions. Use"
                    " 'cd' to specify a decision first.)"
                )
            else:
                dest = graph.getDestination(here, args)
                if dest is None:
                    print(
                        f"Invalid transition {args!r} (no destination for"
                        f" that transition from {graph.identityOf(here)}"
                    )
                here = dest
        elif cmd in ("prm", "primary"):
            pr = exploration.primaryDecision(step)
            if pr is None:
                print(f"Step {step} has no primary decision")
            else:
                print(
                    f"Primary decision for step {step} is:"
                    f" {graph.identityOf(pr)}"
                )
        elif cmd in ("a", "active"):
            active = exploration.getActiveDecisions(step)
            print(f"Active decisions at step {step}:")
            print(graph.namesListing(active))
        elif cmd in ("u", "unexplored"):
            unx = analysis.unexploredBranches(graph)
            fin = ':' if len(unx) > 0 else '.'
            print(f"{len(unx)} unexplored branch(es){fin}")
            for frID, unTr in unx:
                print(f"take {unTr} at {graph.identityOf(frID)}")
        elif cmd in ("x", "explorable"):
            ctx = base.genericContextForSituation(
                exploration.getSituation(step)
            )
            unx = analysis.unexploredBranches(graph, ctx)
            fin = ':' if len(unx) > 0 else '.'
            print(f"{len(unx)} unexplored branch(es){fin}")
            for frID, unTr in unx:
                print(f"take {unTr} at {graph.identityOf(frID)}")
        elif cmd in ("r", "reachable"):
            print("TODO: Reachable does not work yet.")
        elif cmd in ("A", "all"):
            print(
                f"There are {len(graph)} decision(s) at step {step}:"
            )
            for decision in graph.nodes():
                print(f"  {graph.identityOf(decision)}")
        elif cmd in ("M", "mechanisms"):
            count = len(graph.mechanisms)
            fin = ':' if count > 0 else '.'
            print(
                f"There are {count} mechanism(s) at step {step}{fin}"
            )
            for mID in graph.mechanisms:
                where, name = graph.mechanisms[mID]
                state = exploration.mechanismState(mID, step=step)
                if where is None:
                    print(f"  {name!r} (global) in state {state!r}")
                else:
                    info = graph.identityOf(where)
                    print(f"  {name!r} at {info} in state {state!r}")
        else:
            invalid = True

        if invalid:
            if invalidCommands >= 10:
                print("Too many invalid commands; exiting.")
                break
            else:
                if invalidCommands >= 8:
                    print("{invalidCommands} invalid commands so far,")
                    print("inspector will stop after 10 invalid commands...")
                print(f"Unknown command {cmd!r}...")
                invalidCommands += 1
                print(INSPECTOR_HELP)
        else:
            invalidCommands = 0


#--------------#
# Parser setup #
#--------------#

parser = argparse.ArgumentParser(
    prog="python -m exploration",
    description="""\
Runs various commands for processing exploration graphs and journals,
and for converting between them or displaying them in various formats.
"""
)
subparsers = parser.add_subparsers(
    title="commands",
    description="The available commands are:",
    help="use these with -h/--help for more details"
)

showParser = subparsers.add_parser(
    'show',
    help="show an exploration",
    description=textwrap.dedent(str(show.__doc__)).strip()
)
showParser.set_defaults(run="show")
showParser.add_argument(
    "source",
    type=pathlib.Path,
    help="The file to load"
)
showParser.add_argument(
    '-f',
    "--format",
    choices=get_args(SourceType),
    help=(
        "Which format the source file is in (normally that can be"
        " determined from the file extension)."
    )
)
showParser.add_argument(
    '-s',
    "--step",
    type=int,
    default=-1,
    help="Which graph step to show (when loading an exploration)."
)

analyzeParser = subparsers.add_parser(
    'analyze',
    help="analyze an exploration",
    description=textwrap.dedent(str(analyze.__doc__)).strip()
)
analyzeParser.set_defaults(run="analyze")
analyzeParser.add_argument(
    "source",
    type=pathlib.Path,
    help="The file holding the exploration to analyze"
)
analyzeParser.add_argument(
    "destination",
    default=None,
    type=pathlib.Path,
    help=(
        "The file name where the output should be written (this file"
        " will be overwritten without warning)."
    )
)
analyzeParser.add_argument(
    '-f',
    "--format",
    choices=get_args(SourceType),
    help=(
        "Which format the source file is in (normally that can be"
        " determined from the file extension)."
    )
)
analyzeParser.add_argument(
    '-a',
    "--all",
    action='store_true',
    help=(
        "Whether to include all results or just the default ones. Some"
        " of the extended results may cause issues with loading the CSV"
        " file in common programs like Excel."
    )
)
analyzeParser.add_argument(
    '-p',
    "--profile",
    action='store_true',
    help="Set this to profile time taken by analysis functions."
)

convertParser = subparsers.add_parser(
    'convert',
    help="convert an exploration",
    description=textwrap.dedent(str(convert.__doc__)).strip()
)
convertParser.set_defaults(run="convert")
convertParser.add_argument(
    "source",
    type=pathlib.Path,
    help="The file holding the graph or exploration to convert."
)
convertParser.add_argument(
    "destination",
    type=pathlib.Path,
    help=(
        "The file name where the output should be written (this file"
        " will be overwritten without warning)."
    )
)
convertParser.add_argument(
    '-f',
    "--format",
    choices=get_args(SourceType),
    help=(
        "Which format the source file is in (normally that can be"
        " determined from the file extension)."
    )
)
convertParser.add_argument(
    '-o',
    "--output-format",
    choices=get_args(SourceType),
    help=(
        "Which format the converted file should be saved as (normally"
        " that is determined from the file extension)."
    )
)
convertParser.add_argument(
    '-s',
    "--step",
    type=int,
    default=-1,
    help=(
        "Which graph step to save (when converting from an exploration"
        " format to a graph format)."
    )
)

inspectParser = subparsers.add_parser(
    'inspect',
    help="interactively inspect an exploration",
    description=textwrap.dedent(str(inspect.__doc__)).strip()
)
inspectParser.set_defaults(run="inspect")
inspectParser.add_argument(
    "source",
    type=pathlib.Path,
    help="The file holding the graph or exploration to inspect."
)
inspectParser.add_argument(
    '-f',
    "--format",
    choices=get_args(SourceType),
    help=(
        "Which format the source file is in (normally that can be"
        " determined from the file extension)."
    )
)

def main():
    """
    Parse options from command line & run appropriate tool.
    """
    options = parser.parse_args()
    if not hasattr(options, "run"):
        print("No sub-command specified.")
        parser.print_help()
        exit(1)
    elif options.run == "show":
        show(
            options.source,
            formatOverride=options.format,
            step=options.step
        )
    elif options.run == "analyze":
        analyze(
            options.source,
            destination=options.destination,
            formatOverride=options.format,
            includeAll=options.all,
            profile=options.profile
        )
    elif options.run == "convert":
        convert(
            options.source,
            options.destination,
            inputFormatOverride=options.format,
            outputFormatOverride=options.output_format,
            step=options.step
        )
    elif options.run == "inspect":
        inspect(
            options.source,
            formatOverride=options.format
        )
    else:
        raise RuntimeError(
            f"Invalid 'run' default value: '{options.run}'."
        )


if __name__ == "__main__":
    main()
