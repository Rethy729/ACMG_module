HG002_annotated_docker_v2.txt -> vep annotation raw data
filtered_mane_select.tsv -> 위 파일에서 mane_select 된 줄 filtering + mane_select가 없는 변이의 경우에는 임의로 마지막 줄을 포함
ACMG_result.tsv -> 결과


0. 0_mane_filtering.py 실행을 통해 HG002_annotated_docker_v2.txt 파일에서 variant를 filtering 하여 filtered_mane_select.tsv 를 생성

1. 이후 variant에 대해 evidence 부여
    (1_main.py 에서 PM4_BP3.py / PP3_BP4.py / PP5_BP6.py / BS1_BA1_PM2.py / PS1_PM5.py / PS2.py 모듈을 불러오는 구조)

2. 결과는 ACMG_result.tsv 에 저장

추후 계획:
Test code
