with open("/data/data/com.termux/files/home/Projects/polymath-integrated/target/release/polymath-void-agent", "rb") as f:
    data = f.read()

import re
matches = re.findall(b'https://generativelanguage.googleapis.com[^\x00]*', data)
for m in matches:
    print(m)
