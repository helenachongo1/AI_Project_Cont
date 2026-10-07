
#Opening Files in Python
file1=open(r"C:\Users\Acer\Downloads\ict.txt")

#Working in Read mode
#f1 = open(r"C:\Users\Acer\Downloads\ict.txt")
#print(f1.readlines())
# This will print every line one by one in the file
#for each in f1:
#    print (each)

#print (f1.read())

#data = f1.read() 
#print(data)

#print (f1.read(5))

#with open(r"C:\Users\Acer\Downloads\ict.txt",'r') as file:
    #data = file.readlines()
    #for line in data:
       # word = line.split()
        #print (word)

'''file = open("ict1.txt",'w')
file.write("ICT ICT ICT \n")
file.write("ICT ICT ICT ICT ICT")
file.close()

with open("file.txt", "w") as f: 
    f.write("Hello World!!!") 
    f.close()
    
file = open("ict1.txt",'w')
file.write("ICT ICT ICT \n")
file.write("ICT ICT ICT ICT ICT")
file.close()

file1=open("ict1.txt",'a')
file1.write("ICT Enhniring")
file1.close()

with open("file.txt", "w") as f: 
    f.write("Hello World!!!") 
    f.close()
    
file = open("ict1.txt",'a')
file.write("\n Department Department")
file.close()'''

#with open(r'C:\Users\Acer\Downloads\a.tif', 'rb') as file:
  #  binary_data = file.read()
  #  print(binary_data)
  
#with open(r'C:\Users\Acer\Downloads\a.tif', 'rb') as file:
 #   binary_data = file.read()   
#with open("c.tif", 'wb') as f:
#    f.write(binary_data)
#    f.close()'''

#import csv    
#with open('data-1.csv', 'r') as file:
#    reader = csv.reader(file)
#    for row in reader:
#        print(row)

#with open('output.csv', 'w', newline='') as file:
 #   writer = csv.writer(file)
#    writer.writerow(['Name', 'Subject', 'Mark'])
 #   writer.writerow(['Aansh', 'PWP', 9])
 #   writer.writerow(['Ashutosh', 'PWP', 10])
 #   file.close()
 
'''try:
    with open('data_1.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
except FileNotFoundError:
    print("File not found")'''
    
    
#Q1   
#c_line=0
#c_word=0
#c_char=0
   
#with open(r"C:\Users\Acer\Downloads\ict.txt") as f1:
    #for i in f1:
        #c_line+=1
        
        #word='Y'
        #for wr in i:
         #   if(wr != ' ' and word == 'Y'):
        #        c_word+=1
       #         
      #          word='N'
     #       
    #        for jr in wr:
   #             if(jr !="" and jr !="\n"):
  #                  c_char+=1 
 #                   
#print("Number of lines:",c_line)
#print("Number of words:",c_word)
#print("Number of characters:",c_char)

#Q2

#with open(r"C:\Users\Acer\Downloads\ict.txt") as f1:
 # f2=f1.readlines()
  #for e in f2:
   #   print(e)
#print("\nList:")
#f2=[x.strip() for x in f2]
#print(f2)

#Q3c.	Write a Python program to read data from a CSV file data.csv and print each row to the console
#import csv

#import pandas as pd
#df = pd.read_csv(r'C:\Users\Acer\Downloads\data_1.csv')
#print(df)

#with open(r'C:\Users\Acer\Downloads\data_1.csv') as file:
#   rd=csv.reader(file)
#   for i in rd:
#       print(i)

#Q4
#d1=d2=" "

#with open(r"C:\Users\Acer\Downloads\ict.txt") as f1:
#    d1=f1.read()
    
#with open(r"C:\Users\Acer\Downloads\ict1.txt") as f1:
#    d2=f1.read()
    
#d1+="\n"
#d1+=d2

#with open('d3.txt','w') as f1:
#    f1.write(d1)
#    f1.close()
    
#with open('d3.txt','r') as f1:
#    print(f1.readlines())
 
#import csv
#with open(r'C:\Users\Acer\Downloads\data_1.csv') as file:
 #   reader = csv.reader(file)
  #  for row in reader:
   #     print(row)


                
                
                
    











