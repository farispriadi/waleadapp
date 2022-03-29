; This is the generic InnoSetup script used to generate Windows Installer files
; for both OppinetSIM and PertafloSIM
; 
; To use this script you should run it via ISCC.exe which included when installing
; InnoSetup suite.
; 
; Required parameters
; 
; #define MyAppName "PertafloSIM"
; #define MyAppVersion "1.0"
; #define MyAppPublisher "RTC Pertamina - RC-OPPINET ITB"
; #define AppDeployDir "E:\Abit\DEPLOY\Pertaflo Installer"
; #define AppSourceDir "E:\Abit\pyoppinet"
; #define AppLogoPath AppSourceDir + "\system\app\resources\icons\logo_pertaflo.ico"
; #define MyDateTimeString GetDateTimeString('yyyymmdd_hhnn', '-', ':');
; #define AppInstallerName MyAppName + "-" + MyAppVersion + "-setup-" + MyDateTimeString

#define MyAppURL "http://oppinet.ppms.itb.ac.id"
#define MyAppExeName MyAppName + ".exe"

[Setup] 
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{{#MyAppId}}}
AppName={#MyAppTitle}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={code:GetProgramFiles}\{#MyAppName}
DisableProgramGroupPage=yes
Compression=lzma
SolidCompression=yes
OutputBaseFilename={#AppInstallerName}
OutputDir={#AppDeployDir}
SetupIconFile={#AppLogoPath}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#AppSourceDir}\dist\{#MyAppName}\{#MyAppName}.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#AppSourceDir}\dist\{#MyAppName}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs ; Permissions: everyone-full

[Dirs]
Name: "{app}\system"; Permissions: everyone-full
;Name: "{app}\validation"; Permissions: everyone-full
Name: "{app}\docs"; Permissions: everyone-full

[Icons]
Name: "{commonprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

; fitur "Launch after install"
[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

; ref : https://stackoverflow.com/a/38452667/2496217
[Code]

function GetProgramFiles(Param: string): string;
begin
  if IsWin64 then Result := ExpandConstant('{pf64}')
    else Result := ExpandConstant('{pf32}')
end;
