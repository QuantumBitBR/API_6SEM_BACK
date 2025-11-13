chat_template = f"""
---
**Contextualização:**

O objetivo deste processo é gerar um **único relatório consolidado** sobre o histórico de reclamações dos usuários para o suporte de uma empresa. 
Enviarei uma lista contendo informações dessas reclamações com diferentes datas e produtos. Com esses dados consolidados, 
você deverá gerar um relatório formal e padronizado que ofereça uma visão geral da situação das reclamações.

---
**Definição de Padrões:**

Para garantir a consistência dos relatórios, siga as seguintes instruções:

**Template:** O template abaixo define a estrutura de cada relatório. Não crie tópicos fora desta estrutura para manter o padrão.

**Dados:** Os dados serão enviados através de um dataframe, contendo informações específicas que deverão ser incorporadas ao relatório conforme o template.

**Formato de Resposta:** Todas as suas respostas devem ser formatadas em Markdown.

**Envio:** Cada relatório deve ser gerado individualmente, seguindo o template fornecido.

---
**Observações sobre o Template:**

* **Edição de Campos:** Os campos entre `<>` devem ser editados com as informações correspondentes da lista de dados fornecida. Observe que os placeholders seguem o formato `<campo: nome_do_campo>`, indicando qual campo dos seus dados deve ser utilizado. A estrutura do relatório abaixo define como esses campos estão organizados por tópicos, agrupando informações relacionadas.
* **Formato de Saída:** Retorne sempre a resposta em formato Markdown.

---
**Template:**

## Relatório de Chamados - <campo: report_name>

### Descrição da Situação:
Com base nos dados fornecidos, crie uma breve descrição do relatório, incluindo informações como tópicos abordados e principais características observadas.

### Informações sobre prioridade:
* Categoria com maior número de reclamações: <campo: top_complaint_category>
* Produto mais reclamado: <campo: top_complaint_product>
* Mês com maior número de reclamações: <campo: top_complaint_month>
* Total de reclamações: <campo: total_complaints>

### Recomendações:
Com base na análise dos dados, apresente no máximo 5 recomendações em formato de tópicos para identificar produtos e empresas com maiores números de reclamações.
"""

