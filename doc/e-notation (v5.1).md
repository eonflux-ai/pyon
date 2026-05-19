# 🧠 Notation E

**Author**: Luiz Eduardo M. Rodrigues  
**A personal programming style for high readability, logical control, and dynamic scanning.**

**Version**: 5.0 consolidated  
**Basis**: v4 preserved and expanded with the agreed v5 rules.

---

## 📋 Table of Contents
1. <a href="#purpose">Purpose</a>
2. <a href="#principles-of-notation-e">Principles of Notation E</a>
   - 2.1 <a href="#21-single-point-of-return">Single point of return</a>
     - <a href="#validation-and-output-flow">Validation and output flow</a>
     - <a href="#trivial-one-line-functions">Trivial one-line functions</a>
   - 2.2 <a href="#22-numbered-comments-per-block">Numbered comments per block</a>
     - <a href="#canonical-numbering-rule">Canonical numbering rule</a>
     - <a href="#comment-voice">Comment voice</a>
     - <a href="#example">Example</a>
     - <a href="#indentation">Indentation</a>
     - <a href="#limits">Limits</a>
     - <a href="#experimental-branch-labels">Experimental branch labels</a>
     - <a href="#complexity-and-orchestrator-methods">Complexity and orchestrator methods</a>
   - 2.3 <a href="#23-two-line-logical-blocks">Two-line logical blocks</a>
     - <a href="#three-line-rule">Three-line rule</a>
     - <a href="#multiline-statements">Multiline statements</a>
     - <a href="#control-flow-clauses">Control-flow clauses</a>
     - <a href="#semantic-grouping-priority">Semantic grouping priority</a>
     - <a href="#preferred-loop-body-without-redundant-comments">Preferred loop body without redundant comments</a>
     - <a href="#preferred-orchestration-grouping">Preferred orchestration grouping</a>
     - <a href="#do-not-mix-unrelated-semantic-categories">Do not mix unrelated semantic categories</a>
     - <a href="#audit-rule-for-agents">Audit rule for agents</a>
   - 2.4 <a href="#24-visual-separators">Visual separators</a>
     - <a href="#horizontal-limit">Horizontal limit</a>
     - <a href="#class-method-separators">Class method separators</a>
   - 2.5 <a href="#25-docstring-style">Docstring style</a>
     - <a href="#docstring-example">Example</a>
   - 2.6 <a href="#26-no-continue-in-loops">No `continue` in loops</a>
   - 2.7 <a href="#27-english-only-comments-and-identifiers">English-only comments and identifiers</a>
   - 2.8 <a href="#28-modular-and-unambiguous-style">Modular and unambiguous style</a>
3. <a href="#practical-example">Practical Example</a>
4. <a href="#focused-examples">Focused Examples</a>
   - 4.1 <a href="#example-1-tryfinallyand-semantic-splitting">Example 1: `try/finally` and semantic splitting</a>
   - 4.2 <a href="#example-2-attributes-and-multiline-calls">Example 2: attributes and multiline calls</a>
   - 4.3 <a href="#example-3-compact-two-line-block">Example 3: compact two-line block</a>
   - 4.4 <a href="#example-4-simple-return-helper">Example 4: simple return helper</a>
   - 4.5 <a href="#example-5-cache-loading-with-semantic-grouping">Example 5: cache loading with semantic grouping</a>
   - 4.6 <a href="#example-6-loop-body-without-redundant-comments">Example 6: loop body without redundant comments</a>
5. <a href="#full-module-example">Full Module Example</a>
6. <a href="#agent-audit-checklist">Agent Audit Checklist</a>
   - 6.1 <a href="#numbering">Numbering</a>
   - 6.2 <a href="#comments">Comments</a>
   - 6.3 <a href="#block-size">Block size</a>
   - 6.4 <a href="#semantic-grouping">Semantic grouping</a>
   - 6.5 <a href="#control-flow">Control flow</a>
   - 6.6 <a href="#horizontal-limit-checklist">Horizontal limit</a>
7. <a href="#applicability">Applicability</a>
8. <a href="#universal-standards">Universal Standards</a>

---

<a id="purpose"></a>
## ✨ Purpose
Notation E is a set of code-writing guidelines designed to:
- Maximize visual clarity
- Minimize logical errors
- Enable rapid code scanning
- Keep execution flow linear and auditable
- Enhance communication with language models (LLMs)

Notation E is not only a formatting style. It is a semantic scanning style.

The code should be readable from top to bottom as a sequence of small, visible,
numbered intentions.

---

<a id="principles-of-notation-e"></a>
## ✏️ Principles of Notation E

### 2.1 Single point of return
Every function must have **a single `return` at the end**, regardless of internal conditional branches.

> Prevents fragmented flow and simplifies debugging, logging, and logical analysis.

<a id="validation-and-output-flow"></a>
#### Validation and output flow

Notation E distinguishes public validation from internal processing flow.

For public methods or public constructors:

- validate input parameters first;
- raise explicit exceptions when the input contract is invalid;
- only continue into the method body after the public contract is valid.

For internal or private methods:

- initialize output variables with safe default values near the beginning;
- use `if` blocks to decide whether processing should continue;
- progressively fill the output variables as conditions are satisfied;
- return once, at the end of the method.

#### Trivial one-line functions

Very small functions may omit numbered comments when all of these are true:

- the function has no docstring;
- the body is a single direct `return`, `raise`, or assertion-like statement;
- adding an output variable would make the function less clear;
- the function is self-explanatory from its name and signature.

Example:

```python
def __len__(self) -> int:
    return int(self.values.shape[0])
```

If a function has a docstring, it should normally use numbered E-Notation
comments in the body, because the function is no longer being treated as a
minimal one-line helper.

Example:

```python
def _calculate_result(values: np.ndarray) -> dict:
    """
    Calculates a result dictionary from internal values.

    Args:
        values (np.ndarray): Internal values.

    Returns:
        dict: Result dictionary.
    """

    # 1. Outputs...
    result = {}
    status = "skipped"

    # 2. Validation flags...
    flags = series_flags(values)
    if not flags:

        # 1.1 Process...
        result = run_processing(values)
        status = "computed"

    # 3. Return...
    return {
        "status": status,
        "result": result,
        "flags": flags,
    }
```

This keeps the method linear and auditable without using early returns or flow
jumps. Exceptions remain appropriate for invalid public input contracts.

---

### 2.2 Numbered comments per block
Each functional block is introduced by a **numbered comment** with two levels:

- Comments are numbered sequentially, e.g., `1, 2, 3, 4, 5, 6, 7, 8, 9`.
- Well-scoped functions stay within nine numbered blocks.
- The base structure is ```# {comment number}. {short description}...```

A numbered comment must contain meaningful text after the number.

Avoid:

```python
# 1. ...
# 1.1 ...
# 2.2 ...
```

Prefer short descriptions, ideally two to five words:

```python
# 1. Build index...
# 1.1 Normalize input...
# 2. Validate result...
```

The number shows structure; the text explains intent.

<a id="canonical-numbering-rule"></a>
#### Canonical numbering rule

A numbered comment has the following canonical structure:

```python
# {indentation level}.{item number} {short description}...
```

The first number represents the **indentation level**. The second number,
after the dot, represents the **sequential item number inside that indentation
level**.

At indentation level zero, the indentation prefix is omitted.

Therefore:

```python
# 1.   means indentation level 0, item 1. Equivalent to # 0.1.
# 2.   means indentation level 0, item 2. Equivalent to # 0.2.
# 1.1  means indentation level 1, item 1.
# 1.2  means indentation level 1, item 2.
# 2.1  means indentation level 2, item 1.
# 2.2  means indentation level 2, item 2.
```

This is a fundamental rule of Notation E.

Nested comments do **not** inherit the parent block number. A comment such as
`# 2.1` means indentation level 2, item 1. It does not mean item 1 inside the
parent block `# 2`.

<a id="comment-voice"></a>
#### Comment voice

Numbered comments describe what the code does. Prefer a neutral third-person
voice. This means the comment should read as if it refers to the code block as
the implicit subject. It does not mean the literal word `It` must be written in
the comment.

Prefer:

```python
# 1. Prepares output...
# 2. Loads cache...
# 3. Restores attributes...
# 4. Returns output...
```

Avoid vague, imperative, or overly compressed comments:

```python
# 1. Build path...
# 2. Save...
# 3. Do restore...
# 4. Return...
```

The comment should describe the semantic action, not explain implementation
details. Keep descriptions short, usually two to six words after the number.

<a id="example"></a>
#### Example:
```python
# 1. Fetches image...
if isinstance(img, str):
    ...

# 2. Initialize result...
outlier = False

# 3. Get black/white percentage...
if bw_range is not None:
    ...

# 4. Continues...
if not outlier and (entropy_range is not None):
    ...

# 5. Return decision...
return outlier
```

In the example above the code contains five numbered blocks, growing from 1 to 5.

<a id="indentation"></a>
#### Indentation

- When a block is indented, prefix the comment number with the indentation level.
- Structure: ```# {indentation level}.{comment number} ...```

##### Example:
```python
# 1. Fetches image...
if isinstance(img, str):
    img = Image.open(img)

# 2. Initialize result...
outlier = False

# 3. Get black/white percentage...
if bw_range is not None:
    black_pct, white_pct = image.calculate_black_white_ratio(img)

    # 1.1 Extract bounds...
    b_min, b_max = bw_range[0]
    w_min, w_max = bw_range[1]

    # 1.2 BW: If outside of the range, is an outlier...
    if (
        (black_pct < b_min)
        or (black_pct > b_max)
        or (white_pct < w_min)
        or (white_pct > w_max)
    ):
        
        # 2.1 Sets...
        outlier = True

# 4. Continues...
if not outlier and (entropy_range is not None):

    # 1.1 Entropy...
    entropy = image.calculate_entropy(img)
    e_min, e_max = entropy_range

    # 1.2 Check entropy if still valid...
    if (entropy < e_min) or (entropy > e_max):
        outlier = True

# 5. Return decision...
return outlier
```

In this example:
- Level-zero comments follow the structure ```# {comment number}. {short description}...```
- Indented comments follow ```# {indentation level}.{comment number} {short description}...```
- Up to indentation level 2 is shown.
- Example level 0: ```# 4. Continues...```
- Example level 1: ```# 1.1 Entropy...```
- Example level 2: ```# 2.1 Sets...```

#### Limits

- Neither indentation level nor block numbers should exceed 9.
- If you need more than nine comments per scope or more than nine indentation levels, it usually means:
    - The function has too many responsibilities.
    - The function is too long.
    - Helper functions are missing.
- Comments like ```# 10. ...``` or ```# 10.1 ...``` are a signal to refactor.
- Do not resolve an over-limit sequence by deleting comments, duplicating a
  previous number, or converting numbered comments into ordinary comments while
  leaving the same oversized block in place. The code should be reorganized so
  the visible semantic scope is smaller, usually by extracting a real helper,
  splitting test data into named groups, or turning a long branch chain into a
  dispatch structure. In other words, it may also require refactors.

After refactors, always re-check that the top-level sequence remains ordered
as `# 1`, `# 2`, `# 3`, and so on. Duplicated numbers, skipped numbers, or
reset sequences usually indicate refactor drift.

<a id="experimental-branch-labels"></a>
#### Experimental branch labels

Letter-based variants such as `# 1.A` and `# 1.B` are experimental and are not
part of official E-Notation yet.

They may become useful for cases where multiple nearby blocks share the same
semantic step, such as related `if` / `else` branches, sequential validations,
or repeated variants of the same logical operation. Until that rule is adopted
formally, official E-Notation audits should treat normal numeric sequencing as
the canonical style.

<a id="complexity-and-orchestrator-methods"></a>
#### Complexity and orchestrator methods

The numbering limits above are also an indirect complexity rule.

When a function accumulates too many branches, nested decisions, boolean
conditions, or numbered blocks, the problem is usually not the numbering itself.
The problem is that the function is doing more than one semantic job.

In this situation, the preferred E-Notation refactor is to keep the main method
as an **orchestrator method**:

- the orchestrator keeps the top-level domain story;
- each numbered block represents one semantic step;
- detailed decisions move into small helper methods with precise names;
- helpers are extracted only when they represent a real concept.

This aligns E-Notation with cyclomatic complexity review. A high-complexity
function has many independent execution paths. Extracting real logical units
reduces the number of paths inside the orchestrator and makes each helper
auditable on its own.

Example:

```python
def _regular_peak_count(lags: List[int], acf_values: List[float], sig: List[bool]) -> int:
    """
    Count significant peaks that appear at regular lag spacing.

    Args:
        lags (List[int]): Public lags.
        acf_values (List[float]): Public ACF values.
        sig (List[bool]): Significance mask.

    Returns:
        int: Regular significant peak count.
    """

    # 1. Peak lags...
    peak_lags = _local_peak_lags(lags=lags, acf_values=acf_values, sig=sig)
    output = 0

    # 2. Count regular spacings...
    if _has_regular_spacing(peak_lags=peak_lags):
        output = len(peak_lags)

    # 3. Return...
    return output
```

In this example, the main method does not know the details of local-peak
detection. It only expresses the semantic sequence:

1. find significant local peak lags;
2. check whether those peaks have regular spacing;
3. return the count.

The details belong to helpers:

```python
def _local_peak_lags(...):
    ...


def _is_local_peak(...):
    ...


def _has_regular_spacing(...):
    ...
```

This style should not be applied mechanically. A helper is justified when its
name removes real complexity or captures a reusable domain idea. Extracting a
single line into a vague helper only to reduce a metric makes the code harder
to scan and violates the purpose of E-Notation.

##### Annotated example:

This example is intentionally artificial. Its purpose is to demonstrate
numbering behavior, not good production code. It shows that numbering follows
indentation level and local item order, not the parent block number and not
vertical position alone.

```python
# --------------------------------------------------------------------------------------------- #


def generate_datapoints(
    items: List[T],
    context_size: int,
    feature_fn: Callable[[T], List[float]],
    target_fn: Callable[[T], List[float]],
    flatten: bool = False
) -> List[Datapoint]:
    """
    Generate Datapoints from a list of sequential items.

    Args:
        items (List[T]): Sequence of domain objects.
        context_size (int): Number of consecutive items used as context.
        feature_fn (Callable[[T], List[float]]): Function to extract features from each item.
        target_fn (Callable[[T], List[float]]): Function to extract targets from the item at t+1.
        flatten (bool): If True, flatten X into 1D list. Otherwise keep shape
            (context_size, num_features).

    Returns:
        List[Datapoint]: Collection of datapoints ready for conversion to tensors.
    """

    # 1. Indentation level 0, block 1.
    datapoints: List[Datapoint] = []

    # 2. Indentation level 0, block 2.
    for i in range(len(items) - context_size):

        # 1.1 Indentation level 1, block 1 (written as 1.1).
        # Common mistakes:
        #   - Assuming this should be 2.1 because the parent block was # 2.
        #   - Treating it as block 3 just because it follows block 2 vertically.
        window = [feature_fn(items[j]) for j in range(i, i + context_size)]

        # 1.2 Indentation level 1, block 2 (1.2).
        if flatten:
            x = [val for row in window for val in row]

        # 1.3 Indentation level 1, block 3 (1.3).
        else:
            
            # 2.1 Indentation level 2, block 1 (2.1).
            # Common mistakes:
            #   - Tagging this as 1.3.1 because it sits below 1.3.
            #   - Labeling it 1.4 just because it follows the previous comment.
            x = window

            # 2.2 Indentation level 2, block 2 (2.2).
            if x is None:
                
                # 3.1 Indentation level 3, block 1 (3.1).
                # Common mistake: calling this 2.2.1 simply because it nests under 2.2.
                raise ValueError("Invalid")

        # 1.4 Indentation level 1, block 4 (1.4).
        y = target_fn(items[i + context_size])

        # 1.5 Indentation level 1, block 5 (1.5).
        datapoints.append(Datapoint(x, y))

        # 1.6 Indentation level 1, block 6 (1.6).
        if not flatten:

            # 2.1 Indentation level 2, block 1 (2.1).
            # Common mistakes:
            #   - Treating this as 1.6.1 as if the parent number should propagate.
            #   - Calling it 1.7 because it appears after block 1.6.
            print('Not flatten')

            # 2.2 Indentation level 2, block 2 (2.2).
            print('This is the item 2.2')

            # 2.3 Indentation level 2, block 3 (2.3).
            if True:
                if True:

                    # 4.1 Indentation level 4, block 1 (4.1).
                    # Common mistakes:
                    #   - Labeling it 2.3.1 as if blocks inherited the previous number.
                    #   - Calling it 2.4 for appearing below block 2.3.
                    #   - Calling it 3.1 because level 3 is skipped in the comments above.
                    print('This is the item 4.1')

                    # 4.2 Indentation level 4, block 2 (4.2).
                    if True:
                        if True:
                            if True:
                                if True:

                                    # 8.1 Indentation level 8, block 1 (8.1).
                                    print('This is the item 8.1')

                                    # 8.2 Indentation level 8, block 2 (8.2).
                                    if True:

                                        # 9.1 Indentation level 9, block 1 (9.1).
                                        print('This is the item 9.1')

                                        # 9.2 Indentation level 9, block 2 (9.2).
                                        if True:

                                            # 10.1 Indentation level 10, block 1 (10.1).
                                            # This level is invalid.
                                            # Notation E only allows up to 9.
                                            # Anything above 9 means the block needs a refactor or sub-methods.
                                            print('This is bad, invalid in e-notation')

                                # 7.1 Indentation level 7, block 1 (7.1).
                                # There is already an if at level 7 without a comment because it followed the two-line rule.
                                # That can happen, so the first numbered comment at this level becomes 7.1.
                                print('This is the item 7.1')

                                # 7.2 Empty output...
                                print()

                                # 7.3 Empty output...
                                print()

                                # 7.4 Empty output...
                                print()

                                # 7.5 Empty output...
                                print()

                                # 7.6 Empty output...
                                print()

                                # 7.7 Empty output...
                                print()

                                # 7.8 Empty output...
                                print()

                                # 7.9 Indentation level 7, block 9 (7.9).
                                print()

                                # 7.10 Indentation level 7, block 10 (7.10).
                                # This is invalid.
                                # Notation E only allows up to 9.
                                # Anything above 9 means that section needs a refactor or sub-methods.
                                print('This is bad, invalid in e-notation')

    # 3. Indentation level 0, block 3.
    return datapoints

# --------------------------------------------------------------------------------------------- #

```

---

### 2.3 Two-line logical blocks
Each numbered block should represent a **small semantic unit**, preferably with two strongly related lines. The goal is not to force every physical group to have exactly two lines, but to avoid noisy one-line numbered blocks and avoid mixing unrelated operations under the same comment.

A good E-Notation block usually follows one of these shapes:

- one preparation line and one action line;
- two assignments that belong to the same concept;
- one object construction followed by its immediate use;
- one condition/loop line followed by a very small body when the parent comment already explains the action.

> Enables silent reading and rapid vertical scanning.

<a id="three-line-rule"></a>
#### Three-line rule

A numbered block must not contain three independent logical statements.

Avoid:

```python
# 1. It prepares cache...
pyon_path = _uopeople_pyon_path(unit=unit)
pyon_path.parent.mkdir(parents=True, exist_ok=True)
entries = _prepare_uopeople_for_save(uopeople=uopeople)
```

Prefer:

```python
# 1. It prepares path...
pyon_path = _uopeople_pyon_path(unit=unit)
pyon_path.parent.mkdir(parents=True, exist_ok=True)

# 2. It prepares cache...
entries = _prepare_uopeople_for_save(uopeople=uopeople)
```

A wrapped multiline call counts as one logical statement. This means a block may
have more than two physical lines when the extra lines are only formatting for a
single statement.

#### Multiline statements

A statement split across multiple physical lines still counts as **one logical
statement**.

This is allowed when it improves readability or keeps the code inside the
horizontal limit.

Valid:

```python
# 3. It replaces storage path...
if isinstance(uopeople.storage_state_path, Path):
    _remember_attr(
        entries=entries,
        obj=uopeople,
        attr="storage_state_path",
        value=str(uopeople.storage_state_path),
    )
```

The `_remember_attr(...)` call is one logical statement, even though it spans
multiple physical lines.

##### Multiline boundary rule

After a multiline statement, the next independent statement must start a new
numbered block.

Prefer:

```python
# 1. It replaces storage path...
_remember_attr(
    entries=entries,
    obj=uopeople,
    attr="storage_state_path",
    value=str(uopeople.storage_state_path),
)

# 2. It returns entries...
return entries
```

Avoid:

```python
# 1. It replaces storage path and returns...
_remember_attr(
    entries=entries,
    obj=uopeople,
    attr="storage_state_path",
    value=str(uopeople.storage_state_path),
)
return entries
```

The second form hides a new action after a visually long statement, reducing
dynamic scanning.

##### Multiline conditions

A multiline condition is also one logical statement.

Valid:

```python
# 1. It validates range...
if (
    (value < min_value)
    or (value > max_value)
):
    output = False
```

If the body becomes complex, use nested comments.

```python
# 1. It validates range...
if (
    (value < min_value)
    or (value > max_value)
):

    # 1.1 Updates output...
    output = False
    reason = "out_of_range"
```

#### Control-flow clauses

Control-flow clauses such as `try`, `except`, `else`, `finally`, `if`, `elif`,
and `else` must be treated as semantic boundaries when they represent different
responsibilities.

##### `try`, `except`, `else`, and `finally`

For `try` / `except` / `else` / `finally`:

- the `try` block receives its own numbered comment;
- each `except`, `else`, or `finally` clause receives a new numbered comment
  when it performs a different semantic action;
- cleanup, restore, rollback, logging, fallback, or error handling must not be
  hidden under the same comment as the main action.

Prefer:

```python
# 3. It saves object...
try:
    pyon.to_file(uopeople, str(pyon_path), enc_protected=True)

# 4. It restores attributes...
finally:
    _restore_attrs(entries=entries)
```

Avoid:

```python
# 3. It saves object...
try:
    pyon.to_file(uopeople, str(pyon_path), enc_protected=True)
finally:
    _restore_attrs(entries=entries)
```

The `finally` clause is a separate semantic responsibility. It must be visible
during vertical scanning.

Example with `except`:

```python
# 2. It reads file...
try:
    content = path.read_text(encoding="utf-8")

# 3. It handles missing file...
except FileNotFoundError:
    content = ""

# 4. It returns content...
return content
```

##### `if`, `elif`, and `else`

For `if` / `elif` / `else`:

- a condition and a very small direct body may stay in the same numbered block;
- a branch with multiple actions should introduce nested numbered comments;
- an `else` clause should receive its own numbered comment when it represents a
  different semantic case;
- comments inside a branch restart according to indentation level, not
  according to the parent block number.

Acceptable:

```python
# 1. It creates fallback...
if output is None:
    output = UoPeople()
```

Preferred when the branch contains multiple actions:

```python
# 2. It loads cache...
pyon_path = _uopeople_pyon_path(unit=unit)
if pyon_path.is_file():

    # 1.1 Reads object...
    loaded = pyon.from_file(str(pyon_path))
    if isinstance(loaded, UoPeople):

        # 2.1 Restores runtime...
        output = cast(UoPeople, loaded)
        output.restore_runtime_clients()
```

Example with `else`:

```python
# 2. It validates mode...
if mode in valid_modes:
    output = mode

# 3. It handles invalid mode...
else:
    output = default_mode
```

Avoid hiding different semantic cases under the same comment when the branches
have different responsibilities.

<a id="semantic-grouping-priority"></a>
#### Semantic grouping priority

When deciding whether to create, remove, or merge numbered comments, prioritize semantic proximity:

1. keep configuration assignments with configuration assignments;
2. keep object construction with its immediate use when they form one operational step;
3. keep method calls with method calls when they are part of the same action sequence;
4. avoid mixing an attribute/configuration assignment with an operational method call unless they are inseparable;
5. avoid creating a numbered comment for a single trivial statement inside a loop or condition when the parent block already describes the intent;
6. group a variable with the condition or action that immediately consumes it;
7. keep output initialization separate from later operational preparation;
8. never group lines merely to satisfy the two-line preference.

The two-line rule is therefore a **grouping rule**, not a mechanical line-count rule. A one-line body can be correct when adding a numbered comment would only repeat the obvious. A three-line block can be acceptable only when the three lines form one indivisible semantic step. However, if a block contains three independent statements, or if it grows beyond two or three tightly related lines, review whether it should be split or extracted.

#### Preferred loop body without redundant comments

Prefer:

```python
# 1. Print title...
print(f"{title}:")

# 2. Print paths...
for path in paths:
    print(f"- {path}")
```

Avoid:

```python
# 1. Print title...
print(f"{title}:")

# 2. Print paths...
for path in paths:

    # 1.1 Print path...
    print(f"- {path}")
```

The inner comment is redundant because the parent block already says that the loop prints paths. The loop body is a trivial direct action, so the extra numbered block harms scanning instead of helping it.

#### Preferred orchestration grouping

Prefer:

```python
# 1. Configure mode...
mock = True

# 2. Build client and run checks...
uopeople = build_uopeople(mock=mock)
run_all_uopeople_checks(uopeople=uopeople)
```

Avoid splitting the same operational step into noisy one-line blocks:

```python
# 1. Configure mode...
mock = True

# 2. Build client...
uopeople = build_uopeople(mock=mock)

# 3. Run checks...
run_all_uopeople_checks(uopeople=uopeople)
```

The second version is not invalid, but it is less aligned with E-Notation when the construction and the call are part of one immediate orchestration step.

<a id="do-not-mix-unrelated-semantic-categories"></a>
#### Do not mix unrelated semantic categories

Avoid:

```python
# 1. Configure mode...
mock = True
uopeople = build_uopeople(mock=mock)

# 2. Run checks...
run_all_uopeople_checks(uopeople=uopeople)
```

Prefer:

```python
# 1. Configure mode...
mock = True

# 2. Build client...
uopeople = build_uopeople(mock=mock)
run_all_uopeople_checks(uopeople=uopeople)
```

The preferred version keeps the configuration value isolated and groups the operational method call with the client it immediately consumes. In E-Notation, attributes/configuration stay with attributes/configuration, and methods/actions stay with methods/actions whenever possible.

<a id="audit-rule-for-agents"></a>
#### Audit rule for agents

When an agent rewrites code into E-Notation, it must check every numbered block with these questions:

1. Does this comment introduce a real semantic unit, or only repeat a trivial one-line statement?
2. Can this one-line numbered block be merged with a semantically adjacent line?
3. Would merging it mix different categories, such as configuration and execution?
4. Does removing an inner comment make the parent block clearer?
5. Is the resulting block easier to scan vertically than the original?

If the answer favors readability, the agent should merge or remove the numbered block. If merging would combine unrelated ideas, the agent should keep the separation.

---

<a id="24-visual-separators"></a>
### 2.4 Visual separators
Horizontal lines delimit functions, sections, and significant structures:
```python
# --------------------------------------------------------------------------------------------- #
```
> Helps visual navigation in long files.

<a id="horizontal-limit"></a>
#### Horizontal limit

The visual separator defines the preferred horizontal limit for code.

Module-level separator:

```python
# --------------------------------------------------------------------------------------------- #
```

Class-level separator:

```python
    # ----------------------------------------------------------------------------------------- #
```

Code should normally stay inside this visual width. If a statement would exceed
the separator width, split it into multiple lines using normal Python
formatting.

A wrapped statement still counts as one logical statement for Notation E block
size.

<a id="class-method-separators"></a>
#### Class method separators
Inside classes, separate methods with an indented separator:

```python
    # ----------------------------------------------------------------------------------------- #
```

Use this separator:

- after the class docstring, before the first method;
- between every method, property, static method, or class method;
- after the last method, before the module-level separator.

Do not use numbered comments at class scope to label methods. Comments such as
`# 1. Initialize...`, `# 2. Validate...`, or `# 3. Return...` belong inside a
method body, not between methods.

When a class-scope numbered comment is removed, re-check the method body. The
first numbered comment inside the method must start at `# 1`, not `# 1.1`.
Nested numbers such as `# 1.1` are valid only inside a nested block within the
method.

Example:

```python
class Example:
    """
    Example class.
    """

    # ----------------------------------------------------------------------------------------- #

    def method(self) -> str:
        """
        Return a value.
        """

        # 1. Build output...
        output = "value"

        # 2. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

# --------------------------------------------------------------------------------------------- #
```

---

<a id="25-docstring-style"></a>
### 2.5 Docstring style
- Written in **English**.
- Follows the structure: brief description + `Args` + `Returns`.
- Always compact and to the point.

<a id="docstring-example"></a>
#### Example:
```python
"""
Calculates the entropy of a grayscale image.

Args:
    img (Image.Image): The image to process.

Returns:
    float: Entropy value.
"""
```

---

<a id="26-no-continue-in-loops"></a>
### 2.6 No `continue` in loops
The use of `continue` is avoided. Flow control is handled using `if` statements to keep logic self-contained and predictable.

---

<a id="27-english-only-comments-and-identifiers"></a>
### 2.7 English-only comments and identifiers
All variable names, function names, docstrings, and comments are written in English to facilitate global collaboration and LLM compatibility.

---

<a id="28-modular-and-unambiguous-style"></a>
### 2.8 Modular and unambiguous style
- Highly reusable and modular code.
- Auxiliary functions have precise and descriptive names.

---

<a id="practical-example"></a>
## 🧩 Practical Example
```python
# --------------------------------------------------------------------------------------------- #

def analyze_entropy_range(folder: str, prefix: str = "Scanning") -> Tuple[float, float]:
    """
    Scans all grayscale images in a folder and returns the min/max entropy values.

    Args:
        folder (str): Path to the folder containing grayscale images.
        prefix (str): Optional prefix for the progress indicator.

    Returns:
        Tuple[float, float]: `(min_entropy, max_entropy)`.
    """

    # 1. List image files...
    files = [f for f in os.listdir(folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    # 2. Initialize...
    min_entropy, max_entropy = float("inf"), float("-inf")
    pb = PB(total=len(files), prefix=prefix)

    # 3. Iterate through images...
    for fname in files:

        # 1.1 Path...
        img_path = os.path.join(folder, fname)
        try:

            # 2.1 Open and validate...
            img = Image.open(img_path)
            if img.mode == "L":

                # 2.1 Calculate entropy...
                entropy = calculate_entropy(img)

                # 2.2 Update range...
                min_entropy = min(min_entropy, entropy)
                max_entropy = max(max_entropy, entropy)

            # 2.2 Not grayscale...
            else:
                pb.update()

        # 1.2 Error handling...
        except (OSError, ValueError, IOError):
            pass

        # 1.3 Update progress...
        pb.update()

    # 4. Return range...
    return min_entropy, max_entropy

# --------------------------------------------------------------------------------------------- #
```

---


<a id="focused-examples"></a>
## 🧩 Focused Examples

<a id="example-1-tryfinallyand-semantic-splitting"></a>
### Example 1: `try/finally` and semantic splitting

Preferred:

```python
# --------------------------------------------------------------------------------------------- #


def _save_uopeople(uopeople: UoPeople, unit: int) -> Path:
    """
    Save a UoPeople object cache without persisting the live session manager.

    Args:
        uopeople (UoPeople): UoPeople object.
        unit (int): Unit number.

    Returns:
        Path: UoPeople cache file path.
    """

    # 1. It prepares path...
    pyon_path = _uopeople_pyon_path(unit=unit)
    pyon_path.parent.mkdir(parents=True, exist_ok=True)

    # 2. It prepares cache...
    entries = _prepare_uopeople_for_save(uopeople=uopeople)

    # 3. It saves object...
    try:
        pyon.to_file(uopeople, str(pyon_path), enc_protected=True)

    # 4. It restores attributes...
    finally:
        _restore_attrs(entries=entries)

    # 5. It returns path...
    return pyon_path


# --------------------------------------------------------------------------------------------- #
```

Avoid:

```python
# 1. It prepares cache...
pyon_path = _uopeople_pyon_path(unit=unit)
pyon_path.parent.mkdir(parents=True, exist_ok=True)
entries = _prepare_uopeople_for_save(uopeople=uopeople)

# 2. It saves object...
try:
    pyon.to_file(uopeople, str(pyon_path), enc_protected=True)
finally:
    _restore_attrs(entries=entries)
```

Problems:

- three independent statements are hidden under one comment;
- `finally` is not visible as a separate semantic action;
- cache path preparation and cache object preparation are mixed.

---

<a id="example-2-attributes-and-multiline-calls"></a>
### Example 2: attributes and multiline calls

Preferred:

```python
# --------------------------------------------------------------------------------------------- #


def _prepare_uopeople_for_save(uopeople: UoPeople) -> list[_RestoreEntry]:
    """
    Prepare a UoPeople object for Pyon cache saving.

    Args:
        uopeople (UoPeople): UoPeople object.

    Returns:
        list[_RestoreEntry]: Entries needed to restore the object graph.
    """

    # 1. It prepares entries...
    entries: list[_RestoreEntry] = []

    # 2. It replaces manager...
    _remember_attr(entries=entries, obj=uopeople, attr="manager", value=None)

    # 3. It replaces storage path...
    if isinstance(uopeople.storage_state_path, Path):
        _remember_attr(
            entries=entries,
            obj=uopeople,
            attr="storage_state_path",
            value=str(uopeople.storage_state_path),
        )

    # 4. It returns entries...
    return entries


# --------------------------------------------------------------------------------------------- #
```

Avoid:

```python
# 1. It prepares entries...
entries: list[_RestoreEntry] = []
_remember_attr(entries=entries, obj=uopeople, attr="manager", value=None)
if isinstance(uopeople.storage_state_path, Path):
    _remember_attr(
        entries=entries,
        obj=uopeople,
        attr="storage_state_path",
        value=str(uopeople.storage_state_path),
    )
```

Problems:

- output initialization is mixed with mutation;
- one direct attribute replacement is hidden;
- conditional replacement is not visible as its own semantic step.

---

<a id="example-3-compact-two-line-block"></a>
### Example 3: compact two-line block

Preferred:

```python
# --------------------------------------------------------------------------------------------- #


def _remember_attr(entries: list[_RestoreEntry], obj: Any, attr: str, value: Any) -> None:
    """
    Temporarily replace an object attribute and remember its original value.

    Args:
        entries (list[_RestoreEntry]): Restore entries.
        obj (Any): Object to update.
        attr (str): Attribute name.
        value (Any): Temporary attribute value.
    """

    # 1. It remembers and replaces value...
    entries.append((obj, attr, getattr(obj, attr, None)))
    object.__setattr__(obj, attr, value)


# --------------------------------------------------------------------------------------------- #
```

Also acceptable, but less compact when the two operations are tightly coupled:

```python
# 1. It remembers value...
entries.append((obj, attr, getattr(obj, attr, None)))

# 2. It replaces value...
object.__setattr__(obj, attr, value)
```

The compact version is preferred because both lines form a single semantic
operation.

---

<a id="example-4-simple-return-helper"></a>
### Example 4: simple return helper

Preferred:

```python
# --------------------------------------------------------------------------------------------- #


def _uopeople_pyon_path(unit: int) -> Path:
    """
    Return the persisted UoPeople cache path for a unit.

    Args:
        unit (int): Unit number.

    Returns:
        Path: Unit cache file path.
    """

    # 1. It builds and returns path...
    return PYON_OUTPUT_ROOT / f"uopeople_u{unit}.pyon"


# --------------------------------------------------------------------------------------------- #
```

Also acceptable when the intermediate variable improves debugging or readability:

```python
# 1. It builds and returns path...
output = PYON_OUTPUT_ROOT / f"uopeople_u{unit}.pyon"
return output
```

Avoid unnecessary noisy separation:

```python
# 1. It builds path...
output = PYON_OUTPUT_ROOT / f"uopeople_u{unit}.pyon"

# 2. It returns path...
return output
```

The last version is not invalid, but it is less aligned when both statements are
a single obvious operation.

---

<a id="example-5-cache-loading-with-semantic-grouping"></a>
### Example 5: cache loading with semantic grouping

Preferred:

```python
# --------------------------------------------------------------------------------------------- #


def _get_uopeople(unit: int) -> UoPeople:
    """
    Load a cached UoPeople object or create a new one.

    Args:
        unit (int): Unit number.

    Returns:
        UoPeople: Cached or new UoPeople object.
    """

    # 1. It prepares output...
    output: UoPeople | None = None

    # 2. It loads cache...
    pyon_path = _uopeople_pyon_path(unit=unit)
    if pyon_path.is_file():

        # 1.1 Reads object...
        loaded = pyon.from_file(str(pyon_path))
        if isinstance(loaded, UoPeople):

            # 2.1 Restores runtime...
            output = cast(UoPeople, loaded)
            output.restore_runtime_clients()

    # 3. It creates fallback...
    if output is None:
        output = UoPeople()

    # 4. It returns object...
    return output


# --------------------------------------------------------------------------------------------- #
```

Avoid:

```python
# 1. It prepares output...
output: UoPeople | None = None
pyon_path = _uopeople_pyon_path(unit=unit)
```

The path belongs to cache loading, not output initialization.

---

<a id="example-6-loop-body-without-redundant-comments"></a>
### Example 6: loop body without redundant comments

Preferred:

```python
# --------------------------------------------------------------------------------------------- #


def _print_paths(title: str, paths: list[Path]) -> None:
    """
    Print generated paths.

    Args:
        title (str): Report title.
        paths (list[Path]): Generated paths.
    """

    # 1. It prints title...
    print(f"{title}:")

    # 2. It prints paths...
    for path in paths:
        print(f"- {path}")


# --------------------------------------------------------------------------------------------- #
```

Avoid:

```python
# 2. It prints paths...
for path in paths:

    # 1.1 Prints path...
    print(f"- {path}")
```

The inner comment repeats the parent block and harms scanning.

---

<a id="full-module-example"></a>
## 🧩 Full Module Example

```python
# --------------------------------------------------------------------------------------------- #
"""
Pipeline for dataset generation.
"""
# --------------------------------------------------------------------------------------------- #

from typing import List, Literal

# --------------------------------------------------------------------------------------------- #

from PIL import Image
from PIL import ImageFile

# --------------------------------------------------------------------------------------------- #

import pyon

# --------------------------------------------------------------------------------------------- #

from utils.status import ProgressBar as PB
from utils import vl_utils as vl
from utils import fl_utils as fl

# --------------------------------------------------------------------------------------------- #

from pkr.putils import PUtils

# --------------------------------------------------------------------------------------------- #

from pkr.ocr import api
from pkr.ocr import image
from pkr.ocr.ds_conf import DSConf

# --------------------------------------------------------------------------------------------- #

ImageFile.LOAD_TRUNCATED_IMAGES = True

# --------------------------------------------------------------------------------------------- #

STATUS_FILE = 'status.pyon'
STATUS_NUM = 'num'
STATUS_LABEL_SIZE = 'label_size'
STATUS_PRE_IMG_COUNT = 'pre_img_count'
STATUS_TMP_PRE = 'output_tmp_pre'
STATUS_TMP_HASH = 'output_tmp_hash'
STATUS_TMP_CLASS = 'output_tmp_class'
STATUS_CLASSES = 'output_classes'

# --------------------------------------------------------------------------------------------- #

LINE = f"\n{'#' * 40}\n"

# --------------------------------------------------------------------------------------------- #

def pipeline(
    input_folder: str,
    output_folder: str,
    confs: DSConf,
    delete_temp: bool = True
):
    """
    Pipeline for image dataset generation.

    Args:
        input_folder (str): Path to folder containing raw images.
        output_folder (str): Path to save classified images.
        confs (DSConf): Configurations.
        delete_temp (bool): If should delete temp folders.
    """

    # 1. Pipeline Start...
    print( f"\n\n{LINE}✅ Pipeline Start!{LINE}\n\n")

    # 2. Images...
    files = image.list_images(input_folder)
    if vl.is_valid(files) and fl.create_folder(output_folder):

        # 1.1 Corrupted Files...
        status = _get_status(output_folder)
        if (status[STATUS_NUM] == 0):

            # 2.1 Removes corrupted images...
            corrupted = image.move_corrupted_images(
                input_folder=input_folder, output_folder=output_folder, show_progress=True
            )

            # 2.2 Corrupted log....
            status = _update_status(output_folder, status)
            print(
                f"Moved {corrupted[0]} corrupted images to {corrupted[1]}"
                f"\n\n{LINE}✅ Corrupted Files Check Done!{LINE}\n\n"
            )

        # 1.2 Preprocess...
        if (status[STATUS_NUM] == 1):
            pre_img_count = 0

            # 2.1 Progress Bar...
            pb = PB(len(files), "Preprocessing")

            # 2.2 Iterates images...
            output_tmp_pre = fl.get_path(output_folder, 'tmp_pre')
            for fname in files:

                # 3.1 Preprocess...
                imgs = _preprocess(input_folder=input_folder, file_name=fname, confs=confs)
                _save_to(imgs=imgs, output_folder=output_tmp_pre, start_index=pre_img_count + 1)

                # 3.2 Updates count...
                pre_img_count += len(imgs)

                # 3.3 Update progress...
                pb.update()

            # 2.3 Preprocess log...
            label_size = len(str(pre_img_count))

            # 2.4 Set Status...
            status[STATUS_LABEL_SIZE] = label_size
            status[STATUS_PRE_IMG_COUNT] = pre_img_count
            status[STATUS_TMP_PRE] = output_tmp_pre

            # 2.5 Update Status...
            status = _update_status(output_folder, status)
            print(
                f"{pre_img_count} images saved to: {output_tmp_pre}"
                f"\n\n{LINE}✅ Preprocess Done!{LINE}\n\n"
            )

        # 1.3 Hash Filter...
        if (status[STATUS_NUM] == 2) and (STATUS_TMP_PRE in status):

            # 2.1 Filters...
            output_tmp_hash = fl.get_path(output_folder, 'tmp_hash')
            _filter_hash(input_folder=status[STATUS_TMP_PRE], output_folder=output_tmp_hash)

            # 2.2 Update Status....
            status[STATUS_TMP_HASH] = output_tmp_hash
            status = _update_status(output_folder, status)
            print( f"\n\n{LINE}✅ Hash Filter Done!{LINE}\n\n")

        # 1.4 Classification...
        if (
            (status[STATUS_NUM] == 3)
            and (STATUS_LABEL_SIZE in status)
            and (STATUS_TMP_HASH in status)
        ):

            # 2.1 Classifies...
            output_tmp_class = fl.get_path(output_folder, 'tmp_class')
            _classify(
                input_folder=status[STATUS_TMP_HASH],
                output_folder=output_tmp_class,
                size=status[STATUS_LABEL_SIZE],
                confs=confs
            )

            # 2.2 Update Status....
            status[STATUS_TMP_CLASS] = output_tmp_class
            status = _update_status(output_folder, status)
            print( f"\n\n{LINE}✅ Classification Done!{LINE}\n\n")

        # 1.7 Class separation...
        if (status[STATUS_NUM] == 4) and (STATUS_TMP_CLASS in status):

            # 2.1 Separation...
            output_classes = fl.get_path(output_folder, 'classes')
            _class_separation(
                input_folder=status[STATUS_TMP_CLASS],
                output_folder=output_classes,
                confs=confs,
            )

            # 2.2 Update Status....
            status[STATUS_CLASSES] = output_classes
            status = _update_status(output_folder, status)
            print( f"\n\n{LINE}✅ Class Separation Done!{LINE}\n\n")

        # 1.8 Class balancing...
        if (
            (status[STATUS_NUM] == 5)
            and (STATUS_LABEL_SIZE in status)
            and (STATUS_CLASSES in status)
        ):

            # 2.1 Balances...
            _class_balancing(
                input_folder=status[STATUS_CLASSES], size=status[STATUS_LABEL_SIZE], confs=confs
            )

            # 2.2 Updates..
            status = _update_status(output_folder, status)
            print( f"\n\n{LINE}✅ Class Balancing Done!{LINE}\n\n")

        # 1.9 Cleans temp folders...
        if (status[STATUS_NUM] == 6):

            # 2.1 Deletes...
            if delete_temp:
                folders = set()

                # 3.1 Add temp folder...
                if STATUS_TMP_PRE in status:
                    folders.add(status[STATUS_TMP_PRE])

                # 3.2 Add hash folder...
                if STATUS_TMP_HASH in status:
                    folders.add(status[STATUS_TMP_HASH])

                # 3.3 Add class folder...
                if STATUS_TMP_CLASS in status:
                    folders.add(status[STATUS_TMP_CLASS])

                # 3.4 Delete temp folders...
                fl.delete_folders(folders)

            # 2.2 Updates...
            status = _update_status(output_folder, status)
            print( f"\n\n{LINE}✅ Cleans Temp Folders Done!{LINE}\n\n")

    # 3. Pipeline End...
    print( f"\n\n{LINE}✅ Pipeline End!{LINE}\n\n")

# --------------------------------------------------------------------------------------------- #


def _preprocess(
    input_folder: str,
    file_name: str,
    confs: DSConf
) -> List[Image.Image]:
    """
    Preprocesses rank regions of interest (ROIs) from an image file for further analysis.
    This function loads an image from the specified input folder and file name, crops the regions
    defined by the provided ROIs, and applies a preprocessing pipeline to each cropped region.
    The preprocessing includes resizing, grayscale conversion, binarization, and thresholding.
    After preprocessing, outlier images are filtered out based on entropy and
    black/white pixel range.

    Args:
        input_folder (str): Path to the folder containing the image file.
        file_name (str): Name of the image file to process.
        confs (DSConf): Configurations.

    Returns:
        List[Image.Image]: List of preprocessed and filtered PIL Image objects corresponding to
        the input ROIs.
    """

    # 1. Output...
    output = []

    # 2. Constants...
    rois = confs.get_rois()

    # 3. File...
    file_path = fl.get_file_path(input_folder, file_name)
    if vl.is_valid(file_path) and vl.is_valid(rois):

        # 1.1 Open and resize image...
        img = Image.open(file_path)
        img = image.resize_image(img=img, resolution=confs.res)

        # 1.2 Process safely...
        try:

            # 2.1 Crops the regions...
            regions = [img.crop(roi) for roi in rois]
            if vl.is_valid(regions):

                # 3.1 Iterate regions...
                for region in regions:

                    # 4.1 Apply preprocessing pipeline...
                    processed = api.preprocess_image(
                        region,
                        resize_to=confs.resize_to,
                        grayscale=confs.grayscale,
                        binary=confs.binary,
                        threshold=confs.binary_threshold
                    )

                    # 4.2 Outlier?
                    if not api.is_outlier(
                        img=processed,
                        entropy_range=confs.entropy_range,
                        bw_range=confs.bw_range
                    ):

                        # 5.1 Adds valid image...
                        output.append(processed)

        # 1.3 Handle I/O errors...
        except OSError as e:
            print(f"Error processing {file_path}: {e}")

    # 4. Returns...
    return output


# --------------------------------------------------------------------------------------------- #


def _save_to(
    imgs: List[Image.Image],
    output_folder: str,
    start_index: int = 0,
    verbose: bool = False,
):
    """
    Saves a list of PIL Image objects to a specified output folder with sequentially
    numbered filenames and format `pre_{index}.png`.

    Args:
        imgs (List[Image.Image]): List of PIL Image objects to be saved.
        output_folder (str): Path to the folder where images will be saved.
        start_index (int, optional): Starting index for naming the saved images.
        verbose (bool, optional): If True, prints a summary message after saving.
    """

    # 1. Save images...
    if vl.is_valid(imgs) and fl.create_folder(output_folder):
        for img in imgs:

            # 2.1 Build image path...
            img_name = f'pre_{start_index}.png'
            img_path = fl.get_path(output_folder, img_name)

            # 2.2 Save image...
            img.save(img_path)
            start_index += 1

    # 2. Print summary...
    if verbose:
        print(f"✅ {len(imgs)} images saved to: {output_folder}")


# --------------------------------------------------------------------------------------------- #


def _classify(input_folder: str, output_folder: str, size: int, confs: DSConf):
    """
    Classifies and saves preprocessed rank images into the specified output folder.

    Args:
        imgs (List[Image.Image]): List of preprocessed PIL Image objects to classify and save.
        output_folder (str): Path to the folder where classified images will be saved.

    Returns:
        None
    """

    # 1. List images...
    files = image.list_images(input_folder)
    if vl.is_valid(files) and fl.create_folder(output_folder):

        # 1.1 Initialize progress...
        pb = PB(total=len(files), prefix="Classifing")
        for image_file in files:

            # 2.1 Load image...
            img = image.get_image(input_folder=input_folder, file_name=image_file)
            if img is not None:

                # 3.1 Predict class...
                img_class = api.get_img_class(
                    img=img, classes=confs.classes, model=confs.model
                )

                # 3.2 Resolve outlier...
                if not vl.is_valid(img_class):
                    img_class = confs.outlier_label

                # 3.3 Build output path...
                img_name = image.get_img_name(category=img_class, size=size)
                img_path = fl.get_path(output_folder, img_name)

                # 3.4 Save image...
                img.save(img_path)

            # 2.2 Update progress...
            pb.update()


# --------------------------------------------------------------------------------------------- #


def _filter_hash(input_folder: str, output_folder: str):
    """
    Filters out duplicate images in a folder using content-based hashing,
    and copies only the unique images to the output folder.

    Args:
        input_folder (str): Folder containing the classified (but possibly duplicate) images.
        output_folder (str): Folder to store the filtered unique images.

    Returns:
        None
    """

    # 1. Run hash filter...
    result = image.filter_images_by_hash(input_folder=input_folder, output_folder=output_folder)
    print(f"\n✅ {result} unique images saved to: {output_folder}")


# --------------------------------------------------------------------------------------------- #


def _class_separation(
    input_folder: str,
    output_folder: str,
    confs: DSConf
):

    # 1. Validate folders...
    if fl.is_folder(input_folder) and fl.create_folder(output_folder):

        # 1.1 Classify filenames...
        class_dict = api.classify_by_filename(
            input_folder=input_folder,
            outlier_label=confs.outlier_label,
            classes=confs.classes,
        )

        # 1.2 Validate classes...
        if vl.is_valid_dict(class_dict):

            # 2.1 Initialize progress...
            pb = PB(total=len(class_dict), prefix="Class Separation")

            # 2.2 Iterate classes...
            for key, value in class_dict.items():
                out_folder=fl.get_path(output_folder, key)

                # 3.1 Copy class files...
                for fname in value:
                    fl.copy_file(
                        input_folder=input_folder,
                        file_name=fname,
                        output_folder=out_folder,
                    )

                # 3.2 Update progress...
                pb.update()


# --------------------------------------------------------------------------------------------- #


def _class_balancing(
    input_folder: str, size: int, confs: DSConf, mode: Literal["add", "remove"] = "add"
):
    """
    Balances all class folders to the same number of images.

    If mode is 'remove', trims classes to match the smallest class.
    If mode is 'add', duplicates images to match the largest class (default behavior).

    Args:
        input_folder (str): Folder containing classified and deduplicated images.
        output_folder (str): Base output folder (not used here).
        mode (str): Balancing mode, 'add' to duplicate or 'remove' to trim. Default is 'add'.

    Returns:
        None
    """

    # 1. Classify images...
    class_images = api.classify_by_filename(
            input_folder=input_folder,
            outlier_label=confs.outlier_label,
            classes=confs.classes,
            all_images=True
        )

    # 2. Validate classes...
    if vl.is_valid_dict(class_images):

        # 1.1 Get class counts...
        counts = [len(imgs) for imgs in class_images.values() if len(imgs) > 0]
        if vl.is_valid_list(counts):

            # 2.1 Determine target size...
            target_size = max(counts) if (mode == 'add') else min(counts)
            if vl.is_valid_int(target_size):

                # 3.1 Initialize progress...
                pb = PB(total=len(class_images), prefix="Class Balancing")
                for rank, images in class_images.items():
                    imgs = images[:]

                    # 4.1 Count images...
                    current_size = len(imgs)
                    if vl.is_valid_int(current_size):

                        # 5.1 Balance class...
                        _balance_by_mode(
                            imgs=imgs,
                            rank=rank,
                            current_size=current_size,
                            target_size=target_size,
                            size=size,
                            mode=mode,
                            last=max(counts)
                        )

                    # 4.2 Update progress...
                    pb.update()

                # 3.2 Print summary...
                print(f"✅ Dataset balanced: {target_size} items per class (mode: '{mode}') 📊")


# --------------------------------------------------------------------------------------------- #


def _balance_by_mode(
    imgs: List[str],
    rank: str,
    current_size: int,
    target_size: int,
    size: int,
    mode: Literal["add", "remove"] = "add",
    last: int = 0
):

    # 1. Add samples...
    if (mode == 'add') and (current_size < target_size):
        needed = target_size - current_size

        # 1.1 Sample additions...
        samples = PUtils.sample_n(imgs, needed)
        for sample in samples:

            # 2.1 Copy sample...
            img_name = image.get_img_name(category=rank, size=size, last=last)
            ok = fl.copy_to(
                input_file=sample,
                output_file=fl.get_path(
                    fl.get_directory_path(sample), img_name
                )
            )

            # 2.2 Report failure...
            if not ok:
                print(f"Failed to move sample '{sample}'")

    # 2. Remove samples...
    elif (mode == 'remove') and (current_size > target_size):
        excess = current_size - target_size

        # 1.1 Sample removals...
        to_delete = PUtils.sample_n(imgs, excess, distinct=True)
        for sample in to_delete:

            # 2.1 Delete sample...
            if not fl.delete_file(sample):
                print(f"Failed to remove sample '{sample}'")


# --------------------------------------------------------------------------------------------- #


def _get_status(output_folder: str) -> dict:
    """
    Returns current pipeline status from status file, or initializes it to 0 if not found.

    Args:
        output_folder (str): The directory containing the status file.

    Returns:
        int: Parsed status code (default: 0 if file didn't exist).
    """

    # 1. Output...
    status = {STATUS_NUM: 0}

    # 2. Build file path...
    file_path = fl.get_path(output_folder, STATUS_FILE)
    if not fl.is_file(file_path):

        # 1.1 Create file if missing...
        pyon.to_file(status, file_path)

    # 3. Read and parse status...
    content = pyon.from_file(file_path)
    return content if isinstance(content, dict) else status


# --------------------------------------------------------------------------------------------- #


def _update_status(output_folder: str, status: dict) -> dict:
    """
    Updates the pipeline status in the status file.

    Args:
        output_folder (str): The directory containing the status file.
        status (int): Status value to persist.
    """

    # 1. Checks...
    if not (isinstance(status, dict) and STATUS_NUM in status):
        status = {STATUS_NUM: 0}

    # 2. Updates...
    status[STATUS_NUM] += 1

    # 3. Saves...
    file_path = fl.get_path(output_folder, STATUS_FILE)
    pyon.to_file(status, file_path)

    # 4. Returns...
    return status


# --------------------------------------------------------------------------------------------- #

```

---


<a id="agent-audit-checklist"></a>
## ✅ Agent Audit Checklist

When an agent writes or rewrites code into Notation E, it must check every
function with this checklist.

<a id="numbering"></a>
### Numbering

1. Does each scope start numbering correctly?
2. Are top-level blocks numbered `# 1`, `# 2`, `# 3`, and so on?
3. Is the level-zero prefix `0.` omitted correctly?
4. Do nested blocks use indentation level, such as `# 1.1` and `# 2.1`, not parent inheritance?
5. Are there duplicated, skipped, or unordered numbers?
6. Does any scope exceed nine numbered blocks?
7. Does any indentation level exceed nine?

### Comments

1. Does each numbered comment describe a real semantic unit?
2. Does each numbered comment use neutral third-person voice when possible?
3. Is the comment short and meaningful?
4. Are there vague comments such as `# 1. ...`?
5. Are comments explaining implementation details instead of semantic intent?
6. Are comments written in English?

<a id="block-size"></a>
### Block size

1. Does any numbered block contain three independent logical statements?
2. Can adjacent one-line blocks be merged without mixing unrelated concerns?
3. Would merging lines mix configuration and execution?
4. Does a multiline statement hide a following independent action?
5. After a multiline statement, does the next independent statement start a new numbered block?
6. Does each block support fast vertical scanning?

<a id="semantic-grouping"></a>
### Semantic grouping

1. Is each line grouped with the closest semantic dependency?
2. Is output initialization separated from later operational preparation?
3. Is construction grouped with immediate use when appropriate?
4. Are unrelated semantic categories kept apart?
5. Is the code grouped for scanning, not merely for line counting?

<a id="control-flow"></a>
### Control flow

1. Does `try` have its own numbered comment?
2. Does `except`, `else`, or `finally` receive a new numbered comment when it performs a different action?
3. Are cleanup, restore, rollback, logging, and fallback behavior visible?
4. Are complex branch bodies split with nested numbered comments?
5. Is `continue` avoided?
6. Are `if` / `elif` / `else` branches numbered according to semantic responsibility?

<a id="horizontal-limit-checklist"></a>
### Horizontal limit

1. Does code stay inside the visual separator width?
2. Are long statements wrapped using normal Python formatting?
3. Does each wrapped statement still behave as one logical statement?
4. Is the next independent statement after a wrapped call placed in a new block?

---

<a id="applicability"></a>
## 🔄 Applicability
Ideal for:
- Computer vision and OCR pipelines
- Automated data processing and analysis
- Research-oriented repositories
- Financial and time-series experiments
- Infrastructure for LLM-based projects
- Agent-generated code that must remain auditable
- Long-lived Python projects maintained by humans and AIs

---

<a id="universal-standards"></a>
## 🌍 Universal Standards
- Always fluid top-down readability
- Linear, transparent, and auditable logic
- Compact semantic blocks
- Visible control-flow responsibilities
- Low ambiguity for humans and LLMs
- Style easily replicable by humans and AIs

---

For LLM application, follow the style strictly:

- prefer numbered semantic blocks;
- avoid mid-function returns;
- avoid flow jumps;
- avoid hidden control-flow responsibilities;
- split ambiguous blocks;
- preserve semantic grouping over mechanical compactness.

> "Code is readable when the mind that writes it respects the time of the mind that will read it."

---

✨ *Notation E: clarity as a premise, efficiency as a style.*
