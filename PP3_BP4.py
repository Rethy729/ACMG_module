def pp3_bp4(header, variant_data, variant_evidence):
    """
    :param header: annotate vep txt file의 열 정보가 순서대로 나열된 list
    :param variant_data: 한 variant의 정보가 순서대로 나열된 list
    :param variant_evidence: main의 variant_evidence list

    해당 evidence 판별에 필요한 SIFT, PolyPhen data가 없는 경우 아무것도 하지 않고 return

    SIFT와 PolyPhen in silico tool을 사용
    sift는 tolerated / tolerated_low_confidence / deleterious_low_confidence / deleterious 중 하나
    polyphen은 unknown / benign / possibly_damaging / probably_damaging 중 하나
    sift -> tolerated & polyphen -> benign 인 경우 BP4 이므로 대응 하는 variant_evidence[8] = True
    sift -> deleterious & polyphen -> probably_damaging 인 경우 PP3 이므로 대응 하는 variant_evidence[5] = True

    추후 고려 사항: sift와 polyphen의 점수에 따른 임의 판별 기준
    """

    missing_option = [option for option in ['SIFT', 'PolyPhen'] if option not in header]
    if missing_option:
        print(f"Please annotate {', '.join(missing_option).lower()}")
        return
    sift_index = header.index('SIFT') # 22
    polyphen_index = header.index('PolyPhen') # 23

    sift_value = variant_data[sift_index]
    polyphen_value = variant_data[polyphen_index]
    if sift_value != '-' and polyphen_value != '-':
        if 'tolerated' in sift_value and 'benign' in polyphen_value:
            variant_evidence[8] = True
        elif 'deleterious' in sift_value and 'probably_damaging' in polyphen_value:
            variant_evidence[5] = True
