def parent_variant_set_generator():

    file_path_1 = 'HG003_GRCh38_1_22_v4.2.1_benchmark.vcf'
    file_path_2 = 'HG004_GRCh38_1_22_v4.2.1_benchmark.vcf'

    parent_variant_set = set()

    with open(file_path_1, encoding='utf-8') as f_1, open(file_path_2, encoding='utf-8') as f_2:
        for line in f_1:
            if line.startswith('#'):
                continue
            line_data = line.strip().split('\t')
            if ',' not in line_data[4]:
                variant_data = (line_data[0], line_data[1], line_data[3], line_data[4])
                parent_variant_set.add(variant_data)
            elif ',' in line_data[4]:
                alt = line_data[4].split(',')
                for a in alt:
                    variant_data = (line_data[0], line_data[1], line_data[3], a)
                    parent_variant_set.add(variant_data)

        for line in f_2:
            if line.startswith('#'):
                continue
            line_data = line.strip().split('\t')
            if ',' not in line_data[4]:
                variant_data = (line_data[0], line_data[1], line_data[3], line_data[4])
                parent_variant_set.add(variant_data)
            elif ',' in line_data[4]:
                alt = line_data[4].split(',')
                for a in alt:
                    variant_data = (line_data[0], line_data[1], line_data[3], a)
                    parent_variant_set.add(variant_data)

    return parent_variant_set

parent_data_set = parent_variant_set_generator()

def de_novo_variant(variant_set):

    file_path = 'HG002_GRCh38_1_22_v4.2.1_benchmark.vcf'
    output_path = '../denovo_variant.tsv'

    count = 0
    with open(file_path, encoding='utf-8') as f_in, open(output_path, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            if line.startswith('#'):
                continue

            line_data = line.strip().split('\t')

            if ',' not in line_data[4]:
                variant_data = (line_data[0], line_data[1], line_data[3], line_data[4])
                if variant_data not in variant_set:
                    f_out.write('\t'.join(variant_data) + '\n')
                    count += 1

                elif ',' in line_data[4]:
                    alt = line_data[4].split(',')
                    for a in alt:
                        variant_data = (line_data[0], line_data[1], line_data[3], a)
                        if variant_data not in variant_set:
                            f_out.write('\t'.join(variant_data) + '\n')
                            count += 1
    print (count)

de_novo_variant(parent_data_set)
print ('complete')