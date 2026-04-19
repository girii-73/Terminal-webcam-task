import socket
import cv2
import pickle
import struct

def connect_to_webcam(host, port=5555):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(f"Connected to {host}:{port}")
    
    data = b""
    payload_size = struct.calcsize("Q")
    
    try:
        while True:
            # Receive frame size
            while len(data) < payload_size:
                packet = sock.recv(4 * 1024)
                if not packet:
                    break
                data += packet
            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            
            # Receive frame data
            while len(data) < msg_size:
                data += sock.recv(4 * 1024)
            
            frame_data = data[:msg_size]
            data = data[msg_size:]
            
            # Decompress and display
            frame = pickle.loads(frame_data)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            
            cv2.imshow("Remote Webcam", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    import sys
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    connect_to_webcam(host)