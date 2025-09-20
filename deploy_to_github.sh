#!/bin/bash

echo "========================================"
echo "Terabytes Legal AI - GitHub Deployment"
echo "========================================"
echo

echo "[1/5] Initializing Git repository..."
git init

echo
echo "[2/5] Adding all files to Git..."
git add .

echo
echo "[3/5] Committing changes..."
git commit -m "Initial commit: Terabytes Legal AI with PDF upload and Q&A features"

echo
echo "[4/5] Adding remote origin..."
git remote add origin https://github.com/lokeshwaraprasad/Terabytes-Legalai.git

echo
echo "[5/5] Pushing to GitHub..."
git branch -M main
git push -u origin main

echo
echo "========================================"
echo "Deployment completed successfully!"
echo "========================================"
echo
echo "Your repository is now available at:"
echo "https://github.com/lokeshwaraprasad/Terabytes-Legalai"
echo
echo "Next steps:"
echo "1. Set up environment variables in your hosting platform"
echo "2. Deploy using Railway, Render, or your preferred platform"
echo "3. Update the README with your live URL"
echo
