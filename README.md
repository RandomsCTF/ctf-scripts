# ctf-scripts
A collection of short scripts for analysis, encryption and forensics, that can be used for CTF and/or security assessments.

All scripts are GPLv3 licensed unless stated otherwise. Use for **good**, not for evil...

Higly recommended (but not necessary) is the `virtualenv` package, as it virtualizes your Python environments.


## forensics/extract_file.py
Extracts files from a pcap file containing a (fragmented) HTTP download or stream.
Example usage:
```
justsniffer -f myfile.pcap -l "%response" -e 'extract_file.py output.file'
```

This will extract the (fragmented) HTTP download from myfile.pcap and writes the output to output.file
justniffer will take care of the lower protocol layers.

Currently `extract_file.py` only handles streamed input.


## web/timing-bruteforcer.py
Bruteforces passwords by using a timing attack on webforms.
Based on the notion that successful password (characters) are expected to take longer(!) to process than unsuccessful passwords.

Example usage:
```
timing_bruteforcer.py http://my.site.com --username admin
```

Currently only hexadecimal 'passwords' are supported.


## Setup
```
git clone https://github.com/RandomsCTF/ctf-scripts.git
which virtualenv && virtualenv ctf-scripts && pushd ctf-scripts
[ -f bin/activate ] && source bin/activate
[ -f Scripts/Activate ] && source Scripts/Activate
```


