// Teste de integração: API + banco PostgreSQL real (DATABASE_URL)
const request = require('supertest');
const { createPool, initDb } = require('../../src/db');
const { createApp } = require('../../src/app');

let pool;
let app;

beforeAll(async () => {
  pool = createPool();
  await initDb(pool);
  app = createApp(pool);
});

beforeEach(async () => {
  await pool.query('TRUNCATE tasks RESTART IDENTITY');
});

afterAll(async () => {
  await pool.end();
});

describe('API de tarefas (teste de integração)', () => {
  test('GET /health responde ok', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
  });

  test('POST /tasks cria tarefa e grava no banco', async () => {
    const res = await request(app)
      .post('/tasks')
      .send({ title: 'Nova tarefa' });
    expect(res.status).toBe(201);
    expect(res.body).toMatchObject({ title: 'Nova tarefa', done: false });

    const noBanco = await pool.query('SELECT * FROM tasks');
    expect(noBanco.rowCount).toBe(1);
  });

  test('POST /tasks com dados inválidos retorna 400', async () => {
    const res = await request(app).post('/tasks').send({ title: '' });
    expect(res.status).toBe(400);
  });

  test('GET /tasks lista as tarefas', async () => {
    await request(app).post('/tasks').send({ title: 'A' });
    await request(app).post('/tasks').send({ title: 'B' });
    const res = await request(app).get('/tasks');
    expect(res.status).toBe(200);
    expect(res.body).toHaveLength(2);
  });

  test('GET /tasks/:id retorna 404 quando não existe', async () => {
    const res = await request(app).get('/tasks/999');
    expect(res.status).toBe(404);
  });

  test('PUT /tasks/:id atualiza a tarefa', async () => {
    const criada = await request(app).post('/tasks').send({ title: 'Antes' });
    const res = await request(app)
      .put(`/tasks/${criada.body.id}`)
      .send({ title: 'Depois', done: true });
    expect(res.status).toBe(200);
    expect(res.body).toMatchObject({ title: 'Depois', done: true });
  });

  test('DELETE /tasks/:id remove a tarefa', async () => {
    const criada = await request(app).post('/tasks').send({ title: 'Apagar' });
    const res = await request(app).delete(`/tasks/${criada.body.id}`);
    expect(res.status).toBe(204);

    const busca = await request(app).get(`/tasks/${criada.body.id}`);
    expect(busca.status).toBe(404);
  });
});
