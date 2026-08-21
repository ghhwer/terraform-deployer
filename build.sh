#!/usr/bin/env bash
# Build the tf-deployer Docker image.
#
# Default: public PyPI + official Poetry installer.
# Optional custom Artifactory / PyPI mirror: copy build.local.env.example to
# build.local.env (gitignored) or pass --url/--host on the CLI.
#
# Examples:
#   ./build.sh
#   ./build.sh --tag tf-deployer:dev
#   ./build.sh --url https://artifactory.example/simple/ --host artifactory.example
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

LOCAL_ENV_FILE="${LOCAL_ENV_FILE:-$SCRIPT_DIR/build.local.env}"

# Load local overrides first (never committed). CLI flags win afterward.
if [ -f "$LOCAL_ENV_FILE" ]; then
  # shellcheck disable=SC1090
  set -a
  # shellcheck disable=SC1091
  source "$LOCAL_ENV_FILE"
  set +a
fi

IMAGE_TAG="${IMAGE_TAG:-tf-deployer:latest}"
DOCKER="${DOCKER:-docker}"
USE_CUSTOM_PYPI="${USE_CUSTOM_PYPI:-false}"
CUSTOM_PYPI_URL="${CUSTOM_PYPI_URL:-}"
CUSTOM_PYPI_HOST="${CUSTOM_PYPI_HOST:-}"
CUSTOM_PYPI_NAME="${CUSTOM_PYPI_NAME:-custom}"

usage() {
  cat <<'EOF'
Usage: build.sh [options]

Build the tf-deployer Docker image.

Options:
  --custom-pypi       Use a custom PyPI/Artifactory index (from env / build.local.env)
  --tag TAG           Image tag (default: tf-deployer:latest)
  --url URL           Custom simple-index URL (implies custom index)
  --host HOST         Trusted host for the custom index
  --name NAME         Poetry source name (default: custom)
  -h, --help          Show this help

Local config (gitignored):
  build.local.env     Sourced automatically when present.
                      Copy from build.local.env.example.

Environment (also valid in build.local.env):
  IMAGE_TAG           Same as --tag
  DOCKER              Docker CLI (default: docker; e.g. "sudo docker")
  USE_CUSTOM_PYPI     true|false — enable custom index when URL/host are set
  CUSTOM_PYPI_URL     Custom index URL
  CUSTOM_PYPI_HOST    Trusted host
  CUSTOM_PYPI_NAME    Poetry source name
  LOCAL_ENV_FILE      Override path to the local env file
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --custom-pypi)
      USE_CUSTOM_PYPI=true
      shift
      ;;
    --tag)
      IMAGE_TAG="$2"
      shift 2
      ;;
    --url)
      CUSTOM_PYPI_URL="$2"
      USE_CUSTOM_PYPI=true
      shift 2
      ;;
    --host)
      CUSTOM_PYPI_HOST="$2"
      USE_CUSTOM_PYPI=true
      shift 2
      ;;
    --name)
      CUSTOM_PYPI_NAME="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

# If a local/env URL is set, treat that as opting into a custom index.
if [ -n "$CUSTOM_PYPI_URL" ] && [ -n "$CUSTOM_PYPI_HOST" ]; then
  USE_CUSTOM_PYPI=true
fi

# Normalize boolean
case "$USE_CUSTOM_PYPI" in
  1|true|TRUE|yes|YES) USE_CUSTOM_PYPI=true ;;
  *) USE_CUSTOM_PYPI=false ;;
esac

# shellcheck disable=SC2206
DOCKER_CMD=($DOCKER)

BUILD_ARGS=(
  --tag "$IMAGE_TAG"
  --build-arg "USE_CUSTOM_PYPI=$USE_CUSTOM_PYPI"
)

if [ "$USE_CUSTOM_PYPI" = "true" ]; then
  if [ -z "$CUSTOM_PYPI_URL" ] || [ -z "$CUSTOM_PYPI_HOST" ]; then
    echo "Custom PyPI requires CUSTOM_PYPI_URL and CUSTOM_PYPI_HOST (set in build.local.env or via --url/--host)." >&2
    exit 1
  fi
  BUILD_ARGS+=(
    --build-arg "CUSTOM_PYPI_URL=$CUSTOM_PYPI_URL"
    --build-arg "CUSTOM_PYPI_HOST=$CUSTOM_PYPI_HOST"
    --build-arg "CUSTOM_PYPI_NAME=$CUSTOM_PYPI_NAME"
  )
  echo "Building $IMAGE_TAG with custom PyPI ($CUSTOM_PYPI_NAME -> $CUSTOM_PYPI_URL)"
else
  echo "Building $IMAGE_TAG with public PyPI (no custom repository)"
fi

exec "${DOCKER_CMD[@]}" build "${BUILD_ARGS[@]}" .
