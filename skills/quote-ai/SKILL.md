---
name: quote-ai
description: Select reusable famous quotations from the QuoteAI corpus for speeches, writing, scheduled messages, social content, reflection and other Agent workflows. Use when the user explicitly wants quotations or a controlled quote corpus. Do not use merely to generate an original inspirational sentence.
license: MIT
metadata:
  homepage: https://github.com/kevin-meng/quote-ai-skill
  source: QuoteAI
---

# QuoteAI Skill

QuoteAI is a corpus service for AI Agents. The Agent interprets intent; QuoteAI
provides reusable quote records, IDs, collections and metadata. The server does
not call an LLM.

## Install

```bash
npx skills add kevin-meng/quote-ai-skill --skill quote-ai -g -y
```

## Configuration

Set:
- `QUOTEAI_API_KEY`: QuoteAI API key
- `QUOTEAI_BASE_URL`: optional, defaults to `https://quote-api-sable-two.vercel.app`

Free keys allow:
- **50 API calls per UTC day**
- **200 returned quote records per UTC day**

These are separate quotas.

## When to use

Use QuoteAI when the user:
- explicitly asks for a real/famous quotation;
- wants quotes from a controlled corpus rather than generated prose;
- wants several candidates to choose from;
- needs stable opaque quote UUIDs for no-repeat workflows;
- wants daily/scheduled quote content;
- wants author/category/tag/scenario/emotion/tone metadata;
- wants a curated collection such as leadership, Stoicism or public speaking.

Do not call QuoteAI when:
- the user only wants an original motivational sentence;
- a quote is incidental and a sourced quotation was not requested;
- the model can complete the task better without an external corpus.

## Preferred workflow

1. Interpret the user's goal yourself.
2. Read `references/recipes.md` when the request maps to a common scenario.
3. Prefer a relevant Collection when one exists.
4. Otherwise convert intent into a small set of scenario/emotion/tone/tag filters.
5. Request only 1-5 candidates.
6. Make the final semantic choice yourself.
7. Keep quote IDs needed by the workflow and use returned opaque UUIDs with `exclude_ids` to avoid repeats.
8. When a quote is actually used, record `used` feedback. Record `liked` or `skipped` only when the user clearly signals that preference; never infer it from silence.

Read `references/metadata.md` for the supported vocabulary.

## Corpus access discipline

QuoteAI is a selection service, not a bulk export API.

Never:
- guess or enumerate quote identifiers;
- vary search prefixes to reconstruct the corpus;
- repeatedly sample a collection to acquire the full dataset;
- retry after a corpus output-limit error;
- rotate keys to evade limits.

Collection endpoints intentionally do not expose pagination.

Read `references/access-policy.md` for the packaged access policy and
anti-enumeration rules.

## Helper commands

```bash
python scripts/quote_ai.py recommend \
  --context "opening a Monday team meeting about perseverance" \
  --scenarios team-meeting \
  --emotions motivated \
  --tones inspiring \
  --limit 3

python scripts/quote_ai.py collections
python scripts/quote_ai.py collection leadership --scenarios team-meeting --limit 3
python scripts/quote_ai.py search --query "courage" --limit 5
python scripts/quote_ai.py daily --lang zh
python scripts/quote_ai.py random --category wisdom
python scripts/quote_ai.py feedback 550e8400-e29b-41d4-a716-446655440000 used
```

## Agent-oriented endpoint

```http
GET /api/v1/quotes/recommend
  ?context=<natural-language-context>
  &tags=<comma-separated-tags>
  &scenarios=<comma-separated-scenarios>
  &emotions=<comma-separated-emotions>
  &tones=<comma-separated-tones>
  &category=<optional-category>
  &limit=3
  &max_length=180
  &exclude_ids=550e8400-e29b-41d4-a716-446655440000
  &lang=en
```

The response contains `meta.server_llm=false`. The Agent remains responsible
for semantic interpretation and the final choice.

## Collections

- `GET /api/v1/collections`
- `GET /api/v1/collections/{slug}?limit=5&scenarios=...&emotions=...&tones=...`

Collection results are sampled and non-pageable by design.

## Other endpoints

- `GET /api/v1/quotes/search?q=...`
- `GET /api/v1/quotes/{uuid}`
- `GET /api/v1/quotes/daily`
- `GET /api/v1/quotes/random`
- `GET /api/v1/categories`

## Feedback loop

After a quote is actually selected for user-facing output:

- send `used`;
- send `liked` only after explicit positive preference;
- send `skipped` only after explicit rejection / not-useful feedback;
- generate a fresh event UUID for each real event;
- retries must reuse the same event UUID so the server can de-duplicate them.

Endpoint:

```http
POST /api/v1/feedback
Content-Type: application/json
X-API-Key: qk_live_...

{
  "quote_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "used",
  "event_id": "7a506b74-67fc-4df5-b4d8-561657d1aa83",
  "subject_id": "optional-client-local-user-id",
  "context": "team meeting opener"
}
```

Feedback is a weak ranking signal. The Agent must not spam events to influence
ranking.
