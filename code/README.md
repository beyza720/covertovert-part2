# Covert Timing Channel Implementation Using ICMP Packet Inter-Arrival Times

## Overview
This project implements a covert timing channel using ICMP packets. The covert channel encodes a binary message in the inter-arrival times of packets, allowing data transmission between a sender and a receiver. This approach leverages timing-based covert channels to encode bits (`0` or `1`) and sends them across a network.

The implementation supports the following functionalities:
1. **Send**: Generates and sends a binary message using specific time delays between ICMP packets.
2. **Receive**: Listens for ICMP packets, decodes the binary message based on inter-arrival times, and reconstructs the message.

---

## Parameters and Code Configuration

### General Code Information
- **Covert Channel Code**: `CTC-PIT-ICMP` (Covert Timing Channel - Packet Inter-Arrival Times - ICMP)

### Sender Parameters (`send`)

| Parameter       | Description                                                | Value                         |
|-----------------|------------------------------------------------------------|-------------------------------|
| `wait_0`        | Time delay for encoding a `0` bit                          | `0.05` seconds                |
| `wait_1`        | Time delay for encoding a `1` bit                          | `0.01` seconds                |
| `log_file_name` | File to log the sent binary message                        | `ICMP_TimingInterarrivalChannelSender.log` |

### Receiver Parameters (`receive`)

| Parameter       | Description                                                | Value                         |
|-----------------|------------------------------------------------------------|-------------------------------|
| `bound_0`       | Lower bound for identifying a `0` bit                      | `0.1` seconds                 |
| `bound_1`       | Upper bound for identifying a `1` bit                      | `0.04999` seconds             |
| `log_file_name` | File to log the decoded binary message                     | `ICMP_TimingInterarrivalChannelReceiver.log` |

---

## Functional Details

### Sending (`send`)

1. **Message Generation**:
   - A random binary message randomly generated.
   - The message is logged into `ICMP_TimingInterarrivalChannelSender.log`.

2. **Message Encoding**:
   - The binary message is encoded in the time intervals between consecutive ICMP packets.
   - For each bit in the message:
     - A `0` bit is encoded by waiting `0.05` seconds before sending the next packet.
     - A `1` bit is encoded by waiting `0.01` seconds before sending the next packet.

3. **Packet Transmission**:
   - ICMP packets are constructed and sent to the receiver using the Scapy library.
   - A dummy packet is sent at the end to signal termination.

---

### Receiving (`receive`)

1. **Packet Sniffing**:
   - Listens for ICMP packets using a packet sniffer.
   - Records the arrival time of each packet.

2. **Message Decoding**:
   - Calculates the inter-arrival time between consecutive packets.
   - Decodes bits based on timing bounds:
     - If `inter-arrival time < 0.04999`: Encodes a `1` bit.
     - If `0.04999 < inter-arrival time < 0.1`: Encodes a `0` bit.
     - If the inter-arrival time exceeds `0.1`: Decoding is stopped because of long delay.

3. **Message Reconstruction**:
   - Binary data is decoded into characters, reconstructing the original message.
   - If a `.` character is detected, the receiver terminates and logs the full message.

---

## Covert Channel Capacity

The covert channel capacity (in bits per second) was calculated using:
- Binary message length
- Transmission time

The covert channel achieved a capacity of approximately **18.19 bits per second**.

---

## Limitations and Challenges

1. **Network Delay**:
   - Variability in network latency can impact accurate decoding of bits.
   - Fine-tuned bounds (`0.1` and `0.04999`) are essential for reliable decoding.

2. **Timing Constraints**:
   - The minimum threshold for encoding `0` and `1` bits must be carefully chosen to avoid overlap with natural network delays.

3. **Channel Capacity**:
   - Higher delays between packets result in lower capacity, but improve reliability.
   - Optimizing delay parameters is crucial for balancing speed and accuracy.

---

Authors:

İbrahim Ersel Yiğit, 2449072

Beyza Nur Koç, 2443430