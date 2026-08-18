#!/usr/bin/env sh
set -eu

plan="docs/RELEASE_PLAN.md"
test -f "$plan"

milestones="$(grep -Ec '^## v0\.[0-9]+\.0 — ' "$plan")"
goals="$(grep -c '^Goal:$' "$plan")"
deliverables="$(grep -c '^Deliverables:$' "$plan")"
verification="$(grep -c '^Verification:$' "$plan")"
exit_criteria="$(grep -c '^Exit criteria:$' "$plan")"
stops="$(grep -Ec '^- v(0\.[0-9]+\.0|1\.0\.0) implementation stop reached\. Run pentest for this exact commit\.$' "$plan")"

test "$milestones" -eq 200
test "$goals" -eq 201
test "$deliverables" -eq 201
test "$verification" -eq 201
test "$exit_criteria" -eq 201
test "$stops" -eq 201

number=1
while [ "$number" -le 200 ]; do
    grep -q "^## v0\.${number}\.0 — " "$plan"
    number=$((number + 1))
done

grep -q '^## v1\.0\.0 — Serious production release$' "$plan"
