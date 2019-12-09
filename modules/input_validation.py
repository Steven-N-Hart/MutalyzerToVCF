from modules.conversions import *

logger = logging.getLogger(__name__)


def parse_line(line):
    new_line = line.strip().split('\t')
    if len(new_line) < 3:
        return new_line[0], '', None
    else:
        variant, errors, chrom = new_line[:3]
        return variant, errors, chrom


def get_event_type_function(variant):
    event_type = None
    if 'delins' in variant:
        event_type = 'delins'
        parse_function = convert_delins
    elif 'del' in variant:
        event_type = 'del'
        parse_function = convert_del
    elif 'ins' in variant:
        event_type = 'ins'
        parse_function = convert_ins
    elif 'dup' in variant:
        event_type = 'dup'
        parse_function = convert_dup
    elif 'inv' in variant:
        event_type = 'inv'
        parse_function = convert_inv
    elif '>' in variant:
        event_type = 'snp'
        parse_function = convert_snp
    else:
        raise NameError("I do not know what this variant is: {}".format(variant))

    return event_type, parse_function
