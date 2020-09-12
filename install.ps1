# Windows Setup Script For Powershell
# ===================================

$profile_exists = Test-path $profile

# Create Profile If It Does not Exist
if ($profile_exists -ne $true) {
  New-item -type file -force $profile
  $profile_text = "New-Alias ams "+$PSScriptRoot+"\src\powershell_wrapper.ps1"

} else {

  # Read Old Profile
  $profile_text = cat $profile

  # Append Wrapper Script
  $profile_text += "
  New-Alias ams "+$PSScriptRoot+"\src\powershell_wrapper.ps1"

}

# Write New Profile
echo $profile_text > $profile

# Update Current Session
New-Alias ams $PSScriptRoot\src\powershell_wrapper.ps1
