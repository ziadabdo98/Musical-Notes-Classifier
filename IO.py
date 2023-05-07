import os
from skimage import io


class IO:
    file_data = ""
    output_folder = ""
    file_name = ""

    def read_images(self, input_folder):
        files = os.listdir(input_folder)

        images = []
        for fle in files:
            images.append(io.imread(input_folder + "/" + fle))

        return images, files

    def read_image(self, path):
        return io.imread(path)

    def write(self, data):
        self.file_data += data

    def set_name(self, name):
        self.file_name = os.path.splitext(name)[0]
        self.file_name += ".txt"

    def save(self):
        os.makedirs(self.output_folder, exist_ok=True)
        f = open(self.output_folder + "/" + self.file_name, "x+")
        f.write(self.file_data)
        f.close()
        self.file_data = ""
