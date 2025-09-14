import argparse, time, requests, cv2
from ultralytics import YOLO

# CLI args
parser = argparse.ArgumentParser()
parser.add_argument('--source', default=0, help='camera index or video path')
parser.add_argument('--direction', required=True, help='NORTH|SOUTH|EAST|WEST')
parser.add_argument('--server', default='http://localhost:5000', help='backend server URL')
parser.add_argument('--interval', type=float, default=2.0, help='seconds between updates')
parser.add_argument('--sim', action='store_true', help='simulation mode (no YOLO, random counts)')
args = parser.parse_args()

VEHICLE_CLASS_IDS = {2, 3, 5, 7}  # car, motorbike, bus, truck

# Simulation mode (for demo without YOLO)
if args.sim:
    import random
    print("Simulation mode ON")
    while True:
        c = random.randint(0, 30)
        try:
            requests.post(f"{args.server}/update_traffic",
                          json={'direction': args.direction, 'count': c}, timeout=5)
            print(f"Sent {c} vehicles for {args.direction}")
        except Exception as e:
            print("Error sending:", e)
        time.sleep(args.interval)
    exit()

# Load YOLO
print("Loading YOLO model (yolov8n.pt)...")
model = YOLO("yolov8n.pt")

# Open video source
try:
    src = int(args.source)
except ValueError:
    src = args.source

cap = cv2.VideoCapture(src)
if not cap.isOpened():
    raise SystemExit(f"❌ Cannot open source: {args.source}")

last_post = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run inference
    results = model(frame)[0]

    try:
        classes = results.boxes.cls.cpu().numpy().astype(int).tolist()
    except Exception:
        classes = []

    vehicle_count = sum(1 for c in classes if c in VEHICLE_CLASS_IDS)

    # Annotate frame
    annotated = results.plot()
    cv2.putText(annotated, f"Vehicles: {vehicle_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    cv2.imshow(f"Traffic - {args.direction}", annotated)

    # Post to backend
    now = time.time()
    if now - last_post >= args.interval:
        try:
            requests.post(f"{args.server}/update_traffic",
                          json={'direction': args.direction, 'count': vehicle_count}, timeout=5)
        except Exception as e:
            print("Post error:", e)
        last_post = now

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
