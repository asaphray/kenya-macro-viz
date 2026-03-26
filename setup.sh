#!/bin/bash

# Define Project Name
PROJECT_NAME="kenya-macro-viz"

echo "🚀 Starting setup for $PROJECT_NAME..."

# 1. Create Folder Structure
mkdir -p data/cleaned
mkdir -p modules
mkdir -p .streamlit
mkdir -p notebooks

# 2. Create Initial Files
touch app.py
touch requirements.txt
touch .gitignore
touch README.md
touch modules/__init__.py
touch modules/data_loader.py
touch modules/charts.py

# 3. Add Content to .gitignore
cat <<EOT >> .gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
venv/
.env

# Streamlit
.streamlit/config.toml

# Data (Optional: ignore if files are too large for GitHub)
# data/cleaned/*.csv
EOT

# 4. Add Initial Requirements
cat <<EOT >> requirements.txt
streamlit
pandas
plotly
nbformat
EOT

# 5. Initialize Git
git init
git add .
git commit -m "chore: initial project structure and environment setup"

echo "✅ Setup complete! Folder structure created and Git initialized."
echo "💡 Next step: Move your CSV files into 'data/cleaned/'"