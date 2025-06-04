import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox

def compare_images(reference_images, video_source=0, similarity_threshold=0.1):
    # Load the reference images
    references = []
    for image_path in reference_images:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Error: Could not load the reference image {image_path}.")
            return
        references.append((image_path, img))

    # Initialize video capture
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    # ORB detector for feature extraction
    orb = cv2.ORB_create()

    # Compute keypoints and descriptors for each reference image
    reference_data = []
    for image_path, reference_image in references:
        keypoints, descriptors = orb.detectAndCompute(reference_image, None)
        reference_data.append((image_path, keypoints, descriptors))

    # FLANN-based matcher for feature matching
    index_params = dict(algorithm=6,  # FLANN LSH algorithm
                         table_number=6,  # 12
                         key_size=12,     # 20
                         multi_probe_level=1)  # 2
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Function to show a message box
    def show_popup(message):
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        messagebox.showinfo("Notification", message)
        root.destroy()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from video source.")
            break

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Compute keypoints and descriptors for the current frame
        frame_keypoints, frame_descriptors = orb.detectAndCompute(gray_frame, None)

        if frame_descriptors is not None:
            for image_path, ref_keypoints, ref_descriptors in reference_data:
                good_matches = []
                if ref_descriptors is not None:
                    matches = flann.knnMatch(ref_descriptors, frame_descriptors, k=2)

                    # Apply Lowe's ratio test
                    for match in matches:
                        if len(match) == 2:  # Ensure there are two matches to unpack
                            m, n = match
                            if m.distance < 0.7 * n.distance:
                                good_matches.append(m)

                    # Calculate similarity
                    similarity = len(good_matches) / len(ref_keypoints) if len(ref_keypoints) > 0 else 0

                    # Display similarity score and name if above threshold
                    if similarity > similarity_threshold:
                        print(f"{image_path}: Similarity = {similarity:.2f}")
                        cv2.putText(frame, f"{image_path}: {similarity:.2f}", (10, 30 + 30 * reference_data.index((image_path, ref_keypoints, ref_descriptors))), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                        # Trigger the popup if specific images are detected
                        if image_path == "Rubbish_Sorting_System_Germany.jpg":
                            show_popup("Bin Colors & What They Mean:Yellow (Gelbe Tonne): Packaging waste like plastic, metal, and Tetra Paks.")


                        elif image_path == "Public_Laundry_Machines_France_Laundromats.jpg":
                            show_popup("Bring your own laundry detergent or purchase single-use packs from the vending machine in the laundromat.")

                        elif image_path == "Tokyo_Train_Ticket_Machine.jpg":
                            show_popup("Look for the large metro map above the ticket machine.")


        # Display the resulting frame
        cv2.imshow('Video Capture', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Replace the list below with paths to your reference images
compare_images(['Rubbish_Sorting_System_Germany.jpg', 'Public_Laundry_Machines_France_Laundromats.jpg', 'Tokyo_Train_Ticket_Machine.jpg'])