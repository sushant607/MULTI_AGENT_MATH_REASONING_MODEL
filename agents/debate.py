import json
import re
from agents.policy_llm import LLM
from agents.roles import PROPOSER_PROMPT, CRITIC_PROMPT, OPTIMIZER_PROMPT
from verify.sympy_checks import verify_answer
from visualizer.renderer import safe_execute_plot_code, try_extract_plot_code
from datetime import datetime

class DebateSystem:
    def __init__(self, llm_name='stub'):
        self.llm = LLM(name=llm_name)

    def _tolerant_parse(self, text: str) -> dict:
        try:
            return json.loads(text)
        except Exception:
            out = {}
            m = re.search(r"'final'\s*:\s*'([^']+)'", text)
            if not m:
                m = re.search(r'"final"\s*:\s*"([^"]+)"', text)
            if m:
                out['final'] = m.group(1)
            steps = re.findall(r"\[(?:'|\")([^\]]+?)(?:'|\")\]", text)
            if steps:
                out['steps'] = [s.strip() for s in steps[0].split(',')]
            return out

    def run_debate(self, problem_text: str, problem_id: str = None):
        pid = problem_id or f"pid_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f') }"
        prop_raw = self.llm.generate(PROPOSER_PROMPT, problem_text)
        prop = self._tolerant_parse(prop_raw)
        critic_input = f"Problem: {problem_text}\nProposer: {prop_raw}"
        crit_raw = self.llm.generate(CRITIC_PROMPT, critic_input)
        crit = self._tolerant_parse(crit_raw)
        opt_input = f"Problem: {problem_text}\nProposer: {prop_raw}\nCritic: {crit_raw}"
        opt_raw = self.llm.generate(OPTIMIZER_PROMPT, opt_input)
        opt = self._tolerant_parse(opt_raw)
        final_answer = opt.get('final') or opt.get('solution') or ''
        if isinstance(final_answer, list):
            final_answer = final_answer[-1]
        verification = verify_answer(problem_text, final_answer)
        plot_code = try_extract_plot_code(opt_raw) or try_extract_plot_code(prop_raw)
        image_path = None
        plot_exec_result = None
        if plot_code:
            ok, out = safe_execute_plot_code(plot_code)
            if ok:
                image_path = out
                plot_exec_result = {'ok': True, 'path': image_path}
            else:
                plot_exec_result = {'ok': False, 'error': out}
        trace = {
            'problem_id': pid,
            'problem': problem_text,
            'proposer_raw': prop_raw,
            'proposer': prop,
            'critic_raw': crit_raw,
            'critic': crit,
            'optimizer_raw': opt_raw,
            'optimizer': opt,
            'verification': verification,
            'plot': plot_exec_result,
        }
        return trace
