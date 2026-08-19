"""Deterministic safety analysis used when Amazon Bedrock is unavailable.

The demo should continue to turn an uploaded protocol into explainable course
recommendations even when cloud credentials expire or the model is throttled.
This module intentionally uses a small, auditable ruleset instead of pretending
that a failed AI request succeeded.
"""

from __future__ import annotations

import re
from typing import Dict, Iterable, List, Sequence


COURSE_RULES = {
    "HAZCOM-1910.1200": {
        "terms": ("chemical", "chemicals", "hazard communication", "sds", "safety data sheet", "ghs", "labeling", "solvent"),
        "roles": ("lab_tech", "chem_researcher", "facilities_maintenance", "radiation_worker"),
        "priority": "high", "renewal_months": 12, "deadline_days": 14,
    },
    "PPE-201": {
        "terms": ("ppe", "personal protective", "protective equipment", "gloves", "goggles", "eye protection", "face shield"),
        "roles": ("lab_tech", "chem_researcher", "facilities_maintenance", "forklift_operator", "radiation_worker"),
        "priority": "high", "renewal_months": 12, "deadline_days": 14,
    },
    "FIRE-101": {
        "terms": ("fire safety", "fire prevention", "fire extinguisher", "extinguisher", "combustible", "flammable", "evacuation"),
        "roles": (), "priority": "high", "renewal_months": 12, "deadline_days": 14,
    },
    "CHEM-SPILL-110": {
        "terms": ("chemical spill", "spill response", "spill", "leak", "neutralization", "decontamination"),
        "roles": ("lab_tech", "chem_researcher", "facilities_maintenance", "radiation_worker"),
        "priority": "critical", "renewal_months": 12, "deadline_days": 7,
    },
    "LAB-SAFETY-101": {
        "terms": ("laboratory", "lab safety", "laboratory safety", "fume hood", "chemical hygiene", "lab protocol"),
        "roles": ("lab_tech", "chem_researcher", "radiation_worker"),
        "priority": "high", "renewal_months": 12, "deadline_days": 14,
    },
    "BIOSAFETY-BSL1": {
        "terms": ("biosafety", "biological material", "microorganism", "bacteria", "cell culture", "biohazard"),
        "roles": ("lab_tech", "chem_researcher"),
        "priority": "high", "renewal_months": 12, "deadline_days": 14,
    },
    "BIOSAFETY-BSL2": {
        "terms": ("bsl-2", "bsl 2", "pathogen", "infectious material", "virus", "sharps", "access control"),
        "roles": ("lab_tech", "chem_researcher"),
        "priority": "critical", "renewal_months": 12, "deadline_days": 7,
    },
    "BBP-1910.1030": {
        "terms": ("bloodborne", "blood", "bodily fluid", "needle", "needlestick", "sharps", "post-exposure"),
        "roles": ("lab_tech", "chem_researcher"),
        "priority": "critical", "renewal_months": 12, "deadline_days": 7,
    },
    "IDP-101": {
        "terms": ("infectious disease", "respiratory pathogen", "infection prevention", "virus", "pandemic", "ventilation"),
        "roles": (), "priority": "high", "renewal_months": 12, "deadline_days": 14,
    },
    "RESPIRATOR-QUAL-130": {
        "terms": ("respirator", "respiratory protection", "fit test", "airborne", "inhalation"),
        "roles": ("lab_tech", "chem_researcher", "facilities_maintenance", "radiation_worker"),
        "priority": "critical", "renewal_months": 12, "deadline_days": 7,
    },
    "FORKLIFT-OP-120": {
        "terms": ("forklift", "powered industrial truck", "pallet truck", "load handling"),
        "roles": ("forklift_operator", "facilities_maintenance"),
        "priority": "critical", "renewal_months": 36, "deadline_days": 7,
    },
    "RADIATION-ALARA-101": {
        "terms": ("radiation", "radioactive", "ionizing", "dosimetry", "alara", "x-ray", "x ray"),
        "roles": ("radiation_worker", "lab_tech", "chem_researcher"),
        "priority": "critical", "renewal_months": 12, "deadline_days": 7,
    },
    "LASER-CLASS-2-3R": {
        "terms": ("laser", "beam alignment", "class 2 laser", "class 3r"),
        "roles": ("radiation_worker", "lab_tech", "chem_researcher"),
        "priority": "high", "renewal_months": 12, "deadline_days": 14,
    },
    "LOTO-1910.147": {
        "terms": ("lockout", "tagout", "loto", "energy isolation", "hazardous energy", "machine maintenance"),
        "roles": ("facilities_maintenance", "forklift_operator"),
        "priority": "critical", "renewal_months": 12, "deadline_days": 7,
    },
    "LADDER-101": {
        "terms": ("ladder", "fall protection", "scaffold", "working at height", "roof work"),
        "roles": ("facilities_maintenance",),
        "priority": "high", "renewal_months": 12, "deadline_days": 14,
    },
    "HEAT-ILLNESS-CA-3395": {
        "terms": ("heat illness", "heat stress", "high heat", "outdoor work", "hydration", "acclimatization"),
        "roles": ("facilities_maintenance", "forklift_operator"),
        "priority": "high", "renewal_months": 12, "deadline_days": 14,
    },
    "ERG-101": {
        "terms": ("ergonomic", "ergonomics", "computer workstation", "repetitive strain", "neutral posture"),
        "roles": ("office_worker",),
        "priority": "normal", "renewal_months": 24, "deadline_days": 30,
    },
    "WASTE-HAZ-DOT-100": {
        "terms": ("hazmat shipping", "shipping papers", "dangerous goods", "hazardous material shipping", "dot hazmat"),
        "roles": ("lab_tech", "chem_researcher", "forklift_operator"),
        "priority": "high", "renewal_months": 36, "deadline_days": 14,
    },
    "HAZWOPER-40": {
        "terms": ("hazwoper", "hazardous waste operation", "emergency response site", "uncontrolled hazardous waste"),
        "roles": ("lab_tech", "chem_researcher", "facilities_maintenance"),
        "priority": "critical", "renewal_months": 12, "deadline_days": 7,
    },
}


def _contains_term(text: str, term: str) -> bool:
    if len(term) <= 3:
        return re.search(rf"\b{re.escape(term)}\b", text) is not None
    return term in text


def analyze_protocol_locally(protocol_text: str, user_data: Dict, courses: Sequence[Dict], error: str = "") -> Dict:
    """Return explainable recommendations without any external service."""
    text = " ".join(protocol_text.lower().split())
    role = str(user_data.get("role", "")).lower()
    available_ids = {str(course.get("course_id")) for course in courses}
    matches: List[Dict] = []
    matched_terms: List[str] = []

    for course_id, rule in COURSE_RULES.items():
        if course_id not in available_ids:
            continue
        terms = [term for term in rule["terms"] if _contains_term(text, term)]
        if not terms:
            continue
        allowed_roles: Iterable[str] = rule["roles"]
        if allowed_roles and role not in allowed_roles:
            continue
        matches.append({
            "course_id": course_id,
            "priority": rule["priority"],
            "renewal_months": rule["renewal_months"],
            "deadline_days": rule["deadline_days"],
        })
        matched_terms.extend(terms[:2])

    priority_order = {"critical": 0, "high": 1, "normal": 2, "low": 3}
    matches.sort(key=lambda item: (priority_order[item["priority"]], item["course_id"]))
    matches = matches[:6]

    if matches:
        course_names = ", ".join(item["course_id"] for item in matches)
        reason = (
            f"The protocol contains role-relevant safety requirements "
            f"({', '.join(dict.fromkeys(matched_terms[:5]))}); recommended training: {course_names}."
        )
    else:
        reason = "No role-relevant course trigger was found in the extracted protocol text."

    return {
        "should_assign": bool(matches),
        "recommended_courses": matches,
        "reason": reason,
        "analysis_source": "local-safety-rules",
        "analysis_warning": "Cloud AI was unavailable; verified local safety rules were used." if error else "",
    }
