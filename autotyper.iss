[Setup]
AppName=Autotyper
AppVersion=1.0
DefaultDirName={pf}\Autotyper
DefaultGroupName=Autotyper
OutputDir=installer
OutputBaseFilename=AutotyperSetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\Autotyper.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Autotyper"; Filename: "{app}\Autotyper.exe"

[Run]
Filename: "{app}\Autotyper.exe"; Description: "{cm:LaunchProgram,Autotyper}"; Flags: nowait postinstall skipifsilent