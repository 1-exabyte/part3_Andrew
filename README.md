# Reliable File Transfer over UDP

A file is sent over UDP (which can lose, repeat and reorder packets) and arrives complete and correct.
Python 3, standard library only.

## Files

| File | What it does |
|---|---|
| `protocol.py` | The packet format all members agreed on |
| `sender.py` | Sender: splits the file into packets, window and timers |
| `channel.py` | Unreliable channel: drops and reorders packets on purpose |
| `receiver.py` | Receiver: cumulative ACKs, buffering, reassembly, SHA-256 check |
| `practice/` | Practice and test scripts used while building the receiver |

## Packet format

```
type (1 byte) | seq (4 bytes) | data
```

| Type | seq | data |
|---|---|---|
| DATA (0) | chunk number | a piece of the file |
| ACK (1) | next packet expected | nothing |
| END (2) | number of chunks | SHA-256 of the whole file (32 bytes) |

## How to run

Start the receiver first, then the sender:

```
python receiver.py                  # listens on port 9000, writes received.txt
python receiver.py 9000 out.bin     # choose the port and output file
```

The receiver prints its settings, one line per packet (for example `RECV 12 in order -> ACK 13`),
and a summary ending in `SHA-256 : MATCH` or `MISMATCH`.
