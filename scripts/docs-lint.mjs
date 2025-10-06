import { readdir, readFile } from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

async function collectMarkdown(dir) {
  const entries = await readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === 'node_modules' || entry.name === 'docs-site') {
        continue;
      }
      files.push(...(await collectMarkdown(full)));
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      files.push(full);
    }
  }
  return files;
}

function countPipes(line) {
  return (line.match(/\|/g) || []).length;
}

function lintLines(lines) {
  const issues = [];
  let fence = null;
  let expectedPipes = null;
  for (let idx = 0; idx < lines.length; idx += 1) {
    const raw = lines[idx];
    const trimmed = raw.trim();
    if (trimmed.startsWith('```') || trimmed.startsWith('~~~')) {
      const marker = trimmed.slice(0, 3);
      if (!fence) {
        fence = marker;
      } else if (trimmed.startsWith(fence)) {
        fence = null;
      }
      continue;
    }
    if (fence) {
      continue;
    }
    if (trimmed.startsWith('|')) {
      const pipes = countPipes(raw);
      if (expectedPipes === null) {
        expectedPipes = pipes;
      } else if (pipes !== expectedPipes) {
        issues.push({
          line: idx + 1,
          message: `Expected ${expectedPipes} pipe characters but found ${pipes}.`,
        });
      }
    } else {
      expectedPipes = null;
    }
  }
  return issues;
}

async function lintFile(file) {
  const text = await readFile(file, 'utf8');
  const lines = text.split(/\r?\n/);
  return lintLines(lines).map((issue) => ({ ...issue, file }));
}

async function main() {
  const targets = [path.join(ROOT, 'README.md')];
  const docsDir = path.join(ROOT, 'docs');
  targets.push(...(await collectMarkdown(docsDir)));
  targets.sort();

  const problems = [];
  for (const file of targets) {
    const issues = await lintFile(file);
    problems.push(...issues);
  }

  if (problems.length > 0) {
    console.error('Docs lint failed: inconsistent table pipes detected.');
    for (const issue of problems) {
      console.error(` - ${path.relative(ROOT, issue.file)}:${issue.line} ${issue.message}`);
    }
    process.exitCode = 1;
    return;
  }

  console.log('Docs lint passed: table pipes look consistent.');
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });
}
