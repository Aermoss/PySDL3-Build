import sys, os, subprocess

os.environ["SDL_DOC_GENERATOR"] = "0"
os.environ["SDL_DISABLE_METADATA"] = "1"
os.environ["SDL_CHECK_BINARY_VERSION"] = "0"
os.environ["SDL_DOWNLOAD_BINARIES"] = "0"
os.environ["SDL_FIND_BINARIES"] = "0"

import sdl3, asyncio

def main(argv):
    subprocess.run(["git", "config", "--global", "advice.detachedHead", "false"], shell = sdl3.SDL_SYSTEM in ["Windows"])

    for repo, release in asyncio.run(sdl3.SDL_GET_LATEST_RELEASES()).items():
        if repo not in os.listdir():
            print("\33[32m", f"info: cloning '{repo}'", "without any release..." if (dev := release is None or not release.split("-")[1].startswith("3")) else f"with release '{release}'...", "\33[0m", sep = "", flush = True)
            subprocess.run(["git", "clone", f"https://github.com/libsdl-org/{repo}.git"] + ([] if "old" in os.listdir() else ["--recursive"]) + ([] if dev else ["--branch", release]), shell = sdl3.SDL_SYSTEM in ["Windows"])

        else:
            print("\33[35m", f"warning: passing '{repo}' because it already exists...", "\33[0m", sep = "", flush = True)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))