from functools import lru_cache

@lru_cache(maxsize=1)

def de_novo_variant_set_generator():
    """

    :return:
    """

    de_novo_variant_set = set()

    file_path = 'denovo_variant.tsv'
    with open(file_path, encoding='utf-8') as f_in:
        for line in f_in:
            line_data = line.strip().split('\t')
            de_novo_variant_set.add((line_data[0], line_data[1], line_data[3]))

    return de_novo_variant_set

def ps2(header, variant_data, variant_evidence):

    missing_option = [option for option in ['Uploaded_variation', 'Allele'] if option not in header]
    if missing_option:
        print(f"Please annotate {', '.join(missing_option).lower()}")
        return
    uploaded_variation_index = header.index('Uploaded_variation')
    allele_index = header.index('Allele')

    uploaded_variation_data = variant_data[uploaded_variation_index]
    allele_data = variant_data[allele_index]

