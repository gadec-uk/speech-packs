# Speech-Packs

This repository contains station audio announcement Speech Packs for use with the [Matrix Departures Board](https://github.com/gadec-uk/matrix-departures-board) and mini [Departures Board +](https://github.com/gadec-uk/departures-board-plus) open-source software.

To enable audio station announcements you will need a micro-sd card, formatted as FAT32 with the two speech-packs installed. Copy the contents of the sdcard folder to the root of the micro-sd card, retaining the precise file and folder structure here (the root of the card should contain the manifest.lst, version.json and V1 and V2 folders).

The spoken audio was generated using [Chatterbox AI](https://chatterboxai.net/) with public domain voice samples from [LibriVox](https://librivox.org/). "Andy" (V1) was created from a voice sample of [Andy Minter](https://librivox.org/reader/152) and "Ruth" (V2) was created from a voice sample of [Ruth Golding](https://librivox.org/reader/2607). All of the generated audio files were level matched to ITU-R BS.1770-3 Loudness at -17 LUFS and then MP3 mono encoded at 48kbps with a sample rate of 22050Hz.

Additional speech-packs can be added to the card. You must follow the same file and folder naming conventions and all files must be encoded as MP3 mono 22050Hz at 48kbps. User created Speech Packs should be stored in folders VA, VB, VC etc. Folders V3 to V9 are reserved for future system Speech Packs.
