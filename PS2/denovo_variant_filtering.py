def parent_variant_set_generator():

    """
    부모의 원본 vcf 파일 (HG003~, HG004~) 를 둘 다 읽으며 variant 정보를 parent_variant_set에 입력한다(중복제거).
    이때, alternative 서열이 두개 이상인 variant는 각각 다른 원소로 쪼개어 저장한다.
    저장된 원소는 다음과 같다: ... ('chr1', '209131778', 'A', 'C'), ('chr1', '209132143', 'T', 'A') ...
    """

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

    """
    :param variant_set: 위 parent_variant_set_generator() 통해 생성된 parent의 variant 정보를 담은 set을 받는다.

    parent_variant_set_generator() 와 완전히 동일한 방식으로 자식 (HG002~)의 원본 vcf 파일을 읽는다
    이떄, variant_set에 이미 포함된 variant 정보는 제외하고, 나머지 denovo variant 정보는 ../denovo_variant.tsv 에 저장한다.
    """
    file_path = 'HG002_GRCh38_1_22_v4.2.1_benchmark.vcf'
    output_path = '../denovo_variant.tsv'

    #count = 0
    with open(file_path, encoding='utf-8') as f_in, open(output_path, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            if line.startswith('#'):
                continue

            line_data = line.strip().split('\t')

            if ',' not in line_data[4]:
                variant_data = (line_data[0], line_data[1], line_data[3], line_data[4])
                if variant_data not in variant_set:
                    f_out.write('\t'.join(variant_data) + '\n')
                    #count += 1

                elif ',' in line_data[4]:
                    alt = line_data[4].split(',')
                    for a in alt:
                        variant_data = (line_data[0], line_data[1], line_data[3], a)
                        if variant_data not in variant_set:
                            f_out.write('\t'.join(variant_data) + '\n')
                            #count += 1
    #print (count)
de_novo_variant(parent_data_set)
print ('Complete')