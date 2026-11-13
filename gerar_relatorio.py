"""
Gera o relatorio em PDF.
Uso:
  1) Coloque os prints na pasta prints/ com os nomes listados em PRINTS abaixo
  2) Edite NOME e REPO_URL
  3) pip install reportlab && python gerar_relatorio.py
Prints que faltarem aparecem como uma caixa "cole o print aqui".
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Preformatted, Table, TableStyle, Image, KeepTogether)

NOME = "Suelen Souza de Castro"
REPO_URL = "https://github.com/SEU-USUARIO/tarefas-api"   # <- troque pelo seu link
OUT = "Relatorio_CI_GitHub_Actions.pdf"
AQUI = os.path.dirname(os.path.abspath(__file__))

# (arquivo, titulo, o que deve aparecer no print)
PRINTS = [
    ("01-repositorio.png", "Print 1 - Repositório no GitHub",
     "Página inicial do repositório mostrando as pastas src, tests, .github/workflows, o Dockerfile e o README."),
    ("02-pull-request.png", "Print 2 - Pull Request com os checks",
     "Página do PR mostrando a lista de checks (lint, format, security, build, unit-test, integration-test, docker)."),
    ("03-workflow-geral.png", "Print 3 - Visão geral da execução (aba Actions)",
     "Tela da execução do workflow CI com o grafo de jobs, todos com o ícone verde."),
    ("04-lint.png", "Print 4 - Job de análise estática de código",
     "Job 'Analise estatica de codigo' aberto, com o passo 'npm run lint' concluído com sucesso."),
    ("05-format.png", "Print 5 - Job de análise de formatação",
     "Job 'Analise de formatacao' aberto, com 'All matched files use Prettier code style!'."),
    ("06-security.png", "Print 6 - Job de análise estática de segurança",
     "Job 'Analise estatica de seguranca' com os passos CodeQL (init/analyze) e npm audit concluídos."),
    ("07-build.png", "Print 7 - Job de build",
     "Job 'Build' mostrando 'Build concluído em dist/' e o artefato 'dist' gerado."),
    ("08-unit.png", "Print 8 - Job de teste unitário",
     "Job 'Teste unitario' mostrando '7 passed'."),
    ("09-integration.png", "Print 9 - Job de teste de integração",
     "Job 'Teste de integracao' mostrando o service container do PostgreSQL e '7 passed'."),
    ("10-docker.png", "Print 10 - Job de criação da imagem Docker",
     "Job 'Criacao da imagem Docker' concluído com sucesso."),
    ("11-falha-proposital.png", "Print 11 (opcional) - Falha proposital bloqueando o merge",
     "PR com um teste quebrado: job vermelho e botão de merge bloqueado (comprova que o CI funciona)."),
]

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=16, textColor=colors.HexColor("#1F3A5F"), spaceBefore=14, spaceAfter=8)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=12.5, textColor=colors.HexColor("#1F3A5F"), spaceBefore=10, spaceAfter=4, keepWithNext=1)
B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=10.5, leading=15, spaceAfter=6)
BUL = ParagraphStyle("BUL", parent=B, leftIndent=14, bulletIndent=2, spaceAfter=3)
CAP = ParagraphStyle("CAP", parent=B, fontSize=9, textColor=colors.HexColor("#555555"), spaceAfter=10)
CODE = ParagraphStyle("CODE", fontName="Courier", fontSize=7.2, leading=9, backColor=colors.HexColor("#F3F4F6"),
                      borderPadding=6, spaceAfter=10)
TITLE = ParagraphStyle("TITLE", parent=ss["Title"], fontSize=24, leading=30, textColor=colors.HexColor("#1F3A5F"))

def bullets(items):
    return [Paragraph(t, BUL, bulletText="-") for t in items]

CELL = ParagraphStyle("CELL", parent=B, fontSize=9, leading=11.5, spaceAfter=0)
CELLH = ParagraphStyle("CELLH", parent=CELL, textColor=colors.white, fontName="Helvetica-Bold")

def table(rows, widths, header=True):
    rows = [[Paragraph(str(c), CELLH if (header and i == 0) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BBBBBB")),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("FONTSIZE", (0, 0), (-1, -1), 9),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if header:
        st += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F3A5F")),
               ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]
    t.setStyle(TableStyle(st))
    return t

def P(t):
    return Paragraph(t, ss["BodyText"])

def print_block(arq, titulo, desc):
    caminho = os.path.join(AQUI, "prints", arq)
    itens = [Paragraph(titulo, H2), Paragraph("<i>O que deve aparecer:</i> " + desc, CAP)]
    if os.path.exists(caminho):
        from reportlab.lib.utils import ImageReader
        w, h = ImageReader(caminho).getSize()
        largura = 16 * cm
        altura = min(largura * h / w, 12 * cm)
        largura = altura * w / h
        itens.append(Image(caminho, width=largura, height=altura))
    else:
        box = Table([[Paragraph("<para alignment='center'><font color='#888888'>[ COLE AQUI O PRINT: %s ]</font></para>" % arq, B)]],
                    colWidths=[16 * cm], rowHeights=[6 * cm])
        box.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#999999")),
                                 ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
        itens.append(box)
    itens.append(Spacer(1, 8))
    return KeepTogether(itens)

def ler(rel):
    with open(os.path.join(AQUI, rel), encoding="utf-8") as f:
        return f.read().rstrip()

def rodape(c, d):
    c.saveState()
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#777777"))
    c.drawString(2 * cm, 1.2 * cm, "%s - Relatório de CI com GitHub Actions" % NOME)
    c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, "Página %d" % d.page)
    c.restoreState()

s = []
# ---------- Capa
s += [Spacer(1, 5 * cm),
      Paragraph("Implementação de Pipeline de Integração Contínua (CI) com GitHub Actions", TITLE),
      Spacer(1, 1 * cm),
      Paragraph("<para alignment='center'>API REST de Tarefas (Node.js + Express + PostgreSQL)</para>", ss["Heading3"]),
      Spacer(1, 3 * cm),
      Paragraph("<para alignment='center'><b>Aluna:</b> %s</para>" % NOME, B),
      Paragraph("<para alignment='center'><b>Repositório:</b> <link href='%s' color='blue'>%s</link></para>" % (REPO_URL, REPO_URL), B),
      PageBreak()]

# ---------- 1 Introducao
s += [Paragraph("1. Introdução", H1),
      Paragraph("A <b>Integração Contínua (CI)</b> é a prática de validar automaticamente cada alteração de código antes de ela entrar na branch principal. "
                "Este relatório apresenta a <b>implementação prática</b> do roteiro elaborado na atividade anterior: um pipeline no GitHub Actions "
                "aplicado a uma API REST com banco de dados SQL.", B),
      Paragraph("O pipeline é acionado por <b>Pull Request</b> e executa: análise estática de código, análise de formatação, análise estática de segurança, "
                "build, teste unitário, teste de integração e criação da imagem Docker.", B)]

# ---------- 2 Aplicacao
s += [Paragraph("2. Aplicação escolhida", H1),
      Paragraph("Foi criada a <b>Tarefas API</b>, um CRUD simples de tarefas (lista de afazeres). Foi escolhida por ser pequena e fácil de entender, "
                "mas já tem tudo o que a atividade pede: API REST e banco SQL.", B),
      table([["Item", "Tecnologia"],
             ["Linguagem / framework", "Node.js 20 + Express"],
             ["Banco de dados SQL", "PostgreSQL 16 (biblioteca pg, consultas parametrizadas)"],
             ["Análise estática de código", "ESLint"],
             ["Análise de formatação", "Prettier"],
             ["Análise estática de segurança", "CodeQL (SAST) + npm audit (dependências)"],
             ["Testes", "Jest (unitário) e Jest + Supertest (integração)"],
             ["Imagem", "Docker (Dockerfile) com Buildx"]], [6 * cm, 10.5 * cm]),
      Spacer(1, 8),
      Paragraph("Endpoints da API REST", H2),
      table([["Método", "Rota", "O que faz", "Retorno"],
             ["GET", "/health", "Verifica se a API está no ar", "200"],
             ["GET", "/tasks", "Lista todas as tarefas", "200"],
             ["GET", "/tasks/:id", "Busca uma tarefa", "200 ou 404"],
             ["POST", "/tasks", "Cria tarefa", "201 ou 400"],
             ["PUT", "/tasks/:id", "Atualiza tarefa", "200, 400 ou 404"],
             ["DELETE", "/tasks/:id", "Remove tarefa", "204 ou 404"]], [2.2 * cm, 3.3 * cm, 7.5 * cm, 3.5 * cm]),
      Spacer(1, 8),
      Paragraph("Estrutura do projeto", H2),
      Preformatted("""tarefas-api/
 .github/workflows/ci.yml   <- o pipeline de CI
 src/
   app.js          rotas da API REST
   db.js           conexão e tabela do PostgreSQL
   validation.js   regras de validação
   server.js       inicia o servidor
 tests/
   unit/validation.test.js        teste unitário
   integration/tasks.test.js      teste de integração (usa o banco)
 scripts/build.js  build (verifica sintaxe e gera dist/)
 Dockerfile        imagem da aplicação
 eslint.config.js  regras do ESLint
 .prettierrc       regras do Prettier
 package.json      scripts e dependências""", CODE)]

# ---------- 3 Pipeline
s += [PageBreak(), Paragraph("3. Visão geral do pipeline", H1),
      Paragraph("Seguindo o princípio <b>fail fast</b> (falhar rápido) da atividade anterior, as verificações mais baratas rodam primeiro. "
                "Como lint, formatação e segurança são independentes entre si, rodam <b>em paralelo</b>, e o build só começa se os três passarem. "
                "Cada etapa seguinte depende da anterior pela palavra-chave <font face='Courier'>needs</font>.", B),
      Preformatted("""   Pull Request para a main
            |
   +--------+---------+------------+
   |        |         |
  lint    format    security        (em paralelo)
   |        |         |
   +--------+---------+------------+
            |
          build
            |
       unit-test
            |
     integration-test
            |
         docker""", CODE),
      table([["Job", "Objetivo", "Se falhar significa..."],
             ["lint", "Análise estática de código (ESLint)", "Erros de código, variáveis não usadas, má prática"],
             ["format", "Análise de formatação (Prettier)", "Código fora do padrão de estilo"],
             ["security", "Análise estática de segurança (CodeQL + npm audit)", "Vulnerabilidade no código ou em dependência"],
             ["build", "Verifica a sintaxe e gera a pasta dist/", "Erro de sintaxe ou dependência"],
             ["unit-test", "Teste unitário da lógica de validação", "Regra de negócio quebrada"],
             ["integration-test", "Testa a API com PostgreSQL real", "Falha entre API e banco de dados"],
             ["docker", "Constrói a imagem Docker", "Dockerfile inválido"]], [3 * cm, 6.5 * cm, 7 * cm])]

# ---------- 4 Explicacao do workflow
s += [Paragraph("4. Explicação do workflow (ci.yml)", H1),
      Paragraph("O arquivo fica em <font face='Courier'>.github/workflows/ci.yml</font>. Abaixo, cada parte explicada de forma simples.", B),
      Paragraph("4.1 Gatilho: Pull Request", H2),
      Paragraph("O bloco <font face='Courier'>on: pull_request</font> faz o pipeline rodar quando um PR com destino à <b>main</b> é aberto (<i>opened</i>), "
                "recebe novos commits (<i>synchronize</i>) ou é reaberto (<i>reopened</i>). O bloco <font face='Courier'>concurrency</font> cancela "
                "a execução antiga se chegar um commit novo, economizando tempo.", B),
      Paragraph("4.2 Análise estática de código (lint)", H2),
      Paragraph("Faz checkout, instala o Node.js 20 com cache, instala pacotes com <font face='Courier'>npm ci</font> e roda o ESLint, "
                "que lê o código sem executá-lo e aponta erros como variável não usada, uso de <i>var</i> e comparação com <i>==</i>.", B),
      Paragraph("4.3 Análise de formatação (format)", H2),
      Paragraph("O Prettier confere se todo o código segue o mesmo estilo (aspas simples, ponto e vírgula, vírgula final). "
                "Usa-se <font face='Courier'>--check</font>: ele apenas verifica, não altera arquivos.", B),
      Paragraph("4.4 Análise estática de segurança (security)", H2),
      Paragraph("Usa o <b>CodeQL</b>, ferramenta do próprio GitHub que procura vulnerabilidades no código (por exemplo SQL Injection e XSS). "
                "Também roda o <font face='Courier'>npm audit</font>, que procura vulnerabilidades graves nas bibliotecas usadas. "
                "As consultas ao banco usam parâmetros ($1, $2), o que protege contra SQL Injection.", B),
      Paragraph("4.5 Build", H2),
      Paragraph("O projeto é JavaScript, então não precisa compilar. O script <font face='Courier'>scripts/build.js</font> verifica a sintaxe de cada arquivo "
                "e gera a pasta <font face='Courier'>dist/</font>, que é guardada como <b>artefato</b> do workflow. "
                "Só roda se lint, format e security passarem.", B),
      Paragraph("4.6 Teste unitário", H2),
      Paragraph("Testa a função <font face='Courier'>validateTask</font> isoladamente, sem banco de dados. São 7 testes (título vazio, título grande demais, "
                "campo done inválido etc.). É rápido, por isso vem antes do teste de integração.", B),
      Paragraph("4.7 Teste de integração", H2),
      Paragraph("Sobe um <b>PostgreSQL 16 real</b> como <i>service container</i> (descartado ao fim do job) com <i>health check</i> para garantir que o banco esteja pronto. "
                "Os 7 testes chamam a API de verdade (POST, GET, PUT, DELETE) e conferem se os dados foram gravados no banco. "
                "A conexão é passada pela variável <font face='Courier'>DATABASE_URL</font>.", B),
      Paragraph("4.8 Criação da imagem Docker", H2),
      Paragraph("Última etapa. Constrói a imagem a partir do Dockerfile, com tag igual ao hash do commit (<font face='Courier'>github.sha</font>) "
                "para rastreabilidade. Usa <font face='Courier'>push: false</font>: na CI a imagem só é construída e validada; "
                "a publicação em um registro ficaria para a etapa de entrega (CD).", B),
      Paragraph("4.9 Código completo do workflow", H2),
      Preformatted(ler(".github/workflows/ci.yml"), CODE)]

# ---------- 5 Como reproduzir
s += [PageBreak(), Paragraph("5. Como o projeto foi publicado e executado", H1),
      Paragraph("Comandos usados para enviar o projeto ao GitHub e disparar o pipeline pelo Pull Request:", B),
      Preformatted("""# 1. Criar o repositório vazio no GitHub (ex.: tarefas-api) e depois:
git init
git add .
git commit -m "feat: projeto inicial da Tarefas API"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/tarefas-api.git
git push -u origin main

# 2. Criar uma branch nova, fazer uma alteração e enviar
git checkout -b feature/teste-ci
# (edite algo, por exemplo uma linha do README)
git add .
git commit -m "docs: testando o pipeline de CI"
git push -u origin feature/teste-ci

# 3. No GitHub: botão "Compare & pull request" -> Create pull request
#    O pipeline inicia sozinho. Acompanhe na aba Actions.""", CODE),
      Paragraph("Observações importantes", H2)]
s += bullets([
    "O workflow só roda em <b>Pull Request</b>. Por isso o primeiro push direto na main não dispara nada: é preciso abrir o PR.",
    "A análise CodeQL é gratuita em repositórios <b>públicos</b>. Em repositório privado exige GitHub Advanced Security.",
    "Em <i>Settings > Branches > Add branch protection rule</i> (main), marque <i>Require status checks to pass before merging</i> "
    "e selecione os jobs, para que um PR com falha não possa ser mesclado.",
    "Para testar localmente: <font face='Courier'>npm ci</font>, depois <font face='Courier'>npm run lint</font>, "
    "<font face='Courier'>npm run format:check</font>, <font face='Courier'>npm run build</font> e <font face='Courier'>npm run test:unit</font>."])

# ---------- 6 Evidencias
s += [PageBreak(), Paragraph("6. Evidências da execução (prints)", H1),
      Paragraph("As telas abaixo comprovam a execução do pipeline no GitHub Actions.", B)]
for p in PRINTS:
    s.append(print_block(*p))

# ---------- 7 Repo
s += [Paragraph("7. Link do repositório", H1),
      Paragraph("<link href='%s' color='blue'>%s</link>" % (REPO_URL, REPO_URL), B)]

# ---------- 8 Conclusao
s += [Paragraph("8. Conclusão", H1),
      Paragraph("O pipeline automatiza a validação de cada Pull Request com sete verificações encadeadas: análise estática de código, formatação, "
                "segurança, build, teste unitário, teste de integração e criação da imagem Docker. Com isso, erros de estilo, falhas de lógica, "
                "problemas de integração com o banco e vulnerabilidades são detectados antes do código chegar à branch principal, "
                "mantendo a <b>main</b> sempre estável. A ordem adotada prioriza feedback rápido e uso eficiente de recursos, "
                "e serve de base para evoluir futuramente para entrega e implantação contínuas (CD).", B)]

SimpleDocTemplate(os.path.join(AQUI, OUT), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                  topMargin=2 * cm, bottomMargin=2 * cm,
                  title="Relatório CI GitHub Actions", author=NOME).build(s, onFirstPage=lambda c, d: None, onLaterPages=rodape)
print("PDF gerado:", OUT)
