ZER = 0b01 #0
ONE = 0b10 #1
PHI = 0b11 #phi
DNC = 0b00 #-
#or to get correct result

#cover in [[cube1 minterms], [cube2 minterms],...]
def iterated_consensus(cover): #note cover is a list of cubes, each cube being a list of  0,1,-
    change = True
    cover = scc_n2(cover) #scc n2 compares all covers against each other
    while(change): #while the cover is still changing in the loop
        old_cover = cover
        i = 0
        #scc_n2(cover)
        while(i < len(cover)-1): #i keeps track of first vector to do consensus with
            j=i+1 #start one above 1
            while((j<len(cover)) & (j>i)): # j keeps track of second vector to do consensus with
                new_i_flag = False
                [cons, is_valid] = consensus(cover[i],cover[j])

                #Testing
                #print(is_valid)
                #if(is_valid): print_var(cons)
                #print("All Covers:")
                #x=0
                #while (x < len(cover)):
                #    print_var(cover[x])
                #    print("\n")
                #    x+=1
                #TestEnd

                if(is_valid):
                    cover.append(cons)
                    #SCC
                    #need to do Single Cube Containment, implement this in n time, hence why not using scc_n2
                    #n time as we only need to compare previous covers with new cover given by consensus
                    end = len(cover)-1
                    k = 0;
                    while(k < end):
                        and_cov_k_end = []
                        for x in range(len(cover[k])): #and each term in cover[k] and cover[end]
                            and_cov_k_end.append(cover[k][x] & cover[end][x])

                        if(and_cov_k_end == cover[k]): 
                            #cover[end] is contained in cover[k], delete cover[end] and break
                            cover.pop(end)
                            break

                        if(and_cov_k_end == cover[end]):
                            #cover[k] is contained in cover[end], delete cover[k], adjust i, j, and k accordingly
                            cover.pop(k)

                            if(k == i): #if cover[i] is deleted, let k loop finish,
                                #no need to continue j loop doing consensus w cover[i], need to get out to i loop
                                #and start over with new i from beginning of j loop
                                new_i_flag = True
    
                            #adjust i and j accordingly
                            if(k <= j): 
                                j-=1 # if k precedes or is j, decrement j
                            if(k <= i): 
                                i-=1 #if k precedes or is i, decrement i

                            k-=1 #keep k the same (later increase does nothing)
                            end-=1 #decrease end if k is popped 

                        k+=1
                    if(new_i_flag):
                        #i-=1 #make i stay the same value despite increase at end of loop
                        break
                j+=1
            i+=1
        change = (old_cover != cover) #breaks when no change occurs

    x=0
    cover = scc_n2(cover) 
    while (x < len(cover)):
        print_var(cover[x])
        print("\n")
        x+=1
    return
    
    


def scc_n2(cover): #note cover is a list of cubes, each cube being a list of  0,1,-
    #i think can be implemented by bitwise & the cubes, 
    #if the result is the same as one of the inputs, that input contains the other
    #keep original cover if they are the same cover
    i = 0
    while(i < len(cover)): #looping all cubes against each other
        j = i+1
        while(j < len(cover)):
            k=0
            and_cov = []
            for k in range(len(cover[i])):
                and_cov.append(cover[i][k] & cover[j][k])
            if(and_cov == cover[i]):
                cover.pop(j)
                j-=1 # delete cover[j] but keep j pointer the same (new value) (stays same since j+=1 for next loop)
            if(and_cov == cover[j]):
                cover.pop(i)
                i-=1 #keep i the same after loop (i-1+1) break loop to start on new cover[i] value
                break
            j+=1
        i+=1
    return cover 

    #Looking to delete cubes that are contained in another cube
    # a = - 1 0 1 = 00 10 01 10 
    # b = 1 1 0 1 = 10 10 01 10
    # c = 0 1 0 1 = 01 10 01 10

    # - - // 00 00 = 00 contained
    # - 0 // 00 01 = 00 contained
    # - 1 // 00 10 = 00 contained
    # 0 0 // 01 01 = 01 contained
    # 0 1 // 01 10 = 00 not contained
    # 1 1 // 10 10 = 10 contained
    # note that bitwise and, and checking if output is equal to an input gives the input that contains the other

    # a&b = 00 10 01 10
    # a&c = 00 10 01 10
    # b&c = 00 10 01 10 -> note this wouldnt be able to bypass steps as we need to check for #s of phi

    

    
def consensus(f1,f2): #return the consensus and validity that consensus exists
    f_isect = intersect(f1,f2)
    #print(f_isect)
    phi_count = f_isect.count(PHI)
    if(phi_count > 1): #DNE
        result = None, False
    elif(phi_count == 1): #if == 1 replace PHI with DNC
        result = cons_phi_replace(f_isect), True
    elif(phi_count == 0): #if == 0 return the intersect as is
        result = f_isect, True
    else:
        print('ERR: PHI_COUNT')
        result = None, False
    return result


def cons_phi_replace(f1): #replaces PHI with DNC
    i = 0;
    result = []
    while(i < len(f1)):
        if(f1[i] == PHI): result.append(DNC)
        else: result.append(f1[i])
        i+=1
    return (result)


def intersect(f1,f2): #assuming passing lists with 2 bits per element
    #0   = 01
    #1   = 10
    #Phi = 00
    #-   = 11
    if(len(f1) != len(f2)): 
        print('ERR: Intersect Mismatch') 
        return()
    else:
        i = 0;
        result = []
        while(i < len(f1)):
            result.append(f1[i] | f2[i]) # bitwise ors the two bits w two bits
            i+=1
        return (result)


def print_var(f1):
    i = 0
    while(i < len(f1)):
        if(f1[i] == ZER):
            print('ZER ', end="")
        elif (f1[i] == ONE):
            print('ONE ', end="")
        elif (f1[i] == PHI):
            print('PHI ', end="")
        elif (f1[i] == DNC):
            print('DNC ', end="")
        else: print('ERR ', end="")
        i+=1


#a = [DNC, ZER, ZER]
#b = [ONE, ONE, DNC]
#c = [a,b]

print("Test 1:")
a = [DNC, ZER, ZER, DNC]
b = [ONE, ONE, ONE, DNC]
c = [DNC, ZER, ONE, ZER]
d = [ONE, DNC, ZER, ONE]    
cov = [a, b, c, d]
iterated_consensus(cov)
#expected output:
#[- 0 0 -]
#[- 0 - 0]
#[1 - 0 1]
#[1 - 1 0]
#[1 1 1 -]
#[1 1 - 1]

print("Test 2:")
e = [ZER, DNC, DNC, ONE]
f = [DNC, ZER, ZER, DNC]
g = [ONE, ONE, DNC, ZER]
cov2 = [e,f,g]
iterated_consensus(cov2)
#expected output: 
#[0 - - 1]
#[- 0 0 -]
#[1 1 - 0]
#[1 - 0 0]

print("Test 3:")
h = [ONE, ONE, DNC]
i = [ZER, DNC, ONE]
j = [DNC, ONE, ONE]
cov3 = [h, i, j]
iterated_consensus(cov3)
#expected output: 
#[1 1 -]
#[0 - 1]
#[- 1 1]

print("Test 4:")
k = [ONE, ONE, ONE]
cov4 = [h, i, j, k]
iterated_consensus(cov4)
#expected output: 
#[1 1 -]
#[0 - 1]
#[- 1 1]

print("Test 5:")
l = [ONE, ONE, ONE]
m = [ZER, ONE, ONE]
cov5 = [l,m]
iterated_consensus(cov5)
#expected output: 
#[- 1 1]

#iterated_consensus(cov)

#print_var(consensus(a,b))

#print_cons(consensus(ZER,ONE))

    
    
