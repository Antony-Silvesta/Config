#!/bin/bash
echo "Starting Selenium Tests..."
# Detect operating system
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    # Unix-based paths (e.g., GitHub Actions)
    script_path="/home/runner/work/Configuration/configuration"
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win32"* ]]; then
    # Windows-based paths
    script_path="C:/Users/shinba/Configuration"
else
    echo "Unsupported OS type: $OSTYPE"
    exit 1
fi
# Add LoginTest to PYTHONPATH
export PYTHONPATH="$script_path"
# Print the paths for debugging
echo "Using script path: $script_path"
# Run each Selenium test script
python "$script_path/configfile/config.py"
pytest "$script_path/login_testcases/test_invalid_login.py" 
pytest "$script_path/login_testcases/test_valid_login.py" 
echo "All tests completed." 