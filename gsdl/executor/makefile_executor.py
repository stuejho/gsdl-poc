import subprocess

from gsdl.executor import ExecutionResult
from gsdl.executor.i_executor import IExecutor


class MakefileExecutor(IExecutor):
    build_dir: str

    def __init__(
        self,
        build_dir: str,
        build_command_args: list[str],
        run_command_args: list[str],
        template_file_path: str,
        benchmark_file_path: str,
    ):
        self.build_dir = build_dir
        self.build_command_args = build_command_args
        self.run_command_args = run_command_args
        self.template_file_path = template_file_path
        self.benchmark_file_path = benchmark_file_path

    def execute(self, run_id: str, code: str) -> ExecutionResult:
        with open(self.template_file_path, "r") as template_file:
            template_code = template_file.read()

        impl_code = template_code.replace("{{ benchmark_code }}", code)

        with open(self.benchmark_file_path, "w") as benchmark_file:
            benchmark_file.write(impl_code)

        subprocess.run(
            self.build_command_args,
            cwd=self.build_dir,
            stdout=subprocess.DEVNULL,
            stderr=None,
        )

        result = subprocess.run(
            self.run_command_args,
            cwd=self.build_dir,
            stdout=None,
            stderr=None,
            capture_output=True,
        )

        return ExecutionResult(
            id=run_id, code=code, result=result.stdout.decode("utf-8")
        )
