def ba1_bs1_pm2(header, variant_data, variant_evidence):
    """
    :param header: annotate vep txt file의 열 정보가 순서대로 나열된 list
    :param variant_data: 한 variant의 정보가 순서대로 나열된 list
    :param variant_evidence: main의 variant_evidence list

    gnomADg_AF의 값을 ratio로 저장
    ratio >= 0.05 -> BA1 이므로 대응 하는 variant_evidence[11] = True
    0.01 <= ratio < 0.05 -> BS1 이므로 대응 하는 variant_evidence[10] = True
    ratio <= 0.0001 -> PM2 이므로 대응 하는 variant_evidence[2] = True

    0.01 (1%) 는 Carrier frequency 기준 (보인자)
    0.00001 (0.001%) 는 Incidence 기준 (유병률) ( (4억/80억) / (5000~7000) ~= 0.00001 )
    """

    gnomadg_af_index = header.index('gnomADg_AF')

    if variant_data[gnomadg_af_index] != '-':
        ratio = float(variant_data[gnomadg_af_index])
        if ratio >= 0.05:
            variant_evidence[11] = True
        elif 0.01 <= ratio < 0.05:
            variant_evidence[10] = True
        elif ratio <= 0.00001 :
            variant_evidence[2] = True
