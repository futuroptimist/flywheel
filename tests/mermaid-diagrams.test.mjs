import { readFileSync } from 'node:fs';

test('mermaid diagrams in docs/flywheel-physics.md have no backslashes', () => {
  const md = readFileSync(
    new URL('../docs/flywheel-physics.md', import.meta.url),
    'utf8'
  );
  const blocks = [...md.matchAll(/```mermaid\n([\s\S]*?)```/g)];
  for (const [, diagram] of blocks) {
    expect(diagram).not.toMatch(/\\/);
  }
});
