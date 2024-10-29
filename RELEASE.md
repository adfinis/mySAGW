# Release

Releases are automatically created. They follow the following pattern:

- `X.Y.Z` (e.g. `1.2.3`)
- `service-X.Y.Z` (e.g. `api-1.2.3`)

Once one or multiple commits are merged into main, the [`create-releases.yaml`](.github/workflows/create-releases.yaml) workflow will check if any versions (of services/the app) have been modified, if that is the case it will create a release following this pattern: `{{serviceName}}-{{newVersion}}` for services or `{{newVersion}}` for the application.

- `x-version` in `compose.yaml` (version of application)
- `tool.poetry.version` in `api/pyproject.toml` (version of api service)
- `caluma/version.txt` (version of caluma service)
- `.version` in `ember/package.json` (version of ember service)

When services are released the [`release.yaml`](.github/workflows/release.yaml) workflow will build && push them to the ghcr registry as `ghcr.io/adfinis/mysagw/{{serviceName}}`.

## Examples

### Fix in caluma

1. fix a bug in `/caluma`
2. adjust the version in `/caluma/version.txt` from `1.1.0` to `1.1.1`
3. push && merge
4. ci creates a tag called `caluma-1.1.1` and a release for it
5. ci builds and pushes container image to `ghcr.io/adfinis/mysagw/caluma:1.1.1`

### Feature in both API and Ember Frontend

1. add a feature and update both `api` and `ember`
2. `/api/pyproject.toml` from `1.1.1` to `1.2.0`
3. `/ember/package.jsom` from `1.0.6` to `1.1.0`
4. push && merge
5. ci creates tags: `api-1.2.0` and `ember-1.1.0`
6. ci builds and pushes images to `ghcr.io/adfinis/mysagw/api:1.2.0` and `ghcr.io/adfinis/mysagw/ember:1.1.0`

### Creating a release of the application

1. edit the `compose.yaml`
2. edit the `x-version` in `compose` from `1.2.3` to `1.3.0`
3. push && merge
4. ci creates tag `1.3.0`
