import json

from ipykernel.kernelbase import Kernel
from pexpect.replwrap import REPLWrapper

REPL = REPLWrapper("goal", "  ", None)

goal_version = REPL.run_command('''rt.get"v"''').strip()

class GoalKernel(Kernel):
    implementation = "Goal"
    implementation_version = "1.0"
    language = "no-op"
    language_version = "0.1"
    language_info = {
        "name": "goal",
        "mimetype": "text/plain",
        "file_extension": ".goal",
    }
    banner = f"Goal array programming language kernel (version {goal_version})"

    def do_execute(
        self, code, silent, store_history=True, user_expressions=None, allow_stdin=False
    ):
        if not silent:
            output = REPL.run_command(code)
            stream_content = {"name": "stdout", "text": output}
            self.send_response(self.iopub_socket, "stream", stream_content)

        return {
            "status": "ok",
            # The base class increments the execution count
            "execution_count": self.execution_count,
            "payload": [],
            "user_expressions": {},
        }

    def do_complete(self, code, cursor_pos):
        goal_code = f"""""json {{gs:,/rt.get'!"! kw";ms:?["s"=@x;(..p.x%p.gs)#gs;[(..p.x@p.gs)#gs]]; ms@<_ms }}["{code}*"]"""  # using say pollutes STDOUT handling
        status = "ok"
        completions = []
        try:
            goal_eval = REPL.run_command(goal_code)
            # The output of evaluating the Goal program is an encoded JSON string of an encoded JSON array,
            # thus requiring the double json.loads calls. Using `say` from Goal solves this problem,
            # but also pollutes STDOUT handling, such that completion results were showing up in the
            # main console instead of in the auto-complete popup. Given this is small data, it's fast enough.
            completions = json.loads(json.loads(goal_eval))
        except Exception:
            status = "error"
        content = {
            "status": status,
            "matches": completions,
            # The range of text that should be replaced by the above matches when a completion is accepted.
            # typically cursor_end is the same as cursor_pos in the request.
            "cursor_start": cursor_pos - 1,
            "cursor_end": cursor_pos,
            "metadata": {},
        }
        return content
