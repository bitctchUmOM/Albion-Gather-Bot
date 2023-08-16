import ultralytics
model = ultralytics.YOLO('best.pt')

results = model.predict('atack.png', show = False, save=False, imgsz=(1280, 736), conf=0.3, line_width = 1)

for r in results:
    for c in r.boxes:
        print(c.xyxy[0])
    for c in r.boxes.cls:
        print(model.names[int(c)])
