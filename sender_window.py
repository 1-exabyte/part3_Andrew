# Jinan Siefeldeen
# Member 2: sending window, ACK handling, and retransmissions
import time


def fill_window(packets, base, next_seq, window_size, send_packet, state, send_time, stats):
    while next_seq < len(packets) and next_seq < base+window_size:
        send_packet(packets[next_seq])
        state[next_seq] = "S"
        send_time[next_seq] = time.monotonic()
        stats["transmissions"] += 1
        print("SEND", next_seq)
        next_seq += 1
    return next_seq


def process_ack(base, next_seq, ack_num):
    if base < ack_num and ack_num <= next_seq:
        return ack_num
    return base


def retransmit(seq_num, packets, send_packet, state, send_time, stats):
    send_packet(packets[seq_num])

    state[seq_num] = "R"
    send_time[seq_num] = time.monotonic()

    stats["transmissions"] += 1
    stats["retransmissions"] += 1

    print("RETRANSMIT", seq_num)


if __name__ == "__main__":  # Used ai to understand syntax of this if condition
    def practice_send(packet):
        pass
    packets = list(range(8))
    base = 0
    next_seq = 0
    window_size = 3
    state = ["-"] * len(packets)
    send_time = {}
    stats = {"transmissions": 0, "retransmissions": 0}
    next_seq = fill_window(packets, base, next_seq,
                           window_size, practice_send, state, send_time, stats)

    print("base:", base)
    print("next_seq:", next_seq)

    ack_no = 1
    print("Received ACK", ack_no)

    base = process_ack(base, next_seq, ack_no)

    next_seq = fill_window(
        packets, base, next_seq, window_size, practice_send, state, send_time, stats)

    print("base:", base)
    print("next_seq:", next_seq)
    print(state)
    print(stats)
    print("Testing retransmission:")

    retransmit(
        base, packets, practice_send, state, send_time, stats
    )

    print("state:", state)
    print("stats:", stats)
    print("base:", base)
    print("next_seq:", next_seq)
