from functools import lru_cache
from collections import defaultdict
import re

@lru_cache(maxsize=1)
def clinvar_dict_generator():
    """
    filtered_mane_select_clinvar.tsv 파일을 읽어, clinvar_dict를 생성하여 return한다.
    이 dictionary 생성 과정은 @lru_cache(maxsize=1) 에 의해 처음 딱 한번만 진행된다. (1.main에서 호출할 때마다 dictionary를 다시 만드는 비효율적인 과정을 방지하기 위함)

    이 clinvar_dict는 다음과 같은 구조를 가진다:
    filtered_mane_select_clinvar.tsv파일의 모든 data 중, consequence가 missense variant 인 data에 한하여,
    position(key)과 그 position에 존재하는 모든 [hgvs.c, hgvs.p]쌍들의 list (value) 를 짝짓는다

    고려사항 1
    5836	5:137870830	G	ENSG00000120729	ENST00000239926	Transcript	missense_variant	484	179	60	S/C	tCt/tGt	-	MODERATE	-	1	-	MANE_Select	NM_006790.3	-	ENST00000239926.9:c.179C>G	ENSP00000239926.4:p.Ser60Cys	-
    5837	5:137870830	T	ENSG00000120729	ENST00000239926	Transcript	missense_variant	484	179	60	S/F	tCt/tTt	-	MODERATE	-	1	-	MANE_Select	NM_006790.3	-	ENST00000239926.9:c.179C>T	ENSP00000239926.4:p.Ser60Phe	-
    이와 같이 같은 position에 두 개 이상의 [hgvs.c, hgvs.p] 쌍이 존재하는 경우가 있어, clinvar_dict는 defaultdict(list)으로 정의되고,
    한 position (key) 에는 여러개의 [hgvs.c, hgvs.p] 쌍을 원소로 가지는 list가 짝지어진다.

    고려사항 2
    1701565	9:27229171-27229173	ACC	ENSG00000120156	ENST00000380036	Transcript	missense_variant	3680-3682	3314-3316	1105-1106	TT/NP	aCCAcg/aACCcg	-	MODERATE	-	1	-	MANE_Select	NM_000459.5	-	ENST00000380036.10:c.3314_3316delinsACC	ENSP00000369375.4:p.Thr1105_Thr1106delinsAsnPro	-
    이와 같이 missense variant가 single nucleotide variant가 아닐 경우가 있다.
    이때는 가능한 모든 position (9:27229171, 9:27229172, 9:27229173)을 독립적인 key로 간주하고, 각각의 key에는 같은 [hgvs.c, hgvs.p] 쌍을 짝짓는다.
    """

    clinvar_path = 'filtered_mane_select_clinvar.tsv'
    with open(clinvar_path, encoding='utf-8') as f:
        clinvar_header = f.readline().strip().split('\t')  # clinvar_header

    location_index = clinvar_header.index('Location')
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

            location = clinvar_data[location_index]
            hgvs_values = [clinvar_data[hgvs_c_index], clinvar_data[hgvs_p_index]]
            if '-' in location:
                chrom, start, end = re.split(r'[:\-]', location)
                for i in range(int(start), int(end)):
                    key = f'{chrom}:{i}'
                    clinvar_dict[key].append(hgvs_values)
            else:
                clinvar_dict[location].append(hgvs_values)
    return clinvar_dict

def ps1_pm5(header, variant_data, variant_evidence):
    """

    :param header: annotate vep txt file의 열 정보가 순서대로 나열된 list
    :param variant_data: 한 variant의 정보가 순서대로 나열된 list
    :param variant_evidence: main의 variant_evidence list

    missense variant 중 ClinVar_CLNSIG 가 pathogenic 이며
    ClinVar_CLNREVSTAT 이 'practice_guideline', 'reviewed_by_expert_panel', 'criteria_provided,_multiple_submitters,_no_conflicts', 'criteria_provided,_single_submitter'
    인 경우에 한해 PS1을 부여하여 variant_evidence[0] = True

    그 외의 clnsig를 가지는 missense variant 정보를 처리하기 위해 clinvar_dict_generator()를 통해 clinvar의 missense variant data를 담은 dictionary를 불러온다.
    이후, 이 variant의 location이 clinvar database (dictionary)안에 존재한다면,
    우선 두 variant의 hgvs.c를 비교하여 다른 경우에만 hgvs.p를 비교한다.
    두 variant의 hgvs.p가 같다면 PS1을 부여하므로 대응 되는 variant_evidence[0] = True
    두 variant의 hgvs.p가 다르다면 PM5를 부여하므로 대응 되는 variant_evidence[4] = True
    """

    location_index = header.index('Location')
    consequence_index = header.index('Consequence')
    hgvs_c_index = header.index('HGVSc')
    hgvs_p_index = header.index('HGVSp')
    clinvar_clinsig_index = header.index('ClinVar_CLNSIG')
    clinvar_clnrevstat_index = header.index('ClinVar_CLNREVSTAT')

    consequence_data = variant_data[consequence_index]
    if consequence_data == 'missense_variant':

        clnsig_data = variant_data[clinvar_clinsig_index]
        clnrevstat = variant_data[clinvar_clnrevstat_index]
        pass_status = ['practice_guideline', 'reviewed_by_expert_panel',
                       'criteria_provided,_multiple_submitters,_no_conflicts', 'criteria_provided,_single_submitter']

        if 'Pathogenic' in clnsig_data and clnrevstat in pass_status: # missense variant 중 clnsig 가 pathogenic 한 데이터는 PS1으로 분류
            variant_evidence[0] = True
            return

        else:  # 그 외의 경우
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