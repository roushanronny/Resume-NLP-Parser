#!/bin/bash

# Resume NLP Parser - Deployment Setup Script

echo "🚀 Resume NLP Parser - Deployment Setup"
echo "========================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Add all files
echo "📝 Adding files to Git..."
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit"
else
    echo "💾 Committing changes..."
    git commit -m "Resume NLP Parser - Ready for deployment"
    echo "✅ Changes committed"
fi

echo ""
echo "========================================"
echo "✅ Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Create a new repository on GitHub (https://github.com/new)"
echo "2. Copy the repository URL"
echo "3. Run these commands:"
echo ""
echo "   git remote add origin YOUR_GITHUB_REPO_URL"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Go to https://streamlit.io/cloud"
echo "5. Sign in with GitHub"
echo "6. Click 'New app' and select your repository"
echo "7. Set main file path to: main.py"
echo "8. Click 'Deploy!'"
echo ""
echo "🎉 Your app will be live in 5-10 minutes!"
echo ""



