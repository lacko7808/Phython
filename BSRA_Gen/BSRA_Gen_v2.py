def read_input_file(input_file):
    data = []
    with open(input_file, 'r') as f:
        for line in f:
            fields = line.strip().split(';')
            data.append(fields)
            # print(fields)
    return data


def generate_output(data):
    debug_kz = False
    output = []
    current_blz = None
    current_ksg = None
    kst_range_start = None
    kst_range_end = None
    kst_range_extra_start = None
    kst_range_extra_end = None

    kst_range_contains_90 = False
    kst_group_change = False
    ksg_group_change = False
    blz_group_change = False
    kst_index = 0
    kst_diff = 0
    row_index = 0
    input_line_number = len(data) - 1

    for row in data:

        blz, kst, ksg = row

        if int(blz) == 35019 and int(kst) == 251:
            print('stop')

        # a következő sorhoz tartozó változókat (*_next) az utolsó sornál már nem kell feltölteni

        if input_line_number != row_index:
            temp_row_index=row_index + 1
            blz_next, kst_next, ksg_next = data[temp_row_index]
            if int(kst_next) >= int(kst):
                kst_diff = int(kst_next) - int(kst)
            else:
                kst_diff = 0
        else:
            blz_next = 999
            kst_next = 999
            ksg_next = 999
            kst_diff = -1

        # az előző sorhoz tartozó változókat (*_prev) az első sornál nem kell feltölteni

        if row_index != 0:
            temp_row_index=row_index - 1
            blz_prev, kst_prev, ksg_prev = data[temp_row_index]
        else:
            kst_range_start = int(kst)
            blz_prev = -1
            kst_prev = -1
            ksg_prev = -1

        # ha az első sor vagy blz váltásnál nem 0-tól kezdődik a KST, akkor 000 és az első KST-1-ig a 90-es KSG-hez kell rendelni a KST-ket.
        # Pl.: ha az első KST az inputban 015, akkor 000-014 90-es sort kell generálni.
        if row_index == 0 and int(kst) != 0:
            output.append(format_output(blz, 90, 0, int(kst) - 1, False))

        if blz_group_change and int(kst_prev) != 0:
            output.append(format_output(blz, 90, 0, int(kst) - 1, False))

        # ha az utolsó sor blz váltásnál vagy a fájl végén nem 999-re végződik, akkor az utolsó beolvasott KST+1-től a 999-es KST-ig a 90-es KSG-hez kell rendelni a KST-ket.
        # Pl.: ha az utolsó KST az inputban 650, akkor 651-999 90-es sort kell generálni.
        if row_index == input_line_number and int(kst) != 999:
            output.append(format_output(blz, 90, int(kst) + 1, 999, False))

        if blz_group_change and int(kst_prev) != 999:
            output.append(format_output(blz_prev, 90, int(kst_prev) + 1, 999, False))

        # KST csoport elejének és végének meghatározása
        # Ha a következő sorban lévő KSG és aktuális sorban lévő KSG megegyezik, akkor csoportot kell építeni
        # Egyébként csak egyszerűen kiírjuk a sort

        if blz != blz_next:
           if int(kst) != 999:
               if int(kst) > int(kst_next) or kst_next == 999:
                   kst_range_start = int(kst)
               else:
                   kst_range_start = 0
           else:
               kst_range_start = 999
        else:
            if int(ksg) != int(ksg_next) or int(ksg)==90 or int(kst) < int(kst_prev):
                kst_range_start = int(kst)
                #if int(kst) > int(kst_prev):
                #    kst_range_start = int(kst)
                #else:
                #    kst_range_start = int(kst_prev)

        if int(kst_diff)==0:
            if int(kst) != 999:
                if int(kst) > int(kst_next) or kst_next==999:
                    kst_range_start = int(kst)
                else:
                    kst_range_start = 0
                #kst_range_start = 0
            else:
                kst_range_start = 999
            kst_range_end = int(kst_next)-1
        #else:
        #    kst_range_end = int(kst)

        # konkrét sor kiírása, amit éppen most olvastunk be
        #if ksg_group_change or int(ksg)==90 or kst_diff > 1:
        if int(blz) != int(blz_next) or int(ksg) != int(ksg_next) or int(ksg) == 90 or kst_diff > 1:
            kst_range_end = int(kst)
            output.append(format_output(blz, int(ksg), kst_range_start, kst_range_end, kst_range_contains_90))

        if kst_diff > 1:
            output.append(format_output(blz, 90, int(kst)+1, int(kst_next)-1, kst_range_contains_90))
            kst_range_start = int(kst_next)

        #blz, kst illetve ksg váltást eltároljuk és a következő sort ennek fényében kezeljük
        if blz != blz_next:
            blz_group_change = True
        else:
            blz_group_change = False

        if kst != kst_next:
            kst_group_change = True
        else:
            kst_group_change = False

        if ksg != ksg_next:
            ksg_group_change = True
        else:
            ksg_group_change = False

        row_index = row_index + 1

    output.sort()

    return output


def format_output(blz, ksg, kst_range_start, kst_range_end, kst_range_contains_90):
    if kst_range_start == kst_range_end:
        kst_range_str = f"{kst_range_start:03d}    "
    else:
        kst_range_str = f"{kst_range_start:03d}-{kst_range_end:03d}"

    # if ksg == 90:
    if kst_range_contains_90:
        return f"01 {blz}  {ksg} 90"
    else:
        if ksg != 90:
            return f"01 {blz} {kst_range_str}  {ksg}  {kst_range_start:03d}"
        if ksg == 90:
            return f"01 {blz} {kst_range_str}  {ksg}"

def add_lines(output):
    output_with_lines = []
    for i, row in enumerate(output):
        output_with_lines.append(row)
        if i < len(output) - 1 and int(row[3:8]) != int(output[i + 1][3:8]):
            output_with_lines.append('*------------------------')
    return output_with_lines

def write_output_file(output_file, output):
    with open(output_file, 'w') as f:
        for line in output:
            f.write(line + '\n')


def main():
    input_file = 'input.txt'  # A bemeneti fájl neve
    output_file = 'output.txt'  # A kimeneti fájl neve

    # print(input_file)

    ''' így tudjuk kilistázni, hogy mik vannak a könyvtárban!
    import os

    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory
    print("Files in %r: %s" % (cwd, files))
    '''

    data = read_input_file(input_file)
    output = generate_output(data)
    output_with_lines = add_lines(output)
    write_output_file(output_file, output_with_lines)


if __name__ == "__main__":
    main()
