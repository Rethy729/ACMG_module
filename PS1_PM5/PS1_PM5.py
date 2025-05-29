from functools import lru_cache
from collections import defaultdict
import re

@lru_cache(maxsize=1)
def clinvar_dict_generator():
    """

    :return:
    """

    clinvar_path = 'filtered_mane_select_clinvar.tsv'
    with open(clinvar_path, encoding='utf-8') as f:
        clinvar_header = f.readline().strip().split('\t')  # clinvar_header

    consequence_index = clinvar_header.index('Consequence')
    hgvs_c_index = clinvar_header.index('HGVSc')
    hgvs_p_index = clinvar_header.index('HGVSp')
    with open(clinvar_path, encoding='utf-8') as f:
        next(f)  # header 건너 뛰기
        clinvar_dict = defaultdict(list)
        for line in f:
            clinvar_data = line.strip().split('\t')
            if clinvar_data[consequence_index] != 'missense_variant':
                continue

            position = clinvar_data[1]
            hgvs_values = [clinvar_data[hgvs_c_index], clinvar_data[hgvs_p_index]]
            if '-' in position:
                chrom, start, end = re.split(r'[:\-]', position)
                for i in range(int(start), int(end)):
                    key = f'{chrom}:{i}'
                    clinvar_dict[key].append(hgvs_values)
            else:
                clinvar_dict[position].append(hgvs_values)
    return clinvar_dict

def ps1_pm5(header, variant_data, variant_evidence):
    """

    :param header:
    :param variant_data:
    :param variant_evidence:
    :return:
    """

    consequence_index = header.index('Consequence')
    location_index = header.index('Location')
    hgvs_c_index = header.index('HGVSc')
    hgvs_p_index = header.index('HGVSp')

    if variant_data[consequence_index] == 'missense_variant':
        clinvar_dict = clinvar_dict_generator()  # main에서 ps1_pm5가 여러번 호출되어도 dictionary 생성은 단 한번 이루어진다.
        location_data = variant_data[location_index][3:]
        matches = clinvar_dict.get(location_data, [])
        if matches:
            hgvs_c, hgvs_p = variant_data[hgvs_c_index], variant_data[hgvs_p_index]
            for clinvar_c, clinvar_p in matches:
                if hgvs_c != clinvar_c:
                    if hgvs_p == clinvar_p:
                        variant_evidence[0] = True
                    else:
                        variant_evidence[4] = True
