# AI Image to 3D Model Workflow

This repository contains an automated workflow to generate 3D models from images using AI and Blender.

## How it Works

1.  **Upload Image**: Place your image (e.g., a mannequin or turnaround sheet) in the `images/` directory.
2.  **Trigger Workflow**: Go to the **Actions** tab in this repository.
3.  **Run Workflow**: Select "Image to 3D Model Generation" and click "Run workflow". Provide the path to your image (e.g., `images/my_image.png`).
4.  **AI Generation**: The workflow uses GitHub Models (GPT-4o) to generate a 3D OBJ mesh representation.
5.  **Blender Processing**: Blender processes the mesh, applies smoothing, and exports it as a high-quality `.glb` file.
6.  **Output**: The final 3D model will be pushed to the `output/` directory in this repository.

## Requirements

-   A GitHub Personal Access Token (PAT) with `workflow` and `repo` permissions (stored as `GITHUB_TOKEN` in secrets).
-   GitHub Models access (Public Preview).

## Directory Structure

-   `.github/workflows/`: Contains the automation pipeline.
-   `scripts/`: Python scripts for AI generation and Blender processing.
-   `images/`: Place your input images here.
-   `output/`: Generated 3D models will appear here.

## Example Image
The workflow is optimized for simple mannequin-like images or turnaround sheets.

---
*Created by Manus AI*
