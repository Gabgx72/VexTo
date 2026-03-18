# VexTo

VexTo - Gestão Financeira Inteligente

Desenvolvi um aplicaçao em Front end, focada em ajudar a gestao financeira dos usuarios

O Problema do Cliente

Notei que as pessoas nao tinham uma ferramenta de controle financeiro que fosse além das planilhas estáticas com isso resolvi desenvolver um sistema basico para que ajudasse as pessoas a controlar os seus gastos. Os principais "pain points" (pontos de dor) identificados foram:

Falta de Clareza Visual: Dificuldade em entender para onde o dinheiro está indo apenas olhando listas de números.

Excesso de Complexidade: Ferramentas de mercado com excesso de funções que confundem o usuário final.

Falta de Metas Claras: A ausência de um sistema que trave ou alerte quando um limite de gastos por categoria é atingido.

Desenvolvemos uma aplicação Web Full Stack utilizando Python e Flask, focada em performance, UX (Experiência do Usuário) e persistência de dados.

🛠️ Stack Tecnológica
Backend: Python com Framework Flask (Arquitetura minimalista e rápida).

Frontend: HTML5, CSS3 (com suporte a Temas Dark/Light) e JavaScript Puro (Vanilla JS).

Banco de Dados: SQLite (Relacional, leve e integrado para portabilidade).

Gráficos: Chart.js para renderização de dados em tempo real.

💡 Destaques de Implementação
1. Splash Screen Inteligente (UX Avançada)
Para atender ao pedido de uma "experiência de App", implementamos uma tela de carregamento verde (cor da marca) com o mascote.

Técnica utilizada: Uso de sessionStorage no navegador para garantir que a animação de 2 segundos ocorra apenas na primeira abertura da sessão, evitando que o usuário tenha que esperar a cada troca de página.

2. Dashboard Dinâmico e Reativo
Os dados são processados no backend via Python, agrupados por categoria e enviados ao frontend em formato JSON.

Técnica utilizada: Integração entre Jinja2 (template engine) e Chart.js. O sistema identifica automaticamente se há dados para o mês selecionado; caso contrário, renderiza estados de "Empty State" amigáveis.

3. Sistema de Alertas e Metas
Criamos uma lógica de verificação cruzada:

Sempre que um gasto é inserido, o sistema compara o acumulado da categoria com o limite definido na tabela de metas.

Diferencial: Implementamos um sistema de cores dinâmico que dispara pop-ups de alerta caso a meta global ou por categoria seja ultrapassada.

4. Estrutura de Pastas Profissional
O projeto segue o padrão rigoroso de aplicações Flask:

├── app.py              # Lógica do servidor e rotas
├── database.db         # Banco de dados SQLite
├── requirements.txt    # Dependências para Deploy (Render/Heroku)
├── static/             # Assets (CSS, JS, Imagens)
└── templates/          # Visual (Páginas HTML)

O Gemini disse
Excelente! Um repositório com um README técnico e bem estruturado é o que diferencia um "estudante" de um "desenvolvedor profissional" aos olhos de quem visita seu GitHub (ou de um recrutador).

Aqui está um modelo de explicação técnica focado na solução do problema do cliente, estruturado para você copiar e colar no seu arquivo README.md.

📂 VexTo - Gestão Financeira Inteligente
🎯 O Problema do Cliente
O cliente necessitava de uma ferramenta de controle financeiro que fosse além das planilhas estáticas. Os principais "pain points" (pontos de dor) identificados foram:

Falta de Clareza Visual: Dificuldade em entender para onde o dinheiro está indo apenas olhando listas de números.

Excesso de Complexidade: Ferramentas de mercado com excesso de funções que confundem o usuário final.

Falta de Metas Claras: A ausência de um sistema que trave ou alerte quando um limite de gastos por categoria é atingido.

Identidade Visual Inexistente: O desejo de ter um produto que parecesse um "App Premium", com marca própria (o elefante VexTo) e transições suaves.

🚀 A Solução Técnica
Desenvolvemos uma aplicação Web Full Stack utilizando Python e Flask, focada em performance, UX (Experiência do Usuário) e persistência de dados.

🛠️ Stack Tecnológica
Backend: Python com Framework Flask (Arquitetura minimalista e rápida).

Frontend: HTML5, CSS3 (com suporte a Temas Dark/Light) e JavaScript Puro (Vanilla JS).

Banco de Dados: SQLite (Relacional, leve e integrado para portabilidade).

Gráficos: Chart.js para renderização de dados em tempo real.

💡 Destaques de Implementação
1. Splash Screen Inteligente (UX Avançada)
Para atender ao pedido de uma "experiência de App", implementamos uma tela de carregamento verde (cor da marca) com o mascote.

Técnica utilizada: Uso de sessionStorage no navegador para garantir que a animação de 2 segundos ocorra apenas na primeira abertura da sessão, evitando que o usuário tenha que esperar a cada troca de página.

2. Dashboard Dinâmico e Reativo
Os dados são processados no backend via Python, agrupados por categoria e enviados ao frontend em formato JSON.

Técnica utilizada: Integração entre Jinja2 (template engine) e Chart.js. O sistema identifica automaticamente se há dados para o mês selecionado; caso contrário, renderiza estados de "Empty State" amigáveis.

3. Sistema de Alertas e Metas
Criamos uma lógica de verificação cruzada:

Sempre que um gasto é inserido, o sistema compara o acumulado da categoria com o limite definido na tabela de metas.

Diferencial: Implementamos um sistema de cores dinâmico que dispara pop-ups de alerta caso a meta global ou por categoria seja ultrapassada.

4. Estrutura de Pastas Profissional
O projeto segue o padrão rigoroso de aplicações Flask:

Plaintext
├── app.py              # Lógica do servidor e rotas
├── database.db         # Banco de dados SQLite
├── requirements.txt    # Dependências para Deploy (Render/Heroku)
├── static/             # Assets (CSS, JS, Imagens)
└── templates/          # Visual (Páginas HTML)
📈 Resultados Obtidos
Tempo de Resposta: Redução drástica no tempo de inserção de gastos em comparação a planilhas manuais.

Engajamento: A interface intuitiva e o "Mascote" criaram uma conexão emocional com o produto.

Controle: O cliente agora tem consciência exata do seu "Budget" mensal através de feedbacks visuais imediatos.

🔧 Como rodar o projeto
Clone o repositório.

Instale as dependências: pip install -r requirements.txt.

Execute o comando: python app.py.

Acesse http://localhost:5000 no seu navegador.

