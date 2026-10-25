; Installateur Windows de CAT Pilot FT-817 (Inno Setup 6) — logiciel distinct de CAT Pilot.
; Installation par utilisateur, sans droits d'administrateur : la mise à jour
; automatique peut ainsi remplacer CATPilot-FT817.exe.
#ifndef MyVersion
  #define MyVersion "0.0.0"
#endif

[Setup]
AppId={{6B0F8436-7774-4E13-BC98-3FE4A8F00717}
AppName=CAT Pilot FT-817
AppVersion={#MyVersion}
AppPublisher=F4JCF
AppPublisherURL=https://github.com/F4JCF/catpilot-ft817
DefaultDirName={localappdata}\Programs\CATPilot-FT817
DefaultGroupName=CAT Pilot FT-817
PrivilegesRequired=lowest
DisableProgramGroupPage=yes
OutputDir=dist
OutputBaseFilename=CATPilot-FT817-Setup-{#MyVersion}
SetupIconFile=assets\catpilot.ico
UninstallDisplayIcon={app}\CATPilot-FT817.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
CloseApplications=yes

[Languages]
Name: "fr"; MessagesFile: "compiler:Languages\French.isl"
Name: "en"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\CATPilot-FT817.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CAT Pilot FT-817"; Filename: "{app}\CATPilot-FT817.exe"
Name: "{group}\{cm:UninstallProgram,CAT Pilot FT-817}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\CAT Pilot FT-817"; Filename: "{app}\CATPilot-FT817.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\CATPilot-FT817.exe"; Description: "{cm:LaunchProgram,CAT Pilot FT-817}"; Flags: nowait postinstall skipifsilent
