const express = require('express');
const { validateTask } = require('./validation');

// Monta a aplicação recebendo o pool do banco (facilita os testes)
function createApp(pool) {
  const app = express();
  app.use(express.json());

  // Verificação de saúde da API
  app.get('/health', (req, res) => {
    res.json({ status: 'ok' });
  });

  // Listar todas as tarefas
  app.get('/tasks', async (req, res, next) => {
    try {
      const result = await pool.query('SELECT * FROM tasks ORDER BY id');
      res.json(result.rows);
    } catch (err) {
      next(err);
    }
  });

  // Buscar uma tarefa pelo id
  app.get('/tasks/:id', async (req, res, next) => {
    try {
      const result = await pool.query('SELECT * FROM tasks WHERE id = $1', [
        req.params.id,
      ]);
      if (result.rowCount === 0) {
        return res.status(404).json({ error: 'Tarefa não encontrada' });
      }
      res.json(result.rows[0]);
    } catch (err) {
      next(err);
    }
  });

  // Criar tarefa
  app.post('/tasks', async (req, res, next) => {
    try {
      const { valid, errors } = validateTask(req.body);
      if (!valid) {
        return res.status(400).json({ errors });
      }
      const result = await pool.query(
        'INSERT INTO tasks (title, done) VALUES ($1, $2) RETURNING *',
        [req.body.title.trim(), req.body.done ?? false],
      );
      res.status(201).json(result.rows[0]);
    } catch (err) {
      next(err);
    }
  });

  // Atualizar tarefa
  app.put('/tasks/:id', async (req, res, next) => {
    try {
      const { valid, errors } = validateTask(req.body);
      if (!valid) {
        return res.status(400).json({ errors });
      }
      const result = await pool.query(
        'UPDATE tasks SET title = $1, done = $2 WHERE id = $3 RETURNING *',
        [req.body.title.trim(), req.body.done ?? false, req.params.id],
      );
      if (result.rowCount === 0) {
        return res.status(404).json({ error: 'Tarefa não encontrada' });
      }
      res.json(result.rows[0]);
    } catch (err) {
      next(err);
    }
  });

  // Remover tarefa
  app.delete('/tasks/:id', async (req, res, next) => {
    try {
      const result = await pool.query('DELETE FROM tasks WHERE id = $1', [
        req.params.id,
      ]);
      if (result.rowCount === 0) {
        return res.status(404).json({ error: 'Tarefa não encontrada' });
      }
      res.status(204).send();
    } catch (err) {
      next(err);
    }
  });

  // Tratamento de erros (ex.: id inválido, banco indisponível)
  // eslint-disable-next-line no-unused-vars
  app.use((err, req, res, next) => {
    console.error(err.message);
    res.status(500).json({ error: 'Erro interno do servidor' });
  });

  return app;
}

module.exports = { createApp };
