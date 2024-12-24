"""
# `exploration` library Journaling Guide

This page explains the basics of the journaling language that's supported
via the `JournalObserver` class in `journal.py`. More detailed references
for specific types and methods are available in that file, but here we
attempt to summarize them.

This document assumes you are familiar with the stuff described in the
`exploration.overview` file; you should read that first if you haven't
already.


## What is a journal?

While the `exploration.core.DiscreteExploration` class has many methods
for creating and updating exploration records, it's cumbersome to use
them to actually create a full record of gameplay. To make it easier to
record the exploration process, the `exploration.journal` module (and in
particular, the `exploration.journal.JournalObserver` class) is provided
to parse a domain-specific language designed to record exploration
progress. There is a rough correspondence between the
`DiscreteExploration` API and the journal format entries, but there's
some additional automatic state that gets tracked by a `JournalObserver`
object that allows for even more concise specification of exploration
progress.

Fundamentally, a "journal" is text, stored in a file or variable, which
consists of a series of entries, each on a single line (or spanning
multiple lines using `[` and `]` symbols as directional quotation marks).
The entry begins with an entry type, such as 'explore' or 'observe' and
then includes additional parameters which define what the player wants to
note down.


## Journal Entry Types

### Core Entry Types

The most common journal entry types are 'observe', 'explore',
'requirement', 'effect', and 'retrace':

1. 'observe', or 'o' for short, which indicates that a new *transition*
    has been noticed. The name of the transition is the only required
    parameter, if its destination and/or reciprocal name are known, these
    can be supplied as well. Observing a transition does not imply a new
    exploration step has been taken, and typically after exploring to a
    new decision point, multiple observations of options at that decision
    will follow immediately. For example:

        `observe left`

    states that a transition named 'left' has been observed, while
        
        `o right rightSide left`

    states that a transition named 'right' has been observed, which
    connects to a decision named 'rightSide', with a reciprocal
    transition from 'rightSide' back to the current decision which is
    named 'left'.

2. 'explore', or 'x' for short, which indicates that a
    previously-unexplored transition is followed. The name of the
    transition taken is required. If the destination name for that
    transition has not yet been specified, that is required as well, and
    a reciprocal transition name may also be provided. For example:

        `explore right rightSide left`

    would indicate that the 'right' transition from the current decision
    was taken, leading to a decision named 'rightSide' with the
    reciprocal transition back to the previous decision being named
    'left'. (By default, if no reciprocal name is given the reciprocal
    transition will be named 'return'. If '-' is used as the reciprocal
    name, then a one-way transition without a reciprocal will be created.)
    The entry
    
        `x enterDoor innerRoom`

    would thus denote exploring a transition 'enterDoor' to reach a room
    'innerRoom' with the reciprocal transition name defaulting to
    'return'.

    Note that the transition taken need not have already been observed;
    the 'explore' entry will add it if necessary before exploring it.
    Also, if an 'observe' entry already specified at least the
    destination name, then it can be left out when exploring, so a pair
    of entries like:

        ```txt
        o right rightSide left
        x right
        ```

    would first establish the 'right' transition, its destination, and
    its reciprocal, and then explore that transition. This is actually
    useful when other entries happen between the two.

3. 'requirement', or 'q' for short, indicates that the
    most-recently-mentioned transition has a requirement. This will apply
    to the transition just mentioned via an 'observe' or 'explore' entry,
    or possibly other entry types that mention a transition. As discussed
    in the `exploration.overview` documentation, transitions may use
    *capabilities*, *tokens*, and/or *mechanism* states as requirements,
    and may combine these using boolean 'and', 'or', and 'not' operators.
    After the entry type, a 'requirement' entry should include a single
    expression specifying the requirement to apply, using `&` for and,
    `|` for or, and `!` for not. Parentheses `()` can be used for
    grouping sub-expressions, so an entry like:

        `requirement boots|(sandals&!softFeet)`

    would be satisfied by the 'boots' capability, or by the combination
    of the 'sandals' capability and the lack of the 'softFeet' capability.
    Brackets `[]` are necessary to enclose a requirement that includes
    spaces in it, for example:

        `q [ boots | ( sandals & !softFeet ) ]`

    The requirement could even be split across multiple lines if brackets
    are used, provided that the opening bracket is at the end of a line,
    and the closing bracket is alone on a line (this use of brackets to
    combine words into a single parameter applies to all entry types).

    To require at least a certain number of tokens, use the token name,
    followed by `*`, followed by an integer, so

        `q !leaf*3`

    would require that the player has 2 or fewer 'leaf' tokens (note the
    `!`). Requiring a mechanism state uses the fully-specified or generic
    mechanism name, followed by a colon `:` and then the required state,
    for example:

        `q gate:open`

    requires that the 'gate' mechanism be in the 'open' state, whereas

        `q RollingHills::greenHill::gate:open`

    requires that the 'gate' mechanism which is at the 'greenHill'
    decision within the 'RollingHills' zone is in the 'open' state. Note
    the use of `::` to specify a decision name and preceding that a zone
    name for the mechanism location; both are optional, and an additional
    domain may be specified using `//` before the zone. This syntax for
    specifying domain/zone/decision is used in other places as well.

    Of course, token and/or mechanism requirements can be combined with
    capability requirements using boolean operators, for example:

        `q gate:open|coin*3|superJump`

    requires that either the 'gate' mechanism is in the 'open' state, you
    have three 'coin' tokens, or you have the 'superJump' capability.
    This could be combined with a conditional effect stating that if you
    don't have superJump and the gate is not open, you will lose three
    coins and set the gate mechanism to open...

4. 'effect', or 'e' for short, establishes a consequence of the
    most-recently-mentioned transition. Note that it does not apply the
    consequence, it merely establishes it as something that would apply
    were that transition taken, so if you want to note a consequence that
    was applied by the transition you just took, you should use 'apply'
    with the 'transition' target (see below). Consequences are discussed
    in more detail in the `exploration.overview` document and are
    defined as `exploration.base.Consequence`. The syntax for defining
    complex consequences is beyond the scope of this document (see
    `exploration.parsing.ParseFormat.parseConsequence` and related
    methods like `parseCondition`, `parseEffect`, and `parseChallenge`
    although these currently only have a few examples of the relevant
    formats). Simple one-effect consequences can be things like:

        `gain key*1`

    which adds one 'key' token, or

        `set gate:open`

    which sets the 'gate' mechanism to the 'open' state, or simply

        `deactivate`

    which once applied prevents that transition from being taken again.

5. 'retrace'

### Entry Targets

### Additional Entry Types

Besides these core entry types, a few others are used less frequently for
key actions: 'START', 'END', 'return', 'action', 'wait', 'warp', 'apply',
'mechanism', 'zone', 'tag', and 'annotate'


## The Journaling Process


## Debugging a Journal


The 'DEBUG' entry

## Advanced Journal Entry Types

For now, refer to the `exploration.journal.JournalEntryType`
documentation for these additional journal entry types, and for the full
list of all available journal entry types.

### Revising Structure

'unify', 'obviate', 'extinguish', 'complicate'

### Reverting Game State

'revert'

### Unknown Requirements

'fulfills'

### Custom Entry Types

'alias' and 'custom'

### Relative Mode

'relative'
"""

