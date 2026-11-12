# Ambient Light brick

Sample brick for Arduino App Lab, used to test the App Bricks registry submission flow.

```
src/ambient_light/          the brick module: __init__.py, brick_config.yaml, README.md (the brick documentation),
                            requirements.txt (paho-mqtt), brick_compose.yaml (MQTT broker)
examples/basic/             an App Lab app printing the readings
examples/mqtt-monitor/      an App Lab app receiving the readings through MQTT
docs/api.md                 the API the brick provides
LICENSE                     MPL-2.0
.github/workflows/release.yml   the registry release workflow, copied from templates/release.yml
```

Each release is a submittable version. Publish a release whose tag equals `version` in `src/ambient_light/brick_config.yaml` (from the GitHub UI or `gh release create <version> --generate-notes`): the [release workflow](.github/workflows/release.yml) builds the zip of the repository tree at the tag, checks it with the rules of the registry bot, attaches it to the release and appends to the release notes a link to the catalog submission form already filled in.
