def build_verification_prompt(answer, sources):
    evidence = []

    for i, s in enumerate(sources, 1):
        evidence.append(f"[{i}] {s['text']}")

    evidence_text = "\n\n".join(evidence)

    prompt = f"""
You are a scientific fact-checking assistant.

Task:
Verify whether the ANSWER is fully supported by the EVIDENCE.

Rules:
- If all claims are supported, say "VERIFIED".
- If any claim is unsupported, list them explicitly.
- Do NOT add new information.
- Be strict and conservative.

EVIDENCE:
{evidence_text}

ANSWER:
{answer}

Verification result:
"""

    return prompt
