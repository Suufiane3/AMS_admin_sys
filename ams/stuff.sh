#!/bin/bash

clear
echo "=== INFO STOCKAGE ==="

INFO=$(df -h / | grep -v "Filesystem" | tr -s ' ')
TOTAL=$(echo "$INFO" | cut -d' ' -f2)
USED=$(echo "$INFO" | cut -d' ' -f3)
FREE=$(echo "$INFO" | cut -d' ' -f4)
PERCENT=$(echo "$INFO" | cut -d' ' -f5)

echo "{\"total\": \"$TOTAL\", \"used\": \"$USED\", \"free\": \"$FREE\", \"percent\": \"$PERCENT\"}" >> data.json
echo "================"
