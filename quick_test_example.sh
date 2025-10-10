#!/bin/bash
# Quick test example for Plane Python SDK
# This is a simple wrapper script to run the test with environment variables

# Configuration - UPDATE THESE VALUES
BASE_URL="https://api.plane.so"
WORKSPACE_SLUG="your-workspace-slug"
API_KEY="your-api-key-here"
# Alternatively, use ACCESS_TOKEN instead of API_KEY:
# ACCESS_TOKEN="your-access-token-here"

# Run the test
echo "Running Plane Python SDK Test..."
echo "================================"
echo ""

BASE_URL="$BASE_URL" \
WORKSPACE_SLUG="$WORKSPACE_SLUG" \
API_KEY="$API_KEY" \
python test_sdk.py

# If you're using ACCESS_TOKEN instead of API_KEY, use this:
# BASE_URL="$BASE_URL" \
# WORKSPACE_SLUG="$WORKSPACE_SLUG" \
# ACCESS_TOKEN="$ACCESS_TOKEN" \
# python test_sdk.py

