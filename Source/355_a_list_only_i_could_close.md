# 355. A LIST ONLY I COULD CLOSE

*18 Sept 2026. Matt: "update something in the command files/bat files to update the to do list?
You tell me."*

## 1. THE ASYMMETRY

`matt_todo.txt` is the source and `MY_TODO.html` is generated from it, so the page has never been
wrong about the file. **The file was wrong about the world, and only in one direction.**

Matt could read an item, do the thing, and the item stayed open until I noticed and edited the
file for him. Today that gap was **five items**: three runs of `ff.bat` he had already made, the
directive paste he had already done, and the Fable job he had already sent and had already had
returned. The count on the page said 45; the honest count was 40.

**A list only one of us can close drifts in one direction, always,** and the direction is toward
looking like more is outstanding than is.

## 2. WHAT SHIPPED

**`done.bat` and `done.py`.**

```
done ff.bat                    tick the one open item matching that text
done "PASTE THE DIRECTIVE"     quotes when the text has spaces
done --list                    every open item, numbered
done --check ff.bat            say what it would tick, change nothing
done --undo ff.bat             put a ticked item back to open
```

**IT REFUSES RATHER THAN GUESSES.** The text must match exactly one open item. On zero matches or
two it prints the candidates and writes nothing. **Ticking the wrong line silently is worse than
not ticking at all**, because the whole value of the file is that it can be trusted.

Both refusals were **shown firing before it shipped** (0.2):
- `done ff.bat` matched two open items and refused, naming both.
- `done "banana daiquiri"` matched none and refused.
- `--check` on a unique phrase changed nothing, confirmed by hashing the file before and after.
- The real run ticked one, printed the new count, and rebuilt the page and the sheet's stamp.
- `--undo` put it back.

**ONE IMPLEMENTATION.** After writing, it archives the file and calls `todo_page.main()`, which is
the same code path `ff.bat` runs. The page and the week sheet's count cannot drift from the file
because there is only one thing that writes them.

## 3. AND IT IS ON BOTH PAGES FROM ONE LIST

The command was added to `sheet_engine.TODO_CMDS`, which is the single source the to-do page reads
AND the source `make_commands.py` renders into `COMMANDS.html` (doc 353). One entry, two pages, no
third place to update. That is doc 351's defrag rule applied to a new command rather than to old
prose.

## 4. WHAT IT DOES NOT FIX

Matt still cannot tick an item **from the page**, which is where he is reading. The page is static
HTML; a checkbox there would live in one browser's storage and never reach `matt_todo.txt`.
**NOT YET RUN, with the form written: the to-do page could POST to a tiny local handler that
`ff.bat` already has no reason to start, so the honest options are a one-line `done` command (this)
or a real local service.** He has the command; the service is not worth a background process.
