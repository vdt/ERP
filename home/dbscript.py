import csv
from users.models import *
from django.contrib.auth.models import User, Group
from department.models import *
from django.shortcuts import HttpResponseRedirect
import string
import random
from time import sleep
from erp.dashboard.create_test_data import create_group, create_user, parse_user_info_list, create_depts

IN_FILE="home/details-min-3.csv"
OUT_FILE="home/lookup-3.csv"

# Write each entry to the CSV
def writeout(writer, dept, group, username, email, password, nickname, name, chennai_number, summer_number, summer_stay, hostel, roomno):
    writer.writerow([dept, group, username, email, password, nickname, name, chennai_number, summer_number, summer_stay, hostel, roomno])

def create_users (users_file_name = 'lookup.csv'):
    """
    Get user details from users_file_name.
    Create users if they doesn't exist.
    """
    users_file = open (users_file_name, 'r')
    for line in users_file:
        # user_fields = line.split ()
        user_data_list = parse_user_info_list (line.split (','))
        print user_data_list
        create_user (*user_data_list)
    users_file.close ()
    print 'All users created successfully.'
    
# Generate a lowercase+digit sequence of SIZE 
def pass_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def parse_csv(details,writer):
    ''' 
    Reads the CSV line by line and parses it based on length.
    This is not very elegant and changing the format of the CSV
    will force changes in code. Please look at home/details.csv
    for format.
    '''
    line=details.next()
    def parse_line(line,dept=None):
        # This row will then mean a new department.
        if len(line)==2:
            dept=line[0]
            try:
                line=details.next()
                save_user(line,dept)
            except:
                pass
        else:
            save_user(line,dept)
    # Save the details of user to DB and call csvwrite        
    def save_user(line,dept):
        # Very rough and ugly name parser.
        try:  
            firstname=line[0].rsplit(' ',1)[0]
            lastname=line[0].rsplit(' ',1)[1]
        except:
            firstname=line[0]
            lastname=''
        email=line[7]
        if (email==''):
            email= line[2].lower()+"@smail.iitm.ac.in"
        print 'Firstname:', firstname, '\nLastname:', lastname, '\nUsername:', line[3], '\nEmail:', email, '\nDept:', dept
        writeout(writer, dept, 'Coords', line[2].lower(), email, pass_generator(size=8), line[1], line[0], line[5], line[6], '', line[4], line[3])

        try:
            # Incase end of file? Very ugly but I can't find any other way
            #print "sleeping"
            #sleep(1)
            line=details.next()
            parse_line(line,dept)
        except:
            pass 
    return parse_line(line)

# Open one to read and one to write    
def write_into_db(request):
    details=csv.reader(open(IN_FILE, 'rb'))
    outfile=open(OUT_FILE, 'wb')
    writer = csv.writer(outfile)
    # Create group if already not there
    create_group('Coords')
    parse_csv(details,writer)  
    # only closing saves the csv. NOTE: breaking out of the process midway will not save the passes.
    outfile.close()
    create_depts ()
    create_users (users_file_name = OUT_FILE)    
    return HttpResponseRedirect('/')
