import json
import os
import sys
import subprocess

def fetch_all(manifest_path, output_root):
    with open(manifest_path, 'r') as f:
        data = json.load(f)
    
    artifacts = data.get("artifacts", {})
    
    for category, items in artifacts.items():
        # Create folder for each category: artifacts/sectors/
        category_dir = os.path.join(output_root, category)
        os.makedirs(category_dir, exist_ok=True)
        
        for name, version in items.items():
            # Parse repo name from artifact name (convention: repo-name-artifact)
            # Heuristic: "novatrade-api" -> Repo "novatrade"
            # This might need mapping logic if names diverge
            repo_name = name.rsplit('-', 1)[0] 
            
            print(f"⬇️ Downloading {name} ({version})...")
            
            # Re-use the single artifact fetcher logic via subprocess
            # Or import the function if refactored
            cmd = [
                "python3", "scripts/fetch_artifact.py",
                "--repo", repo_name,
                "--tag", version,
                "--artifact", f"{name}.tar.gz",
                "--output-dir", category_dir
            ]
            
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError:
                print(f"❌ Failed to download {name}. Validation Failed.")
                sys.exit(1)

if __name__ == "__main__":
    fetch_all("candidate-manifest.json", "artifacts_cache")