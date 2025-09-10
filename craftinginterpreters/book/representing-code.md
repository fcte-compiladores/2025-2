> To dwellers in a wood, almost every species of tree has its voice as well as
> its feature. <cite>Thomas Hardy, <em>Under the Greenwood Tree</em></cite>

In the [last chapter][scanning], we took the raw source code as a string and
transformed it into a slightly higher-level representation: a series of tokens.
The parser we'll write in the [next chapter][parsing] takes those tokens and
transforms them yet again, into an even richer, more complex representation.

[scanning]: scanning.html
[parsing]: parsing-expressions.html

Before we can produce that representation, we need to define it. That's the
subject of this chapter. Along the way, we'll <span name="boring">cover</span>
some theory around formal grammars, feel the difference between functional and
object-oriented programming, go over a couple of design patterns, and do some
metaprogramming.

<aside name="boring">

I was so worried about this being one of the most boring chapters in the book
that I kept stuffing more fun ideas into it until I ran out of room.

</aside>

Before we do all that, let's focus on the main goal -- a representation for
code. It should be simple for the parser to produce and easy for the interpreter
to consume. If you haven't written a parser or interpreter yet, those
requirements aren't exactly illuminating. Maybe your intuition can help. What is
your brain doing when you play the part of a _human_ interpreter? How do you
mentally evaluate an arithmetic expression like this:

```lox
1 + 2 * 3 - 4
```

Because you understand the order of operations -- the old "[Please Excuse My
Dear Aunt Sally][sally]" stuff -- you know that the multiplication is evaluated
before the addition or subtraction. One way to visualize that precedence is
using a tree. Leaf nodes are numbers, and interior nodes are operators with
branches for each of their operands.

[sally]: https://en.wikipedia.org/wiki/Order_of_operations#Mnemonics

In order to evaluate an arithmetic node, you need to know the numeric values of
its subtrees, so you have to evaluate those first. That means working your way
from the leaves up to the root -- a _post-order_ traversal:

<span name="tree-steps"></span>

<img src="image/representing-code/tree-evaluate.png" alt="Evaluating the tree from the bottom up." />

<aside name="tree-steps">

A. Starting with the full tree, evaluate the bottom-most operation, `2 * 3`.

B. Now we can evaluate the `+`.

C. Next, the `-`.

D. The final answer.

</aside>

If I gave you an arithmetic expression, you could draw one of these trees pretty
easily. Given a tree, you can evaluate it without breaking a sweat. So it
intuitively seems like a workable representation of our code is a <span
name="only">tree</span> that matches the grammatical structure -- the operator
nesting -- of the language.

<aside name="only">

That's not to say a tree is the _only_ possible representation of our code. In
[Part III][], we'll generate bytecode, another representation that isn't as
human friendly but is closer to the machine.

[part iii]: a-bytecode-virtual-machine.html

</aside>

We need to get more precise about what that grammar is then. Like lexical
grammars in the last chapter, there is a long ton of theory around syntactic
grammars. We're going into that theory a little more than we did when scanning
because it turns out to be a useful tool throughout much of the interpreter. We
start by moving one level up the [Chomsky hierarchy][]...

[chomsky hierarchy]: https://en.wikipedia.org/wiki/Chomsky_hierarchy

## Context-Free Grammars

In the last chapter, the formalism we used for defining the lexical grammar --
the rules for how characters get grouped into tokens -- was called a _regular
language_. That was fine for our scanner, which emits a flat sequence of tokens.
But regular languages aren't powerful enough to handle expressions which can
nest arbitrarily deeply.

We need a bigger hammer, and that hammer is a **context-free grammar**
(**CFG**). It's the next heaviest tool in the toolbox of **[formal
grammars][]**. A formal grammar takes a set of atomic pieces it calls its
"alphabet". Then it defines a (usually infinite) set of "strings" that are "in"
the grammar. Each string is a sequence of "letters" in the alphabet.

[formal grammars]: https://en.wikipedia.org/wiki/Formal_grammar

I'm using all those quotes because the terms get a little confusing as you move
from lexical to syntactic grammars. In our scanner's grammar, the alphabet
consists of individual characters and the strings are the valid lexemes --
roughly "words". In the syntactic grammar we're talking about now, we're at a
different level of granularity. Now each "letter" in the alphabet is an entire
token and a "string" is a sequence of _tokens_ -- an entire expression.

Oof. Maybe a table will help:

<table>
<thead>
<tr>
  <td>Terminology</td>
  <td></td>
  <td>Lexical grammar</td>
  <td>Syntactic grammar</td>
</tr>
</thead>
<tbody>
<tr>
  <td>The &ldquo;alphabet&rdquo; is<span class="ellipse">&thinsp;.&thinsp;.&thinsp;.</span></td>
  <td>&rarr;&ensp;</td>
  <td>Characters</td>
  <td>Tokens</td>
</tr>
<tr>
  <td>A &ldquo;string&rdquo; is<span class="ellipse">&thinsp;.&thinsp;.&thinsp;.</span></td>
  <td>&rarr;&ensp;</td>
  <td>Lexeme or token</td>
  <td>Expression</td>
</tr>
<tr>
  <td>It&rsquo;s implemented by the<span class="ellipse">&thinsp;.&thinsp;.&thinsp;.</span></td>
  <td>&rarr;&ensp;</td>
  <td>Scanner</td>
  <td>Parser</td>
</tr>
</tbody>
</table>

A formal grammar's job is to specify which strings are valid and which aren't.
If we were defining a grammar for English sentences, "eggs are tasty for
breakfast" would be in the grammar, but "tasty breakfast for are eggs" would
probably not.

### Rules for grammars

How do we write down a grammar that contains an infinite number of valid
strings? We obviously can't list them all out. Instead, we create a finite set
of rules. You can think of them as a game that you can "play" in one of two
directions.

If you start with the rules, you can use them to _generate_ strings that are in
the grammar. Strings created this way are called **derivations** because each is
_derived_ from the rules of the grammar. In each step of the game, you pick a
rule and follow what it tells you to do. Most of the lingo around formal
grammars comes from playing them in this direction. Rules are called
**productions** because they _produce_ strings in the grammar.

Each production in a context-free grammar has a **head** -- its <span
name="name">name</span> -- and a **body**, which describes what it generates. In
its pure form, the body is simply a list of symbols. Symbols come in two
delectable flavors:

<aside name="name">

Restricting heads to a single symbol is a defining feature of context-free
grammars. More powerful formalisms like **[unrestricted grammars][]** allow a
sequence of symbols in the head as well as in the body.

[unrestricted grammars]: https://en.wikipedia.org/wiki/Unrestricted_grammar

</aside>

- A **terminal** is a letter from the grammar's alphabet. You can think of it
  like a literal value. In the syntactic grammar we're defining, the terminals
  are individual lexemes -- tokens coming from the scanner like `if` or `1234`.

  These are called "terminals", in the sense of an "end point" because they
  don't lead to any further "moves" in the game. You simply produce that one
  symbol.

- A **nonterminal** is a named reference to another rule in the grammar. It
  means "play that rule and insert whatever it produces here". In this way, the
  grammar composes.

There is one last refinement: you may have multiple rules with the same name.
When you reach a nonterminal with that name, you are allowed to pick any of the
rules for it, whichever floats your boat.

To make this concrete, we need a <span name="turtles">way</span> to write down
these production rules. People have been trying to crystallize grammar all the
way back to Pāṇini's _Ashtadhyayi_, which codified Sanskrit grammar a mere
couple thousand years ago. Not much progress happened until John Backus and
company needed a notation for specifying ALGOL 58 and came up with
[**Backus-Naur form**][bnf] (**BNF**). Since then, nearly everyone uses some
flavor of BNF, tweaked to their own tastes.

[bnf]: https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form

I tried to come up with something clean. Each rule is a name, followed by an
arrow (`→`), followed by a sequence of symbols, and finally ending with a
semicolon (`;`). Terminals are quoted strings, and nonterminals are lowercase
words.

<aside name="turtles">

Yes, we need to define a syntax to use for the rules that define our syntax.
Should we specify that _metasyntax_ too? What notation do we use for _it?_ It's
languages all the way down!

</aside>

Using that, here's a grammar for <span name="breakfast">breakfast</span> menus:

<aside name="breakfast">

Yes, I really am going to be using breakfast examples throughout this entire
book. Sorry.

</aside>

```ebnf
breakfast  → protein "with" breakfast "on the side" ;
breakfast  → protein ;
breakfast  → bread ;

protein    → crispiness "crispy" "bacon" ;
protein    → "sausage" ;
protein    → cooked "eggs" ;

crispiness → "really" ;
crispiness → "really" crispiness ;

cooked     → "scrambled" ;
cooked     → "poached" ;
cooked     → "fried" ;

bread      → "toast" ;
bread      → "biscuits" ;
bread      → "English muffin" ;
```

We can use this grammar to generate random breakfasts. Let's play a round and
see how it works. By age-old convention, the game starts with the first rule in
the grammar, here `breakfast`. There are three productions for that, and we
randomly pick the first one. Our resulting string looks like:

```text
protein "with" breakfast "on the side"
```

We need to expand that first nonterminal, `protein`, so we pick a production for
that. Let's pick:

```ebnf
protein → cooked "eggs" ;
```

Next, we need a production for `cooked`, and so we pick `"poached"`. That's a
terminal, so we add that. Now our string looks like:

```text
"poached" "eggs" "with" breakfast "on the side"
```

The next non-terminal is `breakfast` again. The first `breakfast` production we
chose recursively refers back to the `breakfast` rule. Recursion in the grammar
is a good sign that the language being defined is context-free instead of
regular. In particular, recursion where the recursive nonterminal has
productions on <span name="nest">both</span> sides implies that the language is
not regular.

<aside name="nest">

Imagine that we've recursively expanded the `breakfast` rule here several times,
like "bacon with bacon with bacon with..." In order to complete the string
correctly, we need to add an _equal_ number of "on the side" bits to the end.
Tracking the number of required trailing parts is beyond the capabilities of a
regular grammar. Regular grammars can express _repetition_, but they can't _keep
count_ of how many repetitions there are, which is necessary to ensure that the
string has the same number of `with` and `on the side` parts.

</aside>

We could keep picking the first production for `breakfast` over and over again
yielding all manner of breakfasts like "bacon with sausage with scrambled eggs
with bacon..." We won't though. This time we'll pick `bread`. There are three
rules for that, each of which contains only a terminal. We'll pick "English
muffin".

With that, every nonterminal in the string has been expanded until it finally
contains only terminals and we're left with:

<img src="image/representing-code/breakfast.png" alt='"Playing" the grammar to generate a string.' />

Throw in some ham and Hollandaise, and you've got eggs Benedict.

Any time we hit a rule that had multiple productions, we just picked one
arbitrarily. It is this flexibility that allows a short number of grammar rules
to encode a combinatorially larger set of strings. The fact that a rule can
refer to itself -- directly or indirectly -- kicks it up even more, letting us
pack an infinite number of strings into a finite grammar.

### Enhancing our notation

Stuffing an infinite set of strings in a handful of rules is pretty fantastic,
but let's take it further. Our notation works, but it's tedious. So, like any
good language designer, we'll sprinkle a little syntactic sugar on top -- some
extra convenience notation. In addition to terminals and nonterminals, we'll
allow a few other kinds of expressions in the body of a rule:

- Instead of repeating the rule name each time we want to add another production
  for it, we'll allow a series of productions separated by a pipe (`|`).

  ```ebnf
  bread → "toast" | "biscuits" | "English muffin" ;
  ```

- Further, we'll allow parentheses for grouping and then allow `|` within that
  to select one from a series of options within the middle of a production.

  ```ebnf
  protein → ( "scrambled" | "poached" | "fried" ) "eggs" ;
  ```

- Using recursion to support repeated sequences of symbols has a certain
  appealing <span name="purity">purity</span>, but it's kind of a chore to make
  a separate named sub-rule each time we want to loop. So, we also use a postfix
  `*` to allow the previous symbol or group to be repeated zero or more times.

  ```ebnf
  crispiness → "really" "really"* ;
  ```

<aside name="purity">

This is how the Scheme programming language works. It has no built-in looping
functionality at all. Instead, _all_ repetition is expressed in terms of
recursion.

</aside>

- A postfix `+` is similar, but requires the preceding production to appear at
  least once.

  ```ebnf
  crispiness → "really"+ ;
  ```

- A postfix `?` is for an optional production. The thing before it can appear
  zero or one time, but not more.

  ```ebnf
  breakfast → protein ( "with" breakfast "on the side" )? ;
  ```

With all of those syntactic niceties, our breakfast grammar condenses down to:

```ebnf
breakfast → protein ( "with" breakfast "on the side" )?
          | bread ;

protein   → "really"+ "crispy" "bacon"
          | "sausage"
          | ( "scrambled" | "poached" | "fried" ) "eggs" ;

bread     → "toast" | "biscuits" | "English muffin" ;
```

Not too bad, I hope. If you're used to grep or using [regular
expressions][regex] in your text editor, most of the punctuation should be
familiar. The main difference is that symbols here represent entire tokens, not
single characters.

[regex]: https://en.wikipedia.org/wiki/Regular_expression#Standards

We'll use this notation throughout the rest of the book to precisely describe
Lox's grammar. As you work on programming languages, you'll find that
context-free grammars (using this or [EBNF][] or some other notation) help you
crystallize your informal syntax design ideas. They are also a handy medium for
communicating with other language hackers about syntax.

[ebnf]: https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form

The rules and productions we define for Lox are also our guide to the tree data
structure we're going to implement to represent code in memory. Before we can do
that, we need an actual grammar for Lox, or at least enough of one for us to get
started.

### A Grammar for Lox expressions

In the previous chapter, we did Lox's entire lexical grammar in one fell swoop.
Every keyword and bit of punctuation is there. The syntactic grammar is larger,
and it would be a real bore to grind through the entire thing before we actually
get our interpreter up and running.

Instead, we'll crank through a subset of the language in the next couple of
chapters. Once we have that mini-language represented, parsed, and interpreted,
then later chapters will progressively add new features to it, including the new
syntax. For now, we are going to worry about only a handful of expressions:

- **Literals.** Numbers, strings, Booleans, and `nil`.

- **Unary expressions.** A prefix `!` to perform a logical not, and `-` to
  negate a number.

- **Binary expressions.** The infix arithmetic (`+`, `-`, `*`, `/`) and logic
  operators (`==`, `!=`, `<`, `<=`, `>`, `>=`) we know and love.

- **Parentheses.** A pair of `(` and `)` wrapped around an expression.

That gives us enough syntax for expressions like:

```lox
1 - (2 * 3) < 4 == false
```

Using our handy dandy new notation, here's a grammar for those:

```ebnf
expression     → literal
               | unary
               | binary
               | grouping ;

literal        → NUMBER | STRING | "true" | "false" | "nil" ;
grouping       → "(" expression ")" ;
unary          → ( "-" | "!" ) expression ;
binary         → expression operator expression ;
operator       → "==" | "!=" | "<" | "<=" | ">" | ">="
               | "+"  | "-"  | "*" | "/" ;
```

There's one bit of extra <span name="play">metasyntax</span> here. In addition
to quoted strings for terminals that match exact lexemes, we `CAPITALIZE`
terminals that are a single lexeme whose text representation may vary. `NUMBER`
is any number literal, and `STRING` is any string literal. Later, we'll do the
same for `IDENTIFIER`.

This grammar is actually ambiguous, which we'll see when we get to parsing it.
But it's good enough for now.

<aside name="play">

If you're so inclined, try using this grammar to generate a few expressions like
we did with the breakfast grammar before. Do the resulting expressions look
right to you? Can you make it generate anything wrong like `1 + / 3`?

</aside>

## Implementing Syntax Trees

Finally, we get to write some code. That little expression grammar is our
skeleton. Since the grammar is recursive -- note how `grouping`, `unary`, and
`binary` all refer back to `expression` -- our data structure will form a tree.
Since this structure represents the syntax of our language, it's called a <span
name="ast">**syntax tree**</span>.

<aside name="ast">

In particular, we're defining an **abstract syntax tree** (**AST**). In a
**parse tree**, every single grammar production becomes a node in the tree. An
AST elides productions that aren't needed by later phases.

</aside>

Our scanner used a single Token class to represent all kinds of lexemes. To
distinguish the different kinds -- think the number `123` versus the string
`"123"` -- we included a simple TokenType enum. Syntax trees are not so <span
name="token-data">homogeneous</span>. Unary expressions have a single operand,
binary expressions have two, and literals have none.

We _could_ mush that all together into a single Expression class with an
arbitrary list of children. Some compilers do. But I like getting the most out
of Java's type system. So we'll define a base class for expressions. Then, for
each kind of expression -- each production under `expression` -- we create a
subclass that has fields for the nonterminals specific to that rule. This way,
we get a compile error if we, say, try to access the second operand of a unary
expression.

<aside name="token-data">

Tokens aren't entirely homogeneous either. Tokens for literals store the value,
but other kinds of lexemes don't need that state. I have seen scanners that use
different classes for literals and other kinds of lexemes, but I figured I'd
keep things simpler.

</aside>

Something like this:

```python
# lox/expr.py
from dataclasses import dataclass
from typing import Any
from .tokens import Token

class Expr:
    """Abstract Base Class for expressions"""

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass
class Grouping(Expr):
    expression: Expr

@dataclass
class Literal(Expr):
    value: Any

@dataclass
class Unary(Expr):
    operator: Token
    right: Expr
```

<aside name="expr">

I avoid abbreviations in my code because they trip up a reader who doesn't know
what they stand for. But in compilers I've looked at, "Expr" and "Stmt" are so
ubiquitous that I may as well start getting you used to them now.

</aside>

Expr is the base class that all expression classes inherit from.

### Disoriented objects

You'll note that, much like the Token class, there aren't any methods here. It's
a dumb structure. Nicely typed, but merely a bag of data. This feels strange in
an object-oriented architecture. Shouldn't the class _do stuff_?

The problem is that these tree classes aren't owned by any single domain. Should
they have methods for parsing since that's where the trees are created? Or
interpreting since that's where they are consumed? Trees span the border between
those territories, which means they are really owned by _neither_.

In fact, these types exist to enable the parser and interpreter to
_communicate_. That lends itself to types that are simply data with no
associated behavior. This style is very natural in functional languages like
Lisp and ML where _all_ data is separate from behavior, but it feels odd in
Java.

Functional programming aficionados right now are jumping up to exclaim "See!
Object-oriented languages are a bad fit for an interpreter!" I won't go that
far. You'll recall that the scanner itself was admirably suited to
object-orientation. It had all of the mutable state to keep track of where it
was in the source code, a well-defined set of public methods, and a of private
helpers.

My feeling is that each phase or part of the interpreter works fine in an
object-oriented style. It is the data structures that flow between them that are
stripped of behavior.

## Working with Trees

Put on your imagination hat for a moment. Even though we aren't there yet,
consider what the interpreter will do with the syntax trees. Each kind of
expression in Lox behaves differently at runtime. That means the interpreter
needs to select a different chunk of code to handle each expression type. With
tokens, we simply matched on the TokenType.

Similarly, we can use the match statement to match and deconstruct each node of
the tree:

```python
match expr:
    case Binary(left, operator, right):
        ...
    case Grouping(expr):
        ...
    # ...
```

Unfortunally, Python treats each cases sequentially, as if it was a chain of
if/else statements. But all of those sequential tests are slow. Expression types
whose names are alphabetically later would take longer to execute because they'd
fall through more `case` tests before finding the right type. That's not my idea
of an elegant solution.

We have a family of classes and we need to associate a chunk of behavior with
each one. The natural solution in an object-oriented language would be to put
those behaviors into methods on the classes themselves. We could add an abstract
<span name="interpreter-pattern">`interpret()`</span> method on Expr which each
subclass would then implement to interpret itself.

<aside name="interpreter-pattern">

This exact thing is literally called the ["Interpreter pattern"][interp] in
_Design Patterns: Elements of Reusable Object-Oriented Software_, by Erich
Gamma, et al.

[interp]: https://en.wikipedia.org/wiki/Interpreter_pattern

</aside>

This works alright for tiny projects, but it scales poorly. Like I noted before,
these tree classes span a few domains. At the very least, both the parser and
interpreter will mess with them. As [you'll see later][resolution], we need to
do name resolution on them. If our language was statically typed, we'd have a
type checking pass.

[resolution]: resolving-and-binding.html

If we added instance methods to the expression classes for every one of those
operations, that would smush a bunch of different domains together. That
violates [separation of concerns][] and leads to hard-to-maintain code.

[separation of concerns]: https://en.wikipedia.org/wiki/Separation_of_concerns

### The expression problem

This problem is more fundamental than it may seem at first. We have a handful of
types, and a handful of high-level operations like "interpret". For each pair of
type and operation, we need a specific implementation. Picture a table:

<img src="image/representing-code/table.png" alt="A table where rows are labeled with expression classes, and columns are function names." />

Rows are types, and columns are operations. Each cell represents the unique
piece of code to implement that operation on that type.

An object-oriented language like Java assumes that all of the code in one row
naturally hangs together. It figures all the things you do with a type are
likely related to each other, and the language makes it easy to define them
together as methods inside the same class.

<img src="image/representing-code/rows.png" alt="The table split into rows for each class." />

This makes it easy to extend the table by adding new rows. Simply define a new
class. No existing code has to be touched. But imagine if you want to add a new
_operation_ -- a new column. In pure object oriented designs, that means
cracking open each of those existing classes and adding a method to it.

Functional paradigm languages in the <span name="ml">ML</span> family flip that
around. There, you don't have classes with methods. Types and functions are
totally distinct. To implement an operation for a number of different types, you
define a single function. In the body of that function, you use _pattern
matching_ -- sort of a type-based switch on steroids -- to implement the
operation for each type all in one place.

<aside name="ml">

ML, short for "metalanguage" was created by Robin Milner and friends and forms
one of the main branches in the great programming language family tree. Its
children include SML, Caml, OCaml, Haskell, and F#. Even Scala, Rust, and Swift
bear a strong resemblance.

Much like Lisp, it is one of those languages that is so full of good ideas that
language designers today are still rediscovering them over forty years later.

</aside>

This makes it trivial to add new operations -- simply define another function
that pattern matches on all of the types.

<img src="image/representing-code/columns.png" alt="The table split into columns for each function." />

But, conversely, adding a new type is hard. You have to go back and add a new
case to all of the pattern matches in all of the existing functions.

Each style has a certain "grain" to it. That's what the paradigm name literally
says -- an object-oriented language wants you to _orient_ your code along the
rows of types. A functional language instead encourages you to lump each
column's worth of code together into a _function_.

A bunch of smart language nerds noticed that neither style made it easy to add
_both_ rows and columns to the <span name="multi">table</span>. They called this
difficulty the "expression problem" because -- like we are now -- they first ran
into it when they were trying to figure out the best way to model expression
syntax tree nodes in a compiler.

<aside name="multi">

Languages with _multimethods_, like Common Lisp's CLOS, Dylan, and Julia do
support adding both new types and operations easily. What they typically
sacrifice is either static type checking, or separate compilation.

</aside>

People have thrown all sorts of language features, design patterns, and
programming tricks to try to knock that problem down but no perfect language has
finished it off yet. In the meantime, the best we can do is try to pick a
language whose orientation matches the natural architectural seams in the
program we're writing.

Object-orientation works fine for many parts of our interpreter, but these tree
classes rub against the grain of object-orientation. Fortunately, Python also
supports functional programming and we can choose the paradigm that best fits
each sittuation.

### Single dispatch

The naive approach to our problem would be to implement an `interpret`
standalone function using a match/case as hinted before:

```python
def interpret(expr: Expr) -> Any:
    match expr:
        case Binary(left, operator, right):
            return ...
        case Grouping(expr):
            return ...
        # ...
```

As I mentioned before, this approach suffers from a serious performance problem:
each case is tested sequentially. This means that as the number of cases grows,
the cost of interpretation grows proportionally.

The scanner loop has exactly the same problem, however we generally expect much
tighter loops during _interpretation_ than during _parsing_. A small piece file
with only a few lines of code may easily implement a loop that repeat millions
of times. On the other hand, it is not so common to bump into Lox files with
millions bytes.

The Python standard library has a neat solution to this problem using
`functools.singledispatch`. Single dispatch works similarly to the method
dispatch for classes. It associates an implementation function to each class and
its descendants and, but each implementation does not have to live in the class
body.

Before we apply it to our Expr classes, let's walk through a simpler example.
Say we have two kinds of pastries: <span name="beignet">beignets</span> and
crullers.

<aside name="beignet">

A beignet (pronounced "ben-yay", with equal emphasis on both syllables) is a
deep-fried pastry in the same family as doughnuts. When the French colonized
North America in the 1700s, they brought beignets with them. Today, in the US,
they are most strongly associated with the cuisine of New Orleans.

My preferred way to consume them is fresh out of the fryer at Café du Monde,
piled high in powdered sugar, and washed down with a cup of café au lait while I
watch tourists staggering around trying to shake off their hangover from the
previous night's revelry.

</aside>

```python

class Pastry:
    ...

class Beignet(Pastry):
    ...

class Cruller(Pastry):
    ...
```

We want to be able to define new pastry operations -- cooking them, eating them,
decorating them, etc. -- without having to add a new method to each class every
time. Here's how we do it. First, we define the fallback for the desired
operation. If there is no universal fallback, we simply raise a TypeError.

```python
from functools import singledispatch

@singledispatch
def cook(obj: Pastry):
    msg = f"cannot cook {obj.__class__.__name__} objects"
    raise TypeError(msg)
```

Then we provide a separate implementatation for each of the supported types:

```python
@cook.register:
def _(obj: Beignet):
    print("Cooking a Beignet")

@cook.register:
def _(obj: Cruller):
    print("Cooking a Cruller")
```

Each operation that can be performed on pastries is a new <span
name="multimethods">single-dispatch</span> function that register an
implementation for each Pastry subclass. To perform an operation on a pastry, we
simply call the function with the desired pastry object.

<aside name="multimethods">

Another common refinement is passing additional parameters to the dispatch
methods. Python's `singledispatch` accept additional parameters but it only
dispatch based on the first one. Some programming languages have the concept of
multimethods, which allow us to specify different implementations based on a
combination of argument types. Python has external libraries that implement
this, but fortunately it is not necessary in our case, as all operations
dispatch only on expression types.

</aside>

## A (Not Very) Pretty Printer

When we debug our parser and interpreter, it's often useful to look at a parsed
syntax tree and make sure it has the structure we expect. We could inspect it in
the debugger, but that can be a chore.

Instead, we'd like some code that, given a syntax tree, produces an unambiguous
string representation of it. Converting a tree to a string is sort of the
opposite of a parser, and is often called "pretty printing" when the goal is to
produce a string of text that is valid syntax in the source language.

That's not our goal here. We want the string to very explicitly show the nesting
structure of the tree. A printer that returned `1 + 2 * 3` isn't super helpful
if what we're trying to debug is whether operator precedence is handled
correctly. We want to know if the `+` or `*` is at the top of the tree.

To that end, the string representation we produce isn't going to be Lox syntax.
Instead, it will look a lot like, well, Lisp. Each expression is explicitly
parenthesized, and all of its subexpressions and tokens are contained in that.

Given a syntax tree like:

<img src="image/representing-code/expression.png" alt="An example syntax tree." />

It produces:

```text
(* (- 123) (group 45.67))
```

Not exactly "pretty", but it does show the nesting and grouping explicitly. To
implement this, we define a new single dispatch method.

```python
# lox/printer.py
from functools import singledispatch
from .expr import *

@singledispatch
def pretty(expr: Expr) -> str:
    name = expr.__class__.__name__
    raise TypeError(f"cannot display {name} objects")
```

We now need to provide the implementation for each expression type

```python
# lox/printer.py after the pretty() definition
@pretty.register
def _(expr: Binary):
    symbol = expr.operator.lexeme
    return parenthesize(symbol, expr.left, expr.right)

@pretty.register
def _(expr: Grouping):
  return parenthesize("group", expr.expression)

@pretty.register
def _(expr: Literal):
    if expr.value is None:
        return "nil"
    elif expr.value is True:
        return "true"
    elif expr.value is False:
        return "false"
    return str(expr.value)

@pretty.register
def _(expr: Unary):
    symbol = expr.operator.lexeme
    return parenthesize(symbol, expr.right)
```

Literal expressions are easy -- they convert the value to a string with a little
check to handle Python's `None` standing in for Lox's `nil`. The other
expressions have subexpressions, so they use this `parenthesize()` helper
method:

```python
# lox/printer.py
def parenthesize(name: str, *exprs: Expr) -> str:
    parts = [name, *map(pretty, exprs)]
    return "(" + " ".join(parts) + ")"
```

It takes a name and a list of subexpressions and wraps them all up in
parentheses, yielding a string like:

```text
(+ 1 2)
```

Note that it calls `pretty()` on each subexpression and passes in itself. This
is the <span name="tree">recursive</span> step that lets us print an entire
tree.

We don't have a parser yet, so it's hard to see this in action. For now, we'll
hack together a little `main()` method that manually instantiates a tree and
prints it.

```python
# lox/printer.py at the end of file
from .tokens import Token, TokenType as TT

def main():
    minus = Token(TT.MINUS, "-", 1)
    star = Token(TT.STAR, "*", 1)
    expr = Binary(
        Unary(minus, Literal(123)),
        star,
        Grouping(Literal(45.67))
    )
    print(pretty(expr))

if __name__ == "__main__":
    main()
```

If we did everything right, it prints:

```text
(* (- 123) (group 45.67))
```

You can go ahead and delete this method. We won't need it. Also, as we add new
syntax tree types, I won't bother showing the necessary methods for them in
pretty method. If you want to, go ahead and add them yourself. It will come in
handy in the next chapter when we start parsing Lox code into syntax trees. Or,
if you don't care to maintain `pretty()`, feel free to delete it. We won't need
it again.

<div class="challenges">

## Challenges

1.  Earlier, I said that the `|`, `*`, and `+` forms we added to our grammar
    metasyntax were just syntactic sugar. Take this grammar:

    ```ebnf
    expr → expr ( "(" ( expr ( "," expr )* )? ")" | "." IDENTIFIER )+
         | IDENTIFIER
         | NUMBER
    ```

    Produce a grammar that matches the same language but does not use any of
    that notational sugar.

    _Bonus:_ What kind of expression does this bit of grammar encode?

1.  The Visitor pattern lets you emulate the functional style in an
    object-oriented language. Devise a complementary pattern for a functional
    language. It should let you bundle all of the operations on one type
    together and let you define new types easily.

    (SML or Haskell would be ideal for this exercise, but Scheme or another Lisp
    works as well.)

1.  In [reverse Polish notation][rpn] (RPN), the operands to an arithmetic
    operator are both placed before the operator, so `1 + 2` becomes `1 2 +`.
    Evaluation proceeds from left to right. Numbers are pushed onto an implicit
    stack. An arithmetic operator pops the top two numbers, performs the
    operation, and pushes the result. Thus, this:

    ```lox
    (1 + 2) * (4 - 3)
    ```

    in RPN becomes:

    ```lox
    1 2 + 4 3 - *
    ```

    Define a visitor class for our syntax tree classes that takes an expression,
    converts it to RPN, and returns the resulting string.

[rpn]: https://en.wikipedia.org/wiki/Reverse_Polish_notation

</div>
