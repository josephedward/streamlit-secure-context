#!/usr/bin/env node
// Build script for streamlit-secure-context frontend using esbuild
const esbuild = require('esbuild');
const fs = require('fs');
const path = require('path');

async function build() {
  const root = path.resolve(__dirname, '..');
  const publicDir = path.join(root, 'public');
  const buildDir = path.join(root, 'build');
  // Clean build directory
  if (fs.existsSync(buildDir)) {
    fs.rmSync(buildDir, { recursive: true, force: true });
  }
  fs.mkdirSync(buildDir, { recursive: true });

  // Copy static public assets (iframe and worker)
  ['model_iframe.html', 'worker.js'].forEach((file) => {
    const src = path.join(publicDir, file);
    const dest = path.join(buildDir, file);
    fs.copyFileSync(src, dest);
  });

  // Process index.html template: inject bundle script
  const indexHtmlPath = path.join(publicDir, 'index.html');
  let indexHtml = fs.readFileSync(indexHtmlPath, 'utf8');
  indexHtml = indexHtml.replace(
    '</body>',
    '  <script src="index.js"></script>\n</body>'
  );
  fs.writeFileSync(path.join(buildDir, 'index.html'), indexHtml);

  // Bundle React component with esbuild
  await esbuild.build({
    entryPoints: [path.join(root, 'src', 'StreamlitSecureContext.tsx')],
    bundle: true,
    outfile: path.join(buildDir, 'index.js'),
    loader: { '.ts': 'ts', '.tsx': 'tsx' },
    define: { 'process.env.NODE_ENV': '"production"' },
    minify: false,
    sourcemap: false,
    target: ['es2015'],
    logLevel: 'info',
  });
  console.log('Frontend build complete.');
}

build().catch((err) => {
  console.error('Build failed:', err);
  process.exit(1);
});