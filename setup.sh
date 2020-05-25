#!/usr/bin/env bash

# Run this one time only

# Update markdown docs with project name
find . -type f -name "*.md" -print0 | xargs -0 sed -i '' 's/\[GH_REPO\]/covid19\-budget\-tracker/g'

# Setup Conda environment
rm -rf ./.${PWD##*/}
conda create --prefix ./.${PWD##*/}
conda activate ./.${PWD##*/}
pip install -r requirements.txt
conda deactivate

# Create env.sh to initialize environment
echo "conda deactivate" > env.sh
echo "conda activate ./.${PWD##*/}" >> env.sh

# Add to .gitignore
echo "# Local" >> .gitignore
echo ".${PWD##*/}" >> .gitignore
echo "setup.sh" >> .gitignore
echo "env.sh" >> .gitignore

echo "Done! Source env.sh to start Conda environment."
