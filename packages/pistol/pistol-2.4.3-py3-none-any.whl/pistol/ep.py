from .core import main

def ep():
    try:
        main()
    except Exception as exc:
        from .logging import error

        error(f"internal: {str(exc).lower()}")
        exit(1)

if __name__ == "__main__":
    ep()