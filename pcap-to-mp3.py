
import os
import re

MP3_HEADER_REGEX = re.compile(rb'(ID3.{0,1024}|(\xff[\xfb\xf3\xf2][\x00-\xff]{2}))')
LAME_TAG = b'LAME3.100'

def carve_mp3_from_raw(pcap_path, output_folder="raw_carved_mp3"):
    with open(pcap_path, 'rb') as f:
        raw_data = f.read()

    os.makedirs(output_folder, exist_ok=True)

    matches = list(MP3_HEADER_REGEX.finditer(raw_data))
    if not matches:
        print("[-] No MP3 headers found.")
        return

    for i, match in enumerate(matches):
        start = match.start()
        chunk = raw_data[start:start + 10_000_000]
        lame_pos = chunk.find(LAME_TAG)
        if lame_pos != -1:
            print(f"[+] LAME tag found in chunk {i} at offset {lame_pos}")

        out_file = os.path.join(output_folder, f"carved_{i}.mp3")
        with open(out_file, 'wb') as out:
            out.write(chunk)
        print(f"[+] MP3 carved to: {out_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python raw_mp3_carver.py capture.pcap")
        sys.exit(1)

    carve_mp3_from_raw(sys.argv[1])