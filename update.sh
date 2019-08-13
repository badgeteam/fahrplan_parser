#!/bin/bash
wget "https://fahrplan.events.ccc.de/camp/2019/Fahrplan/schedule.json" -O schedule.json
mkdir -p output
rm -rf output/*
python convert.py