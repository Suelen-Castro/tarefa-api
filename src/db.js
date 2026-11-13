const { Pool } = require('pg');

// Cria a conexão com o PostgreSQL usando a variável de ambiente DATABASE_URL
function createPool() {
  return new Pool({ connectionString: process.env.DATABASE_URL });
}

// Cria a tabela caso ainda não exista
async function initDb(pool) {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS tasks (
      id SERIAL PRIMARY KEY,
      title VARCHAR(100) NOT NULL,
      done BOOLEAN NOT NULL DEFAULT FALSE,
      created_at TIMESTAMP NOT NULL DEFAULT NOW()
    )
  `);
}

module.exports = { createPool, initDb };
