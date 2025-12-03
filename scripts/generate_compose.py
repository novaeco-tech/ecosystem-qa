import json
import sys

# Template for a single service entry
SERVICE_TEMPLATE = """
  {name}:
    image: {image}
    build:
      context: .
      dockerfile: environments/Dockerfile.{type}.template
      args:
        ARTIFACT_PATH: ./artifacts_cache/{category}/{artifact_file}
    environment:
      - PORT={port}
    ports:
      - "{port}:{port}"
"""

def generate(manifest_path):
    with open(manifest_path) as f:
        data = json.load(f)
        
    compose = "version: '3.8'\nservices:"
    
    # Load service registry (ports/types)
    with open("config/services.json") as f:
        registry = json.load(f)["artifacts"]

    for category, artifacts in data["artifacts"].items():
        for name, version in artifacts.items():
            if name not in registry:
                print(f"⚠️ Warning: {name} not in registry. Skipping.")
                continue
                
            config = registry[name]
            
            compose += SERVICE_TEMPLATE.format(
                name=name,
                image=f"ghcr.io/novaeco-tech/dev-{config['type']}:latest",
                type=config['type'], # python or node
                category=category,
                artifact_file=f"{name}.tar.gz",
                port=config.get("port", 80)
            )
            
    with open("docker-compose.yml", "w") as f:
        f.write(compose)

if __name__ == "__main__":
    generate(sys.argv[1])