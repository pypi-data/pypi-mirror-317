from .core import main
from .logging import warning

def ep():
    warning("running in verbose mode. this is only recommended for debugging and troubleshooting purposes.")
    main()

if __name__ == "__main__":
    ep()