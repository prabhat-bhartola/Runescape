#!/bin/bash

if [ -z "$1" ]; then
  echo "🚨 Please provide a script name e.g. 'sh run_script.sh legit_script_name'."
  exit 1
fi

SCRIPT_NAME="$1"
SCRIPT_PATH="./scripts/$SCRIPT_NAME.py"

# Check if the script file exists
if [ ! -f "$SCRIPT_PATH" ]; then
  echo "🚨 Script '$SCRIPT_NAME' not found in the scripts folder."
  echo "📝 Available files:"
  for file in ./scripts/*.py; do
    echo "- $(basename "$file")"
  done
  exit 1
fi

echo "Running script '$SCRIPT_NAME'..."
python3 "$SCRIPT_PATH"
