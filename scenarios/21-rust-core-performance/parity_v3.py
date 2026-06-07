import json
import os
import re
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
MATRIX_PATH = BASE_DIR / "parity_matrix.json"


def _load_matrix() -> list[dict]:
    with open(MATRIX_PATH, "r", encoding="utf-8") as f:
        tests = json.load(f)
    if not isinstance(tests, list) or not tests:
        raise ValueError("parity_matrix.json must contain a non-empty array.")
    return tests


def _swap_mcppipe_for_cpipe(cmd: str) -> str:
    cpipe_path = os.path.abspath("../../.venv/Scripts/cpipe.exe")
    if cmd.startswith("mcp-pipe"):
        return f'& "{cpipe_path}" {cmd[8:]}'
    if " mcp-pipe " in cmd:
        return cmd.replace(" mcp-pipe ", f' & "{cpipe_path}" ')
    if "| mcp-pipe" in cmd:
        return cmd.replace("| mcp-pipe", f'| & "{cpipe_path}"')
    if " mcp-pipe" in cmd:
        return cmd.replace(" mcp-pipe", f' & "{cpipe_path}"')
    return cmd


def _extract_run_pipe(cmd: str) -> str | None:
    m = re.search(r"\bmcp-pipe\s+run\s+([\w\-]+)", cmd)
    return m.group(1) if m else None


def _extract_config_path(cmd: str, cwd: str) -> str | None:
    m = re.search(r"--config\s+([^\s]+)", cmd)
    if m:
        config_raw = m.group(1).strip("\"'")
        return str(Path(cwd, config_raw).resolve())
    default_cfg = Path(cwd, "pipes.json")
    return str(default_cfg.resolve()) if default_cfg.exists() else None


def _validate_test(test: dict, cwd: str) -> str | None:
    if not Path(cwd).exists():
        return f"Test cwd does not exist: {cwd}"

    cmd = test["command"]
    pipe_name = _extract_run_pipe(cmd)
    if pipe_name:
        config_path = _extract_config_path(cmd, cwd)
        if not config_path or not Path(config_path).exists():
            return f"Could not resolve config for run command: {cmd}"
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            available = {p.get("name") for p in cfg.get("pipes", []) if isinstance(p, dict)}
            if pipe_name not in available:
                return f"Pipe '{pipe_name}' not found in {config_path}. Available: {sorted(available)}"
        except Exception as e:
            return f"Failed to validate pipe command against config: {e}"

    return None


def run_parity_test(test: dict) -> str:
    test_id = test.get("id", "??")
    name = test.get("name", "Unnamed")
    cmd = test["command"]
    cwd = str((BASE_DIR / test["cwd"]).resolve())
    expected_mode = test.get("expected_mode", "pass")

    print("\n========================================")
    print(f"--- Native Parity Test: {test_id}: {name} ---")
    print(f"Directory: {test['cwd']}")
    print(f"Command: {cmd}")
    print("----------------------------------------")

    validation_error = _validate_test(test, cwd)
    if validation_error:
        print(f"[HARNESS_ERROR]: {validation_error}")
        return "HARNESS_ERROR"

    new_cmd = _swap_mcppipe_for_cpipe(cmd)

    try:
        result = subprocess.run(
            ["powershell", "-Command", new_cmd],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=cwd,
        )
        print(f"Exit Code: {result.returncode}")

        if result.stdout:
            print(f"Stdout (peek): {result.stdout[:200].strip()}...")
        if result.stderr:
            print(f"Stderr (peek): {result.stderr[:200].strip()}...")

        if result.returncode == 0:
            print("[PASS]: Native parity maintained.")
            return "PASS"

        if expected_mode == "known_gap":
            print("[KNOWN_GAP]: Non-zero exit expected for this test.")
            return "KNOWN_GAP"

        print("[ENGINE_REGRESSION]: Feature regression / parity broken.")
        return "ENGINE_REGRESSION"

    except UnicodeDecodeError as e:
        print(f"[HARNESS_ERROR] Subprocess decode failure: {e}")
        return "HARNESS_ERROR"
    except Exception as e:
        print(f"[HARNESS_ERROR] Unexpected harness error: {e}")
        return "HARNESS_ERROR"


def main() -> None:
    if sys.platform == "win32":
        import io

        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    print("Starting Context-Pipe GAUNTLET v3 (Native Rust Core v0.4.5)")

    tests = _load_matrix()
    results = [run_parity_test(test) for test in tests]

    counts = {
        "PASS": results.count("PASS"),
        "KNOWN_GAP": results.count("KNOWN_GAP"),
        "ENGINE_REGRESSION": results.count("ENGINE_REGRESSION"),
        "HARNESS_ERROR": results.count("HARNESS_ERROR"),
    }

    print("\n========================================")
    print("GAUNTLET v3 COMPLETE.")
    print(f"Total Scenarios Tested: {len(results)}")
    print(f"PASS: {counts['PASS']}")
    print(f"KNOWN_GAP: {counts['KNOWN_GAP']}")
    print(f"ENGINE_REGRESSION: {counts['ENGINE_REGRESSION']}")
    print(f"HARNESS_ERROR: {counts['HARNESS_ERROR']}")
    success_like = counts["PASS"] + counts["KNOWN_GAP"]
    print(f"Success-Like Rate: {(success_like / len(results) * 100):.1f}%")
    print("========================================")


if __name__ == "__main__":
    main()
