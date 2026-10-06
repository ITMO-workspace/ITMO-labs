#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

JAR="server/target/server-1.0-SNAPSHOT.jar"
if [[ ! -f "$JAR" ]]; then
  echo "Server jar not found. Run ./build.sh first." >&2
  exit 1
fi

exec java -jar "$JAR"
