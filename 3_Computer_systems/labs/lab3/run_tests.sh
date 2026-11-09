#!/usr/bin/env bash
# Runs the programs in src/ on wrench. Requires `wrench` (and optionally `wrench-fmt`) in PATH.
#
# Expected layout (this script lies next to src/):
#   src/<isa>.s                 program, <isa> in: acc32, f32a, m68k, risc-iv
#   src/<isa>.yaml              config with the assertions (optional)
#   src/tests/<isa>/*.yaml      extra test cases (optional)
#
# Usage: ./run_tests.sh [isa ...]     (no arguments -- all ISAs)
set -u
cd "$(dirname "$0")"

SRC=src
ALL_ISAS="acc32 f32a m68k risc-iv"
ISAS="${*:-$ALL_ISAS}"

# file prefix -> name of the ISA for wrench
wrench_isa() { [ "$1" = "risc-iv" ] && echo "risc-iv-32" || echo "$1"; }

if ! command -v wrench >/dev/null; then
    echo "wrench not found in PATH" >&2
    exit 2
fi

fail=0
ok=0

run() { # <source> <isa> <config>
    out=$(wrench "$1" --isa "$2" -c "$3" 2>&1)
    if [ $? -ne 0 ] || echo "$out" | grep -qiE "assertion fail|error"; then
        echo "FAIL  $3"
        echo "$out" | tail -12
        fail=$((fail + 1))
    else
        echo "ok    $3"
        ok=$((ok + 1))
    fi
}

for name in $ISAS; do
    file="$SRC/$name.s"
    isa=$(wrench_isa "$name")
    if [ ! -f "$file" ]; then
        echo "skip  $file (not found)"
        continue
    fi
    echo "== $name"

    if command -v wrench-fmt >/dev/null; then
        if wrench-fmt "$file" --isa "$isa" --check; then
            echo "ok    format $file"
        else
            echo "FAIL  format $file (run: wrench-fmt $file --isa $isa --inplace)"
            fail=$((fail + 1))
        fi
    fi

    [ -f "$SRC/$name.yaml" ] && run "$file" "$isa" "$SRC/$name.yaml"

    if [ -d "$SRC/tests/$name" ]; then
        for cfg in $(ls "$SRC/tests/$name"/*.yaml | sort -V); do
            run "$file" "$isa" "$cfg"
        done
    fi
done

echo
echo "passed: $ok, failed: $fail"
[ "$fail" -eq 0 ]