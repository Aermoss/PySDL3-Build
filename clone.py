import sys, os, subprocess

import sdl3.SDL

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
            sdl3.SDL_LOGGER.Log(sdl3.SDL_LOGGER.Info, f"Cloning '{repo}' without any release..." if (dev := release is None or not release.split("-")[1].startswith("3")) else f"Cloning '{repo}' with release '{release}'...")
            subprocess.run(["git", "clone"] + ([] if "old" in os.listdir() else ["--recursive"]) + ([] if dev else ["--branch", release]) + [f"https://github.com/libsdl-org/{repo}.git"], shell = sdl3.SDL_SYSTEM in ["Windows"])

        else:
            sdl3.SDL_LOGGER.Log(sdl3.SDL_LOGGER.Warning, f"Skipping '{repo}' because it already exists...")

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))