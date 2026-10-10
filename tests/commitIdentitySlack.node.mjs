import test from 'node:test';
import assert from 'node:assert/strict';
import {
  advise,
  digest,
  reporter,
} from '../.github/scripts/commit-identity.mjs';

const repository = 'futuroptimist/flywheel';
const sha = '1'.repeat(40);
const poison =
  'private@example.invalid\n::error::injected <!channel> https://evil.invalid';
const channel = 'C0123456789';
const slack = { enabled: true, channel, token: 'TEST credential' };
async function exercise({
  mode = 'mismatch',
  notify = 'true',
  config = slack,
  fetcher = async () => Response.json({ ok: true, channel }),
  options = {},
} = {}) {
  const lines = [];
  const calls = [];
  await advise(
    {
      repository,
      eventName: 'workflow_dispatch',
      event: {
        repository: { full_name: repository },
        inputs: { test_case: mode, notify },
      },
      get: () => {
        throw new Error('TEST must not read GitHub commits');
      },
      ...options,
      emit: reporter(repository, (line) => lines.push(line)),
    },
    config,
    async (url, request) => {
      calls.push({ url, request });
      return fetcher(url, request);
    }
  );
  assert.ok(
    lines.every((line) =>
      /^(::warning::)?futuroptimist\/flywheel ([a-f0-9]{40} )?[A-Z_]+\n$/.test(
        line
      )
    )
  );
  assert.ok(!lines.join('').includes('@'));
  assert.ok(!lines.join('').includes('::error::'));
  assert.ok(!lines.join('').includes('credential'));
  return { lines, calls };
}

test('manual mismatch is in memory and every alert has a TEST category', async () => {
  const { lines, calls } = await exercise();
  assert.equal(calls.length, 1);
  assert.equal(calls[0].url, 'https://slack.com/api/chat.postMessage');
  assert.equal(calls[0].request.redirect, 'error');
  assert.deepEqual(JSON.parse(calls[0].request.body), {
    channel,
    text: `${repository} ${sha} TEST_COMMITTER_IDENTITY_MISMATCH`,
    mrkdwn: false,
    parse: 'none',
    unfurl_links: false,
    unfurl_media: false,
  });
  assert.ok(lines.some((line) => line.endsWith('SLACK_DELIVERED\n')));
});

test('benign, disabled and dry dispatch controls never contact Slack', async () => {
  for (const args of [
    { mode: 'benign' },
    { config: {} },
    { config: { ...slack, enabled: 'true' } },
    { notify: 'false' },
    { notify: true },
  ]) {
    assert.equal((await exercise(args)).calls.length, 0);
  }
  assert.ok(
    (await exercise({ mode: 'benign' })).lines.some((line) =>
      line.endsWith('TEST_EXPECTED_COMMITTER\n')
    )
  );
});

test('invalid dispatch modes, repository and notification configuration are sanitized', async () => {
  for (const args of [
    { mode: poison },
    { options: { event: {} } },
    { config: { ...slack, channel: poison } },
    { config: { ...slack, channel: channel + '\n' } },
    { config: { ...slack, token: '' } },
  ]) {
    const { calls, lines } = await exercise(args);
    assert.equal(calls.length, 0);
    assert.ok(lines.some((line) => line.includes('COVERAGE_')));
  }
});

test('Slack errors, redirects, invalid UTF-8, oversized bodies and hostile errors stay warning-only', async () => {
  for (const fetcher of [
    async () => {
      throw new Error(poison);
    },
    async () => {
      throw {
        get message() {
          throw new Error(poison);
        },
      };
    },
    async () => new Response(poison, { status: 302 }),
    async () => new Response(poison, { status: 429 }),
    async () => new Response(poison),
    async () => new Response(new Uint8Array([0xc3, 0x28])),
    async () => new Response('x'.repeat(65537)),
    async () => Response.json({ ok: false, error: poison }),
    async () => Response.json({ ok: true, channel: poison }),
  ]) {
    const { lines } = await exercise({ fetcher });
    assert.ok(
      lines.some((line) => line.endsWith('COVERAGE_SLACK_UNAVAILABLE\n'))
    );
    assert.ok(!lines.some((line) => line.endsWith('SLACK_DELIVERED\n')));
  }
});

test('real inspection sends only validated mismatch metadata and leaves benign attribution alone', async () => {
  const policy = {
    version: 1,
    repositories: {
      [repository]: {
        committers: [
          {
            accountId: 42,
            login: 'reviewed',
            nameSha256: digest('TEST reviewed'),
            emailSha256: digest('test@example.invalid'),
          },
        ],
      },
    },
  };
  for (const mode of [
    'mismatch',
    'expected',
    'outside',
    'bot',
    'null',
    'malformed',
  ]) {
    const expected = mode === 'expected';
    const commit = {
      sha: mode === 'malformed' ? sha + '\n' : sha,
      author: { id: 999 },
      message: poison,
      committer:
        mode === 'null'
          ? null
          : {
              id: mode === 'outside' || mode === 'bot' ? 99 : 42,
              type: mode === 'bot' ? 'Bot' : 'User',
            },
      commit: {
        author: { name: poison, email: poison },
        message: poison,
        committer: {
          name: expected ? 'TEST reviewed' : poison,
          email: expected ? 'test@example.invalid' : poison,
        },
      },
    };
    const { calls } = await exercise({
      options: {
        eventName: 'push',
        policy,
        event: {
          repository: { full_name: repository },
          ref: 'refs/heads/' + poison,
          before: '0'.repeat(40),
          after: sha,
          created: true,
          deleted: false,
          forced: false,
        },
        get: async () => ({ data: commit, link: '' }),
      },
    });
    assert.equal(calls.length, mode === 'mismatch' ? 1 : 0);
    if (calls.length)
      assert.equal(
        JSON.parse(calls[0].request.body).text,
        `${repository} ${sha} COMMITTER_IDENTITY_MISMATCH`
      );
  }
});
