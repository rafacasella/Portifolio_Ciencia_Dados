# 📊 Monitor de Inteligência Geopolítica & Econômica - Truth Social

Este projeto consiste em um pipeline automatizado de extração e monitoramento de dados em tempo real direcionado ao perfil oficial de figuras públicas na plataforma **Truth Social**. O sistema monitora menções a termos estratégicos relacionados a mercado, economia e tensões geopolíticas globais.

Desenvolvido como parte do meu portfólio de Ciência de Dados, o projeto supera os desafios comuns de web scraping tradicional (como bloqueios do Cloudflare, renderização dinâmica de JavaScript e instabilidade de classes CSS) utilizando técnicas avançadas de automação furtiva e interceptação de rede.

---

## 🚀 Principais Funcionalidades

*   **Monitoramento em Segundo Plano (Headless):** O script roda de forma invisível, otimizando o consumo de memória e processamento.
*   **Interceptação Baseada em API Oculta:** Em vez de depender do layout visual (HTML/CSS) que muda frequentemente, o código captura diretamente os pacotes JSON de tráfego de rede trocados entre o navegador e o servidor (`/api/v1/accounts/.../statuses`).
*   **Filtro Inteligente Multitermos:** Análise em tempo real de novas publicações baseada em uma lista de palavras-chave estratégicas: `economy`, `Iran`, `conflict`, `Hormuz`, `oil`, `taxes` e `tariffs`.
*   **Arquitetura Assíncrona e Antidup:** Implementação orientada a eventos com controle estrito de ponteiros (`ID` incremental único), garantindo que nenhum post seja processado duas vezes ou exibido em duplicidade.
*   **Mecanismo Anti-Bloqueio (Stealth Mode):** Ignora impressões digitais de automação (`navigator.webdriver`) e manipula os cabeçalhos de rede para emular o comportamento humano, mitigando desafios do Cloudflare.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

*   **Python 3.13+**: Linguagem base do projeto.
*   **Playwright (Async API):** Framework de automação de navegador utilizado para renderizar o ecossistema React/Next.js da rede social e interceptar requisições de rede.
*   **Asyncio:** Biblioteca nativa para gerenciamento de loops de eventos assíncronos e concorrência.
*   **urllib.parse (urljoin):** Utilizado para normalização estrutural de URLs, blindando o script contra falhas de codificação (*encoding*) locais do sistema operacional.
*   **Regular Expressions (re):** Tratamento e limpeza de strings brutas, eliminando tags HTML contidas nos payloads da API.

---
## 📈 Aprendizados Técnicos

### 1. Resolução de Deadlocks de Carregamento
Redes sociais baseadas na arquitetura Mastodon/Next.js realizam conexões WebSocket e carregamentos de mídia infinitos. O uso estratégico de `wait_until="domcontentloaded"` e limites estritos de *timeout* (35 segundos) impediram que o script sofresse congelamento de execução (*deadlocks*).

### 2. Blindagem de Encoding
Durante a fase de desenvolvimento, identificou-se que variações de ambiente no compilador local omitiam o caractere `/` em strings compostas (`com/@`). O problema foi solucionado de forma definitiva substituindo strings estáticas pela montagem dinâmica via `urljoin` e injeção via código ASCII (`chr(47)`).

### 3. Eficiência de Dados
A extração focada na resposta da API (`response.json()`) provou ser **82% mais rápida** do que a varredura tradicional de elementos visuais do DOM (`page.query_selector_all`), além de tornar o software imune a qualquer atualização de design ou interface da Truth Social.

---
## 📈 Resultado:

### Monitoramento Constante:
O sistema monitora postagens do presidente norte-americano, referente ao conflito vigente na data deste repositório, que visam o impacto nos preços de algumas commodities em especial o petróleo.
Essas postagens tem a possibilidade de impactar fortemente o preço da commoditie e por consequência dos ativos financeiro norte-americanos, bem como do restante do mundo (em particular o brasil, devido a sua forte relação entre commodities X economia).


---

## 🔧 Como Executar o Projeto

1. Clone o repositório para sua máquina local.
2. Certifique-se de estar com o ambiente virtual (`.venv`) ativo.
3. Instale as dependências e o motor de renderização do Chromium:
```bash
pip install playwright
python -m playwright install
```
4. Execute o script principal:
```bash
python truth_social.py
```