#!/usr/bin/env python3

import argparse


def milliseconds_to_days(milliseconds):
    seconds = milliseconds / 1000
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    return days


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert milliseconds to days.")
    parser.add_argument("milliseconds", type=int, help="Time in milliseconds")

    args = parser.parse_args()

    days = milliseconds_to_days(args.milliseconds)
    print(f"{args.milliseconds} milliseconds is equal to {days} days.")
