import struct

points = []

def unpack(f, sig, length):
    s = f.read(length)
    return struct.unpack(sig, s)

def read_triangle(f):
    #each normal vector/point is represented by their x, y, and z components
    #   -> 4 bits * 3 variables = 12 bits
    f.seek(f.tell() + 12) #skip over normal vector
    p1 = unpack(f, "<3f", 12)
    p2 = unpack(f, "<3f", 12)
    p3 = unpack(f, "<3f", 12)
    f.seek(f.tell() + 2)

    points.append(p1)
    points.append(p2)
    points.append(p3)

    return max(p1[0], p2[0], p3[0]), max(p1[1], p2[1], p3[1]), max(p1[2], p2[2], p3[2])


def read_length(f):
    length = struct.unpack("@i", f.read(4))
    return length[0]

def read_header(f):
    f.seek(f.tell()+80)

def parseTriangles(infilename):
        try:
            f = open(infilename, "rb")
            maxX = 0; maxY = 0; maxZ = 0; #used to specify STL file size
            read_header(f)
            l = read_length(f)
            try:
                for _ in range(l):
                    [tempX, tempY, tempZ] = read_triangle(f)
                    maxX = max(maxX, tempX)
                    maxY = max(maxY, tempY)
                    maxZ = max(maxZ, tempZ)
            except Exception as e:
                print("Exception", e)
            print("Finished parsing STL file")
            return points, [maxX, maxY, maxZ]
        except Exception as e:
            print(e)
