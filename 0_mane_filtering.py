def mane_filtering():
    """
    'HG002_annotated_docker.txt' >> 'filtered_mane_select.tsv'

    raw data 에서 mane_select 된 variant data 만 filtering 하여 'filtered_mane_select.tsv' 로 저장 한다.

    HG002_annotated_docker.txt annotated file을 한 줄씩 읽어, '#Uploaded_variation'으로 시작 하는 data는 header로 저장, output에 write 한다.
    이때 raw data는 MANE_SELECT 열을 가지고 있어야 하며, 가지고 있지 않으면 process가 중단 되며, mane_index는 mane_select가 몇번째 열에 존재 하는지 저장 한다.
    만약 mane_select 된 variant 가 없는 경우에는, 임의로 한 data line을 골라 저장한다. (여기서는 마지막 줄)
    alt 가 두개인 경우 (GT가 1/2) 임의로 각각 하나씩의 data line을 골라 저장한다.
    """

    file_path = 'HG002_annotated_docker_v2.txt'
    output_path = 'filtered_mane_select.tsv'

    with open(file_path, encoding='utf-8') as f_in, open(output_path, 'w', encoding='utf-8') as f_out:

        prev_variation = None
        last_line = None
        last_second_line = None
        mane_bool = False

        for line in f_in:
            if line.startswith('#Uploaded_variation'): #line 이 header 일 때
                header = line.lstrip('#')
                f_out.write(header)
                header_split = header.strip().split('\t')
                if 'MANE_SELECT' not in header_split:
                    print ("Please annotate MANE")
                    return
                mane_index = header_split.index('MANE_SELECT')
                continue

            if line.startswith('#'):
                continue

            variant_data = line.strip().split('\t')
            current_variation = variant_data[0]

            if current_variation != prev_variation:
                if not mane_bool and last_line:
                    alt_count = len(last_line.strip().split('\t')[0].split('/')) # alt의 개수, alt_count가 3이면 GT가 1/2인 경우이다.
                    if alt_count == 3 and last_second_line:
                        f_out.write(last_second_line + '\n')
                        f_out.write(last_line + '\n')
                    else:
                        f_out.write(last_line + '\n')
                elif mane_bool:
                    mane_bool = False

            if variant_data[mane_index] != '-':
                f_out.write(line)
                mane_bool = True

            prev_variation = current_variation
            last_second_line = last_line
            last_line = line.strip()

        if not mane_bool and last_line:
            f_out.write(last_line + '\n')

    print("Complete")

mane_filtering()