"""Audit forward-return labels against the final session of a training fold."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date
from math import isfinite
from pathlib import Path


@dataclass(frozen=True)
class Label:
    series: str
    start: date
    endpoint: date
    forward_return: float


def read_panel(path: Path) -> tuple[list[date], dict[str, list[tuple[date, float]]]]:
    """Read a wide session calendar. Empty cells represent missing observations."""
    with path.open(encoding="utf-8-sig", newline="") as file:
        rows = csv.reader(file)
        header = next(rows, [])
        if len(header) < 2 or header[0] != "session" or len(set(header)) != len(header):
            raise ValueError("Use a session column followed by unique series names.")
        if not all(name.strip() for name in header):
            raise ValueError("A series name is empty.")
        observations = {name: [] for name in header[1:]}
        calendar = []
        for line_no, row in enumerate(rows, start=2):
            if len(row) != len(header):
                raise ValueError(f"Wrong number of columns on line {line_no}.")
            session = date.fromisoformat(row[0])
            if calendar and session <= calendar[-1]:
                raise ValueError(f"Sessions must increase strictly on line {line_no}.")
            calendar.append(session)
            for name, raw in zip(header[1:], row[1:]):
                if raw.strip():
                    price = float(raw)
                    if not isfinite(price) or price <= 0:
                        raise ValueError(f"Invalid price for {name} on {session}.")
                    observations[name].append((session, price))
    return calendar, observations


def forward_labels(observations, horizon: int) -> list[Label]:
    """Use the h-th subsequent observed price in each series as its label endpoint."""
    if horizon < 1:
        raise ValueError("The horizon must be at least one observation.")
    labels = []
    for series, prices in observations.items():
        for idx in range(len(prices) - horizon):
            start, initial = prices[idx]
            endpoint, final = prices[idx + horizon]
            labels.append(Label(series, start, endpoint, final / initial - 1))
    return labels


def audit(calendar, labels, cutoff: date, horizon: int):
    if horizon < 1 or cutoff not in calendar:
        raise ValueError("Choose a positive horizon and a cutoff on the supplied calendar.")
    last_start = calendar.index(cutoff) - horizon
    calendar_only = [] if last_start < 0 else [
        label for label in labels if label.start <= calendar[last_start]
    ]
    crossing = [label for label in calendar_only if label.endpoint > cutoff]
    eligible = [label for label in labels if label.endpoint <= cutoff]
    return calendar_only, crossing, eligible


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", type=Path, default=Path(__file__).with_name("sessions.csv"))
    parser.add_argument("--cutoff", type=date.fromisoformat, default=date(2030, 4, 8))
    parser.add_argument("--horizon", type=int, default=2)
    args = parser.parse_args()
    try:
        calendar, observations = read_panel(args.panel)
        labels = forward_labels(observations, args.horizon)
        candidates, crossing, eligible = audit(calendar, labels, args.cutoff, args.horizon)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(f"Cutoff: {args.cutoff} | Horizon: {args.horizon} observations")
    print(f"Calendar-only candidates: {len(candidates)}")
    print(f"Candidates crossing cutoff: {len(crossing)}")
    print(f"Endpoint-verified training rows: {len(eligible)}")
    for label in crossing:
        print(f"  {label.series}: {label.start} -> {label.endpoint}")


if __name__ == "__main__":
    main()
