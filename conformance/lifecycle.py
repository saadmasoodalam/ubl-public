"""Independent public two-state alarm lifecycle illustration, not native benchmark."""
import argparse
import json

from conformance.demo import u7
from conformance.reference import CONTROLS, ContractReference

DEFAULT = [40, 80, 82, 65, 50, 80, 50]


def lifecycle(readings, trip=75, recover=55):
    readings = list(readings)
    for value in [trip, recover, *readings]:
        if type(value) is not int or not 0 <= value <= 127:
            raise ValueError("Readings and thresholds must be integers 0..127")
    if recover >= trip:
        raise ValueError("Recovery threshold must be below trip threshold")
    model = ContractReference(bytes(32))
    alarm = False
    atoms = []
    rows = []

    def emit(value, memory):
        if value in CONTROLS:
            atoms.append(0x06)
            model.feed(0x06)
        atom = (value << 1) | memory
        atoms.append(atom)
        model.feed(atom)

    for reading in readings:
        start = len(atoms)
        emit(reading, 0)
        event = None
        if not alarm and reading >= trip:
            alarm = True
            event = 90
        elif alarm and reading <= recover:
            alarm = False
            event = 91
        if event is not None:
            emit(event, 1)
        rows.append(dict(reading=reading, alarm=alarm, event=event,
                         atoms=bytes(atoms[start:]).hex(" ").upper(),
                         current=model.volatile, ledger=model.ledger[:]))
    return dict(trip=trip, recover=recover, rows=rows, alarm_active=alarm,
                atoms_hex=bytes(atoms).hex(" ").upper(), atom_count=len(atoms),
                final=model.snapshot(),
                scope="Independent public Python illustration; unbounded ledger; no native performance claim.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readings", type=u7, nargs="+", default=DEFAULT)
    parser.add_argument("--trip", type=u7, default=75)
    parser.add_argument("--recover", type=u7, default=55)
    args = parser.parse_args()
    try:
        result = lifecycle(args.readings, args.trip, args.recover)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
