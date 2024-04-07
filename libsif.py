from PIL import Image
import lzma
from io import BytesIO
class SimplisticImageFormat:
    def __init__(self, filename:str, data:list[list[int]], mode:str, width:int, height:int) -> None:
        self.filename = filename
        self.data = data
        self.mode = mode
        self.width = width
        self.height = height

    def fromFileInMemory(binary:bytes):
        img = Image.open(BytesIO(binary))
        print("Converted, image in memory to PIL image.")
        return SimplisticImageFormat.fromImage(img)

    def fromImage(img:Image):
        data = list(img.getdata())
        print("Converted PIL image to pixel data.")
        return SimplisticImageFormat(img.filename, data, img.mode, img.width, img.height)

    # def fromPixelData(self, data:list[list]):
    #     pass


    def getData(self) -> list[list[int]]:
        return self.data

    def pixelDataToBinary(self, data:list[list[int]]) -> bytes:
        pixelData = b""
        print(self.mode)
        # try:
        #     for pixel in data:
        #         p = b""
        #         for layer in pixel:
        #             p += layer.to_bytes()
        #             print(layer)
        #         # p = bytes(bytearray(pixel))
        #         pixelData += p
        # except TypeError:
        #     return bytes(data)
        if type(data[0]) == int or type(data[0]) == bytes:
            pixelData = bytearray(data)
        else:
            pixelData = b"".join(map(bytearray, data))
        print("Pixel Data fetched.")
        return pixelData

    def save(self, filename:str, returnBinary = False) -> None:
        fileData = b""
        fileData += b"SIF2024"
        fileData += self.width.to_bytes(4)
        fileData += self.height.to_bytes(4)
        fileData += self.mode.encode()

        pixelData = self.pixelDataToBinary(self.data)
        pixelData = lzma.compress(pixelData)

        fileData += pixelData
        fileData += b"THEEND"

        if returnBinary:
            print("Returned Image in memory.")

            return fileData
        
        with open(filename, "wb") as f:
            f.write(fileData)
    

    def open(filename:str):
        fileData = b""
        header = b"SIF2024"
        trailer = b"THEEND"
        with open(filename, "rb") as f:
            fileData += f.read()
        
        if fileData[:len(header)] == header:
            print("File format : SIF2024")
        else:
            print(fileData[:20])
            raise ValueError("Image not of format .SIF")

        if fileData[-len(trailer):] != trailer:
            raise ValueError("Image has no trailer.")

        widthOffset = len(header)
        width = int.from_bytes(fileData[widthOffset:widthOffset + 4])
        height = int.from_bytes(fileData[widthOffset + 4:widthOffset + 8])

        modeOffset = widthOffset + 8
        modeBytes = fileData[modeOffset:modeOffset + 4]
        mode = ""
        if modeBytes == b"RGBA":
            mode = "RGBA"
        elif modeBytes[:-1] == b"RGB":
            mode = "RGB"
        elif modeBytes[0] == b"L":
            mode = "L"
        else:
            raise ValueError("Mode not identified : ", modeBytes)

        pixelLength = len(mode) # Number of values per pixel.

        dataOffset = modeOffset + pixelLength
        compressedData = fileData[dataOffset:-len(trailer)]
        pixelData = lzma.decompress(compressedData)

        pixels = []

        for i in range(0, len(pixelData), pixelLength):
            p = pixelData[i:i+pixelLength]
            pixels.append([])
            for byte in p:
                pixels[-1].append(byte)

        
        return SimplisticImageFormat(filename, pixels, mode, width, height)

    def __str__(self) -> str:
        return f"<{self.filename} : ({self.width}, {self.height}) : {self.mode}>"


if __name__ == "__main__":

    # testImage = Image.open("flag.png")
    # i = SimplisticImageFormat.fromImage(testImage)
    # i.save("flag.SIF")

    # file = SimplisticImageFormat.open("C:\\Users\\avani\\Downloads\\picture.SIF")
    # print(file.data, len(file.data), type(file.data[0]))
    # pix = []
    # for i in range(0, len(file.data), file.width):
    #     pix.append(file.data[i:i+file.width])
    
    
    # import numpy as np
    # image = Image.fromarray(np.array(pix, dtype=np.uint8), mode=file.mode)
    # # print((np.array(testImage.getdata()) == np.array(file.data)).all(), np.array(testImage.getdata()).shape, np.array(file.data).shape)
    # # print(np.array(pix).shape)
    # image.show()
    pass