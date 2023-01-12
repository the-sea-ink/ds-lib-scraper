import argparse

parser = argparse.ArgumentParser(description='Applies postprocessing to raw scraped data. Currently only adds '
                                             'an index column.')

parser.add_argument('-i', '--input_file', help='Input file', required=True)
parser.add_argument('-o', '--output_file', help='Output file', required=True)
args = parser.parse_args()


def enum():
    infile_path = args.input_file
    outfile_path = args.output_file

    with open(infile_path) as infile, open(outfile_path, 'w') as outfile:
        for idx, line in enumerate(infile):
            if idx == 0:
                outfile.write(f'index,{line}')
            else:
                outfile.write(f'{idx},{line}')


enum()
