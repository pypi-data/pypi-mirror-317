def stability(dx, start, end):
    val = 0
    for i in range(end-start+1):
        val += dx(start + i)
    return val/(end-start+1)