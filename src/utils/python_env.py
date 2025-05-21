import subprocess
import re
import json


def detect_python_version(python_path):
    """Get Python version from executable"""
    try:
        result = subprocess.run([python_path, "--version"], capture_output=True, text=True, check=False)
        if result.returncode != 0:
            return (None, result.returncode, f"Failed to get Python version: {result.stderr}")
        
        version_str = result.stdout.strip() or result.stderr.strip()
        match = re.search(r'Python (\d+\.\d+\.\d+)', version_str)
        if not match:
            return (None, 0, f"Cannot parse version from: {version_str}")
        return (match.group(1), 0, None)
    except Exception as e:
        return (None, -1, str(e))


def get_installed_packages(python_path):
    """Get installed packages list"""
    try:
        result = subprocess.run(
            [python_path, "-m", "pip", "list", "--format=json"], 
            capture_output=True, text=True, check=False
        )
        
        if result.returncode != 0:
            error_msg = result.stderr.strip() or "Unknown error"
            return (None, result.returncode, f"pip command failed: {error_msg}")
        
        if not result.stdout.strip():
            return (None, 0, "pip returned empty output")
        
        try:
            packages = json.loads(result.stdout)
            packages_formatted = [{"name": pkg["name"], "version": pkg["version"]} for pkg in packages]
            return (packages_formatted, 0, None)
        except (json.JSONDecodeError, KeyError) as e:
            return (None, -1, f"Failed to parse pip output: {e}")
    except Exception as e:
        return (None, -1, str(e))


def run_python_script(python_path, script_path):
    """Run Python script with specified interpreter"""
    try:
        result = subprocess.run(
            [str(python_path), str(script_path)], 
            capture_output=True, text=True, check=False
        )
        return (result.stdout, result.stderr, result.returncode)
    except Exception as e:
        return (None, str(e), -1)
