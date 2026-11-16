"""Read the archived synthetic inputs and print the two portfolio checks."""

import json
import sqlite3
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def observations(filename):
    rows = read(filename)
    if not all(row["passed"] for row in rows):
        raise ValueError(f"Failed assertion in {filename}")
    return {row["assertion"]: row["observed"] for row in rows}


def main():
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE profiles (label TEXT PRIMARY KEY, weights TEXT NOT NULL)")
        for label, profile in read("allocation-policy-v1.json")["profiles"].items():
            weights = {name: str(Fraction(w)) for name, w in profile["model_weights"].items()}
            if sum(map(Fraction, weights.values())) != 1:
                raise ValueError(f"Invalid weights for {label}")
            db.execute("INSERT INTO profiles VALUES (?, ?)", (label, json.dumps(weights, sort_keys=True)))

        db.execute("CREATE TABLE scenarios (name TEXT PRIMARY KEY, principal INTEGER, expected_net INTEGER)")
        for filename, vector, totals, label in (
            ("default-assertions.json", "hand_calculated_vector", "hand_calculated_totals", "Default"),
            ("liquidity-assertions.json", "liquidity_first_vector", "net_and_projection", "Day 3 liquidity"),
        ):
            values = observations(filename)
            principal = sum(map(Fraction, values[vector].values()))
            expected_net = Fraction(values[totals][1])
            if principal.denominator != 1 or expected_net.denominator != 1:
                raise ValueError("This case uses whole CNY amounts")
            db.execute("INSERT INTO scenarios VALUES (?, ?, ?)", (label, int(principal), int(expected_net)))

        print("Target allocations\nprofiles | weights in risk sleeves R1 to R5")
        groups = db.execute("SELECT COUNT(*), weights FROM profiles GROUP BY weights ORDER BY COUNT(*)")
        for count, weights in groups:
            print(count, "|", json.loads(weights))
        results = db.execute("""
            SELECT name, principal, expected_net, 100.0 * expected_net / principal AS pct
            FROM scenarios ORDER BY expected_net DESC
        """)
        print("\nScenario | principal CNY | expected net CNY | expected net / principal")
        for name, principal, net, pct in results:
            print(f"{name} | {principal:,} | {net:,} | {pct:.1f}%")


if __name__ == "__main__":
    main()
