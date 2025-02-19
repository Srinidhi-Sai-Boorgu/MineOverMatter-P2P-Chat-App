# P2P Chat Application
This repository contains the code for Assignment-2 of the course CS-216: Introduction to Blockchain. The feature specificied by the bonus question has been implemented as well.

<div align="center">

### Team: MineOverMatter
| Name         | Roll No |
|--------------|---------|
| Abhinav Bitragunta        | 230001003     |
| Aman Gupta          | 230001006     |
| Srinidhi Sai Boorgu     | 230001072     |

</div>

## Instructions to Run the Program

1. Open a terminal.
2. Navigate to the directory where the script is located.
3. Run the program using the command:
   ```sh
   python app.py
   ```
4. Enter the name of your peer node (one word) when prompted.
5. Enter a port number for your server to listen on (Port: 1024 to 49151).
6. Choose an option from the menu to interact with other peers.

## Functionalities

### 1. Send Message
- Select option `1` from the menu.
- Enter the recipient's IP address and their listening port.
- Type the message you want to send.
- The message is encoded into the required format before transmission.
- On the recipient's side, the message is decoded back into readable format.
- Upon sending a message "exit" (not case sensitive), you will be removed from the recipient's peer list.

### 2. Query Peers
- Select option `2` from the menu.
- Displays a list of peers who have sent you a message or connected to you.
- The list consists of IP addresses, ports, and corresponding peer names.

### 3. Connect to Active Peers (Bonus Feature)
- Select option `3` from the menu.
- Sends a connection message to every peer in your list.
- This ensures that they update their peer list with your information as well.

### 4. Exit
- Select option `0` from the menu.
- Sends an `exit` message to all peers in your list.
- This causes them to remove your information from their peer list.
- Stops the server from listening on its assigned port.

## Technical Details

- Every new peer is bootstrapped with two static IP-port combinations (`10.206.4.201:1255` and `10.206.5.228:6555`).
- The program uses ephemeral ports when making outgoing connections to other peers.
- The server and client run on separate threads to allow simultaneous sending and receiving of messages.
- Messages are encoded in the following format:
```
<IP ADDRESS:PORT> <peer name> <message>
```

## Dependencies 

- Python module `socket`
- Python module `threading`
