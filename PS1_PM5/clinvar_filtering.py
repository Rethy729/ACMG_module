def clinvar_filtering():
    """
    'clinvar.vcf' >> 'clinvar_pathogenic_missense.vcf'

    Clinvar database에서 다운받은 vcf 파일에서, pathogenic하면서 동시에 missense variant인 variant만을 모아 새로운 clinvar_pathogenic_missence.vcf를 만든다.
    이 새로운 vcf파일은 추후 Amazon-EC2 서버로 옮겨져, hgvs과 mane 옵션을 annotation하여 다시 가져오게 된다.
    """

    vcf_file_path = 'clinvar.vcf'
    output_file_path = 'clinvar_pathogenic_missense.vcf'
    with open(vcf_file_path, encoding='utf-8') as f_in, open(output_file_path, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            if line.startswith('#'):
                f_out.write(line)  # 헤더는 그대로 출력
            else:
                clinvar_data = line.strip().split('\t')
                clinvar_info = clinvar_data[7]  # INFO 필드
                clinvar_info_lst = clinvar_info.strip().split(';')
                pathogenic_bool = False
                missense_bool = False
                for data in clinvar_info_lst:
                    if data.startswith('CLNSIG=') and 'Pathogenic' in data:
                        pathogenic_bool = True
                    if 'missense_variant' in data:
                        missense_bool = True
                if pathogenic_bool and missense_bool:
                    f_out.write(line)  # 두 조건 모두 만족하면 출력
    print("Complete")

clinvar_filtering()