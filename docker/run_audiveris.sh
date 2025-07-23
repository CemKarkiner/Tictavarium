#!/bin/bash

# Giriş ve çıkış klasörleri
INPUT_DIR="/input"
OUTPUT_DIR="/output"

# Audiveris JAR dosyasını çalıştır
java -jar /audiveris/audiveris.jar -batch "$INPUT_DIR" -export -output "$OUTPUT_DIR"
