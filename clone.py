import sys, os, subprocess

os.environ["SDL_DOC_GENERATOR"] = "0"
os.environ["SDL_DISABLE_METADATA"] = "1"
os.environ["SDL_DOWNLOAD_BINARIES"] = "0"
os.environ["SDL_FIND_BINARIES"] = "0"

import sdl3, asyncio

def main(argv):
    for repo, release in asyncio.run(sdl3.SDL_GET_LATEST_RELEASES()).items():
        if repo not in os.listdir():
            dev = release is None or not release.split("-")[1].startswith("3")
            print("\33[32m", f"info: cloning '{repo}'", f"with release '{release}'..." if not dev else "without any release...", "\33[0m", sep = "", flush = True)
            subprocess.run(["git", "clone", f"https://github.com/libsdl-org/{repo}.git", "--recursive"], shell = sdl3.SYSTEM not in ["Darwin"])
            if not dev: subprocess.run(["git", "checkout", f"tags/{release}"], cwd = repo, shell = sdl3.SYSTEM not in ["Darwin"])

        else:
            print("\33[35m", f"warning: passing '{repo}' because it already exists...", "\33[0m", sep = "", flush = True)

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))