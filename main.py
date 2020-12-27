import sys
sys.path.append('pypng-lib\code')
import png


# RGB recovery
def read_png(filepath):
    '''
    extract data from pic
    :param filepath: pic
    :return: rows: lines
    :return: width: int
    :return: height: int
    :return: red_pixels: list
    '''
    dimensionPic = png.Reader(filename = filepath).asRGBA8()
    width = dimensionPic[0]
    height = dimensionPic[1]
    rows = list(dimensionPic[2])
    red_pixels = []
    rowsList = rows
    for i in rowsList:
        for red in range(0, len(i), 4):
            red_pixels.append(i[red])
    return rows, width, height, red_pixels



def pix_reduction (red):
    """
    convert red color level to odd to even
    :param red: list
    :return red: list

    """
    for i in range(len(red)):
        if (red[i] % 2 != 0):
            red[i] = red[i] - 1
    return red



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



def encode(redcolor, textbin):
    '''
    Insert text encoded to the red pixel
    :param redcolor: list
    :param textbin: list
    :return redcolor: list
    '''
    bi = ''
    for i in textbin:
        for k in i:
            bi = bi + k
    for j in range(0 , len(bi)):
        redcolor[j] = redcolor[j] + int(bi[j])
    return redcolor



def adapt_rows(rgba_rows):
    """
    adapt rgba as list of tuple
    :param rgb_rows: list
    :return rgb_pixels_list: list
    """

    rgba_pixels_list = []
    for row in rgba_rows:
        rgba_pixels = tuple(row)
        rgba_pixels_list.append(rgba_pixels)
    return rgba_pixels_list



def insert_red_pixels(w, h, red_list, rows):
    '''
    Insert the red pixel encoded to the red pixel of picture
    :param w: int
    :param h: int
    :param red_list:
    :param rows: list of tuple
    '''
    tupleIndice = 0 #ele de tuple
    elementTuple = 0 #ele de list
    i = 0
    while i < h:
        tmp = 0
        l = list(rows[tupleIndice])   #convert tuple to list in order to edit it
        for j in range(0, w):
            l[tmp] = red_list[elementTuple] # edit the red value
            tmp = tmp + 4 # index of red pixels
            elementTuple = elementTuple + 1 # next tuple
        i = i + 1
        rows[tupleIndice] = tuple(l) #insert the list as tuple
        tupleIndice = tupleIndice + 1
    w = png.Writer(w, h, greyscale = False, alpha = True)
    f = open(image_output, 'wb')
    w.write(f, adapt_rows(rows))
    f.close()



def decode(redP):
    '''
    Decode text from image
    (list) --> text
    :param redP: list
    :return Text: str
    '''

    i = 0
    NewList = []
    StringB = ''
    while i < len(redP):
        NewList.append(redP[i : i+8])
        i = i + 8
    values = []
    '''
    check end of text (first 8 pairs of values)
    insert 8 values that contain a possible non-pair
    '''

    for e in NewList:
        if (any(n % 2 == 1 for n in e)):
            values.append(e)
        else:
            break
    for x in values:
        StringB = StringB + ''.join(map(str, [item % 2 for item in x]))
    Text = ''.join(chr(int(StringB[i * 8:i * 8 + 8], 2)) for i in range(len(StringB) // 8))
    return Text



if __name__ == "__main__":

    # Image default image output and inputpath
    image_input = "imageTest.png"
    image_output = "imageTestNew.png"


    #
    rows, width, height, redPix = read_png(image_output)
    #print('--->',height,height)
    reduction_pixel = pix_reduction(redPix)
    print("red pixels adapted: ",reduction_pixel)


    # convert text to binary
    textBinary = convert_text_to_Bin('behind enemy lines')
    print("binary text: ", textBinary)


    # encode: add red_pixels to binary text
    textbin = []
    #print("mm", textBinary)
    redPixels_adjusted = encode(reduction_pixel, textBinary)
    print("new binary text: ",redPixels_adjusted)


    # adaption
    rows_adapted = adapt_rows(rows)
    print('format in tuples:', rows_adapted[0])


    # insert red_pixels encoded in rows and generat new image
    final_rows =  insert_red_pixels(width, height,redPixels_adjusted, rows_adapted)

    #
    rows, width, height, redPix = read_png(image_output)
    #print("red_pixels",redPix)
    print('>',decode(redPix))
