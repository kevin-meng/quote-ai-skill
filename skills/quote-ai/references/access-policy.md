# QuoteAI Agent Access Policy

QuoteAI is a quote-selection service, not a corpus-export service.

## Agent rules

Request only the smallest useful candidate set, normally 1-5 quotes.

Never:
- guess, enumerate or infer quote UUIDs;
- sweep search prefixes, tags, authors or collections to reconstruct the corpus;
- repeatedly sample a collection to accumulate the entire dataset;
- rotate API keys or accounts to evade request or quote-output limits;
- retry after a corpus-output-limit response until the quota resets;
- send synthetic feedback merely to manipulate ranking.

Prefer:
- a curated Collection when it matches the task;
- scenario/emotion/tone filters for Agent context;
- `exclude_ids` for legitimate no-repeat workflows;
- `used` feedback only after a quote is actually selected;
- `liked` or `skipped` only after explicit user preference.

## Server-side protections

The service enforces:
- opaque public quote UUIDs;
- small per-call result caps;
- independent request and quote-output quotas;
- account-level quote-output quotas across multiple API keys;
- non-pageable Collection sampling;
- escaped wildcard search behavior;
- no endpoint for enumerating all quote IDs.

These controls apply to paid plans as well. Higher quotas increase legitimate
usage capacity; they do not grant bulk corpus-export rights.
