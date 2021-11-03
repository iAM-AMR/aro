from owlready2 import *
import csv
import sys
import os

def aro_query(start_id=sys.argv[1], depth=sys.argv[2]):

    #  Load the ontology
    
    os.chdir('..')
    aro_path = os.path.abspath(os.curdir)

    onto = get_ontology(aro_path + '\\aro.owl').load()

    namespace = onto.get_namespace("http://purl.obolibrary.org/obo/")

    #onto.search(label = 'microbial susceptibility test')

    #   Grab the relevant subclasses, starting from start_id and progressing down through the hierarchy <depth> # of times

    #   If the depth is 1, only the subclasses of the initial element are pulled. 
    
    subclass_list = [start_id]
    done = []
    
    for d in range(0,int(depth)):
        
        for sc in range(len(subclass_list)):
            if subclass_list[sc] not in done:
                
                checking = subclass_list[sc]

                # Pull the subclasses and add them to the list
                curr_query_string = 'list(namespace.%s.subclasses())' % (checking)
                subclass_list.extend(eval(curr_query_string))
                
                # Format the ARO IDs: remove '.obo' prefix, convert to string
                subclass_list = [str(aro).split('.')[1] if 'obo.' in str(aro) else aro for aro in subclass_list]
                
                # Prevent the current ARO element from having its subclasses pulled again by marking it as done
                done.append(checking)
    
    #   Extract the parent term of "child" term in the subclass list, and extract the labels for each term in the subclass list
    
    hierarchy_dict = dict.fromkeys(subclass_list)
    label_list = []
    
    for term in hierarchy_dict:
        
        # Extract the labels
        query_label_string = 'namespace.%s.label' % (term)
        label_list.append(eval(query_label_string)[0])
        
        # Search for terms that are subclasses ("children") of the current <term> (the "parent")
        search_string = 'onto.search(is_a = namespace.%s)' % (term)
        children = eval(search_string)
        children = [str(aro).split('.')[1] for aro in children]
        
        # Map the current parent to any of its children that are part of the hierarchy dictionary
        for c in range(len(children)):
            child = children[c]
            
            # Since the onto.search method includes the search term or parent in the returned results, skip the parent (otherwise the parent of this term will be recorded as itself).
            # Also, skip any children that are not present in the hierarchy dictionary.
            if child != term and child in subclass_list:
                hierarchy_dict[child] = term
                
    parent_terms = list(hierarchy_dict.values())
                
    #   Store labels in a separate list

    #label_list = []
    #for i in range(len(subclass_list)):
        #query_label_string = 'namespace.%s.label' % (subclass_list[i])
        #label_list.append(eval(query_label_string)[0])

    #   Combine the lists in preparation for writing to a csv
    rows = zip(subclass_list, label_list, parent_terms)

    #   Write to csv
    file = open('aro-query.csv', 'w', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(['ARO_id', 'label', 'parent_ARO_id'])
        for row in rows:
            writer.writerow(row)

# Allow function to be called from the command line
       
if __name__ == '__main__':
    aro_query(sys.argv[1], sys.argv[2])