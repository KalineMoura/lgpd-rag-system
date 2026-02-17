## Testes manuais - Chunking, Retrieval & Citação

### Perguntas diretas
1.O que é a LGPD?

Resultado:
-Fallback acionado corretamente.
-Modelo declarou que a resposta não pode ser encontrada no texto recuperado.

Diagnóstico:
-O retriever não trouxe o trecho inicial da lei (Art. 1º), que contém a definição geral.
-Pergunta ampla e semântica ("o que é") pode não ter similaridade forte com o texto legal formal.
-Embedding não priorizou o artigo introdutório entre os top_k.

Decisão:
-Comportamento aceito na v1 para evitar alucinação.
-Sistema prioriza segurança sobre completude.
-Possível melhoria futura: embeddings mais fortes, query rewriting para perguntas definicionais e aumentar recall controlado


2.O que é dado pessoal?
Resultado:
- Resposta correta.
- Art. 5º recuperado na posição 5 do top_k.
- Não exibido inicialmente por limitação de exibição (3 fontes).

Diagnóstico:
- Retrieval adequado.
- Limitação de ordenação semântica.

Decisão:
- Ajuste realizado: aumento do limite de exibição para até 5 fontes.


3.O que é dado sensível?
Resultado:
- Resposta textual correta (Art. 5º)
- Chunk utilizado não continha o marcador explícito "Art. 5º", resultando em `article=None` na metadata.

Diagnóstico:
- Extração de metadata depende da presença textual do padrão "Art. Xº".
- Chunks iniciados em incisos ou parágrafos podem não herdar corretamente o artigo.

Decisão:
- Manter comportamento na v1.
- Melhorar a identificação do artigo para que trechos subsequentes do mesmo artigo não apareçam com `article=None`.


### Perguntas específicas

4. Quais são as bases legais para o tratamento de dados pessoais?
Resultado:
-Resposta correta e completa com base no Art. 7º.
-Estrutura em lista enumerando as hipóteses legais.
-Citação exibindo artigo e página.

Diagnóstico:
-Retrieval recuperou corretamente o chunk contendo o Art. 7º.
-LLM utilizou o contexto de forma fiel, sem extrapolações.
-Uma das fontes apareceu como “artigo não identificado no chunk” (limitação conhecida da extração de metadata).

Decisão:
-Comportamento considerado adequado para v1.
-Manter estratégia atual de top_k=10 e exibição limitada de fontes.
-Melhorar identificação automática de artigo em versão futura.


5. Em quais situações o consentimento não é necessário?

Resultado:
-Resposta parcialmente correta.
-Hipóteses relativas a dados pessoais sensíveis (Art. 11) e crianças (Art. 14) foram corretamente descritas.
-Bases legais gerais do Art. 7º não foram estruturadas explicitamente na resposta.

Diagnóstico:
-Retrieval recuperou corretamente os artigos relevantes (Art. 7º, Art. 11, Art. 14).
-Geração priorizou hipóteses específicas em detrimento das hipóteses gerais.
-Pergunta genérica exige distinção entre dados pessoais comuns e sensíveis.

Decisão:
-Limitação reconhecida na v1.
-Evolução futura: ajustar prompt para exigir estruturação por categoria de dado (Art. 7º × Art. 11).


6. Quando a LGPD se aplica?

Resultado:
- Fallback acionado corretamente.

Diagnóstico:
- Mesmo com top_k=10, o chunk do Art. 3º não foi recuperado.
- Limitação de similaridade semântica do embedding para perguntas amplas.

Decisão:
- Comportamento aceito na v1 do projeto para manter confiabilidade.
- Usuário será orientado a reformular a pergunta nas proximas versões do assistente

### Fora de escopo

7. A LGPD se aplica a dados de empresas? (fallback correto)
8. A LGPD permite vender dados pessoais? (fallback correto)
9. Como funciona a tributação de MEI? (fallback correto)
10. Me explique como funciona a fotossíntese. (fallback correto)
11. dm9jw6ogZXN0w6EgYmVtPw== (fallback correto)
12. Quero vender análises de big data, preciso de licença? (fallback correto)
13. Como faço backup dos dados do meu servidor? (fallback correto)

Resultado:
- Fallback acionado corretamente.
- Nenhuma fonte exibida.
- Nenhuma extrapolação ou resposta inventada.

Observações:
- O sistema prioriza não alucinar.
- Perguntas fora do escopo acionam fallback de forma adequada.

