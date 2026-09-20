#!/usr/bin/env node

/**
 * inject-brand-context.cjs
 * Extracts brand context for prompt injection.
 * Usage: node scripts/inject-brand-context.cjs [--json]
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const TOKENS_PATH = path.join(ROOT, 'assets', 'design-tokens.json');
const GUIDELINES_PATH = path.join(ROOT, 'docs', 'brand-guidelines.md');

const isJson = process.argv.includes('--json');

// Read tokens
let tokens;
try {
  tokens = JSON.parse(fs.readFileSync(TOKENS_PATH, 'utf8'));
} catch (e) {
  console.error(`Failed to read design tokens: ${e.message}`);
  process.exit(1);
}

// Read brand guidelines (extract key sections)
let guidelines = '';
try {
  guidelines = fs.readFileSync(GUIDELINES_PATH, 'utf8');
} catch (e) {
  console.warn(`Warning: Could not read brand guidelines: ${e.message}`);
}

// Extract voice section
const voiceMatch = guidelines.match(/## 3\. Voice & Tone[\s\S]*?(?=## 4\.|$)/);
const voice = voiceMatch ? voiceMatch[0].trim() : 'Not defined';

// Extract prohibited terms
const prohibitedMatch = guidelines.match(/### Prohibited Terms[\s\S]*?(?=---|$)/);
const prohibited = prohibitedMatch
  ? prohibitedMatch[0].match(/\| (.+?) \|/g)?.map(m => m.replace(/\| /g, '').replace(/ \|/, '')) || []
  : [];

const context = {
  brand: tokens.brand,
  version: tokens.version,
  updatedAt: tokens.updatedAt,
  colors: {
    primary: tokens.colors.primary['500'],
    accent: tokens.colors.accent['500'],
    background: tokens.colors.neutral['0'],
    foreground: tokens.colors.neutral['900'],
  },
  typography: {
    sans: tokens.typography.fontFamily.sans.split(',')[0].replace(/'/g, ''),
    mono: tokens.typography.fontFamily.mono.split(',')[0].replace(/'/g, ''),
  },
  voice,
  prohibitedTerms: prohibited,
};

if (isJson) {
  console.log(JSON.stringify(context, null, 2));
} else {
  console.log(`Brand: ${context.brand} v${context.version}`);
  console.log(`Primary: ${context.colors.primary}`);
  console.log(`Accent: ${context.colors.accent}`);
  console.log(`Typography: ${context.typography.sans} / ${context.typography.mono}`);
  console.log(`\nVoice:\n${context.voice}`);
  if (context.prohibitedTerms.length > 0) {
    console.log(`\nProhibited: ${context.prohibitedTerms.join(', ')}`);
  }
}
