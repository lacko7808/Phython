def process_input(input_lines):
    result = []
    current_blz = None
    current_ksg = None
    current_kst_start = None
    current_kst_end = None

    for line in input_lines:
        blz, kst, ksg = map(int, line.strip().split(';'))

        if current_blz is None or current_blz != blz:
            if current_blz is not None:
                result.append("*------------------------")
            result.append(f"01 {blz:05d} 000-994   90  000")

        if ksg == 90:
            result.append(f"01 {blz:05d} {kst:03d}           90  000")
        else:
            if current_ksg is None:
                current_ksg = ksg
                current_kst_start = kst
                current_kst_end = kst
            elif current_ksg == ksg and kst == current_kst_end + 1:
                current_kst_end = kst
            else:
                if current_kst_start == current_kst_end:
                    result.append(f"01 {blz:05d} {current_kst_start:03d}           {current_ksg:02d}  {current_kst_start:03d}")
                else:
                    result.append(f"01 {blz:05d} {current_kst_start:03d}-{current_kst_end:03d}   {current_ksg:02d}  {current_kst_start:03d}")
                current_ksg = ksg
                current_kst_start = kst
                current_kst_end = kst

        current_blz = blz

    if current_blz is not None:
        if current_kst_start == current_kst_end:
            result.append(f"01 {current_blz:05d} {current_kst_start:03d}           {current_ksg:02d}  {current_kst_start:03d}")
        else:
            result.append(f"01 {current_blz:05d} {current_kst_start:03d}-{current_kst_end:03d}   {current_ksg:02d}  {current_kst_start:03d}")

    return result


def main():
    input_file_path = "input.txt"
    output_file_path = "output.txt"

    with open(input_file_path, 'r') as input_file:
        input_lines = input_file.readlines()

    output_lines = process_input(input_lines)

    with open(output_file_path, 'w') as output_file:
        output_file.write('\n'.join(output_lines))

if __name__ == "__main__":
    main()
