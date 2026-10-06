# QuoteAI Skill

[![skills.sh](https://skills.sh/b/kevin-meng/quote-ai-skill)](https://skills.sh/kevin-meng/quote-ai-skill/quote-ai)

Agent Skill for selecting real, reusable quotations from the QuoteAI corpus.

QuoteAI is designed as a **controlled quote-selection layer for AI Agents**:
the Agent understands the user's intent and makes the final semantic choice;
QuoteAI provides curated candidates, stable IDs, Collections and structured
scenario / emotion / tone metadata.

## Install

```bash
npx skills add kevin-meng/quote-ai-skill --skill quote-ai -g -y
```

Or with the full GitHub URL:

```bash
npx skills add https://github.com/kevin-meng/quote-ai-skill --skill quote-ai -g -y
```

## Configure

Set your QuoteAI API key:

```bash
export QUOTEAI_API_KEY=qk_live_...
```

Optional custom endpoint:

```bash
export QUOTEAI_BASE_URL=https://quote-api-sable-two.vercel.app
```

Free accounts currently include:

- 50 API requests / UTC day
- 200 returned quote records / UTC day

The two quotas are independent.

## What the Skill helps an Agent do

- choose real quotations for speeches and presentations;
- select leadership, resilience, creativity, relationship and reflection quotes;
- use scenario / emotion / tone metadata instead of keyword-only search;
- avoid repeating quotations with stable opaque quote IDs;
- use curated Collections;
- record bounded `used`, `liked` and `skipped` feedback;
- avoid bulk corpus extraction and enumeration behavior.

## Repository structure

```text
skills/quote-ai/
├── SKILL.md
├── references/
│   ├── access-policy.md
│   ├── metadata.md
│   └── recipes.md
└── scripts/
    └── quote_ai.py
```

## Example

```bash
python skills/quote-ai/scripts/quote_ai.py recommend \
  --context "opening a Monday team meeting about perseverance" \
  --scenarios team-meeting \
  --emotions motivated \
  --tones inspiring \
  --limit 3
```

The Agent should normally request only a few candidates and make the final
choice itself.

## Access policy

QuoteAI is a selection service, not a corpus export channel. The Skill explicitly
prohibits ID enumeration, search-prefix sweeping, repeated collection sampling,
quota evasion and synthetic feedback manipulation.

See `skills/quote-ai/references/access-policy.md`.

## License

MIT
