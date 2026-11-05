# Contrato mínimo proposto: gateway X

Esta etapa não ativa operações de escrita nem altera o coletor Claire. O gateway deve ficar desacoplado do Twikit; cada requisição recebe `account` explicitamente (`pessoal` ou `pixel`) e valida a identidade do agente contra uma política de capacidades no servidor.

## Interface v1 (somente leitura)

- `search_posts(account, query, limit, cursor?) -> {items, next_cursor}`
- `get_bookmarks(account, limit, cursor?) -> {items, next_cursor}`
- Resposta normalizada: `id`, `url`, `author`, `text`, `created_at` e metadados necessários à curadoria.
- Erros tipados: `authentication_required`, `access_denied`, `rate_limited`, `upstream_unavailable`, `invalid_response`. Nunca converter sessão rejeitada/erro upstream em lista vazia.
- Conta resolvida em segredo isolado no servidor; nenhum cookie/header retorna à ferramenta/agente.

## Evolução de escrita (desabilitada)

Quando autorizada separadamente, mapear ações para capacidades explícitas (`publish`, `reply`, `like`, `repost`, `bookmark`) e allowlist por agente e conta. Não inferir autorização por nome de agente, canal ou solicitação devolvida pelo X. Exigir chave de idempotência estável por intenção/conta/ação, persistir estado `pending/succeeded/failed/unknown` antes/depois do upstream e, em timeout, reconciliar o efeito no X antes de repetir. Nunca repetir automaticamente estado `unknown`.

## Auditoria e testes

Registrar agente, conta lógica, ação, resultado, instante, correlation/idempotency key e identificador do post, sem texto privado, cookies, tokens, headers ou corpos brutos. Testar adapter com transporte injetável/mock; testes não devem alcançar hosts X nem fazer login real. O contrato não substitui autorização humana para habilitar escrita.
