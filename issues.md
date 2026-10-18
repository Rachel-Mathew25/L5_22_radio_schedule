cat > issues.md << 'EOF'
# Issues Found in radio_schedule.py

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| SQL injection | Security (Bandit B608, Medium) | 11 | The INSERT query is built with `%` string formatting, so a show name like `x'); DROP TABLE slots;--` could alter the query. | Use a parameterised query with `?` placeholders and pass the values as a tuple. |
| Use of `eval` | Security (Bandit B307, Medium; Pylint W0123) | 21 | `eval(formula)` runs any text it receives as code, so it could execute arbitrary commands. | Remove `eval`. Replace it with a plain function `overlap_free(start_hour, duration_hours, next_start_hour)` that does the comparison directly. |
| Hardcoded password | Security (Bandit B105, Low) | 5 | `STUDIO_PASSWORD = "onair2024"` stores a secret in source code, where it is visible to anyone with repo access. | Read the value from an environment variable with `os.environ.get("STUDIO_PASSWORD")`. |
| Global state out of sync | Bug / Design (Pylint W0603) | 6, 10, 27 | `booked_minutes` is a global that is never decreased when `removeSlot` runs, so it becomes wrong after a slot is removed. | Remove the global. Calculate the total from the database with a `booked_minutes()` function using `SUM(minutes)`. |
| Broad exception caught | Quality (Pylint W0718) | 22 | `except Exception` hides every kind of error and returns `False` silently. | Removed together with `eval`, since the new comparison cannot raise. |
| Function names not snake_case | Style (Pylint C0103) | 9, 15, 19, 26, 31 | `addSlot`, `slotLabel`, `overlapFree`, `morningShows` and `removeSlot` use camelCase. | Rename to `add_slot`, `slot_label`, `overlap_free`, `morning_shows` and `remove_slot`. |
| Missing docstrings | Style (Pylint C0114, C0116) | 1, 9, 15, 19, 26, 31, 35 | The module and every function have no docstring. | Add a short docstring to the module and each function. |
| Lines too long | Style (Pylint C0301, Flake8 E501) | 4, 11, 27 | Three lines are far longer than the 79/100 character limits. | Split the long strings and statements across several lines. |
| Multiple statements on one line | Style (Pylint C0321, Flake8 E701) | 27 | `if ...: return [...]` is written on a single line. | Put the `return` on its own indented line. |
| Old-style string formatting | Style (Pylint C0209) | 11, 16 | `%` and `.format()` are used where an f-string is clearer. | Use an f-string in `slot_label`. The SQL line now uses `?` placeholders instead. |
| `main()` runs on import | Design | 43 | `main()` is called at module level, so importing the file runs the demo. | Wrap the call in `if __name__ == "__main__":`. |
EOF