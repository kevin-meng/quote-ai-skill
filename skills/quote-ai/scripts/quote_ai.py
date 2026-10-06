#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import uuid

BASE_URL = os.getenv("QUOTEAI_BASE_URL", "https://quote-api-sable-two.vercel.app").rstrip("/")
API_KEY = os.getenv("QUOTEAI_API_KEY")


def request(path, params=None, method="GET", payload=None):
    if not API_KEY:
        raise SystemExit("QUOTEAI_API_KEY is required")
    url = BASE_URL + path
    if params:
        clean = {k: v for k, v in params.items() if v not in (None, "", [])}
        url += "?" + urllib.parse.urlencode(clean)
    body = None
    headers = {
        "X-API-Key": API_KEY,
        "Accept": "application/json",
        "User-Agent": "QuoteAI-Skill/1.6",
    }
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    parser = argparse.ArgumentParser(prog="quote_ai")
    sub = parser.add_subparsers(dest="command", required=True)

    rec = sub.add_parser("recommend")
    rec.add_argument("--context", required=True)
    rec.add_argument("--tags", default="")
    rec.add_argument("--scenarios", default="")
    rec.add_argument("--emotions", default="")
    rec.add_argument("--tones", default="")
    rec.add_argument("--category")
    rec.add_argument("--limit", type=int, default=3)
    rec.add_argument("--max-length", type=int)
    rec.add_argument("--exclude-ids", default="")
    rec.add_argument("--lang", default="en", choices=["en", "zh", "both"])

    search = sub.add_parser("search")
    search.add_argument("--query", required=True)
    search.add_argument("--limit", type=int, default=5)
    search.add_argument("--lang", default="en", choices=["en", "zh", "both"])

    daily = sub.add_parser("daily")
    daily.add_argument("--lang", default="en", choices=["en", "zh", "both"])
    daily.add_argument("--time-slot", choices=["morning", "night"])

    rnd = sub.add_parser("random")
    rnd.add_argument("--lang", default="en", choices=["en", "zh", "both"])
    rnd.add_argument("--category")
    rnd.add_argument("--time-slot", choices=["morning", "night"])

    sub.add_parser("categories")
    sub.add_parser("collections")

    coll = sub.add_parser("collection")
    coll.add_argument("slug")
    coll.add_argument("--limit", type=int, default=5)
    coll.add_argument("--scenarios", default="")
    coll.add_argument("--emotions", default="")
    coll.add_argument("--tones", default="")
    coll.add_argument("--lang", default="en", choices=["en", "zh", "both"])

    fb = sub.add_parser("feedback")
    fb.add_argument("quote_id")
    fb.add_argument("event_type", choices=["used", "liked", "skipped"])
    fb.add_argument("--event-id")
    fb.add_argument("--subject-id")
    fb.add_argument("--context")

    args = parser.parse_args()

    if args.command == "recommend":
        data = request("/api/v1/quotes/recommend", {
            "context": args.context,
            "tags": args.tags,
            "scenarios": args.scenarios,
            "emotions": args.emotions,
            "tones": args.tones,
            "category": args.category,
            "limit": args.limit,
            "max_length": args.max_length,
            "exclude_ids": args.exclude_ids,
            "lang": args.lang,
        })
    elif args.command == "search":
        data = request("/api/v1/quotes/search", {
            "q": args.query, "limit": args.limit, "lang": args.lang
        })
    elif args.command == "daily":
        data = request("/api/v1/quotes/daily", {
            "lang": args.lang, "time_slot": args.time_slot
        })
    elif args.command == "random":
        data = request("/api/v1/quotes/random", {
            "lang": args.lang,
            "category": args.category,
            "time_slot": args.time_slot,
        })
    elif args.command == "collections":
        data = request("/api/v1/collections")
    elif args.command == "collection":
        data = request(f"/api/v1/collections/{urllib.parse.quote(args.slug)}", {
            "limit": args.limit,
            "scenarios": args.scenarios,
            "emotions": args.emotions,
            "tones": args.tones,
            "lang": args.lang,
        })
    elif args.command == "feedback":
        data = request("/api/v1/feedback", method="POST", payload={
            "quote_id": args.quote_id,
            "event_type": args.event_type,
            "event_id": args.event_id or str(uuid.uuid4()),
            "subject_id": args.subject_id,
            "context": args.context,
        })
    else:
        data = request("/api/v1/categories")

    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
