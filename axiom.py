#!/usr/bin/env python3
import sys
import os

# Ensure the local src/ package paths are natively available strictly offline
sys.path.insert(0, os.path.abspath("src"))

from axiom_cli.main import main

if __name__ == "__main__":
    main()
