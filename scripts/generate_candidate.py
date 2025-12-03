import json
import os
import sys
import requests

# Configuration
RELEASES_REPO = "novaeco-tech/ecosystem-releases"
MANIFEST_PATH = "release-manifest.json"
BRANCH = "main"

def get_current_manifest(token):
    """Fetches the current stable manifest from ecosystem-releases."""
    url = f"https://api.github.com/repos/{RELEASES_REPO}/contents/{MANIFEST_PATH}?ref={BRANCH}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.raw"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to fetch manifest: {response.text}")
        sys.exit(1)
    return response.json()

def update_manifest(manifest, component_key, new_version, category):
    """Updates the specific artifact version."""
    
    # 1. Check if category exists
    if category not in manifest["artifacts"]:
        print(f"❌ Category '{category}' not found in manifest.")
        sys.exit(1)

    # 2. Check if component exists (or if we allow adding new ones)
    # For safety, we usually only update existing ones unless specified
    if component_key not in manifest["artifacts"][category]:
        print(f"⚠️ Component '{component_key}' not found. Adding new entry.")
    
    old_version = manifest["artifacts"][category].get(component_key, "NEW")
    
    # 3. Update
    manifest["artifacts"][category][component_key] = new_version
    
    print(f"✅ Updated {component_key}: {old_version} -> {new_version}")
    return manifest

if __name__ == "__main__":
    # Usage: python generate_candidate.py <json_payload>
    # Payload format: {"component": "novaagro-api", "version": "v1.2.0", "category": "sectors"}
    
    if len(sys.argv) < 2:
        print("Error: Missing payload argument")
        sys.exit(1)

    payload = json.loads(sys.argv[1])
    token = os.environ.get("GITHUB_TOKEN")

    print("🔍 Fetching baseline manifest...")
    manifest = get_current_manifest(token)
    
    print(f"🛠️ Patching candidate...")
    new_manifest = update_manifest(
        manifest, 
        payload["component"], 
        payload["version"], 
        payload["category"]
    )
    
    # Save locally for the next pipeline step
    with open("candidate-manifest.json", "w") as f:
        json.dump(new_manifest, f, indent=2)
        
    print("💾 Saved candidate-manifest.json")