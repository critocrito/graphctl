#!/usr/bin/env python3
import csv


def write_to_file(output: str, data: list[dict]):
    """Serialize data to a CSV and write it to a file at output."""
    fields = data[0].keys()

    with open(output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
