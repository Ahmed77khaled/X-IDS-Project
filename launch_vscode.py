import os
import sys
import winreg
import subprocess

def find_vscode():
    # 1. Search PATH
    for path in os.environ.get("PATH", "").split(os.pathsep):
        for candidate in ["code.cmd", "Code.exe", "code"]:
            full = os.path.join(path, candidate)
            if os.path.isfile(full):
                return full

    # 2. Search Windows Registry
    reg_keys = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\App Paths\Code.exe"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\Code.exe"),
        (winreg.HKEY_CLASSES_ROOT, r"Applications\Code.exe\shell\open\command"),
        (winreg.HKEY_CLASSES_ROOT, r"Directory\shell\VSCode\command"),
        (winreg.HKEY_CLASSES_ROOT, r"*\shell\VSCode\command"),
    ]
    for root, subkey in reg_keys:
        try:
            with winreg.OpenKey(root, subkey) as k:
                val, _ = winreg.QueryValueEx(k, "")
                if val:
                    # Clean quotes and arguments like "%1"
                    if '"' in val:
                        parts = val.split('"')
                        exe = parts[1] if len(parts) > 1 else parts[0]
                    else:
                        exe = val.split()[0]
                    if os.path.isfile(exe):
                        return exe
        except Exception:
            pass

    # 3. Search Known Windows Install Directories
    local_app = os.environ.get("LOCALAPPDATA", "")
    prog_files = os.environ.get("ProgramFiles", "C:\\Program Files")
    prog_files_x86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")

    candidates = [
        os.path.join(local_app, "Programs", "Microsoft Visual studio Code", "Code.exe"),
        os.path.join(local_app, "Programs", "Microsoft VS Code", "Code.exe"),
        os.path.join(local_app, "Programs", "Microsoft Visual studio Code", "bin", "code.cmd"),
        os.path.join(local_app, "Programs", "Microsoft VS Code", "bin", "code.cmd"),
        os.path.join(prog_files, "Microsoft VS Code", "Code.exe"),
        os.path.join(prog_files, "Microsoft VS Code", "bin", "code.cmd"),
        os.path.join(prog_files_x86, "Microsoft VS Code", "Code.exe"),
        os.path.join(prog_files_x86, "Microsoft VS Code", "bin", "code.cmd"),
        r"C:\Program Files\Microsoft VS Code\Code.exe",
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c

    return None

def main():
    detected = find_vscode()
    if len(sys.argv) > 1 and sys.argv[1] == "--detect":
        if detected:
            print(detected)
            sys.exit(0)
        sys.exit(1)

    project_dir = os.path.abspath(os.path.dirname(__file__))
    notebook = os.path.join(project_dir, "my_model_training.ipynb")

    if detected:
        print(f"[*] Found Visual Studio Code: {detected}")
        print(f"[*] Launching workspace with active notebook: {notebook}")
        cmd = [detected, project_dir, "-g", notebook]
        subprocess.Popen(cmd, shell=True)
        sys.exit(0)
    else:
        print("[!] Visual Studio Code not found on system.")
        sys.exit(1)

if __name__ == "__main__":
    main()
