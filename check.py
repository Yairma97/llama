import platform
import sys
from packaging.tags import sys_tags

def main():
    print("Python version:", sys.version)
    print("Platform:", platform.system())
    print("Machine:", platform.machine())
    print("Python implementation:", platform.python_implementation())
    print("Python version (major.minor):", f"{sys.version_info.major}.{sys.version_info.minor}")

    # Get the wheel tags
    tags = list(sys_tags())
    print("Wheel tags:")
    for tag in tags:
        print(tag)

if __name__ == "__main__":
    main()