# JJ Check-Ins

JJ Check-Ins is a lightweight Windows desktop application for recording visitor attendance. Visitors can enter their information, have their photo taken using a connected camera, and have their check-in information stored locally.

## Features

* Visitor check-in form
* Automatic check-in timestamps
* Live camera support
* Visitor photo capture
* Local Excel record storage
* Local photo storage
* Runs entirely on the local Windows machine
* No internet connection or external database required

## Technologies

* Python
* OpenCV
* OpenPyXL

## Setup

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## Planned

* Desktop GUI
* Live camera preview
* Photo retake functionality
* Windows `.exe` packaging
* Windows installation wizard

## Releasing a New Version

When changes are made to the application, a new Windows installer should be built and published as a new GitHub Release.

### 1. Make and Test Changes

Make the desired changes to the application and test them locally:

```powershell
py main.py
```

Verify that the application works correctly before creating a new release.

### 2. Commit and Push Changes

Commit the completed changes to Git:

```powershell
git add .
git commit -m "Description of changes"
git push
```

Merge the changes into the `main` branch if development was completed on a separate branch.

### 3. Rebuild the Windows Application

Use PyInstaller to generate a new build:

```powershell
pyinstaller --noconfirm --windowed --name "JonathanJenningsVisitorCheckIn" --icon "assets\icons\JJ109PrimaryLogo.ico" --add-data "assets;assets" main.py
```

The new application build will be created under:

```text
dist/JonathanJenningsVisitorCheckIn/
```

Test `JonathanJenningsVisitorCheckIn.exe` before continuing.

### 4. Update the Installer Version

Open:

```text
installer/JJCheckIns.iss
```

Update the application version:

```ini
AppVersion=1.1.0
```

Use semantic versioning when possible:

- `1.0.0` — Initial release
- `1.1.0` — New features or improvements
- `1.1.1` — Bug fixes
- `2.0.0` — Major application changes

### 5. Rebuild the Installer

Open `JJCheckIns.iss` in **Inno Setup Compiler** and compile the installer.

The new installer will be generated as:

```text
JonathanJenningsVisitorCheckIn-Setup.exe
```

Install and test the newly generated installer before publishing it.

### 6. Create a New GitHub Release

1. Open the repository's **Releases** page.
2. Select **Draft a new release**.
3. Create a new version tag, such as `v1.1.0`.
4. Use the same version for the release title.
5. Add release notes describing the changes.
6. Upload `JonathanJenningsVisitorCheckIn-Setup.exe`.
7. Publish the release.

> **Note:** Do not replace previous releases. Each version should have its own GitHub Release so previous versions remain available if needed.

### Release Workflow

```text
Make Changes
     ↓
Test Locally
     ↓
Commit & Push
     ↓
Merge to Main
     ↓
Build with PyInstaller
     ↓
Test Executable
     ↓
Update Installer Version
     ↓
Compile with Inno Setup
     ↓
Test Installer
     ↓
Create GitHub Release
     ↓
Upload Setup.exe
```