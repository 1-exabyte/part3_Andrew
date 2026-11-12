# receiver.py -- Member 3 (Andrew Samaha): receiver and acknowledgements
#
# Packet header (agreed by the group):  type (1 byte) | seq (4 bytes) | data
#   type 0 = DATA   type 1 = ACK   type 2 = END (data = SHA-256 of the file)
#
# Every ACK carries "expected" = the number of the next packet I need.
#
# Run:  python receiver.py              (port 9000, writes received.txt)
#       python receiver.py 9000 out.bin (port, output file)

import hashlib
import socket
import struct
import sys
import time

DATA = 0
ACK = 1
END = 2

port = 9000
out_file = "received.txt"
if len(sys.argv) > 1:
    port = int(sys.argv[1])
if len(sys.argv) > 2:
    out_file = sys.argv[2]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", port))

print("========== RECEIVER (Member 3) ==========")
print(f"Listening on port : {port}")
print(f"Output file       : {out_file}")
print("=========================================")

expected = 0        # next packet number I need
buffer = {}         # packets that came early:  seq -> data
chunks = []         # the file, in order
end_seq = None      # number of the END packet, once it arrives
end_hash = None     # SHA-256 sent inside END

# counters for the summary
received = 0
in_order = 0
out_of_order = 0
gap_fills = 0
duplicates = 0
start_time = None


def send_ack():
    sock.sendto(struct.pack("!BI", ACK, expected), addr)


while True:
    try:
        data, addr = sock.recvfrom(65535)
    except ConnectionResetError:        # Windows quirk when the sender closes: ignore it
        continue

    ptype, seq = struct.unpack("!BI", data[:5])
    payload = data[5:]
    received += 1
    if start_time is None:
        start_time = time.time()

    # ---- END packet: remember where the file ends and its fingerprint (never glued)
    if ptype == END:
        end_seq = seq
        end_hash = payload
        print(f"RECV END({seq}) -> file has {seq} packets")

    # ---- in order: glue it, then glue everything in the buffer that now follows
    elif seq == expected:
        chunks.append(payload)
        expected += 1
        first = seq
        while expected in buffer:
            chunks.append(buffer.pop(expected))
            expected += 1
        if expected - first == 1:
            in_order += 1
            print(f"RECV {seq} in order -> ACK {expected}")
        else:
            gap_fills += 1
            print(f"RECV {seq} fills gap -> ACK {expected}   (glued {first} to {expected - 1})")

    # ---- duplicate: already glued, or already waiting in the buffer
    elif seq < expected or seq in buffer:
        duplicates += 1
        print(f"RECV {seq} duplicate, discarded -> ACK {expected} (re-sent)")

    # ---- out of order: came early, keep it for later
    else:
        buffer[seq] = payload
        out_of_order += 1
        print(f"RECV {seq} out of order, buffered -> DUP ACK {expected}   buffer={sorted(buffer)}")

    # ---- every data packet is here -> count END as received, finish
    if end_seq is not None and expected == end_seq:
        expected += 1
        send_ack()
        print(f"ACK {expected} (END received)")
        break

    send_ack()

# ---- write the file, then check it against the SHA-256 from END
end_time = time.time()
file_data = b"".join(chunks)
with open(out_file, "wb") as f:
    f.write(file_data)
with open(out_file, "rb") as f:
    match = hashlib.sha256(f.read()).digest() == end_hash

print("================ SUMMARY ================")
print(f"Packets received        : {received}")
print(f"  in order              : {in_order}")
print(f"  out of order (buffer) : {out_of_order}")
print(f"  filled a gap          : {gap_fills}")
print(f"  duplicates discarded  : {duplicates}")
print(f"File written            : {out_file} ({len(file_data)} bytes)")
print(f"Transfer time           : {end_time - start_time:.3f} s")
print(f"SHA-256                 : {'MATCH' if match else 'MISMATCH'}")
print("=========================================")
