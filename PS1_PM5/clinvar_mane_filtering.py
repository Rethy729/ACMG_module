def mane_filtering():
    """
    'clinvar_pathogenic_missense_hgvs_docker.txt' >> '../filtered_mane_select_clinvar.tsv'

    0_mane_filtering과 동일한 기능을 하지만, output file이 parent directory에 생성된다. (1.main과 같은 directory에 위치해야 함)
    또한 clinvar_pathogenic_missense_hgvs_docker.txt에 포함된 variant의 경우, 모두가 amino acid 변화를 동반하는 missense variant이기 때문에
    mane select가 하나도 선택 되지 않은 variant는 존재하지 않을 것이다 (직접 확인을 해보지는 않았지만)
    따라서 mane select가 하나도 선택 되지 않는 경우는 배제하고, mane_select 된 data만을 filtering하여 ../filtered_mane_select_clinvar.tsv에 저장한다.
    """

    file_path = 'clinvar_pathogenic_missense_hgvs_docker.txt'
    output_path = '../filtered_mane_select_clinvar.tsv'

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