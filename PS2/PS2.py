from functools import lru_cache
import re

@lru_cache(maxsize=1)
def de_novo_variant_set_generator():
    """
    denovo_variant.tsv의 정보를 한줄씩 읽어, de_novo_variant_set에 저장한다.
    이때, SNV (ref 와 alt 의 길이가 모두 1인 경우)는 그대로 저장할 수 있다.
    indel의 경우, vep annotation을 거치면 ref base의 position이 1씩 밀려난다.
    추후 annotation된 data와의 비교를 위해, indel (ref와 alt의 길이 중 하나가 1보다 큰 경우)은
    길이가 1인 ref 혹은 alt를 '-' 로 대체하고, 길이가 1보다 긴 alt 혹은 ref의 맨 앞 base를 제거하여 저장한다.
    혹시 ref와 alt가 둘 다 길이가 2 이상인 경우가 존재하는 경우, ref base의 position이 변하지 않으므로 고려할 필요가 없다.
    """

    de_novo_variant_set = set()
    file_path = 'denovo_variant.tsv'
    with open(file_path, encoding='utf-8') as f_in:
        for line in f_in:
            line_data = line.strip().split('\t')
            if len(line_data[2]) >= 2:
                de_novo_variant_set.add((line_data[0], str(int(line_data[1]) + 1), line_data[2][1:], '-'))
            elif len(line_data[3]) >= 2:
                de_novo_variant_set.add((line_data[0], str(int(line_data[1]) + 1), '-', line_data[3][1:]))
            else:
                de_novo_variant_set.add((line_data[0], line_data[1], line_data[2], line_data[3]))
    return de_novo_variant_set

def ps2(header, variant_data, variant_evidence):
    """
    :param header: annotate vep txt file의 열 정보가 순서대로 나열된 list
    :param variant_data: 한 variant의 정보가 순서대로 나열된 list
    :param variant_evidence: main의 variant_evidence list

    HG002~ 의 de novo variant 정보가 담긴 de_novo_variant_set을 생성하고 (1_main.py 에서 여러번 호출해도 한번만 생성됨)
    variant_data를 de_novo_variant_set에 담긴 data의 포맷에 맞춘다. ('chr1', '209131778', 'A', 'C') -> variant_data_tuple
    variant_data_tuple 이 de_novo_variant_set에 포함되어 있으면, PS2 를 부여하므로 대응 되는 variant_evidence[1] = True,
    """

    uploaded_variation_index = header.index('Uploaded_variation')
    allele_index = header.index('Allele')

    uploaded_variation_data = variant_data[uploaded_variation_index]
    allele_data = variant_data[allele_index]

    de_novo_variant_set = de_novo_variant_set_generator()

    uploaded_variation_data_list = re.split(r'[_/]', uploaded_variation_data)
    variant_data_tuple = (uploaded_variation_data_list[0], uploaded_variation_data_list[1], uploaded_variation_data_list[2], allele_data)

    if variant_data_tuple in de_novo_variant_set:
        variant_evidence[1] = True