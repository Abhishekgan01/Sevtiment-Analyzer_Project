#!/bin/bash

# Create the .streamlit directory if it doesn't exist
mkdir -p ~/.streamlit/

# Create the config.toml file with the required settings
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
" > ~/.streamlit/config.toml

echo "Setup script executed successfully."
