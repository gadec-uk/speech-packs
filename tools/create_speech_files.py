#
# This is an example python script for creating station announcement speech-pack files, which are
# located in the "Vx" directory (where "x" = A-Z). The script takes two command line parameters,
# the json file containing the phrases to be created and the output directory path for speech-pack.
#
# Example usage (assumes the json file is in the same directory as the script files):
#
# python create_speech_files.py --json="an_general.json" --output="VA"
#
# The script imports functions from audio_processor.py which must be located in the same folder as this script.
# Additionally, audio_processor.py uses FFmpeg to perform two-pass loudness leveling on the Chatterbox created
# .wav file so the FFmpeg binary MUST either be located in the same directory as these scripts or in your PATH.
# The Chatterbox TTS Desktop must be running, with the server enabled. See the audio_processor.py file for more details.
#
# On the SD Card, Speech-Packs must be stored in "Vx" folders, where "x" is a letter A-Z. V1-V9 are reserved.

import json
import os
from pathlib import Path
import argparse
from audio_processor import loudness_match_to_mp3, create_voice_file

# Configuration
VOICE_ARTIST = "Jane" # Change this to your own sampled voice name as shown in Chatterbox

def generate_speech_pack_audio(json_file: Path, base_output_dir: Path):
    # Load JSON data
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {json_file}")
        return
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file '{json_file}': {e}")
        return

    path_suffix = data.get("path", "")
    phrases = data.get("phrases", [])

    output_dir = (
        base_output_dir / path_suffix if path_suffix else base_output_dir
    )

    # Validate path syntax and create the combined output directory
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except (OSError, ValueError) as e:
        print(
            f"Error: Output path '{output_dir}' is invalid or inaccessible: {e}"
        )
        return

    # Process each operator
    for phrase in phrases:
        phrase_text = phrase.get("phrase")
        code = phrase.get("code")

        if not phrase_text or not code:
            print(f"Skipping entry missing phrase or code: {phrase}")
            continue

        # create the speech file
        output_file = os.path.join(output_dir, f"{code}")
        try:
            create_voice_file(phrase_text, VOICE_ARTIST, str(output_file))
        except Exception as e:
            print(f"Failed to create voice file for {phrase_text}: {e}")
            break

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--json", required=True, help="Name of the json file contains the phrases to create")
        parser.add_argument("--output", required=True, help="Output directory path for the speech pack")
        args = parser.parse_args()

        json_path = Path(args.json)
        base_output_dir = Path(args.output)

        # Check if the JSON file exists and is a valid file
        if not json_path.is_file():
            print(f"Error: JSON file not found at '{json_path}'")
            sys.exit(1)

        generate_speech_pack_audio(json_path, base_output_dir)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        input("Press Enter to exit...")
