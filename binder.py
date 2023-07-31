hidden_file_name = 'meta-data'

def bind_data_to_file(file_path, data):
    full_path = file_path + ':' + hidden_file_name
    with open(full_path, 'wb') as file:
        file.write(data)
    return "File binded"

def unbind_data_from_file(file_path):
    full_path = file_path + ':' + hidden_file_name
    with open(full_path, 'rb') as file:
        data = file.read()
    return data

if __name__ == "__main__":
    file = "D:/Languages/Python/Stegno-pro/adver.mp4"
    response = unbind_data_from_file(file)
    print(response)
