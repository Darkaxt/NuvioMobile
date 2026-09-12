#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
configure_script="${script_dir}/configure-nuviodv-release.sh"
test_root="$(mktemp -d)"

cleanup() {
  local resolved_root
  resolved_root="$(cd "${test_root}" && pwd -P)"
  case "${resolved_root}" in
    "${TMPDIR:-/tmp}"/tmp.*) rm -rf -- "${resolved_root}" ;;
    *) echo "Refusing to remove unexpected test directory: ${resolved_root}" >&2 ;;
  esac
}
trap cleanup EXIT

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

encode() {
  printf '%s' "$1" | base64 | tr -d '\r\n'
}

run_configure() {
  local runtime_properties="$1"
  local output_properties="$2"
  RUNTIME_PROPERTIES_BASE64="$(encode "${runtime_properties}")" \
    KEYSTORE_BASE64="$(encode 'test-keystore')" \
    STORE_PASSWORD='test-store-password' \
    KEY_ALIAS='test-key-alias' \
    KEY_PASSWORD='test-key-password' \
    RUNNER_TEMP="${test_root}" \
    OUTPUT_PROPERTIES="${output_properties}" \
    bash "${configure_script}"
}

complete_runtime_properties='NUVIO_SUPABASE_URL=https://primary.example.test
NUVIO_SUPABASE_ANON_KEY=test-anon-key
NUVIO_SUPABASE_FALLBACK_URL=https://fallback.example.test
TRAKT_CLIENT_ID=test-trakt-client
TRAKT_CLIENT_SECRET=test-trakt-secret
SIMKL_CLIENT_ID=test-simkl-client
sdk.dir=/must/not/survive
NUVIO_RELEASE_STORE_FILE=/must/not/survive.jks'

if [[ ! -f "${configure_script}" ]]; then
  fail "release configuration script is missing"
fi

if run_configure \
  $'NUVIO_SUPABASE_URL=https://primary.example.test\nNUVIO_SUPABASE_ANON_KEY=test-anon-key' \
  "${test_root}/incomplete.properties" >/dev/null 2>&1; then
  fail "incomplete runtime configuration was accepted"
fi

output_properties="${test_root}/complete.properties"
run_configure "${complete_runtime_properties}" "${output_properties}"

for expected in \
  'NUVIO_SUPABASE_URL=https://primary.example.test' \
  'NUVIO_SUPABASE_ANON_KEY=test-anon-key' \
  'NUVIO_SUPABASE_FALLBACK_URL=https://fallback.example.test' \
  'TRAKT_CLIENT_ID=test-trakt-client' \
  'TRAKT_CLIENT_SECRET=test-trakt-secret' \
  'SIMKL_CLIENT_ID=test-simkl-client' \
  "NUVIO_RELEASE_STORE_FILE=${test_root}/nuviodv-release.jks" \
  'NUVIO_RELEASE_STORE_PASSWORD=test-store-password' \
  'NUVIO_RELEASE_KEY_ALIAS=test-key-alias' \
  'NUVIO_RELEASE_KEY_PASSWORD=test-key-password'; do
  grep -Fqx "${expected}" "${output_properties}" || fail "missing expected property name: ${expected%%=*}"
done

if grep -Eq '^(sdk\.dir|NUVIO_RELEASE_STORE_FILE=/must/not/survive)' "${output_properties}"; then
  fail "unsafe runtime properties survived sanitization"
fi

[[ -s "${test_root}/nuviodv-release.jks" ]] || fail "keystore was not decoded"

echo 'PASS: authenticated NuvioDV release properties are validated and configured'
