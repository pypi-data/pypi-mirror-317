"""
- Authors: Peter Mawhorter
- Consulted:
- Date: 2022-10-24
- Purpose: Analysis functions for decision graphs an explorations.
"""

from typing import (
    List, Dict, Tuple, Optional, TypeVar, Callable, Union, Any,
    ParamSpec, Concatenate, Set, cast, Type, TypeAlias, Literal,
    TypedDict, Protocol, Sequence, Callable, Collection
)

from types import FunctionType

from . import base, core, parsing

import textwrap
import functools
import inspect
import time

import networkx as nx


#-------------------#
# Text descriptions #
#-------------------#

def describeConsequence(consequence: base.Consequence) -> str:
    """
    Returns a string which concisely describes a consequence list.
    Returns an empty string if given an empty consequence. Examples:

    >>> describeConsequence([])
    ''
    >>> describeConsequence([
    ...     base.effect(gain=('gold', 5), delay=2, charges=3),
    ...     base.effect(lose='flight')
    ... ])
    'gain gold*5 ,2 =3; lose flight'
    >>> from . import commands
    >>> d = describeConsequence([
    ...     base.effect(edit=[
    ...         [
    ...             commands.command('val', '5'),
    ...             commands.command('empty', 'list'),
    ...             commands.command('append')
    ...         ],
    ...         [
    ...             commands.command('val', '11'),
    ...             commands.command('assign', 'var'),
    ...             commands.command('op', '+', '$var', '$var')
    ...         ],
    ...     ])
    ... ])
    >>> d
    'with consequences:\
\\n    edit {\
\\n      val 5;\
\\n      empty list;\
\\n      append $_;\
\\n    } {\
\\n      val 11;\
\\n      assign var $_;\
\\n      op + $var $var;\
\\n    }\
\\n'
    >>> for line in d.splitlines():
    ...     print(line)
    with consequences:
        edit {
          val 5;
          empty list;
          append $_;
        } {
          val 11;
          assign var $_;
          op + $var $var;
        }
    """
    edesc = ''
    pf = parsing.ParseFormat()
    if consequence:
        parts = []
        for item in consequence:
            # TODO: Challenges and Conditions here!
            if 'skills' in item:  # a Challenge
                item = cast(base.Challenge, item)
                parts.append(pf.unparseChallenge(item))
            elif 'value' in item:  # an Effect
                item = cast(base.Effect, item)
                parts.append(pf.unparseEffect(item))
            elif 'condition' in item:  # a Condition
                item = cast(base.Condition, item)
                parts.append(pf.unparseCondition(item))
            else:
                raise TypeError(
                    f"Invalid consequence item (no 'skills', 'value', or"
                    f" 'condition' key found):\n{repr(item)}"
                )
        edesc = '; '.join(parts)
        if len(edesc) > 60 or '\n' in edesc:
            edesc = 'with consequences:\n' + ';\n'.join(
                textwrap.indent(part, '    ')
                for part in parts
            ) + '\n'

    return edesc


def describeProgress(exploration: core.DiscreteExploration) -> str:
    """
    Describes the progress of an exploration by noting each room/zone
    visited and explaining the options visible at each point plus which
    option was taken. Notes powers/tokens gained/lost along the way.
    Returns a string.

    Example:
    >>> from exploration import journal
    >>> e = journal.convertJournal('''\\
    ... S Start::pit
    ... A gain jump
    ... A gain attack
    ... n button check
    ... zz Wilds
    ... o up
    ...   q _flight
    ... o left
    ... x left left_nook right
    ... a geo_rock
    ...   At gain geo*15
    ...   At deactivate
    ... o up
    ...   q _tall_narrow
    ... t right
    ... o right
    ...   q attack
    ... ''')
    >>> for line in describeProgress(e).splitlines():
    ...    print(line)
    Start of the exploration
    Start exploring domain main at 0 (Start::pit)
      Gained capability 'attack'
      Gained capability 'jump'
    At decision 0 (Start::pit)
      In zone Start
      In region Wilds
      There are transitions:
        left to unconfirmed
        up to unconfirmed; requires _flight
      1 note(s) at this step
    Explore left from decision 0 (Start::pit) to 2 (now Start::left_nook)
    At decision 2 (Start::left_nook)
      There are transitions:
        right to 0 (Start::pit)
      There are actions:
        geo_rock
    Do action geo_rock
      Gained 15 geo(s)
    Take right from decision 2 (Start::left_nook) to 0 (Start::pit)
    At decision 0 (Start::pit)
      There are transitions:
        left to 2 (Start::left_nook)
        right to unconfirmed; requires attack
        up to unconfirmed; requires _flight
    Waiting for another action...
    End of the exploration.
    """
    result = ''

    regions: Set[base.Zone] = set()
    zones: Set[base.Zone] = set()
    last: Union[base.DecisionID, Set[base.DecisionID], None] = None
    lastState: base.State = base.emptyState()
    prevCapabilities = base.effectiveCapabilitySet(lastState)
    prevMechanisms = lastState['mechanisms']
    oldActiveDecisions: Set[base.DecisionID] = set()
    for i, situation in enumerate(exploration):
        if i == 0:
            result += "Start of the exploration\n"

        # Extract info
        graph = situation.graph
        activeDecisions = exploration.getActiveDecisions(i)
        newActive = activeDecisions - oldActiveDecisions
        departedFrom = exploration.movementAtStep(i)[0]
        # TODO: use the other parts of this?
        nowZones: Set[base.Zone] = set()
        for active in activeDecisions:
            nowZones |= graph.zoneAncestors(active)
        regionsHere = set(
            z
            for z in nowZones
            if graph.zoneHierarchyLevel(z) == 1
        )
        zonesHere = set(
            z
            for z in nowZones
            if graph.zoneHierarchyLevel(z) == 0
        )
        here = departedFrom
        state = situation.state
        capabilities = base.effectiveCapabilitySet(state)
        mechanisms = state['mechanisms']

        # Describe capabilities gained/lost relative to previous step
        # (i.e., as a result of the previous action)
        gained = (
            capabilities['capabilities']
          - prevCapabilities['capabilities']
        )
        gainedTokens = []
        for tokenType in capabilities['tokens']:
            net = (
                capabilities['tokens'][tokenType]
              - prevCapabilities['tokens'].get(tokenType, 0)
            )
            if net != 0:
                gainedTokens.append((tokenType, net))
        changed = [
            mID
            for mID in list(mechanisms.keys()) + list(prevMechanisms.keys())
            if mechanisms.get(mID) != prevMechanisms.get(mID)
        ]

        for capability in sorted(gained):
            result += f"  Gained capability '{capability}'\n"

        for tokenType, net in gainedTokens:
            if net > 0:
                result += f"  Gained {net} {tokenType}(s)\n"
            else:
                result += f"  Lost {-net} {tokenType}(s)\n"

        for mID in changed:
            oldState = prevMechanisms.get(mID, base.DEFAULT_MECHANISM_STATE)
            newState = mechanisms.get(mID, base.DEFAULT_MECHANISM_STATE)

            details = graph.mechanismDetails(mID)
            if details is None:
                mName = "(unknown)"
            else:
                mName = details[1]
            result += (
                f"  Set mechanism {mID} ({mName}) to {newState} (was"
                f" {oldState})"
            )
            # TODO: Test this!

        if isinstance(departedFrom, base.DecisionID):
            # Print location info
            if here != last:
                if here is None:
                    result += "Without a position...\n"
                elif isinstance(here, set):
                    result += f"With {len(here)} active decisions\n"
                    # TODO: List them using namesListing?
                else:
                    result += f"At decision {graph.identityOf(here)}\n"
            newZones = zonesHere - zones
            for zone in sorted(newZones):
                result += f"  In zone {zone}\n"
            newRegions = regionsHere - regions
            for region in sorted(newRegions):
                result += f"  In region {region}\n"

        elif isinstance(departedFrom, set):  # active in spreading domain
            spreadingDomain = graph.domainFor(list(departedFrom)[0])
            result += (
                f"  In domain {spreadingDomain} with {len(departedFrom)}"
                f" active decisions...\n"
            )

        else:
            assert departedFrom is None

        # Describe new position/positions at start of this step
        if len(newActive) > 1:
            newListing = ', '.join(
                sorted(graph.identityOf(n) for n in newActive)
            )
            result += (
                f"  There are {len(newActive)} new active decisions:"
                f"\n  {newListing}"
            )

        elif len(newActive) == 1:
            here = list(newActive)[0]

            outgoing = graph.destinationsFrom(here)

            transitions = {t: d for (t, d) in outgoing.items() if d != here}
            actions = {t: d for (t, d) in outgoing.items() if d == here}
            if transitions:
                result += "  There are transitions:\n"
                for transition in sorted(transitions):
                    dest = transitions[transition]
                    if not graph.isConfirmed(dest):
                        destSpec = 'unconfirmed'
                    else:
                        destSpec = graph.identityOf(dest)
                    req = graph.getTransitionRequirement(here, transition)
                    rDesc = ''
                    if req != base.ReqNothing():
                        rDesc = f"; requires {req.unparse()}"
                    cDesc = describeConsequence(
                        graph.getConsequence(here, transition)
                    )
                    if cDesc:
                        cDesc = '; ' + cDesc
                    result += (
                        f"    {transition} to {destSpec}{rDesc}{cDesc}\n"
                    )

            if actions:
                result += "  There are actions:\n"
                for action in sorted(actions):
                    req = graph.getTransitionRequirement(here, action)
                    rDesc = ''
                    if req != base.ReqNothing():
                        rDesc = f"; requires {req.unparse()}"
                    cDesc = describeConsequence(
                        graph.getConsequence(here, action)
                    )
                    if cDesc:
                        cDesc = '; ' + cDesc
                    if rDesc or cDesc:
                        desc = (rDesc + cDesc)[2:]  # chop '; ' from either
                        result += f"    {action} ({desc})\n"
                    else:
                        result += f"    {action}\n"

        # note annotations
        if len(situation.annotations) > 0:
            result += (
                f"  {len(situation.annotations)} note(s) at this step\n"
            )

        # Describe action taken
        if situation.action is None and situation.type == "pending":
            result += "Waiting for another action...\n"
        else:
            desc = base.describeExplorationAction(situation, situation.action)
            desc = desc[0].capitalize() + desc[1:]
            result += desc + '\n'

        if i == len(exploration) - 1:
            result += "End of the exploration.\n"

        # Update state variables
        oldActiveDecisions = activeDecisions
        prevCapabilities = capabilities
        prevMechanisms = mechanisms
        regions = regionsHere
        zones = zonesHere
        if here is not None:
            last = here
        lastState = state

    return result


#-----------------------#
# Analysis result types #
#-----------------------#

AnalysisUnit: 'TypeAlias' = Literal[
    'step',
    'stepDecision',
    'stepTransition',
    'decision',
    'transition',
    'exploration',
]
"""
The different kinds of analysis units we consider: per-step-per-decision,
per-step-per-transition, per-step, per-final-decision,
per-final-transition, and per-exploration (i.e. overall).
"""


AnalysisResults: 'TypeAlias' = Dict[str, Any]
"""
Analysis results are dictionaries that map analysis routine names to
results from those routines, which can be of any type.
"""


SpecificTransition: 'TypeAlias' = Tuple[base.DecisionID, base.Transition]
"""
A specific transition is identified by its source decision ID and its
transition name. Note that transitions which get renamed are treated as
two separate transitions.
"""

OverspecificTransition: 'TypeAlias' = Tuple[
    base.DecisionID,
    base.Transition,
    base.DecisionID
]
"""
In contrast to a `SpecificTransition`, an `OverspecificTransition`
includes the destination of the transition, which might help disambiguate
cases where a transition is created, then re-targeted or deleted and
re-created with a different destination. Transitions which get renamed
still are treated as two separate transitions.
"""

DecisionAnalyses: 'TypeAlias' = Dict[base.DecisionID, AnalysisResults]
"""
Decision analysis results are stored per-decision, with a dictionary of
property-name → value associations. These properties either apply to
decisions across all steps of an exploration, or apply to decisions in a
particular `core.DecisionGraph`.
"""

TransitionAnalyses: 'TypeAlias' = Dict[OverspecificTransition, AnalysisResults]
"""
Per-transition analysis results, similar to `DecisionAnalyses`.
"""

StepAnalyses: 'TypeAlias' = List[AnalysisResults]
"""
Per-exploration-step analysis results are stored in a list and indexed by
exploration step integers.
"""

StepwiseDecisionAnalyses: 'TypeAlias' = List[DecisionAnalyses]
"""
Per-step-per-decision analysis results are stored as a list of decision
analysis results.
"""

StepwiseTransitionAnalyses: 'TypeAlias' = List[TransitionAnalyses]
"""
Per-step-per-transition analysis results are stored as a list of
transition analysis results.
"""

ExplorationAnalyses: 'TypeAlias' = AnalysisResults
"""
Whole-exploration analyses are just a normal `AnalysisResults` dictionary.
"""

class FullAnalysisResults(TypedDict):
    """
    Full analysis results hold every kind of analysis result in one
    dictionary.
    """
    perDecision: DecisionAnalyses
    perTransition: TransitionAnalyses
    perStep: StepAnalyses
    perStepDecision: StepwiseDecisionAnalyses
    perStepTransition: StepwiseTransitionAnalyses
    overall: ExplorationAnalyses


def newFullAnalysisResults() -> FullAnalysisResults:
    """
    Returns a new empty `FullAnalysisResults` dictionary.
    """
    return {
        'perDecision': {},
        'perTransition': {},
        'perStep': [],
        'perStepDecision': [],
        'perStepTransition': [],
        'overall': {}
    }


Params = ParamSpec('Params')
'Parameter specification variable for `AnalysisFunction` definition.'


class AnalysisFunction(Protocol[Params]):
    """
    Analysis functions are callable, but also have a `_unit` attribute
    which is a string.
    """
    _unit: AnalysisUnit
    __name__: str
    __doc__: str
    def __call__(
        self,
        exploration: core.DiscreteExploration,
        *args: Params.args,
        **kwargs: Params.kwargs
    ) -> Any:
        ...


StepAnalyzer: 'TypeAlias' = AnalysisFunction[[int]]
'''
A step analyzer is a function which will receive a
`core.DiscreteExploration` along with the step in that exploration being
considered. It can return any type of analysis result.
'''

StepDecisionAnalyzer: 'TypeAlias' = AnalysisFunction[[int, base.DecisionID]]
'''
Like a `StepAnalyzer` but also gets a decision ID to consider.
'''

StepTransitionAnalyzer: 'TypeAlias' = AnalysisFunction[
    [int, base.DecisionID, base.Transition, base.DecisionID]
]
'''
Like a `StepAnalyzer` but also gets a source decision ID, a transition
name, and a destination decision ID to target.
'''


DecisionAnalyzer: 'TypeAlias' = AnalysisFunction[[base.DecisionID]]
'''
A decision analyzer gets full analysis results to update plus an
exploration and a particular decision ID to consider.
'''

TransitionAnalyzer: 'TypeAlias' = AnalysisFunction[
    [base.DecisionID, base.Transition, base.DecisionID]
]
'''
Like a `DecisionAnalyzer` but gets a transition name as well.
'''

ExplorationAnalyzer: 'TypeAlias' = AnalysisFunction[[]]
'''
Analyzes overall properties of an entire `core.DiscreteExploration`.
'''


#--------------------------#
# Analysis caching support #
#--------------------------#

AnyAnalyzer: 'TypeAlias' = Union[
    ExplorationAnalyzer,
    TransitionAnalyzer,
    DecisionAnalyzer,
    StepAnalyzer,
    StepDecisionAnalyzer,
    StepTransitionAnalyzer
]


ANALYSIS_RESULTS: Dict[int, FullAnalysisResults] = {}
"""
Caches analysis results, keyed by the `id` of the
`core.DiscreteExploration` they're based on.
"""


class NotCached:
    """
    Reference object for specifying that no cached value is available,
    since `None` is a valid cached value.
    """
    pass


def lookupAnalysisResult(
    cache: FullAnalysisResults,
    analyzer: AnalysisFunction,
    argsInOrder: Sequence[Any]
) -> Union[Type[NotCached], Any]:
    """
    Looks up an analysis result for the given function in the given
    cache. The function must have been decorated with `analyzer`. The
    bound arguments must match the unit of analysis, for example, if the
    unit is 'stepDecision', the arguments must be those for a
    `StepDecisionAnalyzer`. The bound arguments should have had
    `apply_defaults` called already to fill in default argument values.
    Returns the special object `NotCached` if there is no cached value
    for the specified arguments yet.
    """
    unit = analyzer._unit
    if unit == 'step':
        whichStep = argsInOrder[1]
        perStep = cache['perStep']
        while len(perStep) <= whichStep:
            perStep.append({})
        return perStep[whichStep].get(analyzer.__name__, NotCached)
    elif unit == 'stepDecision':
        whichStep = argsInOrder[1]
        whichDecision = argsInOrder[2]
        perStepDecision = cache['perStepDecision']
        while len(perStepDecision) <= whichStep:
            perStepDecision.append({})
        forThis = perStepDecision[whichStep].get(whichDecision)
        if forThis is None:
            return NotCached
        return forThis.get(analyzer.__name__, NotCached)
    elif unit == 'stepTransition':
        whichStep = argsInOrder[1]
        whichTransition = (argsInOrder[2], argsInOrder[3], argsInOrder[4])
        perStepTransition = cache['perStepTransition']
        while len(perStepTransition) <= whichStep:
            perStepTransition.append({})
        forThis = perStepTransition[whichStep].get(whichTransition)
        if forThis is None:
            return NotCached
        return forThis.get(analyzer.__name__, NotCached)
    elif unit == 'decision':
        whichDecision = argsInOrder[1]
        perDecision = cache['perDecision']
        if whichDecision not in perDecision:
            return NotCached
        return perDecision[whichDecision].get(analyzer.__name__, NotCached)
    elif unit == 'transition':
        whichTransition = (argsInOrder[1], argsInOrder[2], argsInOrder[3])
        perTransition = cache['perTransition']
        if whichTransition not in perTransition:
            return NotCached
        return perTransition[whichTransition].get(
            analyzer.__name__,
            NotCached
        )
    elif unit == 'exploration':
        return cache['overall'].get(analyzer.__name__, NotCached)
    else:
        raise ValueError(f"Invalid analysis unit {unit!r}.")


def saveAnalysisResult(
    cache: FullAnalysisResults,
    result: Any,
    analyzer: AnalysisFunction,
    argsInOrder: Sequence[Any]
) -> None:
    """
    Saves an analysis result in the specified cache. The bound arguments
    must match the unit, for example, if the unit is 'stepDecision', the
    arguments must be those for a `StepDecisionAnalyzer`.
    """
    unit = analyzer._unit
    if unit == 'step':
        whichStep = argsInOrder[1]
        perStep = cache['perStep']
        while len(perStep) <= whichStep:
            perStep.append({})
        perStep[whichStep][analyzer.__name__] = result
    elif unit == 'stepDecision':
        whichStep = argsInOrder[1]
        whichDecision = argsInOrder[2]
        perStepDecision = cache['perStepDecision']
        while len(perStepDecision) <= whichStep:
            perStepDecision.append({})
        forThis = perStepDecision[whichStep].setdefault(whichDecision, {})
        forThis[analyzer.__name__] = result
    elif unit == 'stepTransition':
        whichStep = argsInOrder[1]
        whichTransition = (argsInOrder[2], argsInOrder[3], argsInOrder[4])
        perStepTransition = cache['perStepTransition']
        while len(perStepTransition) <= whichStep:
            perStepTransition.append({})
        forThis = perStepTransition[whichStep].setdefault(whichTransition, {})
        forThis[analyzer.__name__] = result
    elif unit == 'decision':
        whichDecision = argsInOrder[1]
        perDecision = cache['perDecision']
        perDecision.setdefault(whichDecision, {})[analyzer.__name__] = result
    elif unit == 'transition':
        whichTransition = (argsInOrder[1], argsInOrder[2], argsInOrder[3])
        perTransition = cache['perTransition']
        perTransition.setdefault(
            whichTransition,
            {}
        )[analyzer.__name__] = result
    elif unit == 'exploration':
        cache['overall'][analyzer.__name__] = result
    else:
        raise ValueError(f"Invalid analysis unit {unit!r}.")


ALL_ANALYZERS: Dict[str, AnyAnalyzer] = {}
"""
Holds all analyzers indexed by name with the analysis unit plus function
as the value. The `analyzer` decorator registers them.
"""


RECORD_PROFILE: bool = False
"""
Whether or not to record time spent by each analysis function.
"""


class AnalyzerPerf(TypedDict):
    """
    Tracks performance of an analysis function, recording total calls,
    non-cached calls, time spent looking up cached results, and time
    spent in non-cached calls (including the failed cache lookup and
    saving the result in the cache). 
    """
    calls: int
    nonCached: int
    lookupTime: float
    analyzeTime: float


def newAnalyzerPerf() -> AnalyzerPerf:
    """
    Creates a new empty `AnalyzerPerf` dictionary.
    """
    return {
        "calls": 0,
        "nonCached": 0,
        "lookupTime": 0.0,
        "analyzeTime": 0.0
    }


ANALYSIS_TIME_SPENT: Dict[str, AnalyzerPerf] = {}
"""
Records number-of-calls, number-of-non-cached calls, and time spent in
each analysis function, when `RECORD_PROFILE` is set to `True`.
"""


ELIDE: Set[str] = set()
"""
Analyzers which should not be included in CSV output by default.
"""

FINAL_ONLY: Set[str] = set()
"""
Per-step/step-decision/step-transition analyzers which should by default
only be applied to the final step of an exploration to save time.
"""


def getArgsInOrder(
    f: Callable,
    *args: Any,
    **kwargs: Any
) -> List[Any]:
    """
    Given a callable and some arguments, returns a list of argument and
    some arguments, returns a list of argument values in the same order
    as that function would accept them from the given arguments,
    accounting for things like keyword arguments and default values.

    For example:

    >>> def f(a, /, b, *more, x=3, y=10, **kw):
    ...     pass
    >>> sig = inspect.Signature.from_callable(f)
    >>> getArgsInOrder(f, 1, 2)
    [1, 2, 3, 10]
    >>> getArgsInOrder(f, 4, 5, y=2, x=8)
    [4, 5, 8, 2]
    >>> getArgsInOrder(f, 4, y=2, x=8, b=3)
    [4, 3, 8, 2]
    >>> getArgsInOrder(f, 4, y=2, x=8, b=3)
    [4, 3, 8, 2]
    >>> getArgsInOrder(f, 1, 2, 3, 4)
    [1, 2, 3, 4, 3, 10]
    >>> getArgsInOrder(f, 1, 2, 3, 4, q=5, k=9)
    [1, 2, 3, 4, 3, 10, 5, 9]
    """
    sig = inspect.Signature.from_callable(f)
    bound = sig.bind(*args, **kwargs)
    bound.apply_defaults()
    result = []
    for paramName in sig.parameters:
        param = sig.parameters[paramName]
        if param.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        ):
            result.append(bound.arguments[paramName])
        elif param.kind == inspect.Parameter.VAR_POSITIONAL:
            result.extend(bound.arguments[paramName])
        elif param.kind == inspect.Parameter.KEYWORD_ONLY:
            result.append(bound.arguments[paramName])
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            result.extend(bound.arguments[paramName].values())

    return result


def analyzer(unit: AnalysisUnit) -> Callable[
    [Callable[Concatenate[core.DiscreteExploration, Params], Any]],
    AnalysisFunction
]:
    '''
    Decorator which sets up caching for an analysis function in the
    global `ANALYSIS_RESULTS` dictionary. Whenever the decorated function
    is called, it will first check whether a cached result is available
    for the same target exploration (by id) and additional target info
    based on the analysis unit type. If so, the cached result will be
    returned. This allows analysis functions to simply call each other
    when they need results and themselves recursively if they need to
    track things across steps/decisions, while avoiding tons of duplicate
    work.
    '''
    def makeCachedAnalyzer(
        baseFunction: Callable[
            Concatenate[core.DiscreteExploration, Params],
            Any
        ]
    ) -> AnalysisFunction:
        """
        Decoration function which registers an analysis function with
        pre-specified dependencies.
        """
        analysisFunction = cast(AnalysisFunction, baseFunction)
        analysisFunction._unit = unit
        analyzerName= analysisFunction.__name__

        @functools.wraps(analysisFunction)
        def cachingAnalyzer(
            exploration: core.DiscreteExploration,
            *args: Params.args,
            **kwargs: Params.kwargs
        ):
            """
            This docstring will be replaced with the docstring of the
            decorated function plus a note about caching.
            """
            if RECORD_PROFILE:
                ANALYSIS_TIME_SPENT.setdefault(
                    analyzerName,
                    newAnalyzerPerf()
                )
                perf = ANALYSIS_TIME_SPENT[analyzerName]
                perf["calls"] += 1
                start = time.perf_counter()
            cache = ANALYSIS_RESULTS.setdefault(
                id(exploration),
                newFullAnalysisResults()
            )
            argsInOrder = getArgsInOrder(
                baseFunction,
                exploration,
                *args,
                **kwargs
            )
            cachedResult = lookupAnalysisResult(
                cache,
                analysisFunction,
                argsInOrder
            )
            if cachedResult is not NotCached:
                if RECORD_PROFILE:
                    perf["lookupTime"] += time.perf_counter() - start
                return cachedResult

            result = analysisFunction(exploration, *args, **kwargs)
            saveAnalysisResult(cache, result, analysisFunction, argsInOrder)
            if RECORD_PROFILE:
                perf["nonCached"] += 1
                perf["analyzeTime"] += time.perf_counter() - start
            return result

        cachingAnalyzer.__doc__ = (
            textwrap.dedent(analysisFunction.__doc__)
          + """

This function's results are cached in the `ALL_ANALYZERS` dictionary, and
it returns cached results when possible. Use `clearAnalysisCache` to
clear the analysis cache.
"""
        )

        # Save caching version of analyzer
        result = cast(AnalysisFunction, cachingAnalyzer)
        ALL_ANALYZERS[analyzerName] = result
        return result

    return makeCachedAnalyzer


T = TypeVar('T', bound=AnalysisFunction)
'Type variable for `elide` and `finalOnly`.'

def elide(analyzer: T) -> T:
    """
    Returns the given analyzer after noting that its result should *not*
    be included in CSV output by default.
    """
    ELIDE.add(analyzer.__name__)
    return analyzer


def finalOnly(analyzer: T) -> T:
    """
    Returns the given analyzer after noting that it should only be run on
    the final exploration step by default.
    """
    FINAL_ONLY.add(analyzer.__name__)
    return analyzer


#-----------------------#
# Generalizer Functions #
#-----------------------#

AnalyzerType = TypeVar('AnalyzerType', bound=AnyAnalyzer)
"""
Type var to forward through analyzer types.
"""

def registerCount(target: AnalyzerType, sizeName: str) -> AnalyzerType:
    """
    Registers a new analysis routine which uses the same analysis unit as
    the target routine but which returns the length of that routine's
    result. Returns `None` if the target routine does.

    Needs the target routine and the name to register the new analysis
    routine under.

    Returns the analysis function it creates.
    """
    def countAnalyzer(*args, **kwargs):
        'To be replaced'
        result = target(*args, **kwargs)
        if result is None:
            return None
        else:
            return len(result)

    countAnalyzer.__doc__ = (
        f"Measures count of the {target.__name__!r} result applied to"
        f" {target._unit!r}."
    )
    countAnalyzer.__name__ = sizeName

    # Register the new function & return the result
    return cast(
        AnalyzerType,
        analyzer(target._unit)(countAnalyzer)
    )


CombinerResult = TypeVar('CombinerResult')
"""
Type variable for the result of a combiner function.
"""

StepCombiner: 'TypeAlias' = Callable[
    [
        Dict[Union[base.DecisionID, OverspecificTransition], Any],
        core.DiscreteExploration,
        int
    ],
    CombinerResult
]
"""
A combiner function which gets a dictionary of per-decision or
per-transition values along with an exploration object and a step index
and combines the values into a `CombinerResult` that's specific to that
step.
"""

OverallCombiner: 'TypeAlias' = Callable[
    [
        Dict[Union[base.DecisionID, OverspecificTransition, int], Any],
        core.DiscreteExploration
    ],
    CombinerResult
]
"""
A combiner function which gets a dictionary of per-decision,
per-transition, and/or per-step values along with an exploration object
and combines the values into a `CombinerResult`.
"""


def registerStepCombined(
    name: str,
    resultName: str,
    combiner: StepCombiner[CombinerResult]
) -> StepAnalyzer:
    """
    Registers a new analysis routine which combines results of another
    routine either across all decisions/transitions at a step. The new
    routine will have a 'step' analysis unit.

    Needs the name of the target routine, the name to register the new
    analysis routine under, and the function that will be called to
    combine results, given a dictionary of results that maps
    decisions/transitions to results for each.

    Returns the analysis function it creates.
    """
    # Target function
    target = ALL_ANALYZERS[name]
    # Analysis unit of the target function
    targetUnit = target._unit

    if targetUnit not in ('stepDecision', 'stepTransition'):
        raise ValueError(
            f"Target analysis routine {name!r} has incompatible analysis"
            f" unit {targetUnit!r}."
        )

    def analysisCombiner(
        exploration: core.DiscreteExploration,
        step: int
    ) -> CombinerResult:
        'To be replaced'
        # Declare data here as generic type
        data: Dict[
            Union[base.DecisionID, OverspecificTransition, int],
            Any
        ]
        graph = exploration[step].graph
        if targetUnit == "stepDecision":
            analyzeStepDecision = cast(StepDecisionAnalyzer, target)
            data = {
                dID: analyzeStepDecision(exploration, step, dID)
                for dID in graph
            }
        elif targetUnit == "stepTransition":
            edges = graph.allEdges()
            analyzeStepTransition = cast(StepTransitionAnalyzer, target)
            data = {
                (src, transition, dst): analyzeStepTransition(
                    exploration,
                    step,
                    src,
                    transition,
                    dst
                )
                for (src, dst, transition) in edges
            }
        else:
            raise ValueError(
                f"Target analysis routine {name!r} has inconsistent"
                f" analysis unit {targetUnit!r} for 'step' result"
                f" unit."
            )
        return combiner(data, exploration, step)

    analysisCombiner.__doc__ = (
        f"Computes {combiner.__name__} for the {name!r} result over all"
        f" {targetUnit}s at each step."
    )
    analysisCombiner.__name__ = resultName

    # Register the new function & return it
    return analyzer("step")(analysisCombiner)


def registerFullCombined(
    name: str,
    resultName: str,
    combiner: OverallCombiner[CombinerResult]
) -> ExplorationAnalyzer:
    """
    Works like `registerStepCombined` but combines results over
    decisions/transitions/steps across the entire exploration to get one
    result for the entire thing, not one result per step. May also
    target an existing `ExplorationAnalyzer` whose result is a
    dictionary, in which case it will combine that dictionary's values.

    Needs the name of the target routine, the name to register the new
    analysis routine under, and the function that will be called to
    combine results, given a dictionary of results that maps
    decisions/transitions/steps to results for each.

    Returns the analysis function it creates.
    """
    # Target function
    target = ALL_ANALYZERS[name]
    # Analysis unit of the target function
    targetUnit = target._unit
    if targetUnit not in ('step', 'decision', 'transition', 'exploration'):
        raise ValueError(
            f"Target analysis routine {name!r} has incompatible analysis"
            f" unit {targetUnit!r}."
        )

    def analysisCombiner(  # type: ignore
        exploration: core.DiscreteExploration,
    ) -> CombinerResult:
        'To be replaced'
        # Declare data here as generic type
        data: Dict[
            Union[base.DecisionID, OverspecificTransition, int],
            Any
        ]
        if targetUnit == "step":
            analyzeStep = cast(StepAnalyzer, target)
            data = {
                step: analyzeStep(exploration, step)
                for step in range(len(exploration))
            }
        elif targetUnit == "decision":
            analyzeDecision = cast(DecisionAnalyzer, target)
            data = {
                dID: analyzeDecision(exploration, dID)
                for dID in exploration.allDecisions()
            }
        elif targetUnit == "transition":
            analyzeTransition = cast(TransitionAnalyzer, target)
            data = {
                (src, transition, dst): analyzeTransition(
                    exploration,
                    src,
                    transition,
                    dst
                )
                for (src, transition, dst) in exploration.allTransitions()
            }
        elif targetUnit == "exploration":
            analyzeExploration = cast(ExplorationAnalyzer, target)
            data = analyzeExploration(exploration)
        else:
            raise ValueError(
                f"Target analysis routine {name!r} has inconsistent"
                f" analysis unit {targetUnit!r} for 'step' result"
                f" unit."
            )
        return combiner(data, exploration)

    analysisCombiner.__doc__ = (
        f"Computes {combiner.__name__} for the {name!r} result over all"
        f" {targetUnit}s."
    )
    analysisCombiner.__name__ = resultName

    # Register the new function & return it
    return analyzer("exploration")(analysisCombiner)


def sumCombiner(data, *_):
    """
    Computes sum over numeric data as a "combiner" function to be used
    with `registerStepCombined` or `registerFullCombined`.

    Only sums values which are `int`s, `float`s, or `complex`es, ignoring
    any other values.
    """
    return sum(
        x for x in data.values() if isinstance(x, (int, float, complex))
    )


def meanCombiner(data, *_):
    """
    Computes mean over numeric data as a "combiner" function to be used
    with `registerStepCombined` or `registerFullCombined`.

    Only counts values which are `int`s, `float`s, or `complex`es, ignoring
    any other values. Uses `None` as the result when there are 0 numeric
    values.
    """
    numeric = [
        x for x in data.values() if isinstance(x, (int, float, complex))
    ]
    if len(numeric) == 0:
        return None
    else:
        return sum(numeric) / len(numeric)


def medianCombiner(data, *_):
    """
    Computes median over numeric data as a "combiner" function to be used
    with `registerStepCombined` or `registerFullCombined`.

    Only counts values which are `int`s, `float`s, or `complex`es, ignoring
    any other values. Uses `None` as the result when there are 0 numeric
    values.
    """
    numeric = sorted(
        x for x in data.values() if isinstance(x, (int, float, complex))
    )
    if len(numeric) == 0:
        return None
    elif len(numeric) == 1:
        return numeric[0]
    else:
        half = len(numeric) // 2
        if len(numeric) % 2 == 0:
            return (numeric[half - 1] + numeric[half]) / 2
        else:
            return numeric[half]


#---------------------------#
# Simple property functions #
#---------------------------#

@analyzer('decision')
def finalIdentity(
    exploration: core.DiscreteExploration,
    decision: base.DecisionID
) -> str:
    """
    Returns the `identityOf` result for the specified decision in the
    last step in which that decision existed.
    """
    for i in range(-1, -len(exploration) - 1, -1):
        situation = exploration.getSituation(i)
        try:
            return situation.graph.identityOf(decision)
        except core.MissingDecisionError:
            pass
    raise core.MissingDecisionError(
        f"Decision {decision!r} never existed."
    )


@analyzer('step')
def currentDecision(
    exploration: core.DiscreteExploration,
    step: int
) -> Optional[base.DecisionID]:
    """
    Returns the `base.DecisionID` for the current decision in a given
    situation.
    """
    return exploration[step].state['primaryDecision']


@analyzer('step')
def currentDecisionIdentity(
    exploration: core.DiscreteExploration,
    step: int
) -> str:
    """
    Returns the `identityOf` string for the current decision in a given
    situation.
    """
    situation = exploration[step]
    return situation.graph.identityOf(situation.state['primaryDecision'])


@analyzer('step')
def observedSoFar(
    exploration: core.DiscreteExploration,
    step: int
) -> Set[base.DecisionID]:
    """
    Returns the set of all decision IDs observed so far. Note that some
    of them may no longer be present in the graph at the given step if
    they got merged or deleted.
    """
    # Can't allow negative steps (caching would fail)
    if step < 0:
        raise IndexError(f"Invalid step (can't be negative): {step!r}")
    elif step == 0:
        result = set()
    else:
        result = observedSoFar(exploration, step - 1)
    result |= set(exploration[step].graph)
    return result


totalDecisionsSoFar = registerCount(observedSoFar, 'totalDecisionsSoFar')


@analyzer('step')
def justObserved(
    exploration: core.DiscreteExploration,
    step: int
) -> Set[base.DecisionID]:
    """
    Returns the set of new `base.DecisionID`s that first appeared at the
    given step. Will be empty for steps where no new decisions are
    observed. Note that this is about decisions whose existence becomes
    known, NOT decisions which get confirmed.
    """
    if step == 0:
        return observedSoFar(exploration, step)
    else:
        return (
            observedSoFar(exploration, step - 1)
          - observedSoFar(exploration, step)
        )


newDecisionCount = registerCount(justObserved, 'newDecisionCount')


@elide
@analyzer('stepDecision')
def hasBeenObserved(
    exploration: core.DiscreteExploration,
    step: int,
    dID: base.DecisionID
) -> bool:
    """
    Whether or not the specified decision has been observed at or prior
    to the specified step. Note that it may or may not actually be a
    decision in the specified step (e.g., if it was previously observed
    but then deleted).
    """
    return dID in observedSoFar(exploration, step)


@analyzer('exploration')
def stepsObserved(
    exploration: core.DiscreteExploration,
) -> Dict[base.DecisionID, int]:
    """
    Returns a dictionary that holds the step at which each decision was
    first observed, keyed by decision ID.
    """
    result = {}
    soFar: Set[base.DecisionID] = set()
    for step, situation in enumerate(exploration):
        new = set(situation.graph) - soFar
        for dID in new:
            result[dID] = step
        soFar |= new
    return result


@analyzer('decision')
def stepObserved(
    exploration: core.DiscreteExploration,
    dID: base.DecisionID
) -> int:
    """
    Returns the step at which the specified decision was first observed
    (NOT confirmed).
    """
    try:
        return stepsObserved(exploration)[dID]
    except KeyError:
        raise core.MissingDecisionError(
            f"Decision {dID!r} was never observed."
        )


@analyzer('exploration')
def stepsConfirmed(
    exploration: core.DiscreteExploration,
) -> Dict[base.DecisionID, int]:
    """
    Given an exploration, returns a dictionary mapping decision IDs to
    the step at which each was first confirmed. Decisions which were
    never confirmed will not be included in the dictionary.
    """
    result = {}
    for i, situation in enumerate(exploration):
        for dID in situation.graph:
            if (
                dID not in result
            and 'unconfirmed' not in situation.graph.decisionTags(dID)
            ):
                result[dID] = i
    return result


@analyzer('decision')
def stepConfirmed(
    exploration: core.DiscreteExploration,
    dID: base.DecisionID
) -> Optional[int]:
    """
    Returns the step at which the specified decision was first confirmed,
    or `None` if it was never confirmed. Returns `None` for invalid
    decision IDs.
    """
    return stepsConfirmed(exploration).get(dID)


@analyzer('exploration')
def stepsVisited(
    exploration: core.DiscreteExploration,
) -> Dict[base.DecisionID, List[int]]:
    """
    Given an exploration, returns a dictionary mapping decision IDs to
    the list of steps at which each was visited. Decisions which were
    never visited will not be included in the dictionary.
    """
    result: Dict[base.DecisionID, List[int]] = {}
    for i, situation in enumerate(exploration):
        for dID in situation.graph:
            if dID in base.combinedDecisionSet(situation.state):
                result.setdefault(dID, []).append(i)
    return result


@finalOnly
@analyzer('stepDecision')
def hasBeenVisited(
    exploration: core.DiscreteExploration,
    step: int,
    dID: base.DecisionID
) -> bool:
    """
    Whether or not the specified decision has been visited at or prior
    to the specified step. Note that it may or may not actually be a
    decision in the specified step (e.g., if it was previously observed
    but then deleted).
    """
    visits = stepsVisited(exploration).get(dID, [])
    # No visits -> not visited yet
    if len(visits) == 0:
        return False
    else:
        # First visit was at or before this step
        return min(visits) <= step


@analyzer('decision')
def stepFirstVisited(
    exploration: core.DiscreteExploration,
    decision: base.DecisionID,
) -> Optional[int]:
    """
    Returns the first step at which the given decision was visited, or
    `None` if the decision was never visited.
    """
    vis = stepsVisited(exploration)
    if decision in vis:
        return min(vis[decision])
    else:
        return None


@analyzer('decision')
def stepsActive(
    exploration: core.DiscreteExploration,
    decision: base.DecisionID,
) -> Optional[int]:
    """
    Returns the total number of steps in which this decision was active.
    """
    vis = stepsVisited(exploration)
    if decision in vis:
        return len(vis[decision])
    else:
        return 0


@analyzer('exploration')
def stepsTransisionsObserved(
    exploration: core.DiscreteExploration
) -> Dict[OverspecificTransition, int]:
    """
    Returns a dictionary that holds the step at which each transition was
    first observed, keyed by (source-decision, transition-name,
    destination-decision) triples.

    Does NOT distinguish between cases where a once-deleted transition
    was later reinstated (unless it had a different destination in the
    end).
    """
    result = {}
    for i, situation in enumerate(exploration):
        for dID in situation.graph:
            destinations = situation.graph.destinationsFrom(dID)
            for name, dest in destinations.items():
                key = (dID, name, dest)
                if key not in result:
                    result[key] = i
    return result


@analyzer('transition')
def stepObservedTransition(
    exploration: core.DiscreteExploration,
    source: base.DecisionID,
    transition: base.Transition,
    destination: base.DecisionID
) -> Optional[int]:
    """
    Returns the step within the exploration at which the specified
    transition was first observed. Note that transitions which get
    renamed do NOT preserve their identities, so a search for a renamed
    transition will return the step on which it was renamed (assuming it
    didn't change destination).

    Returns `None` if the specified transition never existed in the
    exploration.
    """
    obs = stepsTransisionsObserved(exploration)
    return obs.get((source, transition, destination))


@analyzer('step')
def transitionTaken(
    exploration: core.DiscreteExploration,
    step: int
) -> Optional[OverspecificTransition]:
    """
    Returns the source decision Id, the name of the transition taken, and
    the destination decision ID at the given step. This is the transition
    chosen at that step whose consequences were triggered resulting in
    the next step. Returns `None` for steps where no transition was
    taken (e.g., wait, warp, etc.).

    Note that in some cases due to e.g., a 'follow' effect, multiple
    transitions are taken at a step. In that case, this returns the name
    of the first transition taken (which would have triggered any
    others).

    Also in some cases, there may be multiple starting nodes given, in
    which case the first such node (by ID order) which has a transition
    with the identified transition name will be returned, or None if none
    of them match.
    """
    start, transition, end = exploration.movementAtStep(step)
    graph = exploration[step].graph
    if start is None or transition is None:
        return None
    if isinstance(start, set):
        for dID in sorted(start):
            destination = graph.getDestination(dID, transition)
            if destination is not None:
                return (dID, transition, destination)
        return None
    else:
        destination = graph.getDestination(start, transition)
        if destination is not None:
            return (start, transition, destination)
        else:
            return None


@analyzer('exploration')
def transitionStepsTaken(
    exploration: core.DiscreteExploration
) -> Dict[OverspecificTransition, List[int]]:
    """
    Returns a dictionary mapping each specific transition that was taken
    at least once to the list of steps on which it was taken. Does NOT
    account for transitions elided by 'jaunt' warps, nor for transitions
    taken as a result of follow/bounce effects.

    TODO: Account for those?
    """
    result: Dict[OverspecificTransition, List[int]] = {}
    for i in range(len(exploration)):
        taken = transitionTaken(exploration, i)
        if taken is not None:
            if taken in result:
                result[taken].append(i)
            else:
                result[taken] = [i]

    return result


@analyzer('transition')
def stepsTaken(
    exploration: core.DiscreteExploration,
    source: base.DecisionID,
    transition: base.Transition,
    destination: base.DecisionID
) -> int:
    """
    Returns the list of exploration steps on which a particular
    transition has been taken. Returns an empty list for transitions that
    were never taken.

    Note that this does NOT account for times taken as a result of
    follow/bounce effects, and it does NOT account for all times a
    transition was taken when warp effects are used as shorthand for
    jaunts across the graph.
    
    TODO: Try to account for those?
    """
    return transitionStepsTaken(exploration).get(
        (source, transition, destination),
        []
    )


@analyzer('transition')
def timesTaken(
    exploration: core.DiscreteExploration,
    source: base.DecisionID,
    transition: base.Transition,
    destination: base.DecisionID
) -> int:
    """
    Returns the number of times a particular transition has been taken
    throughout the exploration. Returns 0 for transitions that were never
    taken.

    Note that this does NOT account for times taken as a result of
    follow/bounce effects, and it does NOT account for all times a
    transition was taken when warp effects are used as shorthand for
    jaunts across the graph.
    
    TODO: Try to account for those?
    """
    return len(stepsTaken(exploration, source, transition, destination))


#--------------------#
# Analysis functions #
#--------------------#

def unexploredBranches(
    graph: core.DecisionGraph,
    context: Optional[base.RequirementContext] = None
) -> List[SpecificTransition]:
    """
    Returns a list of from-decision, transition-at-that-decision pairs
    which each identify an unexplored branch in the given graph.

    When a `context` is provided it only counts options whose
    requirements are satisfied in that `RequirementContext`, and the
    'searchFrom' part of the context will be replaced by both ends of
    each transition tested. This doesn't perfectly map onto actually
    reachability since nodes between where the player is and where the
    option is might force changes in the game state that make it
    un-takeable.

    TODO: add logic to detect trivially-unblocked edges?
    """
    result = []
    # TODO: Fix networkx type stubs for MultiDiGraph!
    for (src, dst, transition) in graph.allEdges():
        req = graph.getTransitionRequirement(src, transition)
        localContext: Optional[base.RequirementContext] = None
        if context is not None:
            localContext = base.RequirementContext(
                state=context.state,
                graph=context.graph,
                searchFrom=graph.bothEnds(src, transition)
            )
        # Check if this edge goes from a confirmed to an unconfirmed node
        if (
            graph.isConfirmed(src)
        and not graph.isConfirmed(dst)
        and (localContext is None or req.satisfied(localContext))
        ):
            result.append((src, transition))
    return result


@analyzer('step')
def allUnexploredBranches(
    exploration: core.DiscreteExploration,
    step: int
) -> List[SpecificTransition]:
    """
    Returns the list of unexplored branches in the specified situation's
    graph, regardless of traversibility (see `unexploredBranches`).
    """
    return unexploredBranches(exploration[step].graph)


unexploredBranchCount = registerCount(
    allUnexploredBranches,
    'unexploredBranchCount'
)


@analyzer('step')
def traversableUnexploredBranches(
    exploration: core.DiscreteExploration,
    step: int
) -> List[SpecificTransition]:
    """
    Returns the list of traversable unexplored branches in the specified
    situation's graph (see `unexploredBranches`). Does not perfectly
    account for all traversibility information, because it uses a single
    context from which to judge traversibility (TODO: Fix that).
    """
    situation = exploration[step]
    context = base.genericContextForSituation(
        situation,
        base.combinedDecisionSet(situation.state)
    )
    return unexploredBranches(situation.graph, context)


traversableUnexploredCount = registerCount(
    traversableUnexploredBranches,
    'traversableUnexploredCount'
)


@finalOnly
@analyzer('stepDecision')
def actions(
    exploration: core.DiscreteExploration,
    step: int,
    decision: base.DecisionID
) -> Optional[Set[base.Transition]]:
    """
    Given a particular decision at a particular step, returns the set of
    actions available at that decision in that step. Returns `None` if
    the specified decision does not exist.
    """
    graph = exploration[step].graph
    if decision not in graph:
        return None
    return graph.decisionActions(decision)


actionCount = registerCount(actions, 'actionCount')
finalOnly(actionCount)

totalActions = registerStepCombined(
    'actionCount',
    'totalActions',
    sumCombiner
)
finalOnly(totalActions)

meanActions = registerStepCombined(
    'actionCount',
    'meanActions',
    meanCombiner
)
finalOnly(meanActions)

medianActions = registerStepCombined(
    'actionCount',
    'medianActions',
    medianCombiner
)
finalOnly(medianActions)


@finalOnly
@analyzer('stepDecision')
def branches(
    exploration: core.DiscreteExploration,
    step: int,
    decision: base.DecisionID
) -> Optional[int]:
    """
    Computes the number of branches at a particular decision, not
    counting actions, but counting as separate branches multiple
    transitions which lead to the same decision as each other. Returns
    `None` for unconfirmed and nonexistent decisions so that they aren't
    counted as part of averages, even though unconfirmed decisions do
    have countable branches.
    """
    graph = exploration[step].graph
    if decision not in graph or not graph.isConfirmed(decision):
        return None

    dests = graph.destinationsFrom(decision)
    branches = 0
    for transition, dest in dests.items():
        if dest != decision:
            branches += 1

    return branches


totalBranches = registerStepCombined(
    'branches',
    'totalBranches',
    sumCombiner
)
finalOnly(totalBranches)

meanBranches = registerStepCombined(
    'branches',
    'meanBranches',
    meanCombiner
)
finalOnly(meanBranches)

medianBranches = registerStepCombined(
    'branches',
    'medianBranches',
    medianCombiner
)
finalOnly(medianBranches)


@analyzer('decision')
def arrivals(
    exploration: core.DiscreteExploration,
    decision: base.DecisionID
) -> int:
    """
    Given an `DiscreteExploration` object and a particular `Decision`
    which exists at some point during that exploration, counts the number
    of times that decision was in the active decision set for a step
    after not being in that set the previous step. Effectively, counts
    how many times we arrived at that decision, ignoring steps where we
    remained at it due to a wait or an action or the like.

    Returns 0 even for decisions that aren't part of the exploration.
    """
    visits = stepsVisited(exploration)
    result = 0
    prev = -2  # won't be contiguous with step 0
    for step in visits.get(decision, []):
        # if previous visited step wasn't the prior step it's a revisit
        if prev != step - 1:
            result += 1
        prev = step

    return result


@analyzer('decision')
def revisits(
    exploration: core.DiscreteExploration,
    decision: base.DecisionID
) -> int:
    """
    Returns the number of times we revisited the target decision, which
    is just `arrivals` minus 1 for the first arrival, but not < 0.
    """
    return max(0, arrivals(exploration, decision) - 1)


totalRevisits = registerFullCombined(
    'revisits',
    'totalRevisits',
    sumCombiner
)

meanRevisits = registerFullCombined(
    'revisits',
    'meanRevisits',
    meanCombiner
)

medianRevisits = registerFullCombined(
    'revisits',
    'medianRevisits',
    medianCombiner
)


#-------------------#
# Paths & distances #
#-------------------#

HopPaths: 'TypeAlias' = Dict[
    Tuple[base.DecisionID, base.DecisionID],
    Optional[List[base.DecisionID]]
]
"""
Records paths between decisions ignoring edge directions & requirements.
Stores a list of decision IDs to traverse keyed by a decision ID pair
where the smaller decision ID comes first (since paths are symmetric).
"""

def hopDistance(
    hopPaths: HopPaths,
    src: base.DecisionID,
    dst: base.DecisionID
) -> Optional[int]:
    """
    Returns the number of hops required to move from the given source to
    the given destination, ignoring edge directions & requirements.
    Looks that up in the given `HopPaths` dictionary. Returns 0 when
    source and destination are the same.

    For example:

    >>> e = core.DiscreteExploration.example()
    >>> hops = shortestHopPaths(e)
    >>> hopDistance(hops, 0, 1)
    1
    >>> hopDistance(hops, 1, 0)
    1
    >>> hopDistance(hops, 0, 0)
    0
    >>> hopDistance(hops, 0, 0)
    0
    >>> hopDistance(hops, 0, 4) is None
    True
    >>> hopDistance(hops, 4, 0) is None
    True
    >>> hopDistance(hops, 0, 5)
    2
    >>> hopDistance(hops, 5, 0)
    2
    >>> hopDistance(hops, 5, 1)
    3
    >>> hopDistance(hops, 1, 5)
    3
    >>> hopDistance(hops, 3, 5)
    1
    >>> hopDistance(hops, 5, 3)
    1
    >>> dIDs = list(e[-1].graph)
    >>> for i, src in enumerate(dIDs):
    ...     for j in range(i + 1, len(dIDs)):
    ...         dst = dIDs[j]
    ...         assert (
    ...             hopDistance(hops, src, dst) == hopDistance(hops, dst, src)
    ...         )
    """
    if src == dst:
        return 0
    elif src < dst:
        path = hopPaths.get((src, dst))
        if path is None:
            return None
        else:
            return 1 + len(path)
    else:
        path = hopPaths.get((dst, src))
        if path is None:
            return None
        else:
            return 1 + len(path)


@elide
@analyzer('exploration')
def shortestHopPaths(
    exploration: core.DiscreteExploration,
    edgeFilter: Optional[Callable[
        [base.DecisionID, base.Transition, base.DecisionID, core.DecisionGraph],
        bool
    ]] = None
) -> HopPaths:
    """
    Creates a dictionary that holds shortest paths between pairs of
    nodes, ignoring edge directions and requirements entirely.

    If given an `edgeFilter`, that function is applied with source ID,
    transition name, destination ID, and full graph as arguments and
    edges for which it returns False are ignored when computing hops.
    Note that you have to filter out all edges in both directions between
    two nodes for there not to be a 1-hop path between them.

    Keys in the dictionary are pairs of decision IDs, where the decision
    with the smaller ID always comes first (because shortest hop paths
    are symmetric so we don't store the reverse paths). Values are lists
    of decision IDs that can be traversed to get from the first decision
    to the second, with an empty list indicating adjacent decisions
    (note that these "hop paths" cannot always be traversed in the
    actual graph because they may go the "wrong way" across one-way
    connections). The number of hops required to get between the nodes
    is one more than the length of the path. Decision pairs which are
    not reachable from each other will not be included in the
    dictionary. Only decisions present in the final graph in the
    exploration will be included, and only edges present in that final
    graph will be considered.

    Where there are multiple shortest hop paths, an arbitrary one is
    included in the result.

    TODO: EXAMPLE
    >>> e = core.DiscreteExploration.example()
    >>> print(e[-1].graph.namesListing(e[-1].graph))
      0 (House)
      1 (_u.0)
      2 (Cellar)
      3 (Yard)
      5 (Lane)
    <BLANKLINE>
    >>> shortest = dict(nx.all_pairs_shortest_path(e[-1].graph.connections()))
    >>> for src in shortest:
    ...    print(f"{src} -> {shortest[src]}")
    0 -> {0: [0], 1: [0, 1], 2: [0, 2], 3: [0, 3], 5: [0, 3, 5]}
    1 -> {1: [1], 0: [1, 0], 2: [1, 0, 2], 3: [1, 0, 3], 5: [1, 0, 3, 5]}
    2 -> {2: [2], 0: [2, 0], 3: [2, 3], 1: [2, 0, 1], 5: [2, 3, 5]}
    3 -> {3: [3], 0: [3, 0], 2: [3, 2], 5: [3, 5], 1: [3, 0, 1]}
    5 -> {5: [5], 3: [5, 3], 0: [5, 3, 0], 2: [5, 3, 2], 1: [5, 3, 0, 1]}
    >>> hops = shortestHopPaths(e)
    >>> for src in hops:
    ...     print(f"{src} -> {hops[src]}")
    (0, 1) -> []
    (0, 2) -> []
    (0, 3) -> []
    (0, 5) -> [3]
    (1, 2) -> [0]
    (1, 3) -> [0]
    (1, 5) -> [0, 3]
    (2, 3) -> []
    (2, 5) -> [3]
    (3, 5) -> []
    """
    graph = exploration[-1].graph
    allIDs = sorted(graph)
    connections = graph.connections(edgeFilter)
    shortest = dict(nx.all_pairs_shortest_path(connections))

    result = {}
    for i, src in enumerate(allIDs):
        for j in range(i + 1, len(allIDs)):
            dst = allIDs[j]
            path = shortest.get(src, {}).get(dst, None)
            if path is not None:
                result[(src, dst)] = path[1:-1]

    return result


#---------------#
# Full analysis #
#---------------#

def runFullAnalysis(
    exploration: core.DiscreteExploration, 
    elide: Collection[str] = ELIDE,
    finalOnly: Collection[str] = FINAL_ONLY
) -> FullAnalysisResults:
    """
    Runs every single analysis function on every valid target for that
    function in the given exploration, building up the cache of
    `FullAnalysisResults` in `ALL_ANALYZERS`. Returns the relevant
    `FullAnalysisResults` object.

    Skips analyzers in the provided `elide` collection, which by default
    is the `ELIDE` global set containing functions explicitly decorated
    with `elide`. Analyzers in the `FINAL_ONLY` set are only applied to
    the final decision graph in the exploration (although note that they
    might call other analyzers which recursively need to analyze prior
    steps). `finalOnly` only has an effect for analyzers with 'step',
    'stepDecision', or 'stepTransition' units.
    """
    for aName, analyzer in ALL_ANALYZERS.items():
        # Skip this one if we're told to
        if aName in elide:
            continue
        # Split out cases for each unit & apply as appropriate
        unit = analyzer._unit
        if unit == 'step':
            sa = cast(StepAnalyzer, analyzer)
            if aName in finalOnly:
                sa(exploration, len(exploration) - 1)
            else:
                for step in range(len(exploration)):
                    sa(exploration, step)
        elif unit == 'stepDecision':
            sda = cast(StepDecisionAnalyzer, analyzer)
            # Only apply to final graph if it's in finalOnly
            if aName in finalOnly:
                step = len(exploration) - 1
                for dID in exploration[step].graph:
                    sda(exploration, step, dID)
            else:
                for step in range(len(exploration)):
                    for dID in exploration[step].graph:
                        sda(exploration, step, dID)
        elif unit == 'stepTransition':
            sta = cast(StepTransitionAnalyzer, analyzer)
            if aName in finalOnly:
                step = len(exploration) - 1
                edges = exploration[step].graph.allEdges()
                for (src, dst, transition) in edges:
                    sta(exploration, step, src, transition, dst)
            else:
                for step in range(len(exploration)):
                    edges = exploration[step].graph.allEdges()
                    for (src, dst, transition) in edges:
                        sta(exploration, step, src, transition, dst)
        elif unit == 'decision':
            da = cast(DecisionAnalyzer, analyzer)
            for dID in exploration.allDecisions():
                da(exploration, dID)
        elif unit == 'transition':
            ta = cast(TransitionAnalyzer, analyzer)
            for (src, trans, dst) in exploration.allTransitions():
                ta(exploration, src, trans, dst)
        elif unit == 'exploration':
            ea = cast(ExplorationAnalyzer, analyzer)
            ea(exploration)
        else:
            raise ValueError(f"Invalid analysis unit {unit!r}.")

    return ANALYSIS_RESULTS[id(exploration)]


#--------------------#
# Analysis accessors #
#--------------------#

# These functions access pre-computed analysis results. Call
# `runFullAnalysis` first to populate those.


def getDecisionAnalyses(
    exploration: core.DiscreteExploration,
    dID: base.DecisionID
) -> AnalysisResults:
    """
    Retrieves all pre-computed all-step analysis results for the
    specified decision. Use `runFullAnalysis` or call specific analysis
    functions of interest first to populate these results. Does not
    include per-step decision analyses.

    Returns the dictionary of `AnalysisResults`, which can be modified to
    update stored results if necessary (although it's better to write
    additional analysis routines using the `@analyzer` decorator).
    """
    cached = ANALYSIS_RESULTS.setdefault(
        id(exploration),
        newFullAnalysisResults()
    )
    return cached["perDecision"].setdefault(dID, {})


def getTransitionAnalyses(
    exploration: core.DiscreteExploration,
    source: base.DecisionID,
    transition: base.Transition,
    destination: base.DecisionID
) -> AnalysisResults:
    """
    Like `getDecisionAnalyses` but returns analyses for a transition
    instead of a decision.
    """
    cached = ANALYSIS_RESULTS.setdefault(
        id(exploration),
        newFullAnalysisResults()
    )
    return cached["perTransition"].setdefault(
        (source, transition, destination),
        {}
    )


def getStepDecisionAnalyses(
    exploration: core.DiscreteExploration,
    step: int,
    dID: base.DecisionID
) -> AnalysisResults:
    """
    Like `getDecisionAnalyses` but for analyses applicable only to the
    specified exploration step.
    """
    cached = ANALYSIS_RESULTS.setdefault(
        id(exploration),
        newFullAnalysisResults()
    )
    stepwise = cached.setdefault("perStepDecision", [])
    while step >= len(stepwise):
        stepwise.append({})
    return stepwise[step].setdefault(dID, {})


def getStepTransitionAnalyses(
    exploration: core.DiscreteExploration,
    step: int,
    source: base.DecisionID,
    transition: base.Transition,
    destination: base.DecisionID
) -> AnalysisResults:
    """
    Like `getStepDecisionAnalyses` but for a transition at a particular
    step, not a decision.
    """
    cached = ANALYSIS_RESULTS.setdefault(
        id(exploration),
        newFullAnalysisResults()
    )
    stepwise = cached.setdefault("perStepTransition", [])
    while step >= len(stepwise):
        stepwise.append({})
    return stepwise[step].setdefault((source, transition, destination), {})


def getStepAnalyses(
    exploration: core.DiscreteExploration,
    step: int
) -> AnalysisResults:
    """
    Like `getDecisionAnalyses` but retrieves full-step analysis results
    for the specified exploration step.
    """
    cached = ANALYSIS_RESULTS.setdefault(
        id(exploration),
        newFullAnalysisResults()
    )
    stepwise = cached.setdefault("perStep", [])
    while step >= len(stepwise):
        stepwise.append({})
    return stepwise[step]


def getExplorationAnalyses(
    exploration: core.DiscreteExploration
) -> AnalysisResults:
    """
    Like `getDecisionAnalyses` but retrieves full-exploration analysis
    results.
    """
    cached = ANALYSIS_RESULTS.setdefault(
        id(exploration),
        newFullAnalysisResults()
    )
    return cached.setdefault("overall", {})


class AnalyzersByUnit(TypedDict):
    """
    Holds lists of analyzers for each analysis unit type.
    """
    step: List[StepAnalyzer]
    stepDecision: List[StepDecisionAnalyzer]
    stepTransition: List[StepTransitionAnalyzer]
    decision: List[DecisionAnalyzer]
    transition: List[TransitionAnalyzer]
    exploration: List[ExplorationAnalyzer]


def analyzersByUnit(onlyInclude: Optional[Set[str]] = None) -> AnalyzersByUnit:
    """
    Returns an `AnalyzersByUnit` dictionary containing all analyzers
    from `ALL_ANALYZERS` which are in the given `onlyInclude` set (or
    just all of them if no set is specified). This will by default be all
    analyzers registered so far.
    """
    byUnit: AnalyzersByUnit = {
        "step": [],
        "stepDecision": [],
        "stepTransition": [],
        "decision": [],
        "transition": [],
        "exploration": []
    }
    for analyzerName in ALL_ANALYZERS:
        if onlyInclude is not None and analyzerName not in onlyInclude:
            continue
        analyzer = ALL_ANALYZERS[analyzerName]
        unit = analyzer._unit
        byUnit[unit].append(analyzer)  # type: ignore
        # Mypy will just have to trust that We've put the correct unit
        # values on each analyzer. That relationship is type-checked in
        # the `analyzer` definition.

    return byUnit
