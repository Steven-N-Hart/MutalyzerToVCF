import argparse
import sys

from pyfaidx import Fasta

from modules.input_validation import *


def main():
    """Console script for dicom_wsi."""
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input",
                        dest='input',
                        required=True,
                        help="Output file from mutalyzer")

    parser.add_argument("-f", "--fasta",
                        dest='fasta_file',
                        required=True,
                        help="FASTA file")

    parser.add_argument("-o", "--out",
                        dest='output',
                        default='mutalyzer.out',
                        help="outfile name")

    parser.add_argument("-v", "--verbose",
                        dest="logLevel",
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default="INFO",
                        help="Set the logging level")

    args = parser.parse_args()
    logging.basicConfig(stream=sys.stderr, level=args.logLevel,
                        format='%(name)s (%(levelname)s): %(message)s')

    logger = logging.getLogger(__name__)
    logger.setLevel(args.logLevel)
    fasta_file = Fasta(args.fasta_file)
    o = open(args.output, 'w')

    # Read in mutalyzer file
    with open(args.input, 'r') as f:
        for line in f:
            submitted_variant, errors, returned_variant = parse_line(line)
            if returned_variant is None:
                logger.warning('Line does not have enough columns. Skipping: {}'.format(line))
                continue
            logger.debug('Var: {}'.format(submitted_variant))
            event_type, parse_function = get_event_type_function(returned_variant)
            chr, start, ref, alt = parse_function(returned_variant, fasta_file)
            outline = [submitted_variant, errors, returned_variant, event_type, chr, start, ref, alt]
            outline = '\t'.join([str(x) for x in outline])
            o.write(outline + '\n')

    o.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
