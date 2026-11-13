const { validateTask } = require('../../src/validation');

describe('validateTask (teste unitário)', () => {
  test('aceita tarefa válida', () => {
    expect(validateTask({ title: 'Estudar CI', done: false }).valid).toBe(true);
  });

  test('aceita tarefa sem o campo done', () => {
    expect(validateTask({ title: 'Estudar CI' }).valid).toBe(true);
  });

  test('rejeita título vazio', () => {
    const result = validateTask({ title: '   ' });
    expect(result.valid).toBe(false);
    expect(result.errors).toHaveLength(1);
  });

  test('rejeita título ausente', () => {
    expect(validateTask({}).valid).toBe(false);
  });

  test('rejeita título com mais de 100 caracteres', () => {
    expect(validateTask({ title: 'a'.repeat(101) }).valid).toBe(false);
  });

  test('rejeita done que não seja booleano', () => {
    expect(validateTask({ title: 'ok', done: 'sim' }).valid).toBe(false);
  });

  test('rejeita corpo inexistente', () => {
    expect(validateTask(undefined).valid).toBe(false);
  });
});
