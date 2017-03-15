import os, urllib, json, csv

#File parameters
location = "C:\\Projects\\JSON"
csv_file_input = "C:\\Projects\\AGOLData\\AGOLCat.csv"
csv_file_output = "C:\\Projects\\AGOLData\\ItemTitles.csv"
item_details = "C:\\Projects\\AGOLData\\ItemOpLayers_test.csv"


#AGOL User parameters
# replace <<PLACEHOLDERS>> in next three lines with your information
# e.g., portal = 'https://www.arcgis.com', username = 'jdoe1234', password = 'mypassword'
portal = 'https://hrsd.maps.arcgis.com'
username = 'cmccormick_HRSD'
password = 'drytrak903'

#--------------------------------------Delete File----------------------------------------------------------
try:
    os.remove(item_details)
    print "Deleted " + item_details + ".  Beginning script."
except:
    print item_details + " did not exist.  Beginning script."

#--------------------------------------list of items in AGOL----------------------------------------------------------
data = [] #Buffer list
with open(csv_file_input, "rb") as the_file:
	reader = csv.reader(the_file, delimiter=",")
	for row in reader:

		try:
			new_row = row[0], row[5]
			#Basically ´write the rows to a list
			data.append(new_row)
		except IndexError as e:
			print e
			pass

	with open(csv_file_output, "wb") as to_file:
		writer = csv.writer(to_file, delimiter=",")
		for new_row in data:
			writer.writerow(new_row)

##for stuff in data:
##    print stuff[0]
#--------------------------------------CSV Row to Dictionary----------------------------------------------------------
with open(csv_file_input) as f:
    a1 = [row["id"] for row in csv.DictReader(f)]
###print a1

#-----------------------------------------------Generate Table of Items with URLS-----------------------------------------------------
for item in a1:
    print item
    # Generate token to get item info
    # Generate Token Example
    parameters = urllib.urlencode({'username':username,'password':password,'client':'requestip','f':'json'})
    request = portal + '/sharing/rest/generateToken?'
    response = json.loads(urllib.urlopen(request, parameters).read())
    #print response
    token = response['token']
    #return parameters
    parameters2 = urllib.urlencode({'title' : 'PYTHON', 'token': token, 'f': 'json'})
    request2 = portal + '/sharing/content/items/' + item + '/data?' + parameters2
    itemDataReq = urllib.urlopen(request2).read()
    itemString = str(itemDataReq)
    jsonFile = open(location + "\\" + item + ".json", 'w')
    print >> jsonFile, itemString
    jsonFile.close()

location = "C:\\Projects\\JSON\\"
addrow = open(item_details, 'a')
print >> addrow, "id,title,url"
addrow.close()
for dirpath, dirname, filename in os.walk(location ,topdown=True, onerror=None, followlinks=True):
    print filename

    for file in filename:
        print file
        strfile = file[:-5]
        try:
            log = open(item_details,'a')
            file = json.loads(open(str(dirpath) + str(file)).read())
#print str(file)
#print file
            for url in file['operationalLayers']:
                try:
                    print url['url']
                    print >> log, strfile + "," + url['title'] + "," + url['url']
                except:
                    pass
            log.close()
        except:

            print "No operational layers"



