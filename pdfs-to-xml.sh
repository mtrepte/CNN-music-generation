#!/bin/bash
# A script by Lolzypops
cd audiveris
for file in ../pdf-collection/*.pdf; do
    filename=$(basename "$file")
    filename="${filename%.*}"
    if [ -d "../xml-collection/$filename/" ] # Check if already processed: skip, else: process
    then
        echo "--- $filename already processed ---"
        continue
    else
        echo "--- processing $filename ---"
        gradle run -PcmdLineArgs="-batch,-export,-output,../xml-collection,--,$file"
    fi
done
# Unzipping MXL
cd ../xml-collection
for song in *; do
    if [[ -d "$song" && ! -L "$song" ]]; then # Excluding symlinks
        if [ ! -f "$song/*.xml" ]; then # Checking not already unzipped
            unzip -o "$song/*.mxl" -d "$song"
        fi
    fi
done
