export interface LanguageMixEntry {
  language?: string;
  count?: number;
}

export interface DependencyHealth {
  status?: string;
  missing_lockfiles?: string[];
  missing_manifests?: string[];
}

export interface SpinStats {
  total_files?: number;
  has_readme?: boolean | null;
  has_docs?: boolean | null;
  has_ci_workflows?: boolean | null;
  has_tests?: boolean | null;
  has_lint_config?: boolean | null;
  dependency_health?: DependencyHealth | string | null;
  language_mix?: LanguageMixEntry[];
}

export interface SpinSuggestion {
  id?: string;
  category?: string;
  impact?: string;
  confidence?: number | null;
  title?: string;
  files?: string[];
}

export interface SpinDryRunResult {
  target?: string;
  mode?: string;
  stats?: SpinStats;
  suggestions?: SpinSuggestion[];
}

function formatBool(value: boolean | null | undefined): string {
  if (value === true) {
    return 'yes';
  }
  if (value === false) {
    return 'no';
  }
  return 'skipped';
}

function formatLanguageMix(entries: LanguageMixEntry[] | undefined): string {
  if (!entries || entries.length === 0) {
    return 'none detected';
  }
  const parts = entries.map((entry) => {
    const language = entry.language ?? '';
    const count = entry.count ?? 0;
    return `${language} (${count})`;
  });
  return parts.join(', ');
}

function formatConfidence(value: number | null | undefined): string {
  if (typeof value !== 'number' || Number.isNaN(value) || !Number.isFinite(value)) {
    return '-';
  }
  return value.toFixed(2);
}

function formatStatsLines(stats: SpinStats | undefined): string[] {
  const safeStats = stats ?? {};
  const lines: string[] = [];
  const totalFiles = typeof safeStats.total_files === 'number' ? safeStats.total_files : 0;
  lines.push(`  - total_files: ${totalFiles}`);
  lines.push(`  - has_readme: ${formatBool(safeStats.has_readme ?? null)}`);
  lines.push(`  - has_docs: ${formatBool(safeStats.has_docs ?? null)}`);
  lines.push(
    `  - has_ci_workflows: ${formatBool(safeStats.has_ci_workflows ?? null)}`,
  );
  lines.push(`  - has_tests: ${formatBool(safeStats.has_tests ?? null)}`);
  lines.push(`  - has_lint_config: ${formatBool(safeStats.has_lint_config ?? null)}`);

  const dependency = safeStats.dependency_health;
  let dependencyStatus = 'skipped';
  if (dependency && typeof dependency === 'object' && !Array.isArray(dependency)) {
    dependencyStatus = String(dependency.status ?? 'unknown');
  } else if (typeof dependency === 'string') {
    dependencyStatus = dependency;
  }
  lines.push(`  - dependency_health: ${dependencyStatus}`);

  const mix = Array.isArray(safeStats.language_mix) ? safeStats.language_mix : [];
  lines.push(`  - language_mix: ${formatLanguageMix(mix)}`);
  return lines;
}

function escapeMarkdown(text: string): string {
  return text.replace(/\\|\|/g, (char) => `\\${char}`).replace(/\n/g, ' ');
}

export function formatSpinMarkdown(result: SpinDryRunResult): string {
  const statsLines = formatStatsLines(result.stats);
  const lines: string[] = [
    '# flywheel spin dry-run',
    '',
    `- Target: \`${result.target ?? ''}\``,
    `- Mode: \`${result.mode ?? ''}\``,
  ];
  const convertedStats = statsLines.map((line) => line.replace('  -', '-', 1));
  lines.push(...convertedStats);
  lines.push('');

  const suggestions = Array.isArray(result.suggestions) ? result.suggestions : [];
  if (suggestions.length === 0) {
    lines.push('_No suggestions found._');
    return lines.join('\n');
  }

  const headers = ['#', 'Id', 'Category', 'Impact', 'Confidence', 'Title', 'Files'];
  lines.push(`| ${headers.join(' | ')} |`);
  lines.push(`| ${headers.map(() => '---').join(' | ')} |`);

  suggestions.forEach((suggestion, index) => {
    const files = suggestion.files && suggestion.files.length > 0
      ? suggestion.files.join(', ')
      : '-';
    const cells = [
      String(index + 1),
      escapeMarkdown(suggestion.id ?? '-') || '-',
      escapeMarkdown(suggestion.category ?? '-') || '-',
      escapeMarkdown(suggestion.impact ?? '-') || '-',
      formatConfidence(suggestion.confidence),
      escapeMarkdown(suggestion.title ?? '-') || '-',
      escapeMarkdown(files) || '-',
    ];
    lines.push(`| ${cells.join(' | ')} |`);
  });

  return lines.join('\n');
}

export const __private__ = {
  formatBool,
  formatLanguageMix,
  formatConfidence,
  formatStatsLines,
  escapeMarkdown,
};
