#This part is made by Jean Paul. 
import struct, hashlib
#function split_file returns a list of all chunks the packet was divided into, in order, ,with a set chunk_size.
def split_file(filepath, chunk_size=1024):
    if chunk_size<=0:
        raise ValueError("Chunk size must be greater than 0.")
    
    with open(filepath, "rb") as f:
        data = f.read()
        
    length = len(data)
    chunks = []
    for i in range(0, length, chunk_size):
        chunks.append(data[i:i+chunk_size])
    return chunks
#this function creates a header with the packet type (0= DATA, 1=ACK, 2=END), and the sequence number and also the length (it computes the payload size)
#and it then returns a full packets consisting of header + payload.
#I added handling for out of acceptable range values and for unexpected types.
def make_packet(packet_type, seq, payload):
    if type(packet_type) is not int:
        raise TypeError("Expected an int for packet_type")
    if type(seq) is not int:
        raise TypeError("Expected an int for seq")
    if type(payload) is not bytes:
        raise TypeError("Expected bytes type for payload")
    length = len(payload)
    if length>65535 or length<0:
        raise ValueError("payload length must be in range 0-65,535")
    if packet_type not in (0, 1, 2):
        raise ValueError("packet_type can only be 0, 1 or 2")
    if seq>4294967295 or seq<0:
        raise ValueError("seq must be in range 0-4,294,967,295")
    
    header = struct.pack("!BIH", packet_type, seq, len(payload))
    return header+payload
packet = make_packet(0, 3, b"Hello")

def make_end_packet(filepath, number_of_chunks):
    with open(filepath, "rb") as f:
        data = f.read()
    return make_packet(2, number_of_chunks, hashlib.sha256(data).digest())
