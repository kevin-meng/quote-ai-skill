# QuoteAI Skill Recipes

These recipes are routing patterns for the Agent. They are not separate server
LLM features. Interpret the user's request first, then call the smallest useful
QuoteAI surface.

## Speech opener

Use when the user wants a memorable opening for a speech or presentation.

Preferred:
- collection: `public-speaking`
- scenario: `speech-opening`
- tones: `inspiring` or `bold`
- limit: 3
- max length: 180

The Agent should choose one candidate and write the transition around it.

## Speech closer

Use when the user wants a reflective ending.

Preferred:
- collection: `life-reflection` or `public-speaking`
- scenario: `speech-closing`
- tones: `reflective`
- limit: 3

## Team meeting opener

Preferred:
- collection: `leadership`
- scenarios: `team-meeting,leadership`
- emotions: `motivated,focused`
- tones: `practical,confident`
- limit: 3

## Social post hook

Preferred:
- scenario: `social-post`
- choose tone from the intended post: `inspiring`, `warm`, `humorous`,
  `reflective`
- max length: 160
- limit: 3

Do not post a quote blindly. The Agent should contextualize it.

## Morning reflection

Preferred:
- scenario: `morning-routine`
- emotions: `hopeful,motivated`
- tone: `uplifting`
- limit: 1

## Night reflection / journal

Preferred:
- scenario: `night-reflection` or `journal`
- emotions: `calm,reflective`
- tones: `calm,reflective`
- limit: 1-3

## Resilience after a setback

Preferred:
- collection: `resilience-courage`
- emotions: `hopeful,motivated`
- tone: `inspiring`
- limit: 3

## Relationship / card message

Preferred:
- collection: `love-relationships`
- scenario: `card-message` or `relationship`
- emotions: `warm,affectionate`
- tone: `warm`
- limit: 3

## Writing inspiration

Preferred:
- collection: `writing-creativity`
- scenario: `reflection` or `journal`
- limit: 3

The quote is source material. The Agent should do the writing itself.

## Decision rule

Prefer:
1. matching collection + metadata filters;
2. `recommend` with metadata filters;
3. `search` only when the user names an author/phrase/topic;
4. `random` only when randomness is explicitly desired.
