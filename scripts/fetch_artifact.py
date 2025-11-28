import os
import argparse
import requests
import sys

def download_artifact(repo, tag, artifact_name, output_dir, token):
    print(f"Fetching {artifact_name} from {repo} @ {tag}...")
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 1. Get Release metadata
    url = f"https://api.github.com/repos/novaeco-tech/{repo}/releases/tags/{tag}"
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"Error fetching release: {r.text}")
        sys.exit(1)
        
    release_data = r.json()
    asset_url = None
    
    # 2. Find the specific asset url
    for asset in release_data.get("assets", []):
        if asset["name"] == artifact_name:
            asset_url = asset["url"]
            break
            
    if not asset_url:
        print(f"Artifact '{artifact_name}' not found in release.")
        sys.exit(1)

    # 3. Download the asset
    headers["Accept"] = "application/octet-stream"
    r = requests.get(asset_url, headers=headers, stream=True)
    
    # Force the filename to 'artifact.tar.gz' so the Dockerfile can find it
    out_path = os.path.join(output_dir, "artifact.tar.gz")
    
    with open(out_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
            
    print(f"Downloaded to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN env var missing")
        sys.exit(1)
        
    download_artifact(args.repo, args.tag, args.artifact, args.output_dir, token)