#!/usr/bin/env bash
set -euo pipefail

required_environment=(
  RUNTIME_PROPERTIES_BASE64
  KEYSTORE_BASE64
  STORE_PASSWORD
  KEY_ALIAS
  KEY_PASSWORD
  RUNNER_TEMP
)

for variable_name in "${required_environment[@]}"; do
  if [[ -z "${!variable_name:-}" ]]; then
    echo "Missing required release environment value: ${variable_name}" >&2
    exit 1
  fi
done

output_properties="${OUTPUT_PROPERTIES:-local.properties}"
keystore_path="${RUNNER_TEMP%/}/nuviodv-release.jks"
runtime_properties="$(mktemp "${RUNNER_TEMP%/}/nuviodv-runtime-properties.XXXXXX")"
sanitized_properties="$(mktemp "${RUNNER_TEMP%/}/nuviodv-sanitized-properties.XXXXXX")"
trap 'rm -f "${runtime_properties}" "${sanitized_properties}"' EXIT

printf '%s' "${RUNTIME_PROPERTIES_BASE64}" | base64 --decode > "${runtime_properties}"
printf '%s' "${KEYSTORE_BASE64}" | base64 --decode > "${keystore_path}"

if [[ ! -s "${runtime_properties}" ]]; then
  echo 'Decoded runtime properties are empty.' >&2
  exit 1
fi
if [[ ! -s "${keystore_path}" ]]; then
  echo 'Decoded release keystore is empty.' >&2
  exit 1
fi

sed -E '/^[[:space:]]*(sdk\.dir|NUVIO_RELEASE_STORE_FILE|NUVIO_RELEASE_STORE_PASSWORD|NUVIO_RELEASE_KEY_ALIAS|NUVIO_RELEASE_KEY_PASSWORD)[[:space:]]*=/d' \
  "${runtime_properties}" > "${sanitized_properties}"

required_runtime_properties=(
  NUVIO_SUPABASE_URL
  NUVIO_SUPABASE_ANON_KEY
  NUVIO_SUPABASE_FALLBACK_URL
  TRAKT_CLIENT_ID
  TRAKT_CLIENT_SECRET
  SIMKL_CLIENT_ID
)

for property_name in "${required_runtime_properties[@]}"; do
  if ! grep -Eq "^${property_name}=[^[:space:]].*$" "${sanitized_properties}"; then
    echo "Missing required runtime property: ${property_name}" >&2
    exit 1
  fi
done

cp "${sanitized_properties}" "${output_properties}"
{
  printf '\nNUVIO_RELEASE_STORE_FILE=%s\n' "${keystore_path}"
  printf 'NUVIO_RELEASE_STORE_PASSWORD=%s\n' "${STORE_PASSWORD}"
  printf 'NUVIO_RELEASE_KEY_ALIAS=%s\n' "${KEY_ALIAS}"
  printf 'NUVIO_RELEASE_KEY_PASSWORD=%s\n' "${KEY_PASSWORD}"
} >> "${output_properties}"

chmod 600 "${output_properties}" "${keystore_path}"

echo 'Authenticated NuvioDV release properties configured.'
