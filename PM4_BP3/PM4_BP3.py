from functools import lru_cache
from collections import defaultdict
import re
import bisect

@lru_cache(maxsize=1)
def rmsk_dict_generator():
    """
    http://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/ 의 rmsk.txt.gz의 압축을 풀어 rmsk.txt를 얻었다.
    이 파일을 읽어 대체 서열 구간은 제외하고 (ex. chr21_GL383581v2_alt) repeat 서열의 정보를 rmsk_dict에 저장한다.
    이 dictionary 생성 과정은 @lru_cache(maxsize=1) 에 의해 처음 딱 한번만 진행된다. (1.main에서 호출할 때마다 dictionary를 다시 만드는 비효율적인 과정을 방지하기 위함)

    rmsk_dict의 구조는 다음과 같다.
    {chr1:[(10000, 10468), (10468, 11447) ... ], chr10: [(10000, 10435), (10435, 10793) ... ], ... }
    """

    file_path = 'rmsk.txt'
    with open(file_path, encoding='utf-8') as f_in:
        rmsk_dict = defaultdict(list)
        for line in f_in:
            line_data = line.strip().split('\t')
            chr_num, start_pos, end_pos = line_data[5], line_data[6], line_data[7]
            if len(chr_num) < 6: # alternative region 정보 제외 (ex. chr21_GL383581v2_alt)
                rmsk_dict[chr_num].append((int(start_pos), int(end_pos)))
    return rmsk_dict

def pm4_bp3(header, variant_data, variant_evidence):
    """
    :param header: annotate vep txt file의 열 정보가 순서대로 나열된 list
    :param variant_data: 한 variant의 정보가 순서대로 나열된 list
    :param variant_evidence: main의 variant_evidence list

    Consequence 정보가 stop_lost 인 경우, PM4 부여하므로 대응 되는 variant_evidence[3] = True
    Consequence 정보가 inframe_insertion / inframe_deletion 인 경우엔 추가로 rmsk_dict 를 생성한다.
    이외에 variant 구간이 어떤 rmsk 구간에 완전히 포함되는 경우에만 BP3을 부여하므로 대응되는 variant_evidence[7] = True
    그 이외의 경우에는 PM4 부여하므로 대응되는 variant_evidence[3] = True
    """

    location_index = header.index('Location')
    consequence_index = header.index('Consequence')

    consequence = variant_data[consequence_index]
    if 'stop_lost' in consequence:
        variant_evidence[3] = True

    elif 'inframe_insertion' in consequence or 'inframe_deletion' in consequence:
        rmsk_dict = rmsk_dict_generator()

        location = variant_data[location_index]
        chrom, start, end = re.split(r'[:\-]', location)

        intervals = rmsk_dict[chrom]
        interval_starts = [int(start) for start, _ in intervals]
        idx = bisect.bisect_right(interval_starts, int(start))

        if idx == 0: # variant가 모든 구간 시작보다 앞에 위치할 때, 어차피 겹치는 구간 없으므로 PM4
            variant_evidence[3] = True
        else:
            interval_start, interval_end = intervals[idx - 1] # idx-1인 이유는 bisect_right이기 때문
            if int(interval_start) <= int(start) and int(end) <= int(interval_end): # variant 구간이 rmsk 구간과 완전히 겹치는 경우, BP3
                variant_evidence[7] = True
            else:
                variant_evidence[3] = True