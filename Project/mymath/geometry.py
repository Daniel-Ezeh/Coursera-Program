'''
this module calculates the area of basic shapes
'''

def area_of_rectangle(length,breadth):
    '''calculating the area of a rectangle
    '''
    try:
        area = length * breadth
    except TypeError as e:
        print('you did not provide the right amount of arguments!', e)
        return None
    else:
        return area 





def area_of_circle(radius):
    '''
    calculating the area of a circle
    '''
    pi = 3.1415
    try:
        area = pi * radius
    except TypeError as e:
        print("excepted only the radius")
        return None
    else:
        return area



print(area_of_circle(5,6))