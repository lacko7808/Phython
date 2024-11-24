def read_input_file(input_file):
    data = []
    with open(input_file, 'r') as f:
        for line in f:
            fields = line.strip().split(';')
            data.append(fields)
            #print(fields)
    return data

def generate_output(data):
    debug_kz = True
    output = []
    current_blz = None
    current_ksg = None
    kst_range_start = None
    kst_range_end = None
    kst_range_extra_start = None
    kst_range_extra_end = None

    kst_range_contains_90 = False
    kst_group_change = False
    kst_index = 0
    kst_diff = 0
    akt=0
    nex=1
    input_line_number = len(data)

    for row in data:
        if debug_kz: print("--- NEW LINE ----")
        #print(row)
        #print(data[i][1])
        #print(data[i+1])
        blz, kst, ksg = row
        #print(input_line_number)
        #print(nex)

        if input_line_number != nex:
            blz_next, kst_next, ksg_next = data[nex]
            if int(kst_next) >= int(kst) or kst_range_start is None: kst_diff = int(kst_next)-int(kst)
            else:
                kst_diff = 0
        else:
            blz_next = 999
            kst_next = 999
            ksg_next = 999
            kst_diff = 0

        if debug_kz:
            print("BLZ:", blz, blz_next)
            print("KST:", kst, kst_next)
            print("KSG:", ksg, ksg_next)
            print("KST_Diff: ", kst_diff)

        if kst_range_start is None: kst_range_start = 000
        if current_ksg is None: current_ksg = int(ksg)
        
        if ksg != ksg_next:
            kst_group_change = True
            kst_range_end = int(kst)
            current_ksg = int(ksg)
        else:
            if kst_range_start != 0: kst_group_change = False
            else:
                kst_group_change = True
                current_ksg = int(ksg)

        if blz != blz_next or kst_group_change:
            current_blz = blz
            if kst_diff == 0:
                output.append(format_output(current_blz, ksg_next, 0, int(kst_next)-1, kst_range_contains_90))
            if debug_kz:
                print("Range: ", kst_range_start, kst_range_end, kst_range_contains_90)
                print("csoportváltás", kst_range_start, kst_range_end, current_ksg)
            output.append(format_output(current_blz, current_ksg, kst_range_start, kst_range_end, kst_range_contains_90))
            if kst_diff != 1 and (blz == blz_next or blz_next == 999):
                kst_range_extra_start = int(kst_range_end)+1
                kst_range_extra_end = int(kst_next)-1
                if debug_kz:
                    print("Extra sor kiírása", current_blz, 90, kst_range_extra_start, kst_range_extra_end, kst_range_contains_90)
                output.append(format_output(current_blz, 90, kst_range_extra_start, kst_range_extra_end, kst_range_contains_90))
            if kst_diff != 1 and kst_diff != 0 and blz != blz_next and kst != 999 and blz_next != 999:
                kst_range_extra_start = int(kst_range_end)+1
                kst_range_extra_end = 999
                if debug_kz:
                    print("Extra sor a végéig", current_blz, 90, kst_range_extra_start, kst_range_extra_end, kst_range_contains_90)
                output.append(format_output(current_blz, 90, kst_range_extra_start, kst_range_extra_end, kst_range_contains_90))
        else:
            if debug_kz:
                print("azonos csoport")               

        kst_range_contains_90 = (int(ksg) == 90)

        if blz != blz_next:
           kst_range_start = 000  
        else:
            if kst_group_change:
                kst_range_start = int(kst_next)


        if int(kst_next) < int(kst):
            kst_range_start = 0
            kst_range_end = int(kst_next)-1
        else:
            kst_range_end = int(kst)

        if debug_kz:
            print("Range: ", kst_range_start, kst_range_end, kst_range_contains_90)  
    
        akt=akt+1
        nex=nex+1

    if current_blz is not None:
        output.append(format_output(current_blz, current_ksg, kst_range_start, kst_range_end, kst_range_contains_90))

    return output

def format_output(blz, ksg, kst_range_start, kst_range_end, kst_range_contains_90):
    if kst_range_start == kst_range_end:
        kst_range_str = f"{kst_range_start:03d}    "
    else:
        kst_range_str = f"{kst_range_start:03d}-{kst_range_end:03d}"

    #if ksg == 90:
    if kst_range_contains_90:
        return f"01 {blz}  {ksg} 90"
    else:
        if ksg != 90:
            return f"01 {blz} {kst_range_str}  {ksg}  {kst_range_start:03d}"
        if ksg == 90:
            return f"01 {blz} {kst_range_str}  {ksg}"
def write_output_file(output_file, output):
    with open(output_file, 'w') as f:
        for line in output:
            f.write(line + '\n')

def main():
    input_file = 'input.txt'  # A bemeneti fájl neve
    output_file = 'output.txt'  # A kimeneti fájl neve

    #print(input_file)

    ''' így tudjuk kilistázni, hogy mik vannak a könyvtárban!
    import os

    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory
    print("Files in %r: %s" % (cwd, files))
    '''

    data = read_input_file(input_file)
    output = generate_output(data)
    write_output_file(output_file, output)

if __name__ == "__main__":
    main()
