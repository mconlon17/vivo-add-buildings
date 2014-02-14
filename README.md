# Add university buildings to VIVO

To add buildings to VIVO we wrote a short python program to
read a CSV of university buildings, each with a name and a 
building number, and compare to the university buildings found
in VIVO.  

Information about university buildings at the University of 
Florida (UF) is managed in an enterprise system.  Each building
has been assigned a unique number (the building number).  

#Steps to implement

1. In VIVO, we added ufVivo:buildingNumber to the ontology.
1. In VIVO we manually added the building number to each of the 
university buildings already in VIVO.
1. We downloaded building data and made a CSV file of the 
university buildings for the main campus only.  See
main-campus.csv -- 950 buildings on the main UF campus in
Gainesville, Florida.
1.  We ran the python script, checked the RDF files and uploaded
the files to VIVO.
1. We went in to VIVO and checked the results.  Several of the
buildings that had been hand entered were renamed by the script --
each building in VIVO now has its full official name.

# Safe to re-run

The script is designed to be safe to re-rerun.  It identifies
three cases:
    1. The building is in VIVO and not in the building file. These
	are counted and reported.  No action is taken.
	1. The building is in VIVO and is in the building file.  The
	building file is considered authoritative -- the name of the
	building in the building file replaces the name in VIVO.
	1.  The building is not in VIVO and is in the UF building
	file.  These buildings are added to VIVO.
	
# To maintain the building data in VIVO

1.  Create an updated building CSV file
1.  Run the script
1.  Upload the resulting RDF