from itertools import product
import itertools
import sys
import copy

def convert_to_cnf(exp):
    """
    Function to remove duplicate operations
    """
    con_list = eval(exp)
    
    after_biconditional_removal = biconditional_removal(con_list)
    after_implication_removal = implication_removal(after_biconditional_removal)
    after_push_negation_downwards = push_negation_downwards(after_implication_removal)   
    after_remove_brackets = remove_brackets(after_push_negation_downwards)
    after_distribution_or_over_and = distribution_or_over_and(after_remove_brackets)
    after_duplicates_symbol_removal = duplicates_symbol_removal(after_distribution_or_over_and)
    final_cnf = duplicate_op_removal(after_duplicates_symbol_removal)
    flag=1
    while(final_cnf[0]=="or" and flag==1):
        if (len(final_cnf[2])>1  and final_cnf[2][0]=="and"):
            final_cnf = distributiviton_recursion(final_cnf)
            flag=1
        elif (len(final_cnf[1])>1  and final_cnf[1][0]=="and"):
            final_cnf = distributiviton_recursion(final_cnf)
            flag=1
        else:
            flag=0

    after_duplicates_symbol_removal = duplicates_symbol_removal(after_distribution_or_over_and)
    final_cnf = duplicate_op_removal(after_duplicates_symbol_removal)

    return final_cnf

    #"""write result on the file"""
    #file = open("sentences_CNF.txt", "a+")
    #result_str=str(final_cnf)
    #file.write(result_str+"\n")

    #file.close()

#Function to remove bidirectional implications
def biconditional_removal(exp): 
    if(exp[0]=="iff"):
        list_1=exp[1]
        list_2=exp[2]
        exp[0]="and"
        exp[1]=["implies",list_1,list_2]
        exp[2]=["implies",list_2,list_1]

    for item in exp:
        if((len(item)>1) or isinstance(item, list)):
            biconditional_removal(item)
            
    return exp 

#Function to remove implication  
def implication_removal(exp):  
    if(exp[0]=="implies"):
        list_1=exp[1]
        exp[0]="or"
        exp[1]=["not",list_1]

    for item in exp:
        if((len(item)>1) or isinstance(item, list)):
            implication_removal(item)
            
    return exp 

#Function to remove double negations and De-Morgan's law 
def push_negation_downwards(exp): 
    if(exp[0]=="not"):
        rest=exp[1]

        if(rest[0]=="not"):
            del exp[:]
            if(len(rest[1])==1):
                exp.append(rest[1])
            else:
                for rest_ele in rest[1]:
                    exp.append(rest_ele)

                if(len(exp)>1):
                    push_negation_downwards(exp)

        elif(rest[0]=="or"):
            del exp[:]
            exp.append("and")
            for rest_ele in rest:
                if rest_ele== "or":
                    continue
                else:
                    exp.append(["not",rest_ele])

        elif(rest[0]=="and"):
            del exp[:]
            exp.append("or")
            for rest_ele in rest:
                if rest_ele== "and":
                    continue
                else:
                    exp.append(["not",rest_ele])
        
    for rest in exp:
        if(len(rest)>1 ):
            push_negation_downwards(rest)

    return exp

#Function to remove extra brackets
def remove_brackets(exp):
     i=0
     for item in exp:
        if(len(item)==1):
            temp=str(item)  
            if(len(temp)>1):
              exp[i]=temp[2]
        elif(len(item)>1):
            remove_brackets(item)
        i=i+1
     
     return exp

#Function to implement distributive law
def distribution_or_over_and(exp):
    if(exp[0]=="or"):
        if(len(exp[2])>1  and exp[2][0]=="and"):
            temp1=exp[1]
            temp2=exp[2]
            del exp[:]
            exp.append("and")
            for item1 in temp2:
                if item1=="and":
                    continue
                exp.append(["or",temp1,item1])
        elif(len(exp[1])>1  and exp[1][0]=="and"):
            temp1=exp[1]
            temp2=exp[2]
            del exp[:]
            exp.append("and")
            for item2 in temp1:
                if item2=="and":
                    continue
                exp.append(["or",item2,temp2])

    for item in exp:
        if(len(item)>1 ):
            distribution_or_over_and(item)

    return exp 

#Function to implement distributive law recursively 
def distributiviton_recursion(exp):
    if(exp[0]=="or"):
        if(len(exp[2])>1  and exp[2][0]=="and"):
            temp1=exp[1]
            temp2=exp[2]
            del exp[:]
            exp.append("and")
            for item in temp2:
                if item=="and":
                    continue
                exp.append(["or",temp1,item])
        elif(len(exp[1])>1  and exp[1][0]=="and"):
            temp1=exp[1]
            temp2=exp[2]
            del exp[:]
            exp.append("and")
            for item in temp1:
                if item=="and":
                    continue
                exp.append(["or",item,temp2])

    return exp

#Function to remove duplicate symbols          
def duplicates_symbol_removal(exp):
    temp_exp=copy.copy(exp)
    if((temp_exp[0]=="or") or (temp_exp[0]=="and")):
        for i1,item1 in enumerate(temp_exp):
            for i2 in xrange(i1 + 1, len(temp_exp)):
                if(isinstance(temp_exp[i1], list) and len(temp_exp[i1]) ==1):
                    exp[i1]=remove_brackets(exp[i1])
                if(isinstance(temp_exp[i2], list) and len(temp_exp[i2]) ==1):
                    temp=temp_exp[i2][0]
                    if(temp==temp_exp[i1]):
                        del exp[i2]
                        break
                if(isinstance(temp_exp[i1], list) and isinstance(temp_exp[i2], list)):
                    temp1=temp_exp[i1]
                    temp2=temp_exp[i2]
                    if(sorted(temp1) == sorted(temp2)):
                        del exp[i2]
                        break
                if(temp_exp[i1] == temp_exp[i2]):
                    del exp[i2]
        
    for item in exp:
        if((len(item)>1) or isinstance(item, list)):
            duplicates_symbol_removal(item)

    if((exp[0] == "or" or exp[0] == "and") and len(exp) == 2):
            exp=duplicate_op_removal(exp)
    exp=remove_brackets(exp)    
    return exp 

#Function to remove duplicate operations
def duplicate_op_removal(exp):
    if(exp[0]=="or" and len(exp) > 2):
        rest1=exp[1]
        rest2=exp[2]
        if(rest1[0] == "or" and rest2[0] == "or"):
            del exp[:]
            exp.append("or")
            for i1 in xrange( 1, len(rest1)):
                    exp.append(rest1[i1])
            for i2 in xrange( 1, len(rest2)):
                    exp.append(rest2[i2])
        if(rest1[0] == "or" and rest2[0] != "or"):
            del exp[:]
            exp.append("or")
            for i2 in xrange( 1, len(rest1)):
                    exp.append(rest1[i2])
            exp.append(rest2)
        if(rest2[0] == "or" and rest1[0] != "or"):
            del exp[:]
            exp.append("or")
            exp.append(rest1)
            for i2 in xrange( 1, len(rest2)):
                    exp.append(rest2[i2])
    if(exp[0]=="and" and len(exp) > 2):
        rest1=exp[1]
        rest2=exp[2]
        if(rest1[0] == "and" and rest2[0] == "and"):
            del exp[:]
            exp.append("and")
            for i1 in xrange( 1, len(rest1)):
                    exp.append(rest1[i1])
            for i2 in xrange( 1, len(rest2)):
                    exp.append(rest2[i2])
        if(rest1[0] == "and" and rest2[0] != "and"):
            del exp[:]
            exp.append("and")
            for i2 in xrange( 1, len(rest1)):
                    exp.append(rest1[i2])
            exp.append(rest2)
        if(rest2[0] == "and" and rest1[0] != "and"):
            del exp[:]
            exp.append("and")
            exp.append(rest1)
            for i2 in xrange( 1, len(rest2)):
                    exp.append(rest2[i2])
            
    if((exp[0] == "or" or exp[0] == "and") and len(exp) == 2):
        temp=exp[1]
        del exp[:]
        exp.append(temp)

    for item in exp:
        if((len(item)>1) or isinstance(item, list)):
            duplicate_op_removal(item)
    
    exp=duplicates_symbol_removal(exp)      
    return exp 

""" READ THE INPUT FILE """

end =convert_to_cnf('["implies", ["not", "A"], ["not", ["and", "B", ["not", ["or", "C", ["not", ["and", "D", "E"]]]]]]]')
print(end)

#inputFile = open(sys.argv[2])
#inputFile = open(r"D:\Vivek\USC\AI\Python\Assignment2\test.txt",'r')

#conf=0
#line_number=0
#final_list=[]
#for line in inputFile:
#    if conf==0:
#        spl = line.strip().split(' ')
#        line_number=int(spl[0])
#        file = open("sentences_CNF.txt", "w")
#        file.close()
#        conf=1
#    else:
#        convert_to_cnf(line)
        
#inputFile.close()  
