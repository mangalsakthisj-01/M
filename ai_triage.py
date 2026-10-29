"""Transparent local rule-based triage; no external AI provider or API key required.

Suggestions support human reviewers only. They do not diagnose disease, confirm outbreaks,
or automatically reject complaints.
"""
from __future__ import annotations
from typing import Any

CATEGORIES = [
    "Sanitation", "Water & drainage", "Vector risk", "Waste dumping",
    "Road & infrastructure", "Public facility", "Other",
]

# Transparent keyword rules: each category has terms that commonly appear in reports.
_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Water & drainage", ("stagnant water", "drain", "sewage", "overflow", "flood", "leakage", "waterlogging")),
    ("Vector risk", ("mosquito", "larvae", "breeding", "vector", "dengue", "malaria")),
    ("Sanitation", ("garbage", "waste", "litter", "smell", "dirty", "sanitation", "unhygienic")),
    ("Waste dumping", ("dumping", "illegal dump", "debris", "rubbish pile")),
    ("Road & infrastructure", ("road", "pothole", "streetlight", "footpath", "broken", "sidewalk", "traffic signal")),
    ("Public facility", ("toilet", "hospital", "school", "bus stop", "public tap", "community hall")),
)


def rules_based_triage(title: str, description: str, category: str, media_count: int = 0) -> dict[str, Any]:
    text = f"{title or ''} {description or ''} {category or ''}".casefold()
    scores = {name: sum(1 for term in terms if term in text) for name, terms in _RULES}
    best = max(scores, key=scores.get) if scores else "Other"
    suggested = best if scores.get(best, 0) else (category if category in CATEGORIES else "Other")
    matched = [term for name, terms in _RULES if name == suggested for term in terms if term in text]
    missing: list[str] = []
    if not (description or "").strip():
        missing.append("Add a concise description of what was observed.")
    if media_count == 0:
        missing.append("Optional photo evidence, if safe and appropriate to capture.")
    explanation = (
        f"Local keyword rules suggested '{suggested}' based on: {', '.join(matched[:5])}."
        if matched else "No strong keyword match was found; the selected category is retained for human review."
    )
    return {
        "provider": "rules-based-fallback", "suggested_category": suggested,
        "confidence": None, "explanation": explanation,
        "review_status": "NEEDS_HUMAN_REVIEW", "missing_evidence": missing,
        "visible_hazards": [], "possible_duplicate": False,
        "safety_notice": "Triage support only. This is not a medical diagnosis or proof that an outbreak is confirmed.",
    }


def analyze_image(content: bytes, mime_type: str, title: str, description: str, category: str) -> dict[str, Any]:
    """Image uploads are validated/stored elsewhere; this local triage never claims to inspect pixels."""
    return rules_based_triage(title, description, category, media_count=1 if content else 0)


def analyze_text(title: str, description: str, category: str, media_count: int = 0) -> dict[str, Any]:
    return rules_based_triage(title, description, category, media_count)
