
def clip16( x ):    
    # Clipping for 16 bits

    for i in range (0,len(x)):
        if x[i] > 32767:
            x[i] = 32767
        elif x[i] < -32768:
            x[i] = -32768
        else:
            x[i] = int(x[i])
           
    return x

