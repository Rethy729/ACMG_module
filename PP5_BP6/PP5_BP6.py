def pp5_bp6(header, variant_data, variant_evidence):
    """
    :param header: annotate vep txt file의 열 정보가 순서대로 나열된 list
    :param variant_data: 한 variant의 정보가 순서대로 나열된 list
    :param variant_evidence: main의 variant_evidence list

    해당 evidence 판별에 필요한 CLinVar_CLNSIG, ClinVar_CLNREVSTAT data가 없는 경우 아무것도 하지 않고 return

    ClinVar_CLNREVSTAT 이 'no_assertion_criteria_provided"인 경우에 한해 (기준이 제공되지 않은 경우)
    ClinVar_CLNSIG 가 'Benign' 이거나 'Pathogenic' 한 경우, 각각 BP6 와 PP5 를 부여하므로 대응 되는 variant_evidence[9] = True, variant_evidence[6] = True

    추후 고려 사항: STAT이 single submitter 인 경우, CLNSIG 가 Likely_ 한 경우 or 여러 개의 상태가 중첩된 경우 (ex. Pathogenic|Protective)
    """

    missing_option = [option for option in ['ClinVar_CLNSIG', 'ClinVar_CLNREVSTAT'] if option not in header]
    if missing_option:
        print(f"Please annotate {', '.join(missing_option).lower()}")
        return
    clinvar_clinsig_index = header.index('ClinVar_CLNSIG')  # 42
    clinvar_clnrevstat_index = header.index('ClinVar_CLNREVSTAT')  # 43

    clinsig = variant_data[clinvar_clinsig_index]
    clnrevstat = variant_data[clinvar_clnrevstat_index]
    if clinsig != '-' and clnrevstat != '-':
        if clnrevstat == 'no_assertion_criteria_provided':
            if clinsig == 'Benign':
                variant_evidence[9] = True
            elif clinsig == 'Pathogenic':
                variant_evidence[6] = True
