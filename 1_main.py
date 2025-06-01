from BS1_BA1_PM2 import BS1_BA1_PM2
from PP3_BP4 import PP3_BP4
from PP5_BP6 import PP5_BP6
from PM4_BP3 import PM4_BP3
from PS1_PM5 import PS1_PM5

file_path = 'filtered_mane_select.tsv'
output_path = 'ACMG_result.tsv'

with open(file_path, encoding='utf-8') as f:
    header = f.readline().strip().split('\t') # header

evidence = ['PS1', 'PS2', 'PM2', 'PM4', 'PM5', 'PP3', 'PP5', 'BP3', 'BP4', 'BP6', 'BS1', 'BA1']
with open(file_path, encoding='utf-8') as f_in, open(output_path, 'w', encoding='utf-8') as f_out:
    next(f_in) # header 건너 뛰기

    evidence_count_list = [0] * len(evidence)

    f_out.write('variant\t' + '\t'.join(evidence) + '\n')
    for line in f_in:
        variant_evidence = [False] * len(evidence)
        variant_data = line.strip().split('\t')

        PS1_PM5.ps1_pm5(header, variant_data, variant_evidence)
        BS1_BA1_PM2.ba1_bs1_pm2(header, variant_data, variant_evidence)
        PP3_BP4.pp3_bp4(header, variant_data, variant_evidence)
        PP5_BP6.pp5_bp6(header, variant_data, variant_evidence)
        PM4_BP3.pm4_bp3(header, variant_data, variant_evidence)

        for i, b in enumerate(variant_evidence):
            if b:
                evidence_count_list[i] += 1

        output_line = ['Yes' if b is True else 'x' for b in variant_evidence]
        f_out.write(variant_data[0]+ '\t' + variant_data[2] + '\t' + '\t'.join(output_line) + '\n')

    print ('Complete')
    print (evidence_count_list)