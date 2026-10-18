"""Programme schedule for a radio station.

Books show slots, lists the morning shows, checks timing and removes slots.
"""
import os
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE slots ("
    "id INTEGER PRIMARY KEY, show TEXT, host TEXT, "
    "start_hour INTEGER, minutes INTEGER)"
)
# Read the secret from the environment instead of hardcoding it.
STUDIO_PASSWORD = os.environ.get("STUDIO_PASSWORD")


def add_slot(show, host, start_hour, minutes):
    """Book a new show slot."""
    conn.execute(
        "INSERT INTO slots (show, host, start_hour, minutes) "
        "VALUES (?, ?, ?, ?)",
        (show, host, start_hour, minutes),
    )


def booked_minutes():
    """Return the total number of minutes currently booked."""
    row = conn.execute("SELECT COALESCE(SUM(minutes), 0) FROM slots")
    return row.fetchone()[0]


def slot_label(show, host):
    """Return a display label for a slot."""
    return f"{show} hosted by {host}"


def overlap_free(start_hour, duration_hours, next_start_hour):
    """Return True if a slot finishes before the next one starts."""
    return start_hour + duration_hours <= next_start_hour


def morning_shows():
    """Return the names of all shows starting before noon."""
    if booked_minutes() > 0:
        rows = conn.execute("SELECT show FROM slots WHERE start_hour < 12")
        return [r[0] for r in rows]
    return []


def remove_slot(slot_id):
    """Remove a slot by its id."""
    conn.execute("DELETE FROM slots WHERE id = ?", (slot_id,))


def main():
    """Run a short demonstration."""
    add_slot("Sunrise Beats", "Vik", 7, 60)
    add_slot("Midday Talk", "Anu", 13, 45)
    print(slot_label("Sunrise Beats", "Vik"))
    print(overlap_free(7, 1, 13), morning_shows())
    remove_slot(2)


if __name__ == "__main__":
    main()
