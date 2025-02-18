[Setup]
AppName=Autotyper
AppVersion=1.2.1
AppId={3296af3a-27ab-424e-b4b6-921028d4bd45}
DefaultDirName={pf}\Autotyper
DefaultGroupName=Autotyper
OutputDir=installer
OutputBaseFilename=AutotyperSetup
Compression=lzma
SolidCompression=yes

[Code]
function InitializeSetup(): Boolean;
var
  UninstallString: string;
  ResultCode: Integer;
begin
  // Check for previous installation
  if RegQueryStringValue(HKLM, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\Autotyper_is1', 'UninstallString', UninstallString) or
     RegQueryStringValue(HKCU, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\Autotyper_is1', 'UninstallString', UninstallString) then
  begin
    // Ask the user if they want to uninstall the previous version
    if MsgBox('A previous version of Autotyper was found. Do you want to uninstall it before installing the new version?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      // Run the uninstaller.
      Exec(ExpandConstant('{uninstallexe}'), '', '', SW_SHOW, ewWaitUntilTerminated, ResultCode);
    end;
  end;

  Result := True; // Continue with installation
end;

[Files]
Source: "dist\Autotyper.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Autotyper"; Filename: "{app}\Autotyper.exe"

[Run]
Filename: "{app}\Autotyper.exe"; Description: "{cm:LaunchProgram,Autotyper}"; Flags: nowait postinstall skipifsilent