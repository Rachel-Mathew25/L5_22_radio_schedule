# Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest were the style issues: renaming the camelCase functions to
snake_case, adding docstrings, splitting the long lines, and putting the
`return` on its own line. These were mechanical changes that did not affect
how the program behaves, and the tool messages told me exactly what to do.

The hardest was removing `eval()` from `overlapFree`. I could not just swap
it for a safer call, because the function took a string like "7 + 1 <= 13".
I had to redesign it as `overlap_free(start_hour, duration_hours,
next_start_hour)` and update the call in `main()`. The global
`booked_minutes` was also harder than it looked. Removing the `global`
statement meant changing how the total is calculated, and I found that the
old version never reduced the total when `removeSlot` was called, so it
could go out of sync with the database. I fixed it by calculating the total
from the database with `SUM(minutes)`.

## 2. Did the static analysis tools report any false positives?

There were no clear false positives, but some warnings were less serious in
this specific program. For example, Bandit flagged `eval()` (B307) and the
string-formatted SQL query (B608), but in the demo they were only called with
hardcoded values from `main()`, so nobody could actually exploit them. They
are still real design problems, because the functions would be unsafe as soon
as they received user input. Bandit's hardcoded password warning (B105) is
also low severity here, because `STUDIO_PASSWORD` is never used for anything.
I still fixed it, because storing secrets in source code is a bad habit.
Pylint and Flake8 also reported the same long lines twice with different
limits (100 and 79 characters), which is duplication rather than a false
positive.

## 3. How would I integrate static analysis tools into my workflow?

I would run Flake8 and Pylint in my editor so problems show up while I type.
I would add a pre-commit hook that runs the tools before each commit, so
problems are caught early. I would also run Pylint, Flake8 and Bandit in a
CI pipeline such as GitHub Actions on every pull request, and fail the build
on Bandit medium or high findings and on a Pylint score below an agreed
threshold. I would keep the rules in a config file, such as `.pylintrc` or
`setup.cfg`, so the whole team uses the same settings. If a warning really
is a false positive, I would suppress only that one line with a comment
explaining why, instead of turning the check off completely.

## 4. What tangible improvements did I observe?

- Pylint went from 2.41/10 to 10.00/10, Bandit from 3 issues to 0, and
  Flake8 from 4 issues to 0.
- The SQL query now uses `?` placeholders, which removes the SQL injection
  risk.
- Removing `eval()` removed the risk of running arbitrary code.
- The booked minutes total is now calculated from the database, which fixed a
  hidden bug where it was wrong after a slot was removed.
- The code is easier to read, with consistent names, docstrings, shorter
  lines and no multiple statements on one line.
- Importing the file no longer runs the demo, because `main()` is now behind
  `if __name__ == "__main__":`.
- The program prints exactly the same output as before, so the fixes did not
  change what it does.