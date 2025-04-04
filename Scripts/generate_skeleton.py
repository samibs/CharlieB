import os

# Define the root project path
project_path = r"C:\Scripts\CharlieB"

# Define the folders to create
folders = [
    "CharlieB",
    "CharlieB/app",
    "CharlieB/app/frontend",
    "CharlieB/app/backend",
    "CharlieB/app/data",
    "CharlieB/app/backend/api",
    "CharlieB/app/backend/llm",
    "CharlieB/app/backend/utils",
    "CharlieB/.vscode",
]

# Create folders
for folder in folders:
    os.makedirs(os.path.join(project_path, os.path.relpath(folder, "CharlieB")), exist_ok=True)

"Skeleton folder structure created."
