## FDM Commit script

Cisco Firepower Device Manager allows the automatic download of geolocation, intrusion rule and VDB improvements, but 
does not automatically deploy them.  This is a script to automatically commit intrusion rule, VDB and geolocation 
updates to your FDM.  It checks to make certain that there are no other pending changes to the configuration.  If there 
are additional changes or any errors, the script sends notification with a Webex Teams message.

The script was tested with FTD 6.6, but should also work with some previous versions.  If you are able to test on 
previous versions, I will gladly credit you as a contributor.

I set this script to run once daily after the FDM update task has completed via a cron job on a Pi.  It is still early
days, so I am working on refining error handling to account for common variations of these updates.

## Requirements
* requests
* urllib3
* webexteamssdk

## Environment Variables Required
* USER - FDM admin username
* PASS - FDM admin password
* EMAIL - email address of Webex Teams user to notify with errors
* WEBEX_TEAMS_ACCESS_TOKEN - Bearer token for Webex Teams
* FDMADDRESS - IP address or FQDN of FDM management

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/brbuxton/fdm-commit)