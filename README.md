## FDM Commit script

A script to automatically commit intrusion rule, VDB and geolocation updates to your FDM.  The script sends a Webex
Teams message with any errors.

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