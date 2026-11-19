import json,sys,os
from urllib.request import Request as R,urlopen as O
U=str.upper
def a0(p,b):return json.loads(O(R(os.environ["MAKEFUN_ENV_URL"]+p,json.dumps(b).encode(),H)).read())
N=(-17,-15,-10,-6,6,10,15,17);K=(-9,-8,-7,-1,1,7,8,9);BD=(-9,-7,7,9);RD=(-8,-1,1,8)
SD={"B":BD,"R":RD,"Q":BD+RD};V=dict(zip("PNBRQK",(100,320,330,500,900,0)));M=30000;A="abcdefgh"
def a1(t,f,n):return 0<=t<64 and abs(t%8-f)<=n
def a4(b,q,w):
 f=q%8
 for d in(7,9):
  t=q+d if w else q-d
  if a1(t,f,1)and abs(t%8-f)==1 and b[t]==("P"if w else"p"):return 1
 for d in N:
  if a1(q+d,f,2)and b[q+d]==("N"if w else"n"):return 1
 for dd,g in((BD,"BQ"if w else"bq"),(RD,"RQ"if w else"rq")):
  for d in dd:
   t=q+d
   while 0<=t<64 and abs(t%8-(t-d)%8)<=1:
    if b[t]in g:return 1
    if b[t]!=".":break
    t+=d
 for d in K:
  if a1(q+d,f,1)and b[q+d]==("K"if w else"k"):return 1
 return 0
def a2(b,s,c,ep):
 o=[];Z=lambda x:(U(x)==x)!=s
 for q,p in enumerate(b):
  if p=="."or Z(p):continue
  g=U(p);f=q%8
  if g=="P":
   d=-8 if s else 8;pr=q//8==(1 if s else 6);t=q+d
   if b[t]==".":
    if pr:o+=[(q,t,x)for x in"qrbn"]
    else:
     o.append((q,t,None))
     if q//8==(6 if s else 1)and b[t+d]==".":o.append((q,t+d,None))
   for df in(-1,1):
    if 0<=f+df<8:
     t=q+d+df;z=b[t]
     if z!="."and Z(z):o+=[(q,t,x)for x in"qrbn"]if pr else[(q,t,None)]
     elif t==ep:o.append((q,t,None))
  elif g=="N":o+=[(q,q+d,None)for d in N if a1(q+d,f,2)and(b[q+d]=="."or Z(b[q+d]))]
  elif g=="K":
   o+=[(q,q+d,None)for d in K if a1(q+d,f,1)and(b[q+d]=="."or Z(b[q+d]))]
   if q==(60 if s else 4):
    for ee,cs,rr in(((61,62),"K",63),((59,58,57),"Q",56))if s else(((5,6),"k",7),((3,2,1),"q",0)):
     if cs in c and b[rr]==("R"if s else"r")and all(b[x]=="."for x in ee)and not a4(b,q,not s)and not a4(b,ee[0],not s):o.append((q,ee[1],None))
  else:
   for dd in SD[g]:
    t=q+dd
    while 0<=t<64 and abs(t%8-(t-dd)%8)<=1:
     z=b[t]
     if z==".":o.append((q,t,None))
     else:
      if Z(z):o.append((q,t,None))
      break
     t+=dd
 return o
def a3(b,s,c,ep,m):
 f,t,p=m;q=b[f];nb=b[:];nb[f]=".";nb[t]=(U(p)if s else p)if p else q;ne=None;g=U(q)
 if g=="P":
  if abs(t-f)==16:ne=(f+t)//2
  elif t==ep and b[t]==".":nb[t+(8 if s else -8)]="."
 elif g=="K":
  if t-f==2:nb[t-1],nb[t+1]=b[t+1],"."
  elif f-t==2:nb[t+1],nb[t-2]=b[t-2],"."
 nc=c
 if q in"Kk":nc=c.replace(q,"")
 for sq,ch in((63,"K"),(56,"Q"),(7,"k"),(0,"q")):
  if sq in(f,t):nc=nc.replace(ch,"")
 return nb,not s,nc,ne
def a5(b,s,c,ep):
 o=[]
 for m in a2(b,s,c,ep):
  nb,ns,nc,ne=a3(b,s,c,ep,m)
  if not a4(nb,nb.index("K"if s else"k"),not s):o.append((m,nb,ns,nc,ne))
 return o
NO=[0]
def a8(b,m,ep):
 f,t,p=m
 return(10*V[U(b[t])]-V[U(b[f])]if b[t]!="."else 950)+(p and 800 or 0)
def a9(b,s,c,ep,d,a,bt):
 NO[0]+=1
 if d<=0:return(1 if s else -1)*sum(V[U(p)] if p<"a" else -V[U(p)]for p in b if p!=".")
 ms=a5(b,s,c,ep)
 if not ms:return -M if a4(b,b.index("K"if s else"k"),not s)else 0
 ms.sort(key=lambda z:a8(b,z[0],ep),reverse=1)
 for m,nb,ns,nc,ne in ms:
  sc=-a9(nb,ns,nc,ne,d-1,-bt,-a)
  if sc>a:a=sc
  if a>=bt:break
 return a
def c0(f):
 p=f.split();b=[]
 for w in p[0].split("/"):
  for x in w:b+=(["."]*int(x) if x.isdigit() else[x])
 s=p[1]=="w";c="".join(x for x in"KQkq"if x in p[2]);ep=p[3]!="-"and A.index(p[3][0])+8*(8-int(p[3][1]))or None
 ms=a5(b,s,c,ep)
 if not ms:return None
 ms.sort(key=lambda z:a8(b,z[0],ep),reverse=1);bm=ms[0][0]
 for d in range(1,9):
  NO[0]=0;cu=None;cs=a=-M-1
  for m,nb,ns,nc,ne in ms:
   sc=-a9(nb,ns,nc,ne,d-1,-M-1,-a)
   if sc>cs:cs=sc;cu=m
   if sc>a:a=sc
   if NO[0]>=25000:break
  if cu is None:break
  bm=cu;ms.sort(key=lambda z:1e6*(z[0]==bm)+a8(b,z[0],ep),reverse=1)
  if cs>=M-100 or NO[0]>=25000:break
 f,t,p=bm
 return A[f%8]+str(8-f//8)+A[t%8]+str(8-t//8)+(p or "")
if __name__=="__main__":
 while 1:
  g=a0("/game",{})
  while g["status"]=="your_move":g=a0("/move",{"game":g["game"],"move":c0(g["fen"])})
  if g["status"]=="done":break
