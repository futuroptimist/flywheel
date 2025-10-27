import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

import { formatSpinMarkdown, type SpinDryRunResult, __private__ } from '../../ts-cli/spin.js';

describe('formatSpinMarkdown', () => {
  it('renders markdown table with suggestions', () => {
    const result: SpinDryRunResult = {
      target: '/repo',
      mode: 'dry-run',
      stats: {
        total_files: 5,
        has_readme: true,
        has_docs: false,
        has_ci_workflows: true,
        has_tests: false,
        has_lint_config: null,
        dependency_health: { status: 'warn' },
        language_mix: [
          { language: 'Python', count: 3 },
          { language: 'TypeScript', count: 1 },
        ],
      },
      suggestions: [
        {
          id: 'commit-lockfiles',
          category: 'chore',
          impact: 'medium',
          confidence: 0.75,
          title: 'Commit lockfiles',
          files: ['package.json'],
        },
      ],
    };

    const markdown = formatSpinMarkdown(result);

    const expected = [
      '# flywheel spin dry-run',
      '',
      '- Target: `/repo`',
      '- Mode: `dry-run`',
      '- total_files: 5',
      '- has_readme: yes',
      '- has_docs: no',
      '- has_ci_workflows: yes',
      '- has_tests: no',
      '- has_lint_config: skipped',
      '- dependency_health: warn',
      '- language_mix: Python (3), TypeScript (1)',
      '',
      '| # | Id | Category | Impact | Confidence | Title | Files |',
      '| --- | --- | --- | --- | --- | --- | --- |',
      '| 1 | commit-lockfiles | chore | medium | 0.75 | Commit lockfiles | package.json |',
    ].join('\n');

    assert.equal(markdown, expected);
  });

  it('renders placeholder when suggestions are empty', () => {
    const result: SpinDryRunResult = {
      target: 'repo',
      mode: 'dry-run',
      stats: {
        total_files: 2,
        has_readme: false,
        has_docs: true,
        has_ci_workflows: false,
        has_tests: true,
        has_lint_config: true,
        dependency_health: null,
      },
      suggestions: [],
    };

    const markdown = formatSpinMarkdown(result);

    assert.ok(markdown.includes('_No suggestions found._'));
    assert.ok(markdown.includes('- has_docs: yes'));
  });
});

describe('formatConfidence', () => {
  const { formatConfidence } = __private__;

  it('returns dash for NaN values', () => {
    assert.equal(formatConfidence(Number.NaN), '-');
  });

  it('formats finite numbers to two decimals', () => {
    assert.equal(formatConfidence(0.5), '0.50');
  });
});
