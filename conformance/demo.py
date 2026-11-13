"""Editable temperature example using only the public UBL contract reference."""
import argparse
import json

from conformance.reference import CONTROLS, ContractReference


def temperature_example(readings, threshold=70):
    """Keep every reading transient; append each reading at/above the threshold."""
    values = list(readings)
    for value in [threshold, *values]:
        if type(value) is not int or not 0 <= value <= 127:
            raise ValueError('Readings and threshold must be integers from 0 to 127.')
    reference = ContractReference(bytes(32))  # Explicit illustrative E_0.
    atoms = []
    rows = []
    for reading in values:
        start = len(atoms)
        # This condition belongs to this Python application, not to a UBL opcode.
        for memory in ((0, 1) if reading >= threshold else (0,)):
            if reading in CONTROLS:
                atoms.append(0x06)  # ESC makes the next reserved payload literal.
            atoms.append((reading << 1) | memory)
        for atom in atoms[start:]:
            reference.feed(atom)
        rows.append(dict(reading=reading, atoms=bytes(atoms[start:]).hex(' ').upper(),
                         current=reference.volatile, alarms=reference.ledger[:]))
    return dict(example='temperature', threshold=threshold, rows=rows,
                atoms_hex=bytes(atoms).hex(' ').upper(), atom_count=len(atoms),
                eventid_seed_hex='00' * 32, final=reference.snapshot(),
                scope='Public-contract software illustration; no full framing, hardware, or timing model.')


def u7(text):
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError('Use an integer from 0 to 127.') from None
    if not 0 <= value <= 127:
        raise argparse.ArgumentTypeError('Use an integer from 0 to 127.')
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--readings', type=u7, nargs='+', default=[20, 45, 70, 75, 75, 60, 125])
    parser.add_argument('--threshold', type=u7, default=70)
    parser.add_argument('--json', action='store_true', help='Print a machine-readable trace.')
    args = parser.parse_args()
    result = temperature_example(args.readings, args.threshold)
    if args.json:
        print(json.dumps(result, indent=2))
        return
    print('UBL public-contract temperature example (software only)')
    print(f"Alarm rule: reading >= {result['threshold']}; readings are synthetic seven-bit values.")
    print(f"{'Reading':>7}  {'Atom bytes':<12}  {'Current':>7}  Alarm ledger")
    for row in result['rows']:
        print(f"{row['reading']:>7}  {row['atoms']:<12}  {row['current']:>7}  {row['alarms']}")
    print(f"Total atoms, including ESC controls: {result['atom_count']}")
    print('Raw bytes: ' + result['atoms_hex'])
    print('Edit --readings / --threshold, or conformance/demo.py, and run again.')
    print('No clock, speed, energy, physical persistence or full-kernel conformance claim.')


if __name__ == '__main__':
    main()
