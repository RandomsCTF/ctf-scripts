# ctf-scripts
A collection of short scripts for analysis, encryption and forensics, that can be used for CTF and/or security assessments.

All scripts are GPLv3 licensed unless stated otherwise. Use for **good**, not for evil...

## forensics/extract_file.py
Extracts files from a pcap file containing a (fragmented) HTTP download or stream.
Example usage:
```
justsniffer -f myfile.pcap -l "%response" -e 'extract_file.py output.file'
```

This will extract the HTTP download from myfile.pcap and writes the output to output.file


## Setup
```
git clone https://github.com/RandomsCTF/ctf-scripts.git
virtualenv ctf-scripts
pushd ctf-scripts
source Scripts/Activate
```


