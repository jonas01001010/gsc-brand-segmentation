import argparse, sys, os, json, datetime, time, csv, codecs, io, pandas
from googleapiclient import sample_tools
from multiprocessing import Process

# Takes data from the line inserted in cmd
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('property_uri', type=str,
                       help=('Site or app URI to query data for (including '
                             'trailing slash).'))
argparser.add_argument('start_date', type=str,
                       help=('Start date of the requested date range in '
                             'YYYY-MM-DD format.'))
argparser.add_argument('end_date', type=str,
                       help=('End date of the requested date range in '
                             'YYYY-MM-DD format.'))


def main(argv):
  service, flags = sample_tools.init(
      argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser],
      scope='https://www.googleapis.com/auth/webmasters.readonly')

  # First extract the non brand queries, and send a second request for all queries
  request1 = {
      'startDate': flags.start_date,
      'endDate': flags.end_date,
      'dimensions': ['page'],
      'dimensionFilterGroups': [{
          'filters': [{
              'dimension': 'query',
              'operator': 'notContains',
              'expression': 'brand pattern 1'
           }, {
              'dimension': 'query',
              'operator': 'notContains',
              'expression': 'brand pattern 2'
           }, {
              'dimension': 'query',
              'operator': 'notContains',
              'expression': 'brand pattern 3'
           }, {
              'dimension': 'query',
              'operator': 'notContains',
              'expression': 'brand pattern 4'
          }, {
              'dimension': 'query',
              'operator': 'notContains',
              'expression': 'brand pattern 5'
          }, {
              'dimension': 'query',
              'operator': 'notContains',
              'expression': 'brand pattern 6'
          }, {
              'dimension': 'query',
              'operator': 'notContains',
              'expression': 'brand pattern 7'   
              }]
          }],          
      'rowLimit': 5000
  }
  response1 = execute_request(service, flags.property_uri, request1)
  print_table1(response1, 'Nnonbrand file generated')

  request2 = {
      'startDate': flags.start_date,
      'endDate': flags.end_date,
      'dimensions': ['page'],
      'rowLimit': 5000
  }
  response2 = execute_request(service, flags.property_uri, request2)
  print_table2(response2, 'All queries file generated')

 
def execute_request(service, property_uri, request1):
  """Request data in GSC
  """
  return service.searchanalytics().query(
      siteUrl=property_uri, body=request1).execute()


def print_table1(response1, title):
  """Prints out a response table for the first request - non brand queries
  Each row contains key(s), clicks, impressions, CTR, and average position.
  """
  print(title + '-')

  if 'rows' not in response1:
    print('Empty response')
    return

  rows = response1['rows']
  row_format = '{:<20}' + '{:>20}' * 4
   # print row_format.format('Keys', 'Clicks', 'Impressions', 'CTR', 'Position')
  f = open("./Top_NB_Pages.csv", 'wt', newline='')
  writer = csv.writer(f, delimiter='|')
  writer.writerow( ('query', 'impressions', 'clicks', 'avg_position') )
  for row in rows:
    keys = ''
    # Keys are returned only if one or more dimensions are requested.
    if 'keys' in row:
      keys = u','.join(row['keys'])
    # print row_format.format(
     #   keys, row['clicks'], row['impressions'], row['ctr'], row['position'])
    writer.writerow( (keys, row['impressions'], row['clicks'], row['position']) )
  f.close()

def print_table2(response2, title):
  """Prints out a response table for the second request - all queries
  Each row contains key(s), clicks, impressions, CTR, and average position.
  """
  print(title + '-')

  if 'rows' not in response2:
    print('Empty response')
    return

  rows = response2['rows']
  row_format = '{:<20}' + '{:>20}' * 4
   # print row_format.format('Keys', 'Clicks', 'Impressions', 'CTR', 'Position')
  f2 = open("./Top_all_Pages.csv", 'wt', newline='')
  writer = csv.writer(f2, delimiter='|')
  writer.writerow( ('query', 'impressions', 'clicks', 'avg_position') )
  for row in rows:
    keys = ''
    # Keys are returned only if one or more dimensions are requested.
    if 'keys' in row:
      keys = u','.join(row['keys'])
    # print row_format.format(
     #   keys, row['clicks'], row['impressions'], row['ctr'], row['position'])
    writer.writerow( (keys, row['impressions'], row['clicks'], row['position']) )
  f2.close()

    # 2 CSV files are created. I am merging them into a new and final CSV file
def printpandas():
    with open('Top_all_Pages.csv','r') as lookuplist:
        with open('Top_NB_Pages.csv', "r") as csvinput:
           with open('VlookupOut.csv','wt', newline='', encoding='utf-8') as output:

              reader = csv.reader(lookuplist, delimiter='|')
              reader2 = csv.reader(csvinput, delimiter='|')
              writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_NONE)
       # both files are imported at this stage                         

              for i in reader2:
                  for xl in reader:
                    if  i[:1] == xl[:1]:
                          i.append("".join(xl[2:3]))
                          writer.writerow(i)
                  lookuplist.seek(0)
    
        # it is the pandas' of vlookup: if content of column 1 in all queries matches column 1 of non brand queries
        # then right content on non brand file followed by the columns 4 (0,1,2,3) of all queries file
        # the file non brand has the 4 same cilumns and an additional one with all queries clicks


        # in that file I  used the new temp file which has 5 columns
        # I convert the data in numbers for clicks
        # therefore I can define 2 functions: %nonbrand(NBclicks/ALLclcicks) and %brand (1-%nonbrand)
        # I insert the 2 calculated columns after the 5 temp ones, and rename them
        # I generate a csv file with the 7 columns
    df=pandas.read_csv('VlookupOut.csv', delimiter=',', converters={'clicks':float})
    nonbrand = df['clicks'] / df['clicks.1']
    df.insert(5,'%nonbrand',nonbrand)
    brand = 1- nonbrand
    df.insert(6,'%brand',brand)
    df = df.rename(columns={'query': 'page','impressions':'NB impressions','clicks': 'NBclicks', 'avg_position': 'NB avg_position', 'clicks.1': 'All clicks'})
    df = df.drop(df[df.NBclicks == 0].index) # delete rows when they have no non brand clicks, avoid to divide by 0
    df.to_csv('Brand segmentation per page.csv')
    print("File with brand % created")

    #function to exectute functions from cmd and in the right order

if (__name__ == '__main__'):
  main(sys.argv)
  p1 = Process(target = printpandas)
  p1.start()
