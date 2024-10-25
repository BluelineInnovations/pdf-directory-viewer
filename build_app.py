# build_app.py
import os
import subprocess
import sys
import platform
import shutil

def install_requirements():
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def create_spec_file():
    """Create the spec file with the correct configuration"""
    is_windows = platform.system() == "Windows"
    
    if is_windows:
        spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PIL', 'PIL._imagingtk', 'PIL._tkinter_finder', 'tkinter', 'fitz'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PDF Directory Viewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    codesign_identity=None,
    entitlements_file=None
)
"""
    else:  # macOS
        spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PIL', 'PIL._imagingtk', 'PIL._tkinter_finder', 'tkinter', 'fitz'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PDF Directory Viewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    codesign_identity=None,
    entitlements_file=None,
    target_arch=None
)
"""
    
    with open("pdf_viewer.spec", "w") as f:
        f.write(spec_content)

def build_executable():
    """Build the executable using the spec file"""
    print("Building executable...")
    
    # Basic command
    cmd = ["pyinstaller", "--clean", "--noconfirm"]
    
    # Add spec file
    cmd.append("pdf_viewer.spec")
    
    print(f"Executing command: {' '.join(cmd)}")
    subprocess.check_call(cmd)
    
    # For macOS, we need to make the executable executable
    if platform.system() == "Darwin":
        exe_path = os.path.join("dist", "PDF Directory Viewer")
        if os.path.exists(exe_path):
            os.chmod(exe_path, 0o755)
            print(f"Made executable: {exe_path}")

def cleanup():
    """Clean up build artifacts and temporary files"""
    print("Cleaning up previous build files...")
    paths_to_clean = ['build', 'dist', '*.spec']
    for path in paths_to_clean:
        if '*' in path:
            import glob
            for p in glob.glob(path):
                try:
                    if os.path.isfile(p):
                        os.remove(p)
                        print(f"Removed file: {p}")
                except Exception as e:
                    print(f"Error cleaning {p}: {e}")
        else:
            try:
                if os.path.exists(path):
                    if os.path.isfile(path):
                        os.remove(path)
                        print(f"Removed file: {path}")
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
                        print(f"Removed directory: {path}")
            except Exception as e:
                print(f"Error cleaning {path}: {e}")

def main():
    try:
        print(f"Starting build process for {platform.system()}...")
        
        # Clean up previous builds
        cleanup()
        
        # Install requirements
        install_requirements()
        
        # Create spec file
        create_spec_file()
        
        # Build executable
        build_executable()
        
        print("\nBuild completed successfully!")
        if platform.system() == "Windows":
            print("You can find the executable in the 'dist' directory as 'PDF Directory Viewer.exe'")
        else:
            print("You can find the executable in the 'dist' directory as 'PDF Directory Viewer'")
            print("\nTo run the program:")
            print("1. Open Terminal")
            print("2. Navigate to the dist directory")
            print("3. Run: ./PDF\\ Directory\\ Viewer")
            
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("\nFull error details:")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()