def check_ppe(detected_classes):
    helmet = 1 if "helmet" in detected_classes else 0
    vest = 1 if "vest" in detected_classes else 0
    shoes = 1 if "shoes" in detected_classes else 0
    return helmet, vest, shoes
