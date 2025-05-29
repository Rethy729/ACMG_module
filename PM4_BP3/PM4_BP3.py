def pm4_bp3(header, variant_data, variant_evidence):
    """
    :param header: annotate vep txt file의 열 정보가 순서대로 나열된 list
    :param variant_data: 한 variant의 정보가 순서대로 나열된 list
    :param variant_evidence: main의 variant_evidence list

    해당 evidence 판별에 필요한 Consequence, DOMAINS data가 없는 경우 아무것도 하지 않고 return

    Consequence 정보가 stop_lost 인 경우, PM4 부여하므로 대응 되는 variant_evidence[3] = True
    Consequence 정보가 inframe_insertion / inframe_deletion 인 경우엔 추가로 DOMAINS 정보를 참고한다.
    DOMAINS 정보가 없거나 ('-'), DOMAIN 정보에 intrinsically disordered regions (IDRs) 가 포함되어있거나 ('MobiDB_lite' 포함유무),
    Low complexity regions (LCRs) 가 포함되어 있는 겅우 ('Low_complexity_' 포함유무) BP3을 부여하므로 대응되는 variant_evidence[7] = True
    """

    missing_option = [option for option in ['Consequence', 'DOMAINS'] if option not in header]
    if missing_option:
        print(f"Please annotate {', '.join(missing_option).lower()}")
        return
    consequence_index = header.index('Consequence') # 6
    domains_index = header.index('DOMAINS')  # 24

    consequence = variant_data[consequence_index]
    if 'stop_lost' in consequence:
        variant_evidence[3] = True
    elif 'inframe_insertion' in consequence or 'inframe_deletion' in consequence:
        domain_data = variant_data[domains_index]
        if domain_data == '-' or 'MobiDB_lite' in domain_data or 'Low_complexity_' in domain_data:
            variant_evidence[7] = True
        else:
            variant_evidence[3] = True