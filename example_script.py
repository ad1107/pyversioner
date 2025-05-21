import sys
import platform
import os

def main():
    print(f"Python Version: {sys.version}")
    print(f"Version Info: {sys.version_info}")
    print(f"Platform: {platform.platform()}")
    
    print("\nEnvironment Variables:")
    for key, value in list(os.environ.items())[:5]:
        print(f"{key}: {value}")
    
    print("\nTesting Version-Specific Features:")
    try:
        # Feature introduced in Python 3.9: Dictionary Union
        dict1 = {"a": 1, "b": 2}
        dict2 = {"c": 3, "d": 4}
        merged = dict1 | dict2
        print(f"Dictionary Union (Python 3.9+): {merged}")
    except Exception as e:
        print(f"Dictionary Union (Python 3.9+): Not supported - {type(e).__name__}: {e}")
    
    try:
        # Feature introduced in Python 3.10: Structural Pattern Matching
        value = ("point", 1, 2)
        result = "Pattern matching (Python 3.10+): "
        
        match value:
            case ("point", x, y):
                result += f"Point at ({x}, {y})"
            case ("line", x1, y1, x2, y2):
                result += f"Line from ({x1}, {y1}) to ({x2}, {y2})"
            case _:
                result += "Not a shape"
        
        print(result)
    except SyntaxError:
        print("Pattern matching (Python 3.10+): Not supported - SyntaxError")
    except Exception as e:
        print(f"Pattern matching (Python 3.10+): Error - {type(e).__name__}: {e}")
    
    # Try importing common packages
    print("\nTesting Package Imports:")
    packages_to_test = [
        "numpy",
        "pandas",
        "matplotlib",
        "requests",
        "flask",
        "django",
        "tensorflow",
        "torch"
    ]
    
    for package in packages_to_test:
        try:
            __import__(package)
            version = sys.modules[package].__version__ if hasattr(sys.modules[package], "__version__") else "Unknown"
            print(f"{package}: Imported successfully (Version: {version})")
        except ImportError:
            print(f"{package}: Not installed")
        except Exception as e:
            print(f"{package}: Error - {type(e).__name__}: {e}")

if __name__ == "__main__":
    main()
