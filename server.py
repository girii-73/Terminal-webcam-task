import socket
import cv2
import pickle
import struct

def start_webcam_server(host='0.0.0.0', port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    print(f"Webcam server listening on {host}:{port}")
    
    cap = cv2.VideoCapture(0) 
    
    while True:
        conn, addr = server.accept()
        print(f"Client connected from {addr}")
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
                data = pickle.dumps(buffer)
                message = struct.pack("Q", len(data)) + data
                conn.sendall(message)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()
    
    cap.release()
    server.close()

if __name__ == "__main__":
    start_webcam_server()