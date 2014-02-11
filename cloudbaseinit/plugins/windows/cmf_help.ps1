#
# Powershell script to call CMF SOAP services
#
function Add-ComputerToNsc{
    param(
    [parameter(Mandatory=$true)]
    [string[]] $nsc_ids,
    [parameter(Mandatory=$true)]
    [string] $cmf_service 
    )
    $cmfsvc = New-WebServiceProxy -Uri $cmf_service -UseDefaultCredential

    foreach ($nsc in $nsc_ids){
        Write-Host "Calling CMF service to add ${env:COMPUTERNAME} to NSC number $nsc"
        $cmfsvc.AddComputerToNSC($env:COMPUTERNAME, $nsc)
    }
}
