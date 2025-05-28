def mane_filtering():
    """
    raw data 에서 mane_select 된 variant data 만 filtering 하여 'filtered_mane_select.tsv' 로 저장 한다.
    이때 raw data는 MANE_SELECT 열을 가지고 있어야 하며, 가지고 있지 않으면 process가 중단 된다.

    HG002_annotated_docker.txt annotated file을 한 줄씩 읽어, 열 정보를 담고 있는 ('#Uploaded_variation'으로 시작 하는 행)은 header로 저장, output에 write 한다.
    이때 mane_index는 mane_select가 몇번째 열에 존재 하는지 저장 한다.
    header 행을 찾은 순간 found_header boolean은 True가 되어 실제 데이터 행을 split (variant_data) 하여 읽는다.
    이때 variant_data[mane_index] 가 '-'이 아닌 variant data 만 선별 하여 output에 저장 한다.
    """

    file_path = 'HG002_annotated_docker.txt'
    output_path = 'filtered_mane_select.tsv'

    with open(file_path, encoding='utf-8') as f_in, open(output_path, 'w', encoding='utf-8') as f_out:
        found_header = False
        for line in f_in:
            if not found_header and line.startswith('#Uploaded_variation'): # header를 아직 찾지 못했고, line 이 header 일 때
                header = line.lstrip('#')
                f_out.write(header)
                header_split = header.strip().split('\t')
                print (header_split)
                if 'MANE_SELECT' not in header_split: #test 필요
                    print ("Please annotate MANE")
                    return
                mane_index = header_split.index('MANE_SELECT')
                found_header = True
                continue
            if found_header:
                variant_data = line.strip().split('\t')
                if variant_data[mane_index] != '-':
                    f_out.write(line)
    print("Complete")

mane_filtering()