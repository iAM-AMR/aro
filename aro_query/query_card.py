from owlready2 import *
import csv
import sys

def query_card(start_id=sys.argv[1], depth=sys.argv[2]):

    #  Load the ontology

    #onto = get_ontology("file://C:/Users/CHPHILLI/Documents/CARD/card-ontology/aro.owl").load()
    onto = get_ontology("https://raw.githubusercontent.com/arpcard/aro/master/aro.owl").load()

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
    
    #   Store labels in a separate list

    label_list = []
    for i in range(len(subclass_list)):
        query_label_string = 'namespace.%s.label' % (subclass_list[i])
        label_list.append(eval(query_label_string)[0])

    #   Combine two lists in preparation for writing to a csv
    rows = zip(subclass_list, label_list)

    #   Write to csv
    file = open('card-query.csv', 'w', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(['ARO_id', 'label'])
        for row in rows:
            writer.writerow(row)

# Allow function to be called from the command line
       
if __name__ == '__main__':
    query_card(sys.argv[1], sys.argv[2])