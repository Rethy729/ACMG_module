def data_check(header):
    """
    :param header: 1_main.py 에서 파싱한 'filtered_mane_select.tsv' 의 헤더 정보를 split('\t') 한 list
    :return: 앞으로의 ACMG evidence 판별에 필요한 data가 하나라도 없으면 return False + 어떤 data가 빠져있는지 알려주는 메세지 출력 / 모두 충족하면 return True
    """

    missing_option = [option for option in ['Uploaded_variation', 'Allele', 'Location', 'Consequence', 'gnomADg_AF', 'SIFT', 'PolyPhen','HGVSc', 'HGVSp', 'ClinVar_CLNSIG', 'ClinVar_CLNREVSTAT'] if option not in header]
    if missing_option:
        print(f"Please annotate {', '.join(missing_option).lower()}")
        return False
    else:
        return True