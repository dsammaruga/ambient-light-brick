# Ambient Light brick

Sample brick for Arduino App Lab, used to test the App Bricks registry submission flow.

- `bricks/ambient_light/`: the brick (`__init__.py`, `brick_config.yaml`, `README.md`)
- `bricks/ambient_light/examples/basic/`: an App Lab app using it

Each release is a submittable version: the zip attached to it holds this repository tree. Build it with `scripts/package_brick.sh` of the registry (or `git archive --format=zip HEAD`) and submit the asset URL with its SHA-256.
