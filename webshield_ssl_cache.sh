#!/bin/bash
#Specify more domains
DOMAINS=$(find /home/ -mindepth 1 -maxdepth 1 -type d ! -name 'backup' !  -name 'vmail')

BASE_PATH="/etc/letsencrypt/live"

SCRIPT_PATH="/jsupply_new_ssl.py"
LOG_PATH="/var/log/jsupply_new_ssl.log"

#provided that the certificates for each domain can be found in a similar path,we can enumerate those
for domain in $DOMAINS
do
    domain_base=$(basename "$domain")
    KEY_PATH="$BASE_PATH/$domain_base/privkey.pem"
    CERT_PATH="$BASE_PATH/$domain_base/cert.pem"
    CHAIN_PATH="$BASE_PATH/$domain_base/fullchain.pem"
    # Remove old cache entry, if there is a chance the certificate files will not exist at some point the deletion can me marked as text
   python3  $SCRIPT_PATH -d $domain_base -r >> $LOG_PATH 2>&1

    # Add new certificate to cache
    python3 $SCRIPT_PATH -d $domain_base -k $KEY_PATH -c $CERT_PATH -C $CHAIN_PATH -a >> $LOG_PATH 2>&1
done
