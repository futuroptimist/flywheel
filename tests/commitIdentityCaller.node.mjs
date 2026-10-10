import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

test('thin caller pins workflow and checker to the same immutable revision with opt-in delivery', () => {
  const caller = readFileSync(
    new URL('../.github/workflows/commit-identity.yml', import.meta.url),
    'utf8'
  );
  const workflowSha = caller.match(
    /uses: futuroptimist\/flywheel\/\.github\/workflows\/commit-identity-reusable.yml@([a-f0-9]{40})\s/
  )[1];
  const checkerSha = caller.match(/checker_sha: '([a-f0-9]{40})'/)[1];
  assert.equal(checkerSha, workflowSha);
  assert.ok(!caller.includes('secrets: inherit'));
  assert.ok(!caller.includes('contents: write'));
  assert.ok(!caller.includes('pull-requests: write'));
  assert.ok(caller.includes("vars.COMMIT_IDENTITY_SLACK_ENABLED == 'true'"));
  assert.ok(caller.includes('options: [mismatch, benign]'));
  assert.ok(caller.includes('default: benign'));
  assert.ok(caller.includes('default: false'));
  assert.ok(caller.includes('workflow_dispatch:'));
});
