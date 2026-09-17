# Migrating the MinIO object store to Garage

Repo-specific companion to the [team migration guide](https://codimd.adfinis.com/oZ882KFbSmO9C6bqZeAq6g?edit).

## Deviation from the team guide: the S3 region

The team guide specifies `s3_region = "garage"` together with Caluma >= v12.2.4, which added `MINIO_STORAGE_REGION_NAME`.
Since we are <12, the caluma s3 client probes `GetBucketLocation` signed with the SigV4 default region, and Garage rejects any scope that does not match its configured region with `AuthorizationHeaderMalformed`.

So `garage/garage.toml` sets `s3_region = "us-east-1"` instead. That is what the MinIO it replaces reported: `MINIO_SITE_REGION` was never set in any environment, so MinIO fell back to its default of `us-east-1` and additionally accepted any region a client signed with. The Garage setting therefore reproduces the previous behaviour exactly.

**When Caluma is upgraded to >= 12.2.4**, switch `s3_region` to `garage` and add `MINIO_STORAGE_REGION_NAME=garage` to the `.caluma` env files, in one change. Until then, do not "fix" the region to match the guide: it will break every upload and download.

## Corrections to the team guide

Found while running this migration, worth folding back into the team guide:

* Its `garage.toml` sets `metadata_dir = "/tmp/meta"` and `data_dir = "/tmp/data"`. Those come from the Garage quickstart, which warns they are wiped on reboot. On a productive system that is total object loss on the first restart. This repo uses `/var/lib/garage/{meta,data}` on named volumes.
* The rclone config mount path `/root/.rclone.config` is wrong. The `rclone/rclone` image reads `/config/rclone/rclone.conf`; with the documented path rclone silently falls back to defaults and fails with "didn't find section in config file". The commands below use the working path.
* The `docker run` examples write `-network`, which should be `--network`.
* The `entrypoint.sh` approach for node layout, key import and bucket creation is obsolete as of Garage v2.3. `server --single-node --default-bucket` with `GARAGE_DEFAULT_ACCESS_KEY`, `GARAGE_DEFAULT_SECRET_KEY` and `GARAGE_DEFAULT_BUCKET` does all three on first start, which is what this repo uses. The linked PoC entrypoint.sh 404s.

## What is being migrated

The `caluma-media` bucket, holding Caluma file answers, i.e. documents applicants attach to a form, plus the historical revisions Caluma keeps when a file is replaced. Caluma is the only service using object storage: the API has no S3 configuration, and document-merge-service keeps its templates in the separate `templatefiles` volume.

Uploads and downloads go straight from the browser to the object store via presigned URLs through Caddy on `/caluma-media*`, never through Django.

---

## Phase 1: preparation and sidecar (this change)

Garage runs alongside MinIO. MinIO stays the source of truth and Caluma keeps pointing at it. Nothing user-visible changes.

Already contained in this change:

* `garage` service in `compose.yaml`, plus `garage_meta` and `garage_data` volumes
* `garage/garage.toml`
* `.envs/.<env>/.garage`, and `.garage` wired up in the per-environment compose files
* `minio` and `mc` images repointed to `quay.io`. The public `minio/minio` and `minio/mc` repos on Docker Hub are gone, so the original references fail with `pull access denied`, and without this the sidecar phase cannot deploy on a host that has not cached them. MinIO images are still obtainable: quay.io serves them and is still publishing hotfix rebuilds (the pinned `RELEASE.2025-04-22T22-12-26Z` has one from March 2026), and Docker offers a hardened AGPLv3 build via [Docker Hardened Images](https://hub.docker.com/hardened-images/catalog/dhi/minio), which needs a DHI entitlement. Plain community releases stopped at `RELEASE.2025-09-07T16-13-09Z`, so the edition is unmaintained rather than unavailable. Switch to a hotfix tag or DHI if the migration window is long enough to care about CVEs.

The plan is to reuse the existing MinIO credentials as the Garage key, so that `.envs/.production/.caluma` needs no edit at all and phase 2 touches only the proxy. **Check first that the existing secret is long enough**, because Garage enforces a minimum that MinIO does not:

```bash
awk -F= '/^MINIO_ROOT_PASSWORD=/{print length($2)" chars"}' .envs/.production/.minio
```

Garage requires an access key of at least 8 characters from `[A-Za-z0-9-_.]` and a secret of at least **16** printable ASCII characters. Below that it refuses to start, with `Invalid default access key: Secret keys should be at least 16 characters long`. If the secret is shorter, reuse is off: generate a fresh pair and edit `.caluma` in phase 2 after all.

This is already the case for local development, where `mysagw-minio123` is 15 characters. `.envs/.local/.garage` therefore keeps its own key, and `.envs/.local/.caluma` does need the phase 2 edit.

### Prerequisite: create `.garage` on every server before merging

**Do this first, on each server, before the phase 1 MR is merged.** The MR adds `env_file: ./.envs/.<env>/.garage` to the per-environment compose file. Compose aborts the entire invocation when an `env_file` is missing, every service and not just Garage, so merging ahead of this file takes the environment down on the next deploy:

```
env file /srv/mysagw/.envs/.production/.garage not found: no such file or directory
```

Run this on the host, in the checkout directory. It is a heredoc so the `openssl` calls are evaluated as it writes; pasting those commands into the file as literal text would leave Garage failing with `Invalid RPC secret key: expected 32 bytes of random hex`, because `env_file` performs no shell substitution.

```bash
# substitute the two credential values from .envs/.production/.caluma first
cat > .envs/.production/.garage <<EOF
GARAGE_RPC_SECRET=$(openssl rand -hex 32)
GARAGE_DEFAULT_ACCESS_KEY=<existing MINIO_STORAGE_ACCESS_KEY>
GARAGE_DEFAULT_SECRET_KEY=<existing MINIO_STORAGE_SECRET_KEY>
GARAGE_DEFAULT_BUCKET=caluma-media
GARAGE_ADMIN_TOKEN=$(openssl rand -base64 32)
GARAGE_METRICS_TOKEN=$(openssl rand -base64 32)
EOF
```

Check that the generated values came out as real secrets and not as literal command text:

```bash
grep -E '^(GARAGE_RPC_SECRET|GARAGE_ADMIN_TOKEN|GARAGE_METRICS_TOKEN)=' .envs/.production/.garage
```

Note that `MINIO_STORAGE_ACCESS_KEY` and `MINIO_STORAGE_SECRET_KEY` in `.caluma` are the same pair as `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` in `.minio`: MinIO's root credentials were used directly as the S3 credentials, with no separate IAM user. Reusing them means Caluma keeps authenticating with exactly the credentials it already has.

Deploy, then confirm Garage came up and created its bucket:

```bash
docker compose up -d garage
docker compose exec garage /garage status
docker compose exec garage /garage bucket info caluma-media
```

### Initial bulk copy

With both stores running and the system live. Create `garage/rclone.conf` (gitignored, contains secrets):

```toml
[minio]
type = s3
provider = Other
env_auth = false
access_key_id = <MINIO_ACCESS_KEY>
secret_access_key = <MINIO_SECRET_KEY>
endpoint = http://minio:9000

[garage]
type = s3
provider = Other
env_auth = false
region = us-east-1
access_key_id = <GARAGE_ACCESS_KEY>
secret_access_key = <GARAGE_SECRET_KEY>
endpoint = http://garage:3900
```

Note `region = us-east-1`, not `garage`, per the deviation above.

```bash
docker run --rm --network mysagw_default \
    -v ./garage/rclone.conf:/config/rclone/rclone.conf \
    rclone/rclone copy minio:caluma-media garage:caluma-media --progress
```

---

## Phase 2: data migration and switch-over

Arrange downtime with the customer. It only needs to cover the final sync and the restart, not the bulk copy.

Changes in this phase:

* `.envs/.production/.caluma`: **no edit**, assuming the MinIO credentials were reused as the Garage key in phase 1. Caluma keeps the credentials it already has and simply reaches a different server. Only if the secret was too short for Garage does this file need the new pair.
* `caddy/Caddyfile`: the change is already staged there, commented out under a `STEP 2 GARAGE MIGRATION` marker. Delete the two `minio:9000` lines and uncomment the `garage:3900` one. The `/minio/*` console route is dropped rather than ported, since Garage has no web console.

Leave the `minio` service declared in compose. It is the rollback.

```bash
# 1. stop the only writer. Caluma is the sole service using the bucket, so
#    stopping it is what freezes MinIO; nothing else can write to it.
docker compose stop caluma

# 2. final, delete-aware sync
docker run --rm --network mysagw_default \
    -v ./garage/rclone.conf:/config/rclone/rclone.conf \
    rclone/rclone sync minio:caluma-media garage:caluma-media --progress

# 3. verify by checksum, not by counting
docker run --rm --network mysagw_default \
    -v ./garage/rclone.conf:/config/rclone/rclone.conf \
    rclone/rclone check minio:caluma-media garage:caluma-media
```

`check` must report `0 differences found`. Use `sync`, not `copy`, for the final pass: it removes objects from Garage that were deleted in MinIO during the bulk window, which `copy` would leave behind.

Step 4 is deploying the changes in `caddy/Caddyfile` and `.envs/.<env>/.caluma` (only if new secret needed)

```bash
# 5. pick up the new proxy route and S3 credentials
docker compose up -d caddy caluma

# 6. stop MinIO, but do not remove it or its volume. It is the rollback.
docker compose stop minio mc
```

Test: open a case with an attachment, download it, upload a new one, confirm both work.

## Phase 3: clean-up

Only after phase 2 is verified and has run in production for a while.

* remove the `minio` and `mc` services from `compose.yaml` and from the per-environment compose files
* remove the `minio_data_snsd` volume declaration
* remove `.envs/.<env>/.minio`
* remove `garage/rclone.conf` and any MinIO secrets from CI

```bash
docker compose up -d --remove-orphans
docker volume rm mysagw_minio_data_snsd
```
## Rollback

MinIO is the source of truth until phase 2 is verified. To roll back, revert the phase 2 change so Caddy and Caluma point at MinIO again, then:

```bash
docker compose up -d minio mc caddy caluma
```

The MinIO volume is untouched until phase 3, so nothing is lost. Anything uploaded to Garage after the cutover is not in MinIO, so roll back promptly or sync it back first.
