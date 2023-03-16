import numpy as np

def read_wonky_file(file_name=""):
    if file_name == "":
        file_name = "20_3.npy"
    with open(file_name, 'rb') as f:
        ret = np.load(f)
    return ret

def write_wonky_file(file_name="", a = []):
    if file_name == "":
        try: 
            with open("compressed_vid.npy", "wb") as f:
                pass
            file_name = "compressed_vid.npy"
        except:
            file_name = "compressed_vid.npy"
    with open(file_name, "wb") as f:
        np.save(f, a)
    return file_name
    

if __name__ == "__main__":
    array = read_wonky_file()
    print(array)