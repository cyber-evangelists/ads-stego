    import cv2
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Random import get_random_bytes

    def encrypt(text, key):
        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(text.encode(), AES.block_size))
        return ciphertext, cipher.iv

    def decrypt(ciphertext, key, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted_text = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted_text.decode()


    def hide_encrypted_text_in_video(video_path, secret_text, key, output_path):
        cap = cv2.VideoCapture(video_path)

        # Get the frame count of the video
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Encrypt the text
        key = get_random_bytes(32)  # 256-bit key for AES-256
        encrypted_text, iv = encrypt(secret_text, key)

        # Convert the encrypted text to binary
        binary_text = ''.join(format(byte, '08b') for byte in encrypted_text)

        # Calculate the maximum number of characters that can be hidden in the video
        max_chars = (frame_count * 3) // 8

        if len(binary_text) > max_chars:
            print(f"Error: The text is too long to be hidden in the video. Maximum allowed characters: {max_chars}")
            return

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

        # Embed the binary text in each frame using LSB
        text_index = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Iterate through each pixel of the frame
            for y in range(frame.shape[0]):
                for x in range(frame.shape[1]):
                    for color_channel in range(3):  # Iterate over RGB channels
                        if text_index < len(binary_text):
                            frame[y, x, color_channel] = frame[y, x, color_channel] & ~1 | int(binary_text[text_index])
                            text_index += 1
                        else:
                            break

            out.write(frame)

        cap.release()
        out.release()
        print("Encrypted text hidden in the video successfully.")
        return iv
        

    def extract_encrypted_text_from_video(steg_video_path, key, iv):
        cap = cv2.VideoCapture(steg_video_path)

        binary_text = ""
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Extract the least significant bits from each pixel of the frame
            for y in range(frame.shape[0]):
                for x in range(frame.shape[1]):
                    for color_channel in range(3):  # Iterate over RGB channels
                        binary_text += str(frame[y, x, color_channel] & 1)

        # Convert binary text back to bytes
        ciphertext = bytes(int(binary_text[i:i + 8], 2) for i in range(0, len(binary_text), 8))

        # Decrypt the text
        decrypted_text = decrypt(ciphertext, key, iv)
        return decrypted_text


    # Example usage
    video_path = "main video.mp4"
    secret_text = "This is a secret message!"
    output_video_path = "output_steg_video_encrypted.mp4"

    key = get_random_bytes(32)  # 256-bit key for AES-256

    iv = hide_encrypted_text_in_video(video_path, secret_text, key, output_video_path)

    extracted_text = extract_encrypted_text_from_video(output_video_path, key, iv)
    print("Extracted Text:", extracted_text)