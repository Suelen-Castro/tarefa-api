const { createApp } = require('./app');
const { createPool, initDb } = require('./db');

const PORT = process.env.PORT || 3000;

async function main() {
  const pool = createPool();
  await initDb(pool);
  createApp(pool).listen(PORT, () => {
    console.log(`API rodando na porta ${PORT}`);
  });
}

main().catch((err) => {
  console.error('Falha ao iniciar:', err.message);
  process.exit(1);
});
