from ultralytics import YOLO


def checkID(model, frame):
    
    results = model(frame,verbose=False,half=True)
    boxes = results[0].boxes
    for box in boxes:
        if box.conf >= 0.5:
            return True
    return False