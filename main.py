# https://www.mathweb.fr/euclide/2020/06/13/steganographie-python/?fbclid=IwAR1ERFRz7IONVvriju5UvWyfGq9pFfo7qCA927XLXU3BURV59E9EyIOQ-rw
import sys
sys.path.append('pypng-lib/code')
import png
import argparse

# RGB recovery
def read_png(filepath):
    '''
    extract data from pic
    :param filepath: pic
    :return: rows: lines
    :return: width: int
    :return: height: int
    :return: pixels: list
    '''
    dimensionPic = png.Reader(filename = filepath).asRGBA8()
    width = dimensionPic[0]
    height = dimensionPic[1]
    rows = list(dimensionPic[2])
    pixels = []
    rowsList = rows
    for i in rowsList:
        for j in range(0, len(i)):
            pixels.append(i[j])
    return rows, width, height, pixels



def pix_reduction (pixlist):
    """
    convert the color level of odd pixels to even
    :param pixlist: list
    :return pixlist: list

    """
    for i in range(len(pixlist)):
        if (pixlist[i] % 2 != 0):
            pixlist[i] = pixlist[i] - 1
    return pixlist



def convert_text_to_Bin(text):
    '''
    convert text to binary
    :param text:str
    :return byte_list: list
    '''

    a_byte_array = bytearray(text, "utf8")
    byte_list = []
    for byte in a_byte_array:
        binary_representation = bin(byte)
        byte_list.append(binary_representation.replace("b", "").rjust(8,'0'))
    return byte_list



def encode(rgbaEncoded, textbin):
    '''
    Encode by adding binary text to the least significant bits
    :param rgbaEncoded: list
    :param textbin: list
    :return rgbaEncoded: list
    '''
    binary = ''
    for i in textbin:
        for k in i:
            binary = binary + k
    for j in range(0 , len(binary)):
        rgbaEncoded[j] = rgbaEncoded[j] + int(binary[j])
    return rgbaEncoded


def insert_pixels(w, h, rgba, pic):
    '''
    Insert the pixel encoded to the pixel of picture
    :param w: int
    :param h: int
    :param rgba: list
    :param pic:
    '''
    #adapt rgba as list of tuple
    list_t = []
    tmp = []
    for i in range(0, len(rgba)):
        tmp.append(rgba[i])
        if (len(tmp) == w * 4 and i != 0):
            list_t.append(tuple(tmp))
            tmp.clear()

    w = png.Writer(w, h, greyscale = False, alpha = True)
    f = open(pic, 'wb')
    w.write(f, list_t)
    f.close()



def decode(pixels):
    '''
    Decode text from image
    (list) --> text
    :param pixels: list
    :return Text: str
    '''

    i = 0
    List = []
    StringB = ''
    while i < len(pixels):
        List.append(pixels[i : i+8])
        i = i + 8
    values = []
    '''
    check end of text (first 8 pairs of values)
    insert 8 values that contain a possible non-pair
    '''

    for e in List:
        if (any(n % 2 == 1 for n in e)):
            values.append(e)
        else:
            break
    for x in values:
        StringB = StringB + ''.join(map(str, [item % 2 for item in x]))
    Text = ''.join(chr(int(StringB[i * 8:i * 8 + 8], 2)) for i in range(len(StringB) // 8))
    return Text



if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", '--write', action='store_true')
    parser.add_argument("-f", '--image')
    parser.add_argument("-t", '--text')
    parser.add_argument('output')
    args = parser.parse_args()

    if args.write:
        if args.image and args.text:
            image = args.image
            text = args.text
        else:
            image = input("Set PNG path: ")
            text = input("Enter your text: ")

        # extract PNG params
        rows ,width, height, RGBA = read_png(image)

        # Convert text to binary
        binaryText = convert_text_to_Bin(text)

        # Encode
        RGBAreduced = pix_reduction(RGBA)

        pixelEncoded = encode(RGBAreduced, binaryText)

        # Insert new params to PNG file
        insert_pixels(width, height, pixelEncoded, args.output)

    if not args.write:
        # encode image
        width1, height1, rows1, RGBA1 = read_png(args.output)
        decodeP = decode(RGBA1)
        print("Text decoded from the picture:",decodeP)
