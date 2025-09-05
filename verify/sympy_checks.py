import re
import sympy as sp

def _extract_number(text: str):
    m = re.search(r"(-?\d+\.?\d*)", text)
    if m:
        try:
            return float(m.group(1))
        except:
            return None
    return None

def verify_answer(problem: str, final_answer_text: str) -> dict:
    mul = re.findall(r"(\d+)\s*[\*xX]\s*(\d+)", problem)
    num = _extract_number(final_answer_text or '')
    if mul and num is not None:
        a,b = map(int, mul[-1])
        gt = a*b
        pass_flag = (abs(num - gt) < 1e-9)
        score = 1.0 if pass_flag else max(0.0, 1.0 - abs(num-gt)/abs(gt) )
        return {'pass': pass_flag, 'score': score, 'rationale': f'expected {gt}, got {num}'}

    if 'radius' in problem and 'chord' in problem:
        nums = re.findall(r"([0-9]+(?:\.[0-9]+)?)", problem)
        if len(nums) >= 2 and num is not None:
            r = float(nums[0]); c = float(nums[1])
            half = c/2.0
            if half > r:
                return {'pass': False, 'score': 0.0, 'rationale': 'invalid geometry: chord > diameter'}
            import math
            gt = math.sqrt(max(0.0, r*r - half*half))
            pass_flag = abs(num - gt) < 1e-6
            score = 1.0 if pass_flag else max(0.0, 1.0 - abs(num-gt)/max(1.0, abs(gt)))
            return {'pass': pass_flag, 'score': score, 'rationale': f'expected {gt:.6f}, got {num}'}

    if num is not None:
        return {'pass': True, 'score': 0.5, 'rationale': 'heuristic numeric present'}

    return {'pass': False, 'score': 0.0, 'rationale': 'no numeric answer found'}
