# import pandas as pd
# import csv
# #with open('test.csv') as file:
#  #   csv_reader_object = csv.reader(file)
#   #  for row in csv_reader_object:
#    #     print("CSV row: {0}".format(row))
# count=0
# count1=0
# #for row in csv_f:
#  # print (row)

# df = pd.read_csv('isHand.csv')
# # df.to_csv('output.csv', index=False)
# # f = open('output.csv')
# csv_f = df.reader(f)
# for row in csv_f:
#   if(row[1]=='index1'):
#     count=count+1
#   elif(row[1]=='index3'):
#   	count1=count1+1
# print(count)
# print(count1)

import pandas as pd

df = pd.read_csv('isHand.csv')
s = df['Gesture'].value_counts().rename('Total_Gesture')
s.to_csv('test_hand.csv')
df1 = pd.read_csv('test_Hand.csv')
df1.columns.values[0] = 'index'
df1.to_csv('test_hand.csv',index=False)
print(s)
