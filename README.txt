HG002_annotated_docker.txt -> vep annotation raw data
filtered_mane_select.tsv -> 위 파일에서 mane_select 된 줄만 filtering
ACMG_result.tsv -> 결과

0. 0.mane_filtering.py 실행을 통해 HG002_annotated_docker.txt 파일에서 mane select 된 variant만 filtering 하여 filtered_mane_select.tsv 를 생성

1. 이후 variant에 대해 evidence 부여
    (1.main.py 에서 PM4_BP3.py / PP3_BP4.py / PP5_BP6.py / BS1_BA1_PM2.py / PS1_PM5.py 모듈을 불러오는 구조)

2. 결과는 ACMG_result.tsv 에 저장

추후 계획:
PM2 판별 module
BS1 & PM2 정확한 threshold (gene에 연계된 disease의 정보와 그 disease의 유병률 / 성질을 알아야 함)
PP3 & BP4 에 활용하기 위해 sift, polyphen 이외에 in-silico tool 추가하기 (MutationTaster, CADD)
Test code
