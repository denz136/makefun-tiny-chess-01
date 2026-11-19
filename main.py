# tiny-chess-01: negamax+ab, ID, quiescence, MVV-LVA, PST. No payload.
import json,os,sys,urllib.request,urllib.error
U=str.upper
def p0(p,b):
 try:return json.loads(urllib.request.urlopen(Request(os.environ["MAKEFUN_ENV_URL"]+p,json.dumps(b).encode(),{"Content-Type":"application/json"})).read())
 except urllib.error.HTTPError as e:sys.exit(p,e.code,e.read())
N=(-17,-15,-10,-6,6,10,15,17);K=(-9,-8,-7,-1,1,7,8,9);BD=(-9,-7,7,9);RD=(-8,-1,1,8)
SD={"B":BD,"R":RD,"Q":BD+RD};V={"P":100,"N":320,"B":330,"R":500,"Q":900,"K":0};M=30000
A="abcdefgh";E="."
# PST x7 (P N B R Q K-mid K-end), a8..h1 white view, val=ord-66
T=[[ord(x)-66 for x in g]for g in"BBBBBBBBttttttttLLV``VLLGGL[[LGGBBBVVBBBG=8BB8=GGLL..LLGBBBBBBBB|$$$$$$$$$.BBBB.$$BLQQLB$$GQVVQG$$BQVVQB$$GLQQLG$$.BGGB.$$$$$$$$$|.888888.8BBBBBB88BGLLGB88GGLLGG88BLLLLB88LLLLLL88GBBBBG8.888888.|BBBBBBBBGLLLLLLG=BBBBBB==BBBBBB==BBBBBB==BBBBBB==BBBBBB=BBBGGBBB|.88==88.8BBBBBB88BGGGGB8=BGGGGB=BBGGGGB=8GGGGGB88BGBBBB8.88==88.|$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$.$$$$$$.8......8VVBBBBVVV`LBBL`V|$$$..$$$$.8BB8.$$8V``V8$$8`jj`8$$8`jj`8$$8V``V8$$$BBBB$$$$$$$$$$".split("|")]
def p4(b,q,w):
 f=q%8
 for df in(-1,1):
  t=q+(7 if df<0 else 9)if w else q-(7 if df<0 else 9)
  if 0<=t<64 and abs(t%8-f)==1 and b[t]==("P"if w else"p"):return 1
 for d in N:
  t=q+d
  if 0<=t<64 and abs(t%8-f)<=2 and b[t]==("N"if w else"n"):return 1
 for dd,g in((BD,"BQ"if w else"bq"),(RD,"RQ"if w else"rq")):
  for d in dd:
   t=q+d
   while 0<=t<64 and abs(t%8-(t-d)%8)<=1:
    if b[t]in g:return 1
    if b[t]!=".":break
    t+=d
 for d in K:
  t=q+d
  if 0<=t<64 and abs(t%8-f)<=1 and b[t]==("K"if w else"k"):return 1
 return 0
def p2(b,s,c,ep):
 o=[];R=(1 if s else 6);r=(6 if s else 1);Rk="R"if s else"r";Z=lambda x:(U(x)==x)!=s
 for q,p in enumerate(b):
  if p=="."or Z(p):continue
  u=U(p);f=q%8
  if u=="P":
   d=-8 if s else 8
   pr=(lambda t:[(q,t,x)for x in"qrbn"])if q//8==R else(lambda t:[(q,t,None)])
   t=q+d
   if b[t]==".":o+=pr(t)+([(q,t+d,None)]if q//8==r and b[t+d]=="."else[])
   for df in(-1,1):
    if 0<=f+df<8:
     t=q+d+df;z=b[t]
     if z!="."and Z(z):o+=pr(t)
     elif t==ep and ep is not None:o.append((q,t,None))
  elif u=="N":o+=[(q,q+dd,None)for dd in N if 0<=q+dd<64 and abs((q+dd)%8-f)<=2 and(b[q+dd]=="."or Z(b[q+dd]))]
  elif u=="K":
   o+=[(q,q+dd,None)for dd in K if 0<=q+dd<64 and abs((q+dd)%8-f)<=1 and(b[q+dd]=="."or Z(b[q+dd]))]
   if q==(60 if s else 4):
    for ee,cs,rr in(((61,62),"K",63),((59,58,57),"Q",56))if s else(((5,6),"k",7),((3,2,1),"q",0)):
     if cs in c and b[rr]==Rk and all(b[x]=="."for x in ee)and not p4(b,q,not s)and not p4(b,ee[0],not s):o.append((q,ee[1],None))
  else:
   for dd in SD[u]:
    t=q+dd
    while 0<=t<64 and abs(t%8-(t-dd)%8)<=1:
     z=b[t]
     if z==".":o.append((q,t,None))
     else:
      if Z(z):o.append((q,t,None))
      break
     t+=dd
 return o
def p3(b,s,c,ep,m):
 f,t,p=m;q=b[f];nb=b[:];nb[f]=".";nb[t]=(U(p) if s else p)if p else q;ne=None;u=U(q)
 if u=="P":
  if abs(t-f)==16:ne=(f+t)//2
  elif t==ep and b[t]==".":nb[t+(8 if s else -8)]="."
 elif u=="K":
  if t-f==2:nb[t-1],nb[t+1]=b[t+1],"."
  elif f-t==2:nb[t+1],nb[t-2]=b[t-2],"."
 nc=c
 if q in"Kk":nc=c.replace(q,"").replace("Q"if q=="K"else"q","")
 for sq,ch in((63,"K"),(56,"Q"),(7,"k"),(0,"q")):
  if sq in(f,t):nc=nc.replace(ch,"")
 return nb,not s,nc,ne
def p5(b,s,c,ep):
 o=[]
 for m in p2(b,s,c,ep):
  nb,ns,nc,ne=p3(b,s,c,ep,m)
  if not p4(nb,nb.index("K"if s else"k"),not s):o.append((m,nb,ns,nc,ne))
 return o
NO=[0]
def p6(b):
 sc=0;wb=bb=hv=0
 for q,p in enumerate(b):
  if p==".":continue
  w=p<"a";u=U(p);i=q^56*(not w)
  if u=="B":wb+=w;bb+=not w
  elif u not in"PK":hv+=1
  g=V[u]+T["PNBRQ".index(u)][i]if u in"PNBRQ"else T[6][i]
  sc+=g if w else-g
 t=T[6]if hv>4 else T[5];k=b.index("K");j=b.index("k")
 return sc+t[k]-t[j^56]+(wb>1)*30-(bb>1)*30
def p7(b,s,c,ep,a,bt):
 NO[0]+=1
 if"K"not in b or"k"not in b:return(M-2)if("K"in b)==s else-(M-2)
 st=(1 if s else -1)*p6(b)
 if st>=bt:return bt
 if st>a:a=st
 cp=[(V[U(b[m[1]])]*10-V[U(b[m[0]])],m,nb,ns,nc,ne)for m,nb,ns,nc,ne in p5(b,s,c,ep)if b[m[1]]!="."]
 cp.sort(reverse=1)
 for _,m,nb,ns,nc,ne in cp:
  sc=-p7(nb,ns,nc,ne,-bt,-a)
  if sc>=bt:return bt
  if sc>a:a=sc
 return a
def p8(b,m,ep):
 f,t,p=m;v=0
 if b[t]!=".":v=10*V[U(b[t])]-V[U(b[f])]
 elif t==ep and U(b[f])=="P":v=950
 if p:v+=800+V[U(p)]
 return v
def p9(b,s,c,ep,d,a,bt,pl):
 NO[0]+=1
 if d<=0:return p7(b,s,c,ep,a,bt)
 ms=p5(b,s,c,ep)
 if not ms:return -M+pl if p4(b,b.index("K"if s else"k"),not s)else 0
 ms.sort(key=lambda z:p8(b,z[0],ep),reverse=1);bs=-M-1
 for m,nb,ns,nc,ne in ms:
  sc=-p9(nb,ns,nc,ne,d-1,-bt,-a,pl+1)
  if sc>bs:bs=sc
  if sc>a:a=sc
  if a>=bt:break
 return bs
def cm(f):
 p=f.split();b=[]
 for w in p[0].split("/"):
  for x in w:b+=(["."]*int(x) if x.isdigit() else[x])
 s=p[1]=="w";c="".join(x for x in"KQkq"if x in p[2]);ep=(p[3]!="-" and A.index(p[3][0])+(8-int(p[3][1]))*8 or None)
 ms=p5(b,s,c,ep)
 if not ms:return None
 ms.sort(key=lambda z:p8(b,z[0],ep),reverse=1);bm=ms[0][0]
 for d in range(1,9):
  NO[0]=0;cu=None;cs=a=-M-1
  for m,nb,ns,nc,ne in ms:
   sc=-p9(nb,ns,nc,ne,d-1,-a-1,-a,1)
   if a<sc<M-100:sc=-p9(nb,ns,nc,ne,d-1,-M-1,-a,1)
   if sc>cs:cs=sc;cu=m
   if sc>a:a=sc
   if NO[0]>=25000:break
  if cu is None:break
  bm=cu;ms.sort(key=lambda z:1e6*(z[0]==bm)+p8(b,z[0],ep),reverse=1)
  if cs>=M-100 or NO[0]>=25000:break
 f,t,p=bm
 return A[f%8]+str(8-f//8)+A[t%8]+str(8-t//8)+(p or "")
if __name__=="__main__":
 while 1:
  g=p0("/game",{})
  while g["status"]=="your_move":g=p0("/move",{"game":g["game"],"move":cm(g["fen"])})
  print(g["game"],g["outcome"],g["reason"],file=sys.stderr)
  if g["status"]=="done":break
 print(g.get("wins"),g.get("draws"),g.get("losses"),file=sys.stderr)
