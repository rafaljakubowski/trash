#!/usr/bin/python
import numpy as np
do_chain=0

'''
dirty style variables definitio; why use command line? 
'''
war=['wt','l55p','v30m']
chains=['TTRA','TTRB','TTRC','TTRD']
pat='/home/rafal/doktorat/ttr_con/all/'

'''
function extracts the right piece of data from EUCB CONTACT.log
more info on EUCB: wiki.econ.uoi.gr/wiki/index.php/Eucb
'''
def suck_data(inf):
  start=0
  stop=0
  res=[]
  for i in inf:
    if "#SYNOPSIS" in i:
      stop=1
    if stop==1:
      return res
    if start==2:
      res.append(i.split())
    if start==1:
      start=2
    if "#STATISTICS" in i:
      start=1


'''
three methods below should be merged into parametrized one, but...
'''
def count_vdw(inp):
  col_s=2
  col_md=5
  s=0
  md=0
  s_z=0
  md_z=0
  for i in inp:   
    s=s+int(i[col_s])
    if int(i[col_s])!=0:
      s_z=s_z+1
    if int(i[col_md])!=0:
      md_z=md_z+1
    md=md+int(i[col_md])
  return s, md, s_z, md_z

def count_hb(inp):
  col_s=3
  col_md=6
  s=0
  s_z=0
  md=0
  md_z=0
  for i in inp:
      s=s+int(i[col_s])
      if int(i[col_s])!=0:
        s_z=s_z+1
      md=md+int(i[col_md])
      if int(i[col_md])!=0:
        md_z=md_z+1
  return s, md, s_z, md_z

def count_sb(inp):
  col_s=4
  col_md=7
  s=0
  md=0
  s_z=0
  md_z=0
  for i in inp:
    s=s+int(i[col_s])
    if int(i[col_s])!=0:
          s_z=s_z+1
    if int(i[col_md])!=0:
      md_z=md_z+1
    md=md+int(i[col_md])
  return s, md, s_z, md_z

'''
function finds distinct and common interaction sets
'''

def do_comparison(triples, name="TTRA"):
  distincts=[]
  common=[]
  print len(triples[0])
  print len(triples[1])
  print len(triples[2])
  #we need only one loop to detect all commons!
  s=triples[0]


  dist=[]
  a=[]
  for i in s:
    z=0
    for j in range(1,3):
      #print j
      for jj in triples[j]:
        #print jj
        if i[0]==jj[0] and i[1]==jj[1]:
          z=z+1
          #print z
      if z==2:
         #print i,jj
         common.append(i)
      if z==0:
        a.append(i)
  
  dist.append(a)

  #crappy way...
  a=[]
  s=triples[1]
  for i in s:
      z=0
      for j in (0,2):
                #print j
       for jj in triples[j]:
                              #print jj
         if i[0]==jj[0] and i[1]==jj[1]:
             z=z+1
                                                          #print z
       if z==0:
            a.append(i)
  dist.append(a)                                                                                                

  a=[]
  s=triples[2]
  for i in s:
      z=0
      for j in (0,1):
                #print j
       for jj in triples[j]:
                              #print jj
         if i[0]==jj[0] and i[1]==jj[1]:
             z=z+1
                                                          #print z
       if z==0:
            a.append(i)
  dist.append(a)                                                                                                
  
  
  dd=[]
  a=[]  
  s=triples[0]
  
  for i in s:
      for jj in triples[1]:
	if i[0]==jj[0] and i[1]==jj[1]:
	     a.append(i)

  dd.append(a)
  a=[]
  s=triples[0]
  z=0
  for i in s:
      z=z+1
      for jj in triples[2]:
         if i[0]==jj[0] and i[1]==jj[1]:
	     #print i, jj,z
	     a.append(i)
  dd.append(a)

#parami
  print "wsp: "+str(len(dd[0]))
  print "wsp: "+str(len(dd[1]))
  print "wsp: "+str(len(dd))

  print len(dist[0])
  print len(dist[1])
  print len(dist[2])
#  print dist[1]
  ope=open(name+"_dist.dat",'w')
  ope1=open(name+"_hbonds_dist.dat",'w')
  ope2=open(name+"_sb_dist.dat",'w')	
  ope3=open(name+"_pure_list.dat",'w')
  ope4=open(name+"_all_pure_list.dat",'w')
  ll=0
  l1=0
  for lk in dist[1]:
#	print lk
		

	a=lk[0].split(':')
	b=lk[1].split(':')
	ope.write("(segname "+str((a[0]))+" and (resid "+str(int(a[1]))+" or resid "+b[1]+")) ")
        ope4.write(str(lk)+"\n")
	                        
#	print lk[6]	
	if int(lk[6])>0:
			ope1.write("(segname "+str((a[0]))+" and (resid "+str(int(a[1]))+" or resid "+b[1]+")) or ")
			#ope4.write(str(lk)+"\n")
                        ope3.write(str(lk)+"\n")
			                        
			l1=l1+1
	if int(lk[7])>0:
			ope2.write("(segname "+str((a[0]))+" and (resid "+str(int(a[1]))+" or resid "+b[1]+")) or ")
			#ope3.write(str(lk)+"\n")
			l1=l1+1		
	
	ll=ll+1
	if ll<len(dist[1]):
		ope.write('or ')
  ope.close()
  ope1.close()
  p1=open('wt_inter_common.dat','w')
  p1a=open('wt_inter_hbonds_common.dat','w')
  for i in dd[0]:
    p1.write(str(i)+"\n")
    if int(i[6])>0:
      p1a.write(str(i)+'\n')
  p1a.close()
  p1.close()

  p2=open("wt_inter_dist.dat",'w')
  p2a=open("wt_inter_bonds_dist.dat",'w')
  for i in dist[0]:
    p2.write(str(i)+"\n")
    if int(i[6])>0:
      p2a.write(str(i)+'\n')
    
  p2.close()
  p2a.close()

#  print len(common)
'''
main jobs below
'''
r=open('grube_inter_in.dat','w')                      
files=[]
#do_chain=j

for j in range(0,len(war)):
#  print "\n\n"+chains[j]
 # r.write("\n\n"+chains[j]+'\n\n')
  
  files.append(open(pat+war[j]+"_contact.log",'r'))
print len(files)
org=[]
for i in files:
   org.append(suck_data(i))
print len(org)  
#for i in 
do_comparison(org,"overall")

  
#  print "\n"
for i in org:
      print "totel: "+str(len(i))
      r.write('total: '+str(len(i))+"\n")
      aa,bb, aa1, bb1=count_vdw(i)
      
      print "vdw: "+str(aa)+" "+str(bb)+" "+str(aa1)+" "+str(bb1)
      
      r.write("vdw: "+str(aa)+" "+str(bb)+" "+str(aa1)+" "+str(bb1)+'\n')
      cc,dd,cc1,dd1=count_hb(i)
      print "hb: "+str(cc)+" "+str(dd)+" "+str(cc1)+" "+str(dd1)
      r.write("hb: "+str(cc)+" "+str(dd)+" "+str(cc1)+" "+str(dd1)+'\n')
      ee,ff,ee1,ff1=count_sb(i)
      print "sb: "+str(ee)+" "+str(ff)+" "+str(ee1)+" "+str(ff1)+'\n'
      r.write("sb: "+str(ee)+" "+str(ff)+" "+str(ee1)+" "+str(ff1)+'\n\n')    
           
r.close()

#print len(files[0])
