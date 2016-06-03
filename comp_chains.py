#!/usr/bin/python
import numpy as np
do_chain=0

'''
dirty style variables definitio; why use command line? 
'''
war=['wt','l55p','v30m']
chains=['TTRA','TTRB','TTRC','TTRD']
pat='/home/rafal/doktorat/ttr_con/'

'''
function extracts the right piece of data from EUCB CONTACT.log
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
main jobs below
'''
r=open('grube_in.dat','w')                      
files=[]

for j in range(0,len(chains)):
  print "\n\n"+chains[j]
  r.write("\n\n"+chains[j]+'\n\n')
  do_chain=j
  files=[]
  for i in war:
    files.append(open(pat+i+"/CONTACT_"+chains[do_chain]+"_"+chains[do_chain]+".log",'r'))
  
  org=[]
  for i in files:
    org.append(suck_data(i))
  
  print "\n"
  for i in org:
      print len(i)
      r.write('total: '+str(len(i))+"\n")
      aa,bb, aa1, bb1=count_vdw(i)
      
      print "vdw: "+str(aa)+" "+str(bb)+" "+str(aa1)+" "+str(bb1)
      
      r.write("vdw: "+str(aa)+" "+str(bb)+" "+str(aa1)+" "+str(bb1)+'\n')
      cc,dd,cc1,dd1=count_hb(i)
      print "hb: "+str(cc)+" "+str(dd)+" "+str(cc1)+" "+str(dd1)
      r.write("hb: "+str(cc)+" "+str(dd)+" "+str(cc1)+" "+str(dd1)+'\n')
      ee,ff,ee1,ff1=count_sb(i)
      print "sb: "+str(ee)+" "+str(ff)
      r.write("sb: "+str(ee)+" "+str(ff)+" "+str(ee1)+" "+str(ff1)+'\n\n')    
           
r.close() 
#print len(files[0])