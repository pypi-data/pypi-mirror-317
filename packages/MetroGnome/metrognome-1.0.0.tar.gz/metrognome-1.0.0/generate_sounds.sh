#!/usr/bin/env bash

RESOURCES=metrognome/resources
mkdir -p ${RESOURCES}

ffmpeg -y -f lavfi -i "sine=frequency=440:duration=0.1" -c:a pcm_s16le -ar 44100 -ac 1 -loglevel error ${RESOURCES}/beep.wav
ffmpeg -y -f lavfi -i "sine=frequency=750:duration=0.1" -c:a pcm_s16le -ar 44100 -ac 1 -loglevel error ${RESOURCES}/click.wav
ffmpeg -y -f lavfi -i "anoisesrc=d=0.15" -c:a pcm_s16le -ar 44100 -ac 1 -loglevel error ${RESOURCES}/snare.wav
ffmpeg -y -f lavfi -i "sine=frequency=60:duration=0.3" -c:a pcm_s16le -ar 44100 -ac 1 -loglevel error ${RESOURCES}/kick.wav
