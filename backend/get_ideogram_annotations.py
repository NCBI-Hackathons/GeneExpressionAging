import json

# Our longitudinal expression data provides 3 replicates for each age
# This function averages those replicates
def get_mean_gene_expressions_over_time(tissue):

    with open(data_dir + tissue + '.cleaned.norm.counts.csv') as f:
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
        if age in age_indexes_by_age:
            age_indexes_by_age[age].append(i + 1)
        else:
            age_indexes_by_age[age] = [i + 1]

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

        expressions[gene_id] = mean_expression_by_age

    return expressions


def get_gene_locations():

    gene_locations = {}

    with open(data_dir + 'mouse_geneid_map_grch37_081417.csv') as f:
        lines = f.readlines()[1:]

    for line in lines:
        columns = [column.strip('"') for column in line.split(',')]
        gene_id = columns[0]
        gene_locations[gene_id] = {
            'chromosome': columns[6],
            'start': int(columns[7]),
            'end': int(columns[8])
        }

    return gene_locations


# @param gene_locations Dictionary of form "gene_id: {chromosome, start, end}"
# @param expressions Dictionary mean gene expression by age; of form "gene_id: {age1, age2, ..., ageN}"
def get_annotations(gene_locations, expressions):

    annotations = {}

    for gene_id in list(expressions.keys())[:10]:

        if gene_id not in gene_locations:
            print('Gene locations missing for ' + gene_id)
            continue

        location = gene_locations[gene_id]
        chromosome = location['chromosome']
        start = location['start']
        length = location['end'] - location['start']

        ordered_mean_expressions_by_age = []

        for age in sorted(expressions):
            ordered_mean_expressions_by_age.append(expressions[age])

        annotation = [gene_id, start, length, 0]
        annotation += ordered_mean_expressions_by_age

        if chromosome in annotations:
            annotations[chromosome].append(annotation)
        else:
            annotations[chromosome] = [annotation]

    keys = ['gene_id', 'start', 'length', 'traceIndex']

    example_gene_id = list(expressions.keys())[0]
    ages = sorted(expressions[example_gene_id])

    keys.extend(ages)

    annotations = {
        'keys': keys,
        'annotations': annotations
    }

    return annotations


data_dir = '../data/'

expressions = get_mean_gene_expressions_over_time('lung')

gene_locations = get_gene_locations()

annotations = get_annotations(gene_locations, expressions)

print(json.dumps(annotations['annotations'], indent=2))

