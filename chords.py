import argparse
import json
import sys

def load_chords(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {file_path}. Ensure it is a valid JSON file.")
        sys.exit(1)

def search_chord(chords, instrument, chord_name):
    chord_name = chord_name.lower()  # Normalize input to lowercase

    # Iterate through all chords in the JSON
    for chord, data in chords.items():
        aliases = [alias.lower() for alias in data.get("aliases", [])]  # Normalize aliases to lowercase
        if chord_name == chord.lower() or chord_name in aliases:
            # Get the fingerings for the specified instrument
            fingerings = data.get("fingerings", {}).get(instrument)
            if fingerings:
                # Return the fingerings as a comma-separated string
                return ", ".join(fingerings)
            else:
                return f"No {instrument} fingerings available for '{chord}'."

    # If no match is found
    return f"No fingerings found for '{chord_name}'."

def main():
    parser = argparse.ArgumentParser(description="Search for chord fingerings.")
    parser.add_argument("chord", help="The name of the chord to search for (e.g., 'C Major').")
    parser.add_argument("-u", "--ukulele", action="store_true", help="Search for ukulele fingerings instead of guitar.")
    args = parser.parse_args()

    chords = load_chords("chords.json")
    instrument = "ukulele" if args.ukulele else "guitar"
    result = search_chord(chords, instrument, args.chord)
    print(result)

if __name__ == "__main__":
    main()