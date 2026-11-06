# Ambient Light brick

Sample brick for Arduino App Lab, used to test the App Bricks registry submission flow.

- `bricks/ambient_light/`: the brick (`__init__.py`, `brick_config.yaml`, `README.md`)
- `bricks/ambient_light/examples/basic/`: an App Lab app using it

Each release is a submittable version. Publish a release whose tag equals `version` in `brick_config.yaml` (from the GitHub UI or `gh release create <version> --generate-notes`): the [release workflow](.github/workflows/release.yml) builds the zip of the repository tree at the tag, attaches it to the release and appends to the release notes the zip URL, the hash and a link to the catalog submission form already filled in.
