def mane_filtering():
    """
    'HG002_annotated_docker.txt' >> 'filtered_mane_select.tsv'

    raw data 에서 mane_select 된 variant data 만 filtering 하여 'filtered_mane_select.tsv' 로 저장 한다.
    이때 raw data는 MANE_SELECT 열을 가지고 있어야 하며, 가지고 있지 않으면 process가 중단 된다.

    HG002_annotated_docker.txt annotated file을 한 줄씩 읽어, '#Uploaded_variation'으로 시작 하는 data는 header로 저장, output에 write 한다.
    이때 mane_index는 mane_select가 몇번째 열에 존재 하는지 저장 한다.
    '#'으로 시작하지 않는 data line은 variant data 로 저장, 이때 variant_data[mane_index] 가 '-'이 아닌 variant data 만 선별 하여 output에 write 한다.
    """

    file_path = 'HG002_annotated_docker_v2.txt'
    output_path = 'filtered_mane_select.tsv'

    with open(file_path, encoding='utf-8') as f_in, open(output_path, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            if line.startswith('#Uploaded_variation'): #line 이 header 일 때
                header = line.lstrip('#')
                f_out.write(header)
                header_split = header.strip().split('\t')
                if 'MANE_SELECT' not in header_split: #test 필요
                    print ("Please annotate MANE")
                    return
                mane_index = header_split.index('MANE_SELECT')
                continue

            if not line.startswith('#'):
                variant_data = line.strip().split('\t')
                if variant_data[mane_index] != '-':
                    f_out.write(line)
    print("Complete")

mane_filtering()