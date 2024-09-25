import faostat
import timeit
import os
import csv


def lands_inquire_set():
    '''
    '''
    # get the available datasets
    fd = faostat.list_datasets()

    codes = []
    for f in fd:
      sliced = f[1]
      search_term = ['Land Use', 'Annual population']
    # Check if both strings are in the joined data
      if any(term in sliced for term in search_term):
        #print(f)
        codes.append(f[0])

    #print (codes)
    print('1','__'*20)

    # # List the Parameters per Code
    # params = [faostat.list_pars(co) for co in codes]
    # for c, val in enumerate(params):
    #   print(codes[c], params[c], '\n')
    # print('3','__'*20)
    
    # 'element' param choosen for both codes:
    par = 'element'
    fv = [faostat.get_par(c, par) for c in codes]
    for c, val in enumerate(fv):
      print (codes[c], fv[c])
    #fv = faostat.get_par(code[1], par)
    #print('for ',par, ' :', fv)
    print('4','__'*20)
    
    
    # # Element values code chossen:
    c0 = [codes[0], int(fv[0]['Area'])]
    c1 = [codes[1], list(map(int,(fv[1].values())))]
       
    print ('herrrr : ', c0, '\n', c1)
        # #pars = {'element':5110}
    # pars = {'element':[511, 512, 513, 551, 561]}
    # alldata = faostat.get_data(code[1], pars=pars,
    #                     show_flags=True, 
    #                     null_values=True, 
    #                     show_notes=False, 
    #                     strval=True)
    # print(len(alldata), type(alldata))
    # return alldata
    
#elapsed_time = timeit.timeit(lands_inquire_set, number=1)
##elapsed_time = timeit.timeit(lands_inquire_df, number=1)
#print("----> Average execution time:", elapsed_time, "seconds")

def list_to_csv(data, file_path):
  """
  Converts a list of lists to a CSV file.
  """

  with open(file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(data)