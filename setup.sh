#!/bin/bash
# Setup script for Streamlit Cloud deployment

# Download spaCy English model if not present
python -m spacy download en_core_web_sm || echo "Model download failed, will try during runtime"

