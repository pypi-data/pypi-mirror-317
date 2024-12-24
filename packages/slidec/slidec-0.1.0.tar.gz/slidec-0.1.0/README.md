# slidec

A simple python tool to present markdown in your terminal as slides.

Useful if you are wanting to do demos from the command line and refer to notes.

Works well with tmux (etc.) split planes, one for live demo, one for the
slides/notes.

Option to fuzzy search and jump to selected slide if
[`fzf`](https://github.com/junegunn/fzf) is installed.


<img src="assets/demo.gif">

## Slide Format

Slides are written in a single markdown file separated by `---`.

E.g.

```markdown
# Example slide 1

-  Content

---

# Example slide 2

- More content

```

> [!NOTE]
> There should be no trailing white space after `---`.


## Run
```terminal
slidec example_slides.md
```

## Install

### Dev
In chosen python environment, from repo root directory, run
```terminal
pip install -e .
```

## Navigation
Once in presentation mode

- Next slide: `n` or `j`
- Previous slide: `p` or `k`
- Select slide: `g` navigate with fuzzy search (requires [`fzf`](https://github.com/junegunn/fzf))
- quit: `q`

## Inspiration

There are other much more robust tools for this task, such as
[`lookatme`](https://github.com/d0c-s4vage/lookatme) or
[`slides`](https://github.com/maaslalani/slides).

However, I found I could get all the functionality I needed in a single small python
script.

As an exercise, I have since turned the `slidec.py` script it into a python package for
easy install, though it still works on it's own.
