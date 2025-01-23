import sys, os, shutil, platform, zipfile

def main(argv):
    repos = ["SDL", "SDL_image", "SDL_mixer", "SDL_ttf", "SDL_rtf", "SDL_net"]
    binaries = ["SDL3", "SDL3_image", "SDL3_mixer", "SDL3_ttf", "SDL3_rtf", "SDL3_net"]
    system, workDir, outDir = platform.system(), os.getcwd(), "artifacts"

    if not os.path.exists(os.path.join(workDir, outDir)):
        os.mkdir(os.path.join(workDir, outDir))

    for index, repo in enumerate(repos):
        file = {"Windows": "{}.dll" , "Linux": "lib{}.so", "Darwin": "lib{}.dylib"}[system].format(binaries[index])
        path = os.path.join(workDir, repo, "build", *(["Release", file] if system in ["Windows"] else [file]))
        shutil.copyfile(path, os.path.join(workDir, outDir, file))

    with zipfile.ZipFile(f"{outDir}.zip", "w", zipfile.ZIP_DEFLATED) as ref:
        for root, _, files in os.walk(outDir):
            for file in files:
                ref.write(path := os.path.join(root, file), os.path.relpath(path, outDir))

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))