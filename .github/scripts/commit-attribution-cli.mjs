import { readFile } from 'node:fs/promises';
import { policyEntries } from './commit-identity.mjs';
import {
  metadataClient,
  scan,
  publicReporter,
} from './commit-attribution-scanner.mjs';

const emit = publicReporter();
async function main() {
  const args = process.argv.slice(2);
  // No default activation, no arbitrary endpoints, no CLI-supplied credentials.
  if (args.length !== 1 || args[0] !== '--dry-run') {
    emit('COVERAGE_INVALID_POLICY');
  } else {
    const config = JSON.parse(
      await readFile(
        new URL('../commit-attribution-scan.json', import.meta.url)
      )
    );
    const policy = JSON.parse(
      await readFile(new URL('../commit-identity-policy.json', import.meta.url))
    );
    const entries = policyEntries(policy, config.reviewedPolicyRepository);
    // Dry run is bounded, read-only and ephemeral: it reports baseline/visibility gaps.
    // Persistent prospective scanning is a library operation requiring separate activation.
    const store = { load: async () => null, save: async () => {} };
    await scan({
      get: metadataClient(process.env.GITHUB_TOKEN, config),
      entries,
      config,
      store,
      emit,
    });
  }
}
main().catch(() => emit('COVERAGE_UNEXPECTED_ERROR'));
