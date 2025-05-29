def mane_filtering():
    """
    0.mane_filtering과 동일한 기능을 하지만, output file이 parent directory에 생성된다. (1.main과 같은 directory에 위치해야 함)
    clinvar_pathogenic_missense_hgvs_docker.txt >> ../filtered_mane_select_clinvar.tsv
    """

    file_path = 'clinvar_pathogenic_missense_hgvs_docker.txt'
    output_path = '../filtered_mane_select_clinvar.tsv'

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