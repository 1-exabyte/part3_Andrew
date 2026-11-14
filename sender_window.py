# Jinan Sief El Deen
# Member 2: sending window, ACK handling, and retransmissions
import time


def fill_window(packets, base, next_seq, window_size, send_packet, state, send_time, stats):
    while next_seq < len(packets) and next_seq < base+window_size:

        print("SEND", next_seq)
        send_packet(packets[next_seq])
        state[next_seq] = "S"
        send_time[next_seq] = time.monotonic()
        stats["transmissions"] += 1
        next_seq += 1
    return next_seq


def process_ack(base, next_seq, ack_num, dup_count, packets, send_packet, state, send_time, stats):

    if base < ack_num and ack_num <= next_seq:
        for i in range(base, ack_num):
            state[i] = "A"
        base = ack_num
        dup_count = 0
        print("ACK ", ack_num, ", slide window, base =", base)
        # ACK 4 -> slide window, base = 4
    elif ack_num == base and base < next_seq:
        dup_count += 1
        print("DUP ACK ", ack_num, "(", dup_count, ")")

        if dup_count == 3:
            print("3 DUP ACKS, fast retransmit")
            retransmit(base, packets, send_packet, state, send_time, stats)
    return base, dup_count


def retransmit(seq_num, packets, send_packet, state, send_time, stats):

    print("RETRANSMIT", seq_num)
    send_packet(packets[seq_num])

    state[seq_num] = "R"
    send_time[seq_num] = time.monotonic()

    stats["transmissions"] += 1
    stats["retransmissions"] += 1


if __name__ == "__main__":
    def practice_send(packet):
        pass

    packets = list(range(8))
    base = 0
    next_seq = 0
    dup_count = 0
    window_size = 4

    state = ["-"] * len(packets)
    send_time = {}
    stats = {"transmissions": 0, "retransmissions": 0}

    # Send packets 0, 1, 2, 3.
    next_seq = fill_window(
        packets, base, next_seq, window_size,
        practice_send, state, send_time, stats
    )

    # ACK 1 confirms packet 0.
    base, dup_count = process_ack(
        base, next_seq, 1, dup_count,
        packets, practice_send, state, send_time, stats
    )

    # The newly available slot lets us send packet 4.
    next_seq = fill_window(
        packets, base, next_seq, window_size,
        practice_send, state, send_time, stats
    )

    # Pretend three more ACKs arrive, all requesting packet 1.
    for _ in range(3):
        base, dup_count = process_ack(
            base, next_seq, 1, dup_count,
            packets, practice_send, state, send_time, stats
        )

    print("After duplicate ACKs:")
    print("state:", state)
    print("stats:", stats)

    # Pretend the retransmission succeeds and ACK 5 arrives.
    base, dup_count = process_ack(
        base, next_seq, 5, dup_count,
        packets, practice_send, state, send_time, stats
    )

    print("After ACK 5:")
    print("state:", state)
    print("base:", base)
    print("next_seq:", next_seq)
    print("dup_count:", dup_count)
