# protocol.py -- shared packet format (agreed by all members)
#
# Every packet:   type (1 byte) | seq (4 bytes) | data
#
#   DATA (0): seq = chunk number,          data = a piece of the file
#   ACK  (1): seq = next packet expected,  data = nothing
#   END  (2): seq = number of chunks,      data = SHA-256 of the whole file (32 bytes)
