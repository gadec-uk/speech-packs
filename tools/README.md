# Speech-Pack Creation Scripts [![License Badge](https://img.shields.io/badge/BY--NC--SA%204.0%20License-grey?style=flat&logo=creativecommons&logoColor=white)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

This folder contains the necessary python scripts and json data files to create your own speech-packs for use with the [Matrix Departures Board](https://github.com/gadec-uk/matrix-departures-board) and mini [Departures Board +](https://github.com/gadec-uk/departures-board-plus) open-source software.

To use these scripts, you will need the following installed:

- The **Chatterbox TTS Desktop** client available [here](https://ampedhorizon.itch.io/chatterbox-tts-desktop).
- **FFmpeg** available [here](https://ffmpeg.org/download.html). Note: The FFmpeg binary must either be in the same folder as the scripts or in your PATH.
- **Python 3** available [here](https://www.python.org/downloads/)

You will need to have a high quality 10 to 20 second 24kHz voice sample WAV file to use with Chatterbox. This should be stored in the **Voices** directory of your Chatterbox TTS Desktop client. You will need to edit the **create_speech_file.py** script to set the VOICE_ARTIST configuration setting to use your voice sample. For example, if you are using a sample named "James.wav", you would change the line in the script file to *VOICE_ARTIST = "James"*.

The **audio_processor.py** script calls the Chatterbox server api to create a temporary 24kHz mono WAV file of the speech. It then uses a two-pass process with FFmpeg to perform loudness level matching to ITU-R BS.1770-3 at -17 LUFS outputting a mono MP3 encoded audio at 48kbps with a sample rate of 22050Hz. If you are using macOS or Linux you will need to manually install and setup a Chatterbox server.

Please do **not** post issues or help requests here regarding the Chatterbox AI client/server, FFmpeg or Python configuration.

Speech-Packs must be stored on the sd card in directories "VA", "VB", "VC" etc. Directories "V1" to "V9" are reserved. Each speech-pack must have a *voice.json* file in its root directory. A sample is provided (see also the standard *V1* and *V2* speech-packs).

The directory and file names created by the scripts are important and must not be changed.

After starting Chatterbox TTS Desktop, click the **Download/Set** button to load the AI model. The first time you do this, a 3Gb model will be downloaded. On subsequent runs, the model will be loaded from your local copy. To allow the scripts to generate speech files, click on the **Start Server** button, this will run a temporary local server on your computer which the python script can access.

To create the audio files, run the **create_speech_files.py** python script against each of the provided json files. For example, if you are creating a speech-pack "VA", you would use the following command to create the general announcement files:

**python create_speech_files.py --json=an_general.json --output=VA**

The script will create the appropriate sub-directories under the output path you provide.

**NOTE:** Chatterbox, like all AIs, makes mistakes and occasionally has hallucinations. These scripts will provide a good basis for creating your own Speech-Pack, but you will also need to do some manual checking of results and finessing. The AI was trained on American English so does not perform well with non-English placenames and often needs the input text tweaking to get close to the correct pronunciations. The generated speech can sometimes lean toward an American accent (even with a non-American sample) - if this occurs, try adjusting the *exaggeration* setting (to change this permanently, edit the value in the **audio_processor.py** script).
