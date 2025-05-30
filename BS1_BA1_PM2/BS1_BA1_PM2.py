def ba1_bs1_pm2(header, variant_data, variant_evidence):
    """
    :param header: annotate vep txt file의 열 정보가 순서대로 나열된 list
    :param variant_data: 한 variant의 정보가 순서대로 나열된 list
    :param variant_evidence: main의 variant_evidence list

    해당 evidence 판별에 필요한 gnomADe_AF data가 없는 경우 아무것도 하지 않고 return

    gnomADe_AF의 값을 ratio로 저장
    ratio >= 0.05 -> BA1 이므로 대응 하는 variant_evidence[11] = True
    0.01 <= ratio < 0.05 -> BS1 이므로 대응 하는 variant_evidence[10] = True
    ratio == 0 -> PM2 이므로 대응 하는 variant_evidence[2] = True

    추후 고려 사항: 0.01 << 이 숫자의 타당성
    """

    if 'gnomADe_AF' not in header:
        print("Please annotate gnomADe_AF")
        return
    gnomade_af_index = header.index('gnomADe_AF') # 28

    if variant_data[gnomade_af_index] != '-':
        ratio = float(variant_data[gnomade_af_index])
        if ratio >= 0.05:
            variant_evidence[11] = True
        elif 0.01 <= ratio < 0.05:
            variant_evidence[10] = True
        elif ratio == 0 :
            variant_evidence[2] = True
