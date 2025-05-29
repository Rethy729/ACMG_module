from functools import lru_cache

@lru_cache(maxsize=1)
def clinvar_dict_generator():
    clinvar_path = 'blahblah.txt'
    with open(clinvar_path, encoding='utf-8') as f:
        clinvar_header = f.readline().strip().split('\t')  # clinvar_header

    hgvs_c_index = clinvar_header.index('HGVSc')
    hgvs_p_index = clinvar_header.index('HGVSp')

    with open(clinvar_path, encoding='utf-8') as f:
        next(f)  # header 건너 뛰기
        clinvar_dict = {}
        for line in f:
            clinvar_data = line.strip().split('\t')
            clinvar_dict[clinvar_data[1]] = [clinvar_data[hgvs_c_index], clinvar_data[hgvs_p_index]]  # dictionary로 파싱 예) {(2, 444324):[hgvs.g, hgvs.p], ... }
    return clinvar_dict

def ps1_pm5(header, variant_data, variant_evidence):
    consequence_index = header.index('Consequence')
    location_index = header.index('Location')

    if variant_data[consequence_index] == 'missense_variant':

        clinvar_dict_cache = clinvar_dict_generator() # main에서 ps1_pm5가 여러번 호출되어도 dictionary 생성은 단 한번 이루어진다.

        print (variant_data[consequence_index], variant_data[location_index])
        location_data = variant_data[location_index].split(':')
        print (location_data)




