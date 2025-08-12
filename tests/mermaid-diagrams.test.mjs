import { readFileSync } from 'node:fs';
import { describe, test, jest } from '@jest/globals';

// Stub dompurify for mermaid in Node
jest.unstable_mockModule('dompurify', () => ({
  default: { sanitize: (s) => s, addHook: () => {} }
}));

const mermaid = await import('mermaid');
mermaid.default.initialize({ startOnLoad: false });

function parse(code) {
  return mermaid.default.parse(code);
}

describe('mermaid diagrams in docs', () => {
  const doc = readFileSync('docs/flywheel-physics.md', 'utf8');
  const blocks = [...doc.matchAll(/```mermaid\n([\s\S]*?)```/g)].map(m => m[1]);
  blocks.forEach((code, idx) => {
    test(`diagram ${idx + 1} parses`, async () => {
      await parse(code);
    });
  });
});
