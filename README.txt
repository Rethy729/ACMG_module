0. HG002_annotated_docker.txt 파일에서 mane select 된 variant만 filtering 하여 filtered_mane_select.tsv 를 생성
    (0.mane_filtering.py)
1. 이후 variant에 대해 evidence 할당
    (1.main.py 에서 PM4_BP3.py / PP3_BP4.py / PP5_BP6.py / BS1_BA1_PM2.py 불러오는 구조)
2. 결과는 ACMG_result.tsv 에 저장