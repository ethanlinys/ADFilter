from datetime import datetime

import requests

HOSTS_DICT = {
    "StevenBlack": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
    "yhosts": "https://raw.githubusercontent.com/VeleSila/yhosts/master/hosts.txt",
}

# download the conf file
for k, v in HOSTS_DICT.items():
    with requests.get(v, stream=True) as r:
        r.raise_for_status()
        with open(f"{k}.hosts", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

# convert conf file to list
for k in HOSTS_DICT:
    with open(f"{k}.hosts") as in_f:
        with open(f"{k}.list", "w") as out_f:
            out_f.write(f"# {datetime.now()}\n")
            for line in in_f.read().splitlines():
                if line.strip():
                    if line.startswith("#"):
                        continue
                    if not (line.startswith("0.0.0.0") or line.startswith("127.0.0.1")):
                        continue
                    domain_str = line.split(" ")[1]
                    if domain_str == "localhost.localdomain":
                        continue
                    if domain_str == "0.0.0.0":
                        continue
                    if "." not in domain_str:
                        continue
                    out_f.write(f"{domain_str}\n")
