#!/bin/bash

ARTIFACT_PATH=$(realpath ./_site 2>/dev/null || echo "$(pwd)/_site")

echo "artifact_path=$ARTIFACT_PATH" >> $GITHUB_OUTPUT

echo "## GitHub Workflow Run ID: ${{ github.run_id }}" >> $GITHUB_STEP_SUMMARY
echo "## Absolute artifact path: $ARTIFACT_PATH" >> $GITHUB_STEP_SUMMARY

echo "Workflow Run ID: ${{ github.run_id }}"
echo "Artifact Absolute Path: $ARTIFACT_PATH"