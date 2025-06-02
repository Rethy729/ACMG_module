def pp5_bp6(header, variant_data, variant_evidence):
    """
    :param header: annotate vep txt file의 열 정보가 순서대로 나열된 list
    :param variant_data: 한 variant의 정보가 순서대로 나열된 list
    :param variant_evidence: main의 variant_evidence list

    해당 evidence 판별에 필요한 CLinVar_CLNSIG, ClinVar_CLNREVSTAT data가 없는 경우 아무것도 하지 않고 return

    ClinVar_CLNREVSTAT 이 'practice_guideline', 'reviewed_by_expert_panel', 'criteria_provided,_multiple_submitters,_no_conflicts', 'criteria_provided,_single_submitter'인 경우에 한해
    ClinVar_CLNSIG 가 'Benign' 이거나 'Pathogenic' 한 경우, 각각 BP6 와 PP5 를 부여하므로 대응 되는 variant_evidence[9] = True, variant_evidence[6] = True
    하지만 PP5의 판별에서 missense_variant는 제외한다.
    """

    missing_option = [option for option in ['Consequence', 'ClinVar_CLNSIG', 'ClinVar_CLNREVSTAT'] if option not in header]
    if missing_option:
        print(f"Please annotate {', '.join(missing_option).lower()}")
        return
    consequence_index = header.index('Consequence')
    clinvar_clinsig_index = header.index('ClinVar_CLNSIG')  # 42
    clinvar_clnrevstat_index = header.index('ClinVar_CLNREVSTAT')  # 43

    clinsig = variant_data[clinvar_clinsig_index]
    clnrevstat = variant_data[clinvar_clnrevstat_index]
    consequence_data = variant_data[consequence_index]

    if clinsig != '-' and clnrevstat != '-':
        pass_status = ['practice_guideline', 'reviewed_by_expert_panel', 'criteria_provided,_multiple_submitters,_no_conflicts', 'criteria_provided,_single_submitter']
        if clnrevstat in pass_status:
            if clinsig == 'Benign':
                variant_evidence[9] = True
            elif clinsig == 'Pathogenic' and consequence_data != 'missense_variant':
                variant_evidence[6] = True