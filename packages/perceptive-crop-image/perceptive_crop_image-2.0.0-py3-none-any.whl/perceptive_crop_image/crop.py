import cv2
import numpy as np

def manual_crop(image_path, output_path='cropped_image.jpg'):
    count = 0
    points = []
    base_img = cv2.imread(image_path)

    def mouseTrack(event, x, y, flags, param):
        nonlocal count, points, base_img

        if event == cv2.EVENT_LBUTTONDBLCLK:
            count += 1
            cv2.circle(base_img, (x, y), 2, (0, 255, 0), 2)
            points.append((x, y))
            if count >= 4:
                print(points)
                roi_pts = np.array(points, dtype=np.float32)
                top_left = points[0]
                top_right = points[1]
                btm_left = points[2]
                btm_right = points[3]
                print(np.linalg.norm(np.array(top_right) - np.array(top_left)))

                width = int(np.linalg.norm(np.array(top_right) - np.array(top_left)))
                height = int(np.linalg.norm(np.array(btm_left) - np.array(top_left)))
                pts_dst = np.array([
                    [0, 0],
                    [width - 1, 0],
                    [0, height - 1],
                    [width - 1, height - 1]
                ], dtype=np.float32)
                matrix = cv2.getPerspectiveTransform(roi_pts, pts_dst)
                cropped_img = cv2.warpPerspective(base_img, matrix, (width, height))
                cv2.imwrite(output_path, cropped_img)
                cv2.imshow("cropped_img Image", cropped_img)
                count = 0
                points.clear()
            cv2.imshow("Base Image", base_img)
            
            print("Successfully Cropped based on co-ordinate points")

    cv2.namedWindow('Base Image')
    cv2.setMouseCallback('Base Image', mouseTrack)

    while True:
        cv2.imshow("Base Image", base_img)
        if cv2.waitKey(1) & 0xFF == 27:  # Escape key
            break

    cv2.destroyAllWindows()
