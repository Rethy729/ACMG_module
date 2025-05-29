def ps1_pm5(header, variant_data, variant_evidence):

    vcf_file_path = 'clinvar.vcf'

    consequence_index = header.index('Consequence')
    location_index = header.index('Location')

    if variant_data[consequence_index] == 'missense_variant':
        print (variant_data[consequence_index], variant_data[location_index])
        location_data = variant_data[location_index].split(':')
        print (location_data)

        with open(vcf_file_path, encoding='utf-8') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                else:
                    if
