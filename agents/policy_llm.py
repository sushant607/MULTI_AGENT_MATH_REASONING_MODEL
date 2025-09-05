import re
import random

class LLM:
    """A minimal stub for the LLM. It tries to detect simple arithmetic/multiplication patterns
    and returns formatted pseudo-JSON strings for each role.
    Replace `generate` with real model generation when ready.
    """
    def __init__(self, name='stub'):
        self.name = name

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        text = user_prompt
        mul = re.findall(r"(\d+)\s*[\*xX]\s*(\d+)", text)
        nums = re.findall(r"([0-9]+(?:\.[0-9]+)?)", text)

        if 'Propose' in system_prompt or 'propose' in system_prompt.lower() or 'proposer' in system_prompt.lower():
            if mul:
                a,b = map(int, mul[-1])
                prod = a*b
                return f"{{ 'steps': [ 'Compute {a} * {b} = {prod}' ], 'final': '{prod}' }}"
            if 'radius' in text and 'chord' in text:
                r = float(nums[0]) if nums else 5.0
                c = float(nums[1]) if len(nums)>1 else 8.0
                half = c/2.0
                d = (r*r - half*half)**0.5
                return f"{{ 'steps': [ 'r = {r}', 'c = {c}', 'half = {half}', 'd = sqrt(r^2 - half^2) = {d:.6f}' ], 'final': '{d:.6f}' }}"
            candidate = random.choice([42, 0])
            return f"{{ 'steps': ['I translated the problem to equations and solved it.'], 'final': '{candidate}' }}"

        if 'critic' in system_prompt.lower():
            if mul:
                return "{ 'issues': ['Check multiplication step explicitly.'], 'fixes': ['Verify 12*9 = 108.'] }"
            return "{ 'issues': ['Solution is terse or missing verification.'], 'fixes': ['Show intermediate checks.'] }"

        if 'optimizer' in system_prompt.lower():
            if mul:
                a,b = map(int, mul[-1])
                prod = a*b
                return f"{{ 'solution': [ 'Compute {a} * {b} = {prod}' ], 'final': '{prod}' }}"
            return "{ 'solution': ['Consolidated steps.'], 'final': '0' }"

        return "{ 'out': 'no-op' }"
