# Windows Setup Script For Powershell
# ===================================

echo "Searching for profile..."
$profile_exists = Test-path $profile

# Create Profile If It Does not Exist
if ($profile_exists -ne $true) {
  echo "No profile found. Creatin new one..."
  New-item -type file -force $profile

  echo "Updating start-up script..."
  $profile_text = "New-Alias ams "+$PSScriptRoot+"\src\powershell_wrapper.ps1"

} else {

  # Read Old Profile
  $profile_text = cat $profile

  # Append Wrapper Script
  echo "Updating start-up script..."
  $profile_text += "
  New-Alias ams "+$PSScriptRoot+"\src\powershell_wrapper.ps1"

}

# Write New Profile
echo "Saving to Disk..."
echo $profile_text > $profile

# Update Current Session
New-Alias ams $PSScriptRoot\src\powershell_wrapper.ps1

echo "
===========
|| DONE! ||
===========
"
