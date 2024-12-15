import sys, os, subprocess, shutil, enum, ctypes, traceback

def clone(repo, org = "libsdl-org"):
    if repo not in os.listdir():
        subprocess.run(["git", "clone", f"https://github.com/{org}/{repo}.git", "--recursive"], shell = True)
    
    else:
        print("Passing '{}' because it already exists...".format(repo))

    return os.path.abspath(repo)

def main(argv):
    repos = ["SDL", "SDL_image", "SDL_mixer", "SDL_net", "SDL_rtf", "SDL_ttf"]
    binaries = ["SDL3", "SDL3_image", "SDL3_mixer", "SDL3_net", "SDL3_rtf", "SDL3_ttf"]
    workDir = os.getcwd()

    # if "win32" in sys.platform and "--aarch64" not in argv:
    #     subprocess.run(["wsl", "-u", "root", "sudo", "python3", "main.py", "--aarch64"], shell = True)
    #     subprocess.run(["pause"], shell = True)
    #     return
    # 
    # repos = ["SDL_ttf", "SDL_rtf"]
    # binaries = ["SDL3_ttf", "SDL3_rtf"]

    if "linux" in sys.platform:
        arch = "arm64" if "--aarch64" in argv else "amd64"
        subprocess.run(["sudo", "apt", "install", "-y", f"libfreetype6:{arch}", f"libfreetype6-dev:{arch}", f"linux-libc-dev:{arch}"])

    for index, repo in enumerate(repos):
        file = f"{binaries[index]}.dll" if "win32" in sys.platform else f"lib{binaries[index]}.so"
        if not os.path.exists(os.path.join(workDir, "bin")): os.mkdir(os.path.join(workDir, "bin"))
        folder = "windows-x86_64" if "win32" in sys.platform else ("linux-aarch64" if "--aarch64" in argv else "linux-x86_64")
        if not os.path.exists(os.path.join(workDir, "bin", folder)): os.mkdir(os.path.join(workDir, "bin", folder))
        if os.path.exists(os.path.join(workDir, "bin", folder, file)): continue
        os.chdir(clone(repo))

        if os.path.exists(os.path.join(os.getcwd(), "build")):
            shutil.rmtree(os.path.join(os.getcwd(), "build"), ignore_errors = True)

        parallel = True
        flags = ["-DCMAKE_TOOLCHAIN_FILE=build-scripts/cmake-toolchain-mingw64-x86_64.cmake"] if repo in ["SDL"] and "win32" in sys.platform else []
        if "linux" in sys.platform and "--aarch64" in argv: flags += ["-DCMAKE_C_COMPILER=aarch64-linux-gnu-gcc"]
        subprocess.run(["cmake", "-S", ".", "-B", "build"] + flags + ["-DCMAKE_BUILD_TYPE=Release"], shell = "win32" in sys.platform)
        subprocess.run(["cmake", "--build", "build", "--config", "Release"] + (["--parallel"] if parallel else []), shell = "win32" in sys.platform)
        subprocess.run(["cmake", "--install", "build"], shell = "win32" in sys.platform)

        path = os.path.join(os.getcwd(), *(["build"] + (["Release"] if "win32" in sys.platform else []) + [file]))
        shutil.copyfile(path, os.path.join(workDir, "bin", folder, file))
        os.chdir(workDir)

    if "win32" in sys.platform:
        subprocess.run(["wsl", "-u", "root", "sudo", "python3", "main.py"], shell = True)
        subprocess.run(["pause"], shell = True)

    if "linux" in sys.platform and "--aarch64" not in argv:
        subprocess.run(["python3", "main.py", "--aarch64"], shell = False)
        
    return 0

class SW(enum.IntEnum):
    HIDE = 0
    MAXIMIZE = 3
    MINIMIZE = 6
    RESTORE = 9
    SHOW = 5
    SHOWDEFAULT = 10
    SHOWMAXIMIZED = 3
    SHOWMINIMIZED = 2
    SHOWMINNOACTIVE = 7
    SHOWNA = 8
    SHOWNOACTIVATE = 4
    SHOWNORMAL = 1

class ERROR(enum.IntEnum):
    ZERO = 0
    FILE_NOT_FOUND = 2
    PATH_NOT_FOUND = 3
    BAD_FORMAT = 11
    ACCESS_DENIED = 5
    ASSOC_INCOMPLETE = 27
    DDE_BUSY = 30
    DDE_FAIL = 29
    DDE_TIMEOUT = 28
    DLL_NOT_FOUND = 32
    NO_ASSOC = 31
    OOM = 8
    SHARE = 26

if __name__ == "__main__":
    if "win32" in sys.platform and not ctypes.windll.shell32.IsUserAnAdmin():
        hinstance = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, sys.argv[0], None, SW.SHOWNORMAL)
        if hinstance <= 32: raise RuntimeError(ERROR(hinstance))

    else:
        try:
            sys.exit(main(sys.argv))
        
        except Exception as exception:
            traceback.print_exc()

            if "win32" in sys.platform:
                subprocess.run(["pause"], shell = True)

            sys.exit(-1)