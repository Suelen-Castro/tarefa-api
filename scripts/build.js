// "Build" da aplicação: verifica a sintaxe de todos os arquivos e gera a pasta dist/
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const srcDir = path.join(__dirname, '..', 'src');
const distDir = path.join(__dirname, '..', 'dist');

fs.rmSync(distDir, { recursive: true, force: true });
fs.mkdirSync(distDir, { recursive: true });

for (const file of fs.readdirSync(srcDir)) {
  const origem = path.join(srcDir, file);
  execFileSync(process.execPath, ['--check', origem]); // falha se houver erro de sintaxe
  fs.copyFileSync(origem, path.join(distDir, file));
  console.log(`OK: ${file}`);
}

console.log('Build concluído em dist/');
