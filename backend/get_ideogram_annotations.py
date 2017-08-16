import argparse
import json

parser = argparse.ArgumentParser(description=
    "Get ideogram annotations from expression data\n" +
    "Example:\n" +
    "python3 get_ideogram_annotations.py --output ../webapp/genvis/static/js/ideogram/dist/data/annotations/mouse_aging.json",
    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument("--output", "-o",
                    help="Output JSON file path",
                    default='ideo_annots.json')

args = parser.parse_args()

output_path = args.output


# Our longitudinal expression data provides multiple replicates for each age
# This function averages those replicates, combining "age" and "flu" components
def get_mean_gene_expressions_over_time(tissue):

    with open(data_dir + tissue + '.shuff.norm.counts.csv') as f:
        lines = f.readlines()

    # Get column headers, without surrounding quotation marks
    headers = [header.strip('"') for header in lines[0].split(',')]

    age_indexes_by_age = {}

    # Average expressions values over time for each gene
    expressions = {}

    for i, header in enumerate(headers[1:]):
        # See ../data/column_components.csv
        components = header.split('_')
        age = components[2]
        flu = components[3]
        age_flu = age + '_' + flu
        if age_flu in age_indexes_by_age:
            age_indexes_by_age[age_flu].append(i + 1)
        else:
            age_indexes_by_age[age_flu] = [i + 1]

    for line in lines[1:]:

        columns = line.split(',')
        gene_id = columns[0].strip('"')
        mean_expression_by_age = {}

        for age in age_indexes_by_age:
            age_indexes = age_indexes_by_age[age]
            num_samples_at_age = len(age_indexes)
            mean_expression_by_age[age] = 0
            for age_index in age_indexes:
                expression = float(columns[age_index])
                mean_expression_by_age[age] += expression/num_samples_at_age

            for age in mean_expression_by_age:
                mean = mean_expression_by_age[age]
                # filterMap = {
                #     "expression-level": {
                #         "extremely-high": 7,
                #         "very-high": 6,
                #         "high": 5,
                #         "moderately-high": 4,
                #         "moderate": 3,
                #         "low": 2,
                #         "very-low": 1
                #     }
                # };

                if mean < 1:
                    value = 1
                elif mean < 2.5:
                    value = 2
                elif mean < 5:
                    value = 3
                elif mean < 10:
                    value = 4
                elif mean < 20:
                    value = 5
                elif mean < 30:
                    value = 6
                elif mean >= 30:
                    value = 7

                mean_expression_by_age[age] = value

        expressions[gene_id] = mean_expression_by_age

    return expressions


def get_gene_locations():

    gene_locations = {}

    with open(data_dir + 'mouse_geneid_map_GRCm38_081517.csv') as f:
        lines = f.readlines()[1:]

    for line in lines:
        columns = [column.strip('"') for column in line.split(',')]
        gene_id = columns[0]

        chromosome = columns[6]

        if chromosome == 'MT':
            continue

        gene_locations[gene_id] = {
            'chromosome': chromosome,
            'start': int(columns[7]),
            'end': int(columns[8])
        }

    return gene_locations


# Sorts compound age_flu key by age, then flu
# Example input:
# ['01M_F0', '24M_F150', '24M_F10', '18M_F0', '18M_F10', '04M_F0', '04M_F10', '04M_F150', '09M_F150', '12M_F150', '12M_F0', '09M_F0', '12M_F10', '24M_F0', '18M_F150', '09M_F10']
# Example output:
# ['01M_F0', '04M_F0', '09M_F0', '12M_F0', '18M_F0', '24M_F0', '04M_F10', '09M_F10', '12M_F10', '18M_F10', '24M_F10', '04M_F150', '09M_F150', '12M_F150', '18M_F150', '24M_F150']
def sort_age_flu(age_flu_list):

    age_flu_list.sort(key=lambda x: int(x.split('_')[0][:-1]))
    age_flu_list.sort(key=lambda x: int(x.split('_')[1][1:]))

    return age_flu_list


# @param gene_locations Dictionary of form "gene_id: {chromosome, start, end}"
# @param expressions Dictionary mean gene expression by age; of form "gene_id: {age1, age2, ..., ageN}"
def get_annotations(gene_locations, expressions):

    annots_list = []
    annots_by_chr = {}

    example_gene_id = list(expressions.keys())[0]
    ages = expressions[example_gene_id]

    # Example "age_flu": 18M_F150 (18 months, f150).  All ages are in months.
    sorted_ages = sort_age_flu(list(ages.keys()))

    for gene_id in list(expressions.keys()):

        if gene_id not in gene_locations:
            print('Gene locations missing for ' + gene_id)
            continue

        location = gene_locations[gene_id]
        chromosome = location['chromosome']
        start = location['start']
        length = location['end'] - location['start']

        ordered_mean_expressions_by_age = []

        expression = expressions[gene_id]

        for age in sorted_ages:
            ordered_mean_expressions_by_age.append(expression[age])

        annotation = [gene_id, start, length, 0]
        annotation += ordered_mean_expressions_by_age

        if chromosome in annots_by_chr:
            annots_by_chr[chromosome].append(annotation)
        else:
            annots_by_chr[chromosome] = [annotation]

    for chromosome in annots_by_chr:
        annots_list.append({
            'chr': chromosome,
            'annots': annots_by_chr[chromosome]
        })

    keys = ['name', 'start', 'length', 'trackIndex']

    keys.extend(sorted_ages)

    annotations = {
        'keys': keys,
        'annots': annots_list
    }

    return annotations

data_dir = '../data/'

expressions = get_mean_gene_expressions_over_time('lung')

print('Number of genes with expression data:')
print(len(expressions))

gene_locations = get_gene_locations()

annotations = get_annotations(gene_locations, expressions)

num_annots = 0
for annots in annotations['annots']:
    num_annots += len(annots['annots'])

print('Number of annotations:')
print(str(num_annots))

ideo_annots = json.dumps(annotations)

open(output_path, 'w').write(ideo_annots)