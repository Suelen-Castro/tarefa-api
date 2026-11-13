// Regras de validação de uma tarefa (lógica pura, fácil de testar com teste unitário)
function validateTask(body) {
  const errors = [];

  if (!body || typeof body !== 'object') {
    return { valid: false, errors: ['Corpo da requisição inválido'] };
  }

  if (typeof body.title !== 'string' || body.title.trim() === '') {
    errors.push('title é obrigatório e deve ser um texto');
  } else if (body.title.trim().length > 100) {
    errors.push('title deve ter no máximo 100 caracteres');
  }

  if (body.done !== undefined && typeof body.done !== 'boolean') {
    errors.push('done deve ser true ou false');
  }

  return { valid: errors.length === 0, errors };
}

module.exports = { validateTask };
