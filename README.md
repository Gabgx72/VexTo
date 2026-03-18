# VexTo

📂 VexTo - Gestão Financeira Inteligente

O VexTo é uma aplicação web desenvolvida com o objetivo de ajudar usuários a terem mais controle e clareza sobre seus gastos do dia a dia, de forma simples, visual e eficiente.

🧠 O Problema

Durante a análise do comportamento de usuários, foi possível identificar dificuldades comuns no controle financeiro pessoal:

1. **Falta de clareza visual**  
   Dificuldade em entender para onde o dinheiro está indo apenas com listas ou planilhas.

2. **Excesso de complexidade**  
   Ferramentas existentes possuem muitas funcionalidades, tornando o uso confuso.

3. **Baixa praticidade no dia a dia**  
   Registrar gastos manualmente em planilhas não é rápido nem intuitivo.

## 🚀 A Solução

O VexTo foi desenvolvido como uma solução simples e eficiente para controle financeiro, permitindo:

- Registro rápido de gastos
- Visualização do total gasto
- Organização por categorias
- Gráfico dinâmico para análise visual dos gastos

🛠️ Stack Tecnológica
Backend: Python com Framework Flask (Arquitetura minimalista e rápida).

Frontend: HTML5, CSS3 (com suporte a Temas Dark/Light) e JavaScript Puro (Vanilla JS).

Banco de Dados: SQLite (Relacional, leve e integrado para portabilidade).

Gráficos: Chart.js para renderização de dados em tempo real.

💡 Destaques de Implementação

1. Splash Screen Inteligente (UX Design)
Para atender ao pedido de uma "experiência de App", implementamos uma tela de carregamento com o mascote.

Técnica utilizada: Uso de sessionStorage no navegador para garantir que a animação de 2 segundos ocorra apenas na primeira abertura da sessão, evitando que o usuário tenha que esperar a cada troca de página.

2. Dashboard Dinâmico e Reativo
Os dados são processados no backend via Python, agrupados por categoria e enviados ao frontend em formato JSON.

Técnica utilizada: Integração entre Jinja2 (template engine) e Chart.js. O sistema identifica automaticamente se há dados para o mês selecionado; caso contrário, renderiza estados de "Empty State" amigáveis.

3. Sistema de Alertas e Metas
Criei uma lógica de verificação cruzada:

Sempre que um gasto é inserido, o sistema compara o acumulado da categoria com o limite definido na tabela de metas.

Diferencial: Implementei um sistema de cores dinâmico que dispara pop-ups de alerta caso a meta global ou por categoria seja ultrapassada.

4. Estrutura de Pastas Profissional
O projeto segue o padrão rigoroso de aplicações Flask:

Plaintext
controle-gastos/
│
├── app.py
├── database.db
├── requirements.txt
├── static/
│ ├── style.css
│ └── script.js
└── templates/
└── index.html

📈 Resultados Obtidos

Tempo de Resposta: Redução drástica no tempo de inserção de gastos em comparação a planilhas manuais.

Engajamento: A interface intuitiva e o "Mascote" criaram uma conexão emocional com o produto.

Controle: O cliente agora tem consciência exata do seu "Budget" mensal através de feedbacks visuais imediatos.

🔧 Como rodar o projeto

Clone o repositório.

Instale as dependências: pip install -r requirements.txt.

Execute o comando: python app.py.

Acesse http://localhost:5000 no seu navegador.


## 🚀 Próximas melhorias

- 1. Sistema de Login e Multi-usuário 👤
Atualmente, o banco de dados é compartilhado. Se você abrir o link, verá os mesmos dados que qualquer outra pessoa.

Melhoria: Criar uma tela de Login e Cadastro.

Técnica: Usar a biblioteca Flask-Login e criar uma relação no banco de dados onde cada gasto possui um user_id. Assim, os dados ficam privados para cada pessoa.

- 2. Leitura Automática de Comprovantes (OCR) 📸
Digitar gastos manualmente é o que faz a maioria das pessoas desistir de apps financeiros.

Melhoria: Um botão para tirar foto do cupom fiscal e o app preencher o valor e a categoria sozinho.

Técnica: Integrar com uma API de IA ou usar a biblioteca Tesseract (OCR) para extrair o texto da imagem.

- 3. Exportação de Relatórios Avançados 📄
O cliente pode precisar desses dados para o Imposto de Renda ou para apresentar a um sócio/cônjuge.

Melhoria: Botões de "Exportar para PDF" ou "Baixar Planilha Excel".

Técnica: Usar bibliotecas como ReportLab (PDF) ou Pandas (Excel) para gerar os arquivos na hora.


- 4. Notificações via WhatsApp ou E-mail 🔔
Ajudar o usuário a não esquecer de contas fixas ou avisar quando o limite está em 90%.

Melhoria: Um sistema de alertas automáticos.

Técnica: Usar Twilio (WhatsApp) ou Flask-Mail para enviar avisos tipo: "Ei, sua meta de Lazer já atingiu 90% este mês! 🐘"

---

## 📌 Autor

Desenvolvido por Gabriel Souza 🚀
