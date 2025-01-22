import sys, os, subprocess

def main(argv):
    for repo in ["SDL", "SDL_image", "SDL_mixer", "SDL_net", "SDL_rtf", "SDL_ttf"]:
        if repo not in os.listdir():
            subprocess.run(["git", "clone", f"https://github.com/libsdl-org/{repo}.git", "--recursive"], shell = True)
        
        else:
            print("Passing '{}' because it already exists...".format(repo))

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))