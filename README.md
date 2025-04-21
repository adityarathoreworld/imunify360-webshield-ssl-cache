**WebShield SSL-cache is not configured**

**Introduction**
This is for the Imunify360 users who are facing issues with the webshield module due to the SSL cache.

**Instructions**

ownload webshield_ssl_cache.sh
change permission with chmod -x  webshield_ssl_cache.sh  
Run this script in cron. 

Also, check /var/log/jsupply_new_ssl.log to see if there is any error.

**Require** 
jsupply_new_ssl.py script from "https://cloudlinux.zendesk.com/hc/en-us/articles/360016054460-WebShield-SSL-cache-configuration-on-Imunify360-stand-alone-installation"

**How to run cron?**
crontab -e
0 * * * * /webshield_ssl_cache.sh.

**Configurations**
Change the path to see the domain name /home/$domain name is a default path in CyberPanel. I had excluded vmail and backup directory you can exclude more via (! - name "excluded folder name")

**CODE**
DOMAINS=$(find /home/ -mindepth 1 -maxdepth 1 -type d ! -name 'backup' !  -name  'vmail')
$domain_base=$(basename "$domain")

**Change path for script and log**
SCRIPT_PATH="/jsupply_new_ssl.py"
LOG_PATH="/var/log/jsupply_new_ssl.log"

**Change the path of SSL and filename for private key, chain and cert**

BASE_PATH="/etc/letsencrypt/live"

KEY_PATH="$BASE_PATH/$domain_base/privkey.pem"
CERT_PATH="$BASE_PATH/$domain_base/cert.pem"
CHAIN_PATH="$BASE_PATH/$domain_base/fullchain.pem"
                                                                                                                                                                                                                                 
- Script by Aditya Rathore from a2zcloud.net for imunify360 webshield ssl cache issue on cyberpanel
