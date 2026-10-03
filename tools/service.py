import ast
import os
import platform
import subprocess
import sys
from pathlib import Path
from functools import wraps

from security.audit import AuditLogger
from security.permissions import (
    PermissionLevel,
    PermissionManager,
    PermissionRequest,
)
from security.tool_allowlist import ToolAllowlist
from tools.models import (
    ToolAction,
    ToolActionType,
    ToolResult,
)


def _audit_tool_call(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            result = method(self, *args, **kwargs)
        except Exception as exc:
            self.audit.record(
                event="TOOL_EXECUTION",
                action=method.__name__,
                status="ERROR",
                details={
                    "error": str(exc),
                },
            )
            raise

        if isinstance(result, ToolResult):
            if not result.executed and result.success:
                status = "DRY_RUN"
            elif result.success and result.verified:
                status = "SUCCESS"
            elif result.success:
                status = "UNVERIFIED"
            else:
                status = "FAILED"

            self.audit.record(
                event="TOOL_EXECUTION",
                action=result.action.action_type.value,
                status=status,
                details={
                    "target": result.action.target,
                    "executed": result.executed,
                    "verified": result.verified,
                    "success": result.success,
                    "return_code": result.return_code,
                },
            )

        return result

    return wrapper

class ToolService:

    def __init__(
        self,
        project_root: Path | str | None = None,
        permissions: PermissionManager | None = None,
        audit: AuditLogger | None = None,
        allowlist: ToolAllowlist | None = None,
    ):
        self.project_root = (
            Path(project_root).resolve()
            if project_root is not None
            else Path(__file__).resolve().parents[1]
        )

        self.permissions = (
            permissions
            or PermissionManager()
        )
        self.audit = (
            audit
            or AuditLogger(
                str(self.project_root / "data" / "audit.jsonl")
            )
        )

        self.allowlist = (
            allowlist
            or ToolAllowlist()
        )

        self._applications = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
        }

    def _resolve_project_path(
        self,
        path: str | Path,
    ) -> Path:

        candidate = Path(path)

        if not candidate.is_absolute():
            candidate = self.project_root / candidate

        resolved = candidate.resolve()

        try:
            resolved.relative_to(
                self.project_root
            )
        except ValueError:
            raise PermissionError(
                "Path is outside the authorized ANNA project directory."
            )

        return resolved

    def _authorize(
        self,
        action: str,
        level: PermissionLevel,
        resource: str,
        confirmed: bool = False,
    ) -> None:

        rule = self.allowlist.get_rule(action)

        if rule is None or not rule.enabled:
            self.audit.record(
                event="PERMISSION",
                action=action,
                status="DENIED",
                details={
                    "level": int(level),
                    "resource": resource,
                    "confirmed": confirmed,
                    "reason": "Tool action is not allowlisted.",
                },
            )
            raise PermissionError(
                f"Tool action is not allowlisted: {action}"
            )

        if rule.permission_level != int(level):
            self.audit.record(
                event="PERMISSION",
                action=action,
                status="DENIED",
                details={
                    "level": int(level),
                    "resource": resource,
                    "confirmed": confirmed,
                    "reason": "Tool permission level does not match the allowlist rule.",
                },
            )
            raise PermissionError(
                "Tool permission level does not match the allowlist rule."
            )

        result = self.permissions.evaluate(
            PermissionRequest(
                action=action,
                level=level,
                resource=resource,
            ),
            confirmed=confirmed,
        )

        self.audit.record(
            event="PERMISSION",
            action=action,
            status="ALLOWED" if result.allowed else "DENIED",
            details={
                "level": int(level),
                "resource": resource,
                "confirmed": confirmed,
                "requires_confirmation": result.requires_confirmation,
            },
        )

        if not result.allowed:
            raise PermissionError(
                result.reason,
            )

    def _run(
        self,
        action: ToolAction,
        argv: list[str],
        confirmed: bool = False,
    ) -> ToolResult:

        if action.dry_run:
            return ToolResult(
                action=action,
                executed=False,
                verified=False,
                success=True,
                output=(
                    "DRY-RUN: "
                    + action.description
                ),
            )

        self._authorize(
            action=action.action_type.value,
            level=action.permission_level,
            resource=action.target,
            confirmed=confirmed,
        )

        try:
            completed = subprocess.run(
                argv,
                cwd=self.project_root,
                text=True,
                capture_output=True,
                timeout=120,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            output = str(exc.stdout or exc.stderr or "").strip()
            return ToolResult(
                action=action,
                executed=True,
                verified=False,
                success=False,
                output=output,
                error="Tool execution timed out after 120 seconds.",
                return_code=None,
            )
        success = (
            completed.returncode == 0
        )
        output = (
            completed.stdout
            or completed.stderr
            or ""
        ).strip()

        verified = success

        return ToolResult(
            action=action,
            executed=True,
            verified=verified,
            success=success,
            output=output,
            error=completed.stderr.strip(),
            return_code=completed.returncode,
        )

    def propose_system_info(
        self,
    ) -> ToolAction:

        return ToolAction(
            action_type=ToolActionType.SYSTEM_INFO,
            target="local-system",
            permission_level=PermissionLevel.READ_ONLY,
            description=(
                "Read local Python/runtime and operating-system information."
            ),
        )

    @_audit_tool_call
    def system_info(
        self,
    ) -> ToolResult:

        action = self.propose_system_info()

        self._authorize(
            action=action.action_type.value,
            level=action.permission_level,
            resource=action.target,
        )

        output = "\n".join(
            (
                f"OS: {platform.platform()}",
                f"Python: {sys.version.split()[0]}",
                f"Architecture: {platform.machine()}",
                f"CPU count: {os.cpu_count()}",
                f"Project root: {self.project_root}",
            )
        )

        return ToolResult(
            action=ToolAction(
                action_type=action.action_type,
                target=action.target,
                permission_level=action.permission_level,
                description=action.description,
                dry_run=False,
            ),
            executed=True,
            verified=True,
            success=True,
            output=output,
            return_code=0,
        )

    def propose_code_inspection(
        self,
        path: str,
    ) -> ToolAction:

        resolved = self._resolve_project_path(path)

        return ToolAction(
            action_type=ToolActionType.CODE_INSPECTION,
            target=str(resolved),
            permission_level=PermissionLevel.READ_ONLY,
            description=(
                f"Inspect Python source syntax and structure: {resolved}"
            ),
        )

    @_audit_tool_call
    def inspect_python(
        self,
        path: str,
    ) -> ToolResult:

        resolved = self._resolve_project_path(path)

        if not resolved.exists():
            raise FileNotFoundError(
                f"Python file does not exist: {resolved}"
            )

        if resolved.suffix.lower() != ".py":
            raise ValueError(
                "Code inspection currently supports Python files only."
            )

        action = self.propose_code_inspection(
            path
        )

        self._authorize(
            action=action.action_type.value,
            level=action.permission_level,
            resource=action.target,
        )

        source = resolved.read_text(
            encoding="utf-8-sig"
        )

        try:
            tree = ast.parse(
                source,
                filename=str(resolved),
            )

            imports = [
                node.names[0].name
                for node in ast.walk(tree)
                if isinstance(
                    node,
                    ast.Import,
                )
                and node.names
            ]

            syntax = "valid"
            error = ""

        except SyntaxError as exc:
            imports = []
            syntax = "invalid"
            error = (
                f"{exc.msg} at line {exc.lineno}"
            )

        output = "\n".join(
            (
                f"File: {resolved}",
                f"Syntax: {syntax}",
                f"Lines: {len(source.splitlines())}",
                f"Top-level imports: {', '.join(imports) or 'none'}",
            )
        )

        return ToolResult(
            action=ToolAction(
                action_type=action.action_type,
                target=action.target,
                permission_level=action.permission_level,
                description=action.description,
                dry_run=False,
            ),
            executed=True,
            verified=True,
            success=(syntax == "valid"),
            output=output,
            error=error,
            return_code=0 if syntax == "valid" else 1,
        )

    def propose_run_tests(
        self,
    ) -> ToolAction:

        return ToolAction(
            action_type=ToolActionType.RUN_TESTS,
            target="project-test-suite",
            permission_level=PermissionLevel.LOW_RISK,
            description=(
                "Run the ANNA Python test suite with cache provider disabled."
            ),
        )

    @_audit_tool_call
    def run_tests(
        self,
        dry_run: bool = True,
    ) -> ToolResult:

        action = ToolAction(
            action_type=ToolActionType.RUN_TESTS,
            target="project-test-suite",
            permission_level=PermissionLevel.LOW_RISK,
            description=(
                "Run the ANNA Python test suite with cache provider disabled."
            ),
            dry_run=dry_run,
        )

        python = (
            self.project_root
            / "anna-env"
            / "Scripts"
            / "python.exe"
        )

        argv = [
            str(python),
            "-B",
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
        ]

        return self._run(
            action=action,
            argv=argv,
        )

    def propose_list_directory(
        self,
        path: str = ".",
    ) -> ToolAction:

        resolved = self._resolve_project_path(
            path
        )

        return ToolAction(
            action_type=ToolActionType.LIST_DIRECTORY,
            target=str(resolved),
            permission_level=PermissionLevel.READ_ONLY,
            description=(
                f"List files under authorized project path: {resolved}"
            ),
        )

    @_audit_tool_call
    def list_directory(
        self,
        path: str = ".",
    ) -> ToolResult:

        resolved = self._resolve_project_path(
            path
        )

        if not resolved.exists():
            raise FileNotFoundError(
                f"Directory does not exist: {resolved}"
            )

        if not resolved.is_dir():
            raise NotADirectoryError(
                f"Not a directory: {resolved}"
            )

        action = self.propose_list_directory(
            path
        )

        self._authorize(
            action=action.action_type.value,
            level=action.permission_level,
            resource=action.target,
        )

        entries = sorted(
            item.name
            for item in resolved.iterdir()
        )

        return ToolResult(
            action=ToolAction(
                action_type=action.action_type,
                target=action.target,
                permission_level=action.permission_level,
                description=action.description,
                dry_run=False,
            ),
            executed=True,
            verified=True,
            success=True,
            output="\n".join(entries),
            return_code=0,
        )

    @_audit_tool_call
    def create_directory(
        self,
        path: str,
        dry_run: bool = True,
    ) -> ToolResult:

        resolved = self._resolve_project_path(
            path
        )

        action = ToolAction(
            action_type=ToolActionType.CREATE_DIRECTORY,
            target=str(resolved),
            permission_level=PermissionLevel.LOW_RISK,
            description=(
                f"Create authorized project directory: {resolved}"
            ),
            dry_run=dry_run,
        )

        if action.dry_run:
            return ToolResult(
                action=action,
                executed=False,
                verified=False,
                success=True,
                output=(
                    f"DRY-RUN: would create {resolved}"
                ),
            )

        self._authorize(
            action=action.action_type.value,
            level=action.permission_level,
            resource=action.target,
        )

        resolved.mkdir(
            parents=True,
            exist_ok=True,
        )

        verified = (
            resolved.exists()
            and resolved.is_dir()
        )

        return ToolResult(
            action=action,
            executed=True,
            verified=verified,
            success=verified,
            output=str(resolved),
            error=(
                ""
                if verified
                else "Directory creation could not be verified."
            ),
            return_code=0 if verified else 1,
        )

    @_audit_tool_call
    def launch_application(
        self,
        name: str,
        dry_run: bool = True,
        confirmed: bool = False,
    ) -> ToolResult:

        normalized = name.strip().lower()

        if normalized not in self._applications:
            raise ValueError(
                "Application is not in the safe application allowlist."
            )

        executable = self._applications[
            normalized
        ]

        action = ToolAction(
            action_type=ToolActionType.LAUNCH_APPLICATION,
            target=executable,
            permission_level=PermissionLevel.IMPORTANT_CHANGE,
            description=(
                f"Launch allowlisted application: {executable}"
            ),
            dry_run=dry_run,
        )

        if action.dry_run:
            return ToolResult(
                action=action,
                executed=False,
                verified=False,
                success=True,
                output=(
                    f"DRY-RUN: would launch {executable}"
                ),
            )

        self._authorize(
            action=action.action_type.value,
            level=action.permission_level,
            resource=executable,
            confirmed=confirmed,
        )

        process = subprocess.Popen(
            [executable],
            cwd=self.project_root,
        )

        verified = (
            process.poll() is None
        )

        return ToolResult(
            action=action,
            executed=True,
            verified=verified,
            success=verified,
            output=(
                f"Launched {executable}"
                if verified
                else f"{executable} exited immediately."
            ),
            error="",
            return_code=None,
        )


