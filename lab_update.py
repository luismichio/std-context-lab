import os
import subprocess
import sys
import re

def run_cmd(cmd, cwd=None):
    print(f"Executing: {cmd} (cwd: {cwd or 'root'})")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result

def get_version_from_file(path, pattern):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        content = f.read()
        match = re.search(pattern, content)
        return match.group(1) if match else None

def update_repo(repo_path):
    print(f"\n--- Updating {repo_path} ---")
    run_cmd("git pull", cwd=repo_path)

def main():
    root = os.getcwd()
    venv_python = os.path.join(root, ".venv", "Scripts", "python.exe")
    cpipe_bin = os.path.join(root, ".venv", "Scripts", "cpipe.exe")
    sift_bin = os.path.join(root, ".venv", "Scripts", "sift-core.exe")

    # 1. Update Source
    update_repo("target_repos/context-pipe")
    update_repo("target_repos/semantic-sift")

    # 2. Run Fetch Scripts
    run_cmd(f'"{venv_python}" scripts/fetch_cpipe.py', cwd="target_repos/context-pipe")
    run_cmd(f'"{venv_python}" scripts/fetch_sift_core.py', cwd="target_repos/semantic-sift")

    # 3. Check for Version Mismatches
    cp_toml = os.path.join("target_repos/context-pipe/crates/cpipe/Cargo.toml")
    cp_target_version = get_version_from_file(cp_toml, r'version = "([^"]+)"')
    
    if os.path.exists(cpipe_bin):
        cp_actual = run_cmd(f'"{cpipe_bin}" --version').stdout.strip()
        print(f"cpipe: target={cp_target_version}, actual={cp_actual}")
        if cp_target_version and cp_target_version not in cp_actual:
            print("Mismatch detected! Rebuilding cpipe from source...")
            run_cmd("cargo build --release", cwd="target_repos/context-pipe/crates/cpipe")
            run_cmd(f'cp target/release/cpipe.exe "{cpipe_bin}"', cwd="target_repos/context-pipe/crates/cpipe")

    ss_toml = os.path.join("target_repos/semantic-sift/pyproject.toml")
    ss_target_version = get_version_from_file(ss_toml, r'version = "([^"]+)"')
    if os.path.exists(sift_bin):
        ss_actual = run_cmd(f'"{sift_bin}" --version').stdout.strip()
        print(f"sift-core: target={ss_target_version}, actual={ss_actual}")

    # 4. Final Onboarding (CPP only)
    print("\n--- Running Final Onboarding ---")
    run_cmd(f'"{venv_python}" -m context_pipe.onboarding --environment Gemini', cwd="target_repos/context-pipe")

    print("\nUpdate complete. Please verify LAB_STATUS.md.")
    print("âš ï¸  IMPORTANT: Restart your CLI or IDE to ensure all changes and new binaries are loaded.")

if __name__ == "__main__":
    main()
