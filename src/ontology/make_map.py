import csv

input_file = "old_ids.tsv"
output_file = "rename_map.tsv"

with open(input_file, mode='r', encoding='utf-8') as f:
    # Use DictReader to handle the TSV structure
    reader = csv.DictReader(f, delimiter='\t')
    
    with open(output_file, "w", encoding='utf-8') as out:
        out.write("Old IRI\tNew IRI\n")
        
        count = 1
        for row in reader:
            # Get the IRI from the row
            old_iri = row.get('IRI')
            
            if not old_iri:
                continue
            
            # ONLY process IRIs that belong to your EMPTY ontology (the 9-digit ones)
            # This ensures we don't accidentally rename UBERON or OBI terms
            if 'http://purl.obolibrary.org/obo/EMPTY_' in old_iri:
                # Create the 7-digit ID (e.g., EMPTY_0000001)
                new_id = f"EMPTY_{str(count).zfill(7)}"
                new_iri = f"http://purl.obolibrary.org/obo/{new_id}"
                
                out.write(f"{old_iri}\t{new_iri}\n")
                count += 1

print(f"Success! Created {output_file} with {count-1} mappings for EMPTY terms.")