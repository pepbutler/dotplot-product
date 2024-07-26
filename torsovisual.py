import cv2


# Rough coordinates, adjust as necessary
GRID_BOUNDARY = (420, 890)
BOX_DIM = 75

def convert(coordinate):
    # Define top left corner position of box in coordinates.png image using the scan coordinate
    x = GRID_BOUNDARY[0] + (ord(coordinate[0]) - ord("A")) * BOX_DIM
    y = GRID_BOUNDARY[1] + (int(coordinate[1]) - 1) * BOX_DIM

    return (x, y)

def generate_image(patient_id, coordinate):
    torso_image = cv2.imread("coordinates.png")

    # Box coordinates
    top_left = convert(coordinate)
    bottom_right = (top_left[0] + BOX_DIM, top_left[1] + BOX_DIM)

    color = (0, 0, 255)  # red color in BGR format

    # Draw location of breast lesion onto image as a red rectangle and save
    cv2.rectangle(torso_image, top_left, bottom_right, color, thickness=cv2.FILLED)
    patient_id = str(patient_id)
    cv2.imwrite(f"patient-images/{patient_id}.png")



