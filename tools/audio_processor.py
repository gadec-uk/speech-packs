#
# This module uses FFmpeg to perform two-pass loudness leveling on the Chatterbox created .wav file,
# the FFmpeg binary MUST be either located in the same directory as the script or in your PATH.
#
# Chatterbox TTS Desktop must be running, with the server enabled. Change the CHATTERBOX_URL below if you are
# running Chatterbox on a different machine to this script.
#
import json
import re
import os
import subprocess
import requests
from pathlib import Path

CHATTERBOX_URL = "http://localhost:8001/v1/audio/speech" # Standard local Chatterbox API port

def create_voice_file(text_to_speak: str, voice_artist: str, output_filename: str):
    wav_filename = output_filename + ".wav"
    mp3_filename = output_filename + ".mp3"

    print(f"Generating audio for '{text_to_speak}' -> {wav_filename}...")
    # Payload structure expected by Chatterbox / OpenAI-style TTS endpoints
    payload = {
        "input": text_to_speak,
        "voice": voice_artist,
        "response_format": "wav",
        "exaggeration": 0.5
    }

    try:
        response = requests.post(CHATTERBOX_URL, json=payload, timeout=30)

        if response.status_code == 200:
            # Save the raw binary WAV audio stream
            with open(wav_filename, "wb") as audio_file:
                audio_file.write(response.content)
            print(f"Saved: {wav_filename}")
            try:
                loudness_match_to_mp3(
                    input_file=str(wav_filename),
                    output_file=str(mp3_filename),
                    target_lufs=-17.0,
                    max_tp_dbtp=-0.5
                )
                os.remove(wav_filename)  # Delete the temporary .wav file
            except Exception as e:
                print(f"Failed to process mp3 for {text_to_speak}: {e}")

        else:
            print(f"Failed to generate speech for '{text_to_speak}'. Server returned {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Connection error while calling Chatterbox: {e}")


def loudness_match_to_mp3(
    input_file: str,
    output_file: str,
    target_lufs: float = -17.0,
    max_tp_dbtp: float = -0.5,
) -> None:
    """Normalizes a WAV file to target LUFS/True-Peak and encodes it to a

    22050Hz mono MP3 at 48k bitrate with stripped metadata.
    """
    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Pass 1: Measure integrated loudness, LRA, and True Peak
    pass1_cmd = [
        "ffmpeg",
        "-hide_banner",
        "-y",
        "-i",
        str(input_path),
        "-af",
        f"loudnorm=I={target_lufs}:TP={max_tp_dbtp}:print_format=json",
        "-f",
        "null",
        "-",
    ]

    result = subprocess.run(
        pass1_cmd, capture_output=True, text=True, check=True
    )

    # Extract JSON metrics from stderr
    json_match = re.search(r"\{[\s\S]*\}", result.stderr)
    if not json_match:
        raise RuntimeError("Failed to parse measurement data from FFmpeg.")

    stats = json.loads(json_match.group(0))

    # Pass 2: Apply linear normalization and output with target MP3 encoding options
    pass2_cmd = [
        "ffmpeg",
        "-hide_banner",
        "-y",
        "-i",
        str(input_path),
        "-af",
        (
            f"loudnorm=I={target_lufs}:TP={max_tp_dbtp}:"
            f"measured_i={stats['input_i']}:"
            f"measured_tp={stats['input_tp']}:"
            f"measured_lra={stats['input_lra']}:"
            f"measured_thresh={stats['input_thresh']}:"
            f"offset={stats['target_offset']}:"
            f"linear=true"
        ),
        "-c:a",
        "libmp3lame",
        "-b:a",
        "48k",
        "-ac",
        "1",
        "-ar",
        "22050",
        "-write_xing",
        "0",
        "-map_metadata",
        "-1",
        "-write_id3v1",
        "0",
        str(output_path),
    ]

    subprocess.run(pass2_cmd, check=True)
    print(f"Successfully processed and saved to: {output_path}")


if __name__ == "__main__":
    loudness_match_to_mp3(
        input_file="input_24kHz_16bit_mono.wav",
        output_file="output_22050Hz_48k.mp3",
        target_lufs=-17.0,
        max_tp_dbtp=-0.5,
    )