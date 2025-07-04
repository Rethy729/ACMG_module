def pp3_bp4(header, variant_data, variant_evidence):
    """
    :param header: annotate vep txt file의 열 정보가 순서대로 나열된 list
    :param variant_data: 한 variant의 정보가 순서대로 나열된 list
    :param variant_evidence: main의 variant_evidence list

    SIFT와 PolyPhen in silico tool을 사용
    sift는 tolerated / tolerated_low_confidence / deleterious_low_confidence / deleterious 중 하나
    polyphen은 unknown / benign / possibly_damaging / probably_damaging 중 하나
    sift -> tolerated & polyphen -> benign 인 경우 BP4 이므로 대응 하는 variant_evidence[8] = True
    sift -> deleterious & polyphen -> probably_damaging 인 경우 PP3 이므로 대응 하는 variant_evidence[5] = True
    """

    sift_index = header.index('SIFT')
    polyphen_index = header.index('PolyPhen')

    sift_value = variant_data[sift_index]
    polyphen_value = variant_data[polyphen_index]
    if sift_value != '-' and polyphen_value != '-':
        if 'tolerated' in sift_value and 'benign' in polyphen_value:
            variant_evidence[8] = True
        elif 'deleterious' in sift_value and 'probably_damaging' in polyphen_value:
            variant_evidence[5] = True
