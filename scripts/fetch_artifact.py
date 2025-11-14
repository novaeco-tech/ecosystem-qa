# This file would be a Python script using requests and argparse to:

#     Take --repo, --tag, and --output-dir as arguments.

#     Get the GITHUB_TOKEN from environment variables.

#     Call the GitHub API: GET /repos/nova-ecosystem/{repo}/releases/tags/{tag}.

#     Iterate through the assets in the JSON response.

#     Find assets ending in .tar.gz.

#     Download each asset to the specified --output-dir.