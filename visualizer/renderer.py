import re
import ast
import tempfile
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def try_extract_plot_code(text: str):
    if not text:
        return None
    m = re.search(r"```(?:python)?\n([\s\S]+?)\n```", text)
    if m:
        return m.group(1)
    if 'matplotlib' in text or 'plt.' in text:
        return text
    return None

ALLOWED_SUBSTRINGS = [
    'import matplotlib', 'import matplotlib.pyplot', 'plt.', 'fig', 'ax', 'Circle', 'add_patch',
    'plot(', 'scatter(', 'set_aspect', 'savefig', 'show', 'subplots('
]

def _is_safe_code(code: str) -> bool:
    forbidden = ['import os', 'import sys', 'subprocess', 'open(', 'requests', 'socket', 'eval(', 'exec(', '__']
    for f in forbidden:
        if f in code:
            return False
    if not any(s in code for s in ALLOWED_SUBSTRINGS):
        return False
    return True

def safe_execute_plot_code(code: str):
    if not _is_safe_code(code):
        return False, 'unsafe code detected'
    try:
        tmp = tempfile.mkdtemp(prefix='plot_exec_')
        save_path = os.path.join(tmp, 'plot.png')
        safe_code = code.replace('plt.show()', f"plt.savefig(r'{save_path}')")
        exec_globals = {'plt': plt}
        exec(safe_code, exec_globals)
        if os.path.exists(save_path):
            return True, save_path
        files = os.listdir(tmp)
        for fn in files:
            if fn.endswith('.png'):
                return True, os.path.join(tmp, fn)
        return False, 'no image produced'
    except Exception as e:
        return False, str(e)
