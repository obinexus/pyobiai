"""Verb-Noun knowledge capsule implementation."""

from typing import Dict, Any, Optional
import math


class VerbNounCapsule:
    """Representation of a verb-noun pair with cost and constraints."""

    def __init__(self, verb: str, noun: str, context: Optional[Dict[str, Any]] = None):
        self.action = verb
        self.object = noun
        self.context = context or {}
        self.cost_weight = self.calculate_cost(verb, noun, self.context)
        self.schema_constraints = self.derive_constraints(verb, noun)

    def calculate_cost(self, verb: str, noun: str, context: Dict[str, Any]) -> float:
        """Calculate conceptual cost using simple string metrics."""
        verb_score = sum(ord(c) for c in verb)
        noun_score = sum(ord(c) for c in noun)
        diff = abs(verb_score - noun_score) / 1000.0
        context_entropy = math.log(len(context) + 1, 2)
        return diff + context_entropy

    def derive_constraints(self, verb: str, noun: str) -> Dict[str, Any]:
        """Derive basic schema constraints from the verb and noun."""
        return {
            "action_type": "dynamic" if verb.endswith("ing") else "static",
            "object_required": noun.lower(),
            "relationship": f"{verb}_{noun}",
        }
