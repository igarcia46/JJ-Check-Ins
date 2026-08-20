[Setup]
AppId={{9E6F0C3A-2E8A-4E63-9CF0-4B0A3A8D6C11}
AppName=Jonathan Jennings Visitor Check-In
AppVersion=1.0.2
AppPublisher=Isaac Garcia

DefaultDirName={autopf}\Jonathan Jennings Visitor Check-In
DefaultGroupName=Jonathan Jennings Visitor Check-In

OutputDir=output
OutputBaseFilename=JonathanJenningsVisitorCheckIn-Setup

SetupIconFile=..\assets\icons\JJ109PrimaryLogo.ico
UninstallDisplayIcon={app}\JonathanJenningsVisitorCheckIn.exe

Compression=lzma
SolidCompression=yes
WizardStyle=modern

PrivilegesRequired=admin

UninstallDisplayName=Jonathan Jennings Visitor Check-In

[Files]
Source: "..\dist\JonathanJenningsVisitorCheckIn\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Jonathan Jennings Visitor Check-In"; Filename: "{app}\JonathanJenningsVisitorCheckIn.exe"

Name: "{autodesktop}\Jonathan Jennings Visitor Check-In"; Filename: "{app}\JonathanJenningsVisitorCheckIn.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Run]
Filename: "{app}\JonathanJenningsVisitorCheckIn.exe"; Description: "Launch Jonathan Jennings Visitor Check-In"; Flags: nowait postinstall skipifsilent