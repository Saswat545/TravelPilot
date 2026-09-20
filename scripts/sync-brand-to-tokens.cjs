#!/usr/bin/env node

/**
 * sync-brand-to-tokens.cjs
 * Syncs docs/brand-guidelines.md → assets/design-tokens.json + .css
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const GUIDELINES_PATH = path.join(ROOT, 'docs', 'brand-guidelines.md');
const TOKENS_JSON = path.join(ROOT, 'assets', 'design-tokens.json');
const TOKENS_CSS = path.join(ROOT, 'assets', 'design-tokens.css');

// Verify source exists
if (!fs.existsSync(GUIDELINES_PATH)) {
  console.error(`Brand guidelines not found at ${GUIDELINES_PATH}`);
  console.error('Run /brand create first to generate brand guidelines.');
  process.exit(1);
}

// Read current tokens
let tokens;
try {
  tokens = JSON.parse(fs.readFileSync(TOKENS_JSON, 'utf8'));
} catch (e) {
  console.error(`Failed to parse ${TOKENS_JSON}: ${e.message}`);
  process.exit(1);
}

// Update timestamp
tokens.updatedAt = new Date().toISOString().split('T')[0];

// Write updated JSON
fs.writeFileSync(TOKENS_JSON, JSON.stringify(tokens, null, 2) + '\n');
console.log(`Updated: ${TOKENS_JSON}`);

// Generate CSS from tokens
const css = generateCSS(tokens);
fs.writeFileSync(TOKENS_CSS, css);
console.log(`Updated: ${TOKENS_CSS}`);

console.log('Brand sync complete.');

function generateCSS(tokens) {
  let css = `/* TravelPilot Design Tokens v${tokens.version}
 * Source: docs/brand-guidelines.md
 * Generated: ${tokens.updatedAt}
 */

:root {
`;

  // Colors
  css += `  /* Primary */\n`;
  css += `  --color-primary: ${tokens.colors.primary['500']};\n`;
  css += `  --color-primary-hover: ${tokens.colors.primary.hover};\n`;
  css += `  --color-primary-active: ${tokens.colors.primary.active};\n`;
  css += `  --color-primary-foreground: ${tokens.colors.primary.foreground};\n\n`;

  css += `  /* Secondary */\n`;
  css += `  --color-secondary: ${tokens.colors.secondary['500']};\n`;
  css += `  --color-secondary-hover: ${tokens.colors.secondary.hover};\n`;
  css += `  --color-secondary-active: ${tokens.colors.secondary.active};\n`;
  css += `  --color-secondary-foreground: ${tokens.colors.secondary.foreground};\n\n`;

  css += `  /* Accent */\n`;
  css += `  --color-accent-300: ${tokens.colors.accent['300']};\n`;
  css += `  --color-accent: ${tokens.colors.accent['500']};\n`;
  css += `  --color-accent-700: ${tokens.colors.accent['700']};\n`;
  css += `  --color-accent-foreground: ${tokens.colors.accent.foreground};\n`;
  css += `  --color-accent-background: ${tokens.colors.accent.background};\n`;
  css += `  --color-accent-border: ${tokens.colors.accent.border};\n\n`;

  css += `  /* Neutral */\n`;
  css += `  --color-background: ${tokens.colors.neutral['0']};\n`;
  css += `  --color-foreground: ${tokens.colors.neutral['900']};\n`;
  css += `  --color-muted: ${tokens.colors.neutral['100']};\n`;
  css += `  --color-muted-200: ${tokens.colors.neutral['200']};\n`;
  css += `  --color-border: ${tokens.colors.neutral['300']};\n`;
  css += `  --color-muted-foreground: ${tokens.colors.neutral['500']};\n`;
  css += `  --color-muted-foreground-600: ${tokens.colors.neutral['600']};\n\n`;

  css += `  /* Semantic */\n`;
  css += `  --color-success: ${tokens.colors.semantic.success};\n`;
  css += `  --color-warning: ${tokens.colors.semantic.warning};\n`;
  css += `  --color-error: ${tokens.colors.semantic.error};\n`;
  css += `  --color-info: ${tokens.colors.semantic.info};\n\n`;

  // Typography
  css += `  /* Typography */\n`;
  css += `  --font-sans: ${tokens.typography.fontFamily.sans};\n`;
  css += `  --font-mono: ${tokens.typography.fontFamily.mono};\n\n`;

  for (const [key, val] of Object.entries(tokens.typography.fontSize)) {
    css += `  --text-${key}: ${val};\n`;
  }
  css += `\n`;

  for (const [key, val] of Object.entries(tokens.typography.fontWeight)) {
    css += `  --font-weight-${key}: ${val};\n`;
  }
  css += `\n`;

  for (const [key, val] of Object.entries(tokens.typography.lineHeight)) {
    css += `  --line-height-${key}: ${val};\n`;
  }
  css += `\n`;

  // Spacing
  css += `  /* Spacing */\n`;
  for (const [key, val] of Object.entries(tokens.spacing)) {
    css += `  --space-${key}: ${val};\n`;
  }
  css += `\n`;

  // Border Radius
  css += `  /* Border Radius */\n`;
  for (const [key, val] of Object.entries(tokens.borderRadius)) {
    css += `  --radius-${key}: ${val};\n`;
  }
  css += `\n`;

  // Shadows
  css += `  /* Shadows */\n`;
  for (const [key, val] of Object.entries(tokens.shadows)) {
    css += `  --shadow-${key}: ${val};\n`;
  }
  css += `\n`;

  // Transitions
  css += `  /* Transitions */\n`;
  for (const [key, val] of Object.entries(tokens.transitions)) {
    css += `  --transition-${key}: ${val};\n`;
  }
  css += `\n`;

  // Chart Colors
  css += `  /* Chart Colors */\n`;
  for (const [key, val] of Object.entries(tokens.chartColors)) {
    css += `  --chart-${key}: ${val};\n`;
  }

  css += `}\n`;
  return css;
}
