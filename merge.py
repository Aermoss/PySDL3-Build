import sys, os

os.environ["SDL_DOC_GENERATOR"] = "0"
os.environ["SDL_DISABLE_METADATA"] = "1"
os.environ["SDL_DOWNLOAD_BINARIES"] = "0"
os.environ["SDL_FIND_BINARIES"] = "0"

import sdl3, shutil, zipfile

def main(argv):
    repos, binaries = sdl3.SDL_REPOSITORIES, list(sdl3.SDL_BINARY_VAR_MAP_INV.keys())
    workDir, outDir = os.getcwd(), "artifacts"

    if not os.path.exists(os.path.join(workDir, outDir)):
        os.mkdir(os.path.join(workDir, outDir))

    for index, repo in enumerate(repos):
        file = sdl3.SDL_BINARY_PATTERNS[sdl3.SDL_SYSTEM][0].format(binaries[index])
        path = os.path.join(workDir, repo, "build", *(["Release", file] if sdl3.SDL_SYSTEM in ["Windows"] else [file]))
        shutil.copyfile(path, os.path.join(workDir, outDir, file))

    with zipfile.ZipFile(f"{outDir}.zip", "w", zipfile.ZIP_DEFLATED) as ref:
        for root, _, files in os.walk(outDir):
            for file in files:
                ref.write(path := os.path.join(root, file), os.path.relpath(path, outDir))

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))