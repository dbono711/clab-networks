#!/bin/bash

for r in clab-evpn-vxlan-01-spine01 clab-evpn-vxlan-01-spine02 clab-evpn-vxlan-01-leaf01; do
  echo -n "Checking for installed cRPD license on $r..."
  license=$(docker exec -it $r cli show system license | grep SKU | xargs)
  if [ -z "$license" ]; then
    if [ ! -e junos_sfnt.lic ]; then
      echo "please download your free eval license key from https://www.juniper.net/us/en/dm/crpd-free-trial.html"
      echo "(login required) and rename it to 'junos_sfnt.lic' add place it in the root of this repository"
    fi
    echo -n "[FAILED] >>> Adding license key 'junos_sfnt.lic' to $r..."
    docker cp junos_sfnt.lic $r:/config/license/safenet/junos_sfnt.lic >/dev/null 2>&1
    docker exec -it $r cli request system license add /config/license/safenet/junos_sfnt.lic >/dev/null 2>&1
    echo "[OK]"
  else
    echo "[OK]"
  fi
done
