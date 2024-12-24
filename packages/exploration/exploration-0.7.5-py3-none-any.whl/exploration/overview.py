"""
# `exploration` library Overview

This page explains an overview of the most important concepts that the
`exploration` library deals with.

## What is it for?

The `exploration` library is designed to support **formal** analysis of
exploration processes in videogame spaces which can be approximated as a
graph of **discrete** and **repeatable** decisions. It's heavily inspired
by [the Boss Keys YouTube
series](https://www.youtube.com/playlist?list=PLc38fcMFcV_ul4D6OChdWhsNsYY3NA5B2)

It could also be applied in some non-game contexts as well. Adventure
games, 2D RPGs, action-adventure games, and most centrally, Metroidvania
games (roughly, side-scrolling 2D exploration-adventure games) are all
genres where it should be applicable. The kinds of questions it might
help answer include questions like:

- "Which areas are accessible via which other areas, with which items?"
- "How many untaken branches has the player passed at this point?"
- "What percentage of players get item X before item Y?"

Along with more qualitative analysis, it might also help support research
into other questions, like "what level structures make players feel
claustrophobic?" The main goal is to have a data format that can be used
to write down exploration processes, which is abstract enough to enable
comparisons between different games and/or different players playing the
same game (though there are lots of issues with the latter application).

It does rely on human judgement to figure out what should be classified
as a "decision," and it also does not work well for certain types of
games, like open-world games, where you never really make the same
decision twice (code for dealing with these types of games is in the
planning stages).


## The DTER Model

We model the exploration process in games using a highly abstract model
that includes Decisions, Transitions, Effects, and Requirements as part
of a **decision graph** (represented by the `core.DecisionGraph` class).
Many aspects of the game, such as how difficult the enemies are, what the
story, graphics, and audio are like, and how a player specifically
navigates the geometry of individual rooms are by default not
represented, although some of that information could be added as
annotations. The four key components of the model are:

1. Decisions. These represent a position or small region where the player
is forced to make a decision about where to go next. See the section on
"Decisions are Fractal" below for more details about what qualifies as a
decision, but for one example, we can imagine each room might be a
decision, where the options are the doors of the room. Each decision is
assigned an ID number, and is also given a name (which does not have to
be unique).

2. Transitions. These are the links between decisions, and represent the
available options. For each move the player could make (e.g., for each
door going out of a room), we add a transition and connect it to another
decision representing where the player would be once they take that
transition. Each transition has a name, which must be unique among all
transitions outgoing from a particular decision (but which is usually NOT
unique across the entire graph). Something like "west" can be used to
indicate "the west door of this room." Each transition starts from a
specific decision and ends at a specific decision. Transitions are
allowed to start and end at the same decision, we call these "actions"
and they represent things like pulling a lever where the options you're
faced with don't directly change, but some kind of effect might be
applied which indirectly changes things.

3. Effects. Each transition has the immediate effect of changing the
player's current decision, and thus the options available to them.
Transitions may also apply one or more secondary effects, which interact
with the player state composed of **capabilities** and **tokens**, plus
the world state composed of **mechanism states**. A secondary effect can
be something like gaining a new key, gaining a certain number of coins,
or setting a mechanism in the world to a particular state. By creating
standardized data structures for player & world states, we enable deeper
comparisons between different games, although in some cases we then need
to abstract some of the details of those games. See the "Effects and
Requirements" section below for more details.

4. Requirements. Using the same abstract player & world state data that
effects manipulate, each transition may have a requirement to represent
situations like a locked door requiring a certain key, or a bridge where
a toll must be paid at each crossing (a toll would also involve an effect
to represent losing the money paid). When figuring out the options
available to the player, the system can automatically disregard
transitions at the current decision whose requirements are not met. A
requirement can be a series of specific capabilities, token counts,
and/or mechanism states which are combined using AND (`&`), OR (`|`),
and/or NOT (`!`) operators. For example, the requirement
`fly | (climb & stamina*3)` represents a situation where the player must
either have the "fly" capability, or they must have the "climb"
capability, along with *at least* three "stamina" tokens. As with
effects, sometimes expressing the exact requirements imposed by a
particular game engine is difficult, and some abstraction must be used,
but the format of requirements has been designed and tested to cover most
situations that arise in the videogame genres we've studied. See the
"Effects and Requirements" section below for more details.

Putting together Decisions, Transitions, Effects, and Requirements, we
create a "decision graph" (represented by the `core.DecisionGraph`
class). This details every decision, each transition at that decision,
and what the effects of those transitions are along with the requirements
necessary for taking them. These decision graphs are rich enough models
of game spaces to allow for lots of analysis, and because they're
abstract, they allow for comparison between different games (although
they remain fundamentally subjective).


## Decisions are Fractal

When creating decision graphs, the player needs to choose what level of
decision they wish to capture. Since the actions used to carry out most
decisions can be decomposed into a series of more-local decisions, we can
view decisions in games as having a fractal structure. For example, the
actions taken as a result of a decision to "visit the water temple"
probably involve many specific navigation moves, like "go left at the
crossroads" or "cut across the field towards the river," and each of
these is the result of a decision that's made in support of the
higher-level goal of reaching the water temple. Likewise, "go left at the
crossroads" requires deciding to move the character to the left by a
certain amount, and that lower-level decision could even be broken down
into individual decisions to press certain buttons required to make that
happen. In theory, a decision map could be constructed at the level of
button presses, but it would be excruciatingly hard to do so manually,
and analysis of such a map would probably be very difficult. Instead,
analyzing at the "go left at the crossroads" level is probably more
productive, since at that level, we can see that many similar game states
result in very similar sets of choices (e.g., you always have the option
to go left or right at the crossroads, and those two choices always lead
to similar subsequent decisions). One could of course analyze decisions
at the level of "go to the water temple" instead, and here there might
still be enough similarity in decisions for this to be useful (e.g., when
at the water temple, you always have the same few options of what to
visit next).

The `exploration` library does not require you to use any particular
level of decision, and through the use of `Zone`s it does allow grouping
base-level decisions into larger groups to capture multiple levels of
decision structure. Zones can also be stacked within other zones to
represent complex multi-layer groupings. Support for deriving a
higher-level decision graph from zones of a lower-level graph is a
planned feature.


## Effects and Requirements

To model game state in a manner that can be abstracted across multiple
games, we use the following kinds of state:

1. **Capabilities**: Each capability is identified by a unique string,
    and represents some specific capability that affects which
    transitions a player can take. Examples include movement abilities
    (e.g., "doubleJump") and re-usable key items (e.g., "yellowKeyCard").
    At each step of an exploration, a player either has or does not have
    each capability, which is represented by a set of capability strings
    that they player has. The 'gain' effect adds a capability to this
    set, while the 'lose' effect removes one (in both cases nothing
    happens if the capability is already present/absent). A requirement
    may stipulate that a player must have or must not have a certain
    capability in order to traverse a transition.
2. **Tokens**: using capabilities alone, it's difficult to represent
    situations where items can be accumulated (like holding multiple keys
    that get used up when unlocking doors). So we also maintain a mapping
    from token names to integers, and the 'gain' and 'lose' effects can
    specify a token name plus number to add or remove that many tokens of
    the specified type. Currently, minimum or maximum token limits are
    not supported, but we plan to add these in a future release. For
    tokens, a 'set' effect is also available that sets the token count to
    a specific amount regardless of the previous amount. A token
    requirement means "at-least-this-many" and negating it thus means
    "fewer-than-this-many". Using 'and', 'or', and/or 'not' more specific
    requirements can be created. By combining a token requirement with a
    'lose' effect on the same transition, we can create transitions that
    have costs.
3. **Mechanisms*: in many games there are things like levers that open
    nearby doors. These could be represented by creating unique
    capability names for each lever, but that becomes tedious and
    error-prone, since if you re-use the same name by accident, the
    library will assume that the capability for one location applies
    equally to the other. So we include **mechanisms**, which are tied to
    a particular decision point, and their name only needs to be unique
    at-that-decision. When referring to a mechanism by name alone, the
    system will assume that we mean a mechanism at the current decision
    point, or if no such mechanism exists, one with that name in the
    current zone, searching higher-level zones if necessary and finally
    the entire decision map. Each mechanism can have any number of
    specific states, each identified by a string. The associated effect
    is 'set' with a mechanism name + state string, which changes the
    mechanism's current state to the specified one (each mechanism starts
    out as not-in-any-state and once given a state, can only be in one
    state at once). Requirements can be that a mechanism is in a specific
    state, or that it's not in a specific state. There is also a 'toggle'
    effect which cycles the mechanism through a specific sequence of
    states on each activation. When a mechanism requirement exists on a
    transition, we start looking for the named mechanism at both ends of
    the transition first. A mechanism may also be identified by a
    decision ID plus mechanism name to avoid the search process. In the
    most common case where, for example, multiple levers open different
    doors, but each lever is adjacent to the door it opens and no two
    levers are at adjacent decisions, each lever could use the same
    mechanism name, and each door could simply require that that
    mechanism be in the 'open' state, and the search process would match
    up levers with doors correctly. Using names like "leftLever" and
    "rightLever" might be necessary when multiple levers are in the same
    or adjacent locations, but that's often natural in any case.

Whereas capabilities and tokens are stored as part of the player state,
mechanism states are stored as part of a separate global decision-graph
state This helps in situations where, for example, the map state gets
reset while the player state stays the same, or vice versa. Although we
won't get into it here, there's also support for maintaining multiple
separate player states for games where the player switches between
different avatars with different capabilities.

Besides the 'gain', 'lose', 'set', and 'toggle' effects mentioned above,
a transition can also have a 'deactivate' effect which disables that
transition once taken; this is useful for things like chests that can
only be opened once.


## Advanced Effects can Challenges

The base effects system triggers each effect whenever a transition is
taken, and this can cover probably 90% of cases. However, in some
situations, things are more complex than that. The effects of a
transition are actually represented as a `Conesquence`, which is a list
that can contain `Effect`s as well as `Condition`s or `Challenge`s, and
the latter two options can contain their own sub-`Consequence`s. This
forms a tree structure of consequence and sub-consequence lists, which
can represent quite complicated situations, including conditional and
random effects. The three types that can be present in a `Consequence`
list are:

1. `Effect`s are as described above, and are applied in-order. When a
    consequence list is applied, each effect in the list is applied to
    the current state.
2. `Condition`s specify a `Requirement`, and trigger their
    sub-`Consequence` list of additional effects if that requirement is
    met. This is different from `Requirement`s applied to transitions,
    which prevent the player from taking that transition. Even if a
    `Condition` requirement is not met, the associated transition can
    still be taken, but the sub-effects of that specific condition will
    not be applied. We can use this to represent situations like "if you
    don't have the master key you will use up a small key" (with "master
    key or one small key" as a requirement to take the transition).
3. `Challenge`s are used to represent random outcomes, and they have two
    sub-`Consequence` lists: one for 'success' and the other for
    'failure' (although these need not represent exactly those two
    things). Multi-outcome processes can be represented by nesting
    challenges inside each other. By default, each option has a 50/50
    chance of happening, although in practice, the player usually knows
    which outcome actually did happen during a particular traversal.
    There is a `Skill`s system to indicate how player skills and/or
    upgrades might affect probabilities of different outcomes (see the
    `Challenge` documentation), and in theory challenges allow for a
    model to be playable, although we have not yet implemented an
    interface for this. Although challenges only offer a rough
    approximation of potentially very complex game systems, they do allow
    for comparison between games when players are able to estimate the
    likelihood of different outcomes and the effects of skills on those
    likelihoods. In theory, we hope that this will enable things like
    checking whether players who lose to a 'difficult' boss are more
    likely to decide to explore other areas compared to players who lose
    to a boss they think they can beat in a few more tries.

Because `Challenge`s can be placed inside of `Condition`s and vice-versa,
relatively complex game logic can be attached to a particular transition.
There are a few more complex effects that can be used to control
traversal of decision graphs when used conditionally:

- 'bounce' is an effect which cancels the movement associated with a
    transition. Each transition has a destination and normally the
    player's next decision will be made using the options at that
    destination (we call this decision the 'primary decision').
    If a 'bounce' effect triggers when taking a transition, the player's
    primary decision will stay the same, even though other effects of
    that transition may also apply. This can model situations where the
    player can attempt to take a transition, but without the proper
    requirements they will be unable to actually complete the transition.
    It can also model challenges which must be passed in order to
    progress, where a 'bounce' effect is included in the challenge
    failure outcome.
- 'goto' is an effect which sets the player's primary decision to a
    particular decision. Normally unnecessary since the transition has a
    destination, but it could be used to model a movement challenge where
    the player falls down to another decision point if they fail, for
    example.
- 'follow' is an effect which names a transition, and forces the player
    to immediately take the named transition once they arrive at their
    initial destination. Again most useful with a `Condition` or
    `Challenge`, it can be used in situations where without meeting
    certain requirements, a player is shunted off to a different
    destination, or it could force the player to trigger an action at the
    destination of a transition. Effects of the secondary transition are
    applied as normal after all effects of the initial transition, so a
    chain of 'follow' effects might occur.

These more complex effects are rarely needed, but help model games more
faithfully for certain key design patterns, such as the "broken bridge"
scenario where the player's initial attempt to reach a goal unexpectedly
redirects them elsewhere.

Additionally, transitions can be tagged as 'trigger' transitions, and
whenever the player faces a decision, any 'trigger' transitions at that
decision will apply their effects before the player actually gets to make
a choice. This can approximate things like environmental hazards that
apply passive damage over time.


## Saving, Loading, and Endings

The effects described above can model or at least approximate most game
logic (although note that token values being integers restricts things a
bit). However, dying and restoring from a save point is a common
occurrence in games that isn't well modeled by anything described above.
For this specific mechanic, we have a 'save' effect which snapshots the
current game state, and a 'load' action can be taken by the player to
restore state to that snapshot. 'save' as an `Effect` can be applied to
any transition, whereas 'load' is not a transition effect but rather a
type of action the player can take regardless of which other options are
available to them based on the current decision.

There are options to control exactly which parts of the game state are
restored when loading a saved state, since in many games only some state
reverts upon death. Multiple save slots with different names can be used.

To represent endings, including death but also various ways of beating
the game, we use a special domain. Domains are parallel decision spaces,
where when making a decision the player can chose any transition from an
active decision in any of their current domains. However, the 'endings'
domain is special: When any ending decision point is active, the only
legitimate action is to load a previous state. So by activating a 'death'
decision point in the 'endings' domain, we can represent the fact that
the player has died, and their only option remaining is to load a saved
game.

Usually, we can annotate the possibility of death as a 'goto' effect of a
challenge failure, or when dying accidentally even when a challenge is
not significant enough to be annotated, a special 'warp' action can be
used to represent movement without taking a listed transition.


## More Details

More details of the API not mentioned here can be found in the
documentation for various API functions and core classes. The
`exploration.base` and `exploration.core` modules contain most of the
relevant definitions, particularly the methods of the
`exploration.core.DecisionGraph` and
`exploration.core.DiscreteExploration` classes, plus the `Requirement`,
`Effect`, `Challenge`, `Condition`, and `Consequence` definitions in the
`exploration.base` module.
"""

