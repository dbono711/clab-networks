#!/bin/bash
SWITCHES=("spine01" "spine02" "leaf01" "leaf02" "leaf03")

for switch in ${SWITCHES[@]}; do
  echo -n "Checking for installed cRPD license on $switch..."
  license=$(docker exec -it clab-evpn-vxlan-01-$switch cli show system license | grep SKU | xargs)
  if [ -z "$license" ]; then
    if [ ! -e junos_sfnt.lic ]; then
      echo "please download your free eval license key from https://www.juniper.net/us/en/dm/crpd-free-trial.html"
      echo "(login required) and rename it to 'junos_sfnt.lic' add place it in the root of this repository"
    fi
    echo -n "[FAILED] >>> Adding license key 'junos_sfnt.lic' to clab-evpn-vxlan-01-$switch..."
    docker cp junos_sfnt.lic clab-evpn-vxlan-01-$switch:/config/license/safenet/junos_sfnt.lic >/dev/null 2>&1
    docker exec -it clab-evpn-vxlan-01-$switch cli request system license add /config/license/safenet/junos_sfnt.lic >/dev/null 2>&1
    echo "[OK]"
  else
    echo "[OK]"
  fi
done
