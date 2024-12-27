from decimal import ROUND_HALF_UP, Decimal, getcontext
from random import randint, seed


__DecimalPrecision=16


getcontext().rounding=ROUND_HALF_UP


def setpr(__p:int)->None:global __DecimalPrecision;__DecimalPrecision=__p;

def getpr()->int:return __DecimalPrecision;


def deciml(__a:float|int|str|Decimal,__pr=getpr())->Decimal:
    try:
        if (sa:=str(__a))=='NaN' or sa=='Inf' or sa=='-Inf':return __a;
        def __exp(__a:str)->list:
            match len(a:=__a.split('e')):
                case 1:
                    match len(a:=__a.split('E')):
                        case 1:return a+['0',]; 
                        case 2:return a;
                        case _:return None;
                case 2:return a;
                case _:return None;
        __a=str(__a)
        if __a[0]=='-':a0=__a[0];__a=__a[1:];
        else:a0='';
        if (a1:=__exp(__a)) is None:raise Exception;
        if len(a2:=a1[0].split('.'))==1:a2+=['0',];
        if Decimal(a1[0])==0:return Decimal('0.0');
        if int(a2[0])==0:
            if a2[1][0]=='0':
                c=1
                for i in a2[1][1:]:
                    if i=='0':c+=1;
                    else:break;
                a2[0]=a2[1][c];a2[1]=a2[1][c+1:];a1[1]=str(int(a1[1])-c-1);
        if len(a2[1])>__pr:
            a2[1]=a2[1][:__pr+1];del __pr,__a;
            if int(a2[1][-1])>=5:
                a2[1]=a2[1][:-2]+str(int(a2[1][-2])+1);
            else:a2[1]=a2[1][:-1];
        return Decimal(a0+a2[0]+'.'+a2[1]+'E'+a1[1]);
    except:return Decimal('NaN');

# args: (start number,end number), decimal precision, seed
def rint(__i:int,__j:int,__n=1,s=None)->int|tuple[int,...]:
    try:
        if s is not None:seed(s);
        if __n==1:return randint(__i,__j);
        return tuple(map(lambda _:randint(__i,__j),range(__n)))
    except Exception as e:print("Invalid command: rint\n",e);

# rdeciml(num1,num2,precision)
# rdeciml.random(n,seed)
# .cgpr(new precision)
class rdeciml():
    
    def __init__(self,__a:int|float|Decimal|str,__b:int|float|Decimal|str,__pr=getpr())->None:
        try:
            __a=str(__a);__b=str(__b);
            def __exp(__a)->list:
                match len(a1:=__a.split('E')):
                    case 1:
                        match len(a2:=__a.split('e')):
                            case 1:return a2+[0,];
                            case 2:return a2;
                            case _:return None;
                    case 2:return a1;
                    case _:return None;
            def __dtd(__a)->list:
                match len(a1:=__a.split('.')):
                    case 1:return a1+['',];
                    case 2:
                        if a1[0]=='':a1[0]='0';
                        return a1;
                    case _:return None;
            def __etd(__a)->list:
                __a,a1=__a
                if (i1a:=int(__a[1]))>=0:
                    if (la1:=len(a1[1]))<i1a:
                        z=''
                        for _ in range(i1a-la1):z+='0';
                        return [a1[0]+a1[1]+z,'0'];
                    elif la1>=i1a:
                        return [a1[0]+a1[1][:(da:=i1a-la1)],a1[1][da:]]
                    else:return None
                else:
                    if (la0:=len(a1[0]))<(ni1a:=-i1a):
                        z=''
                        for _ in range(ni1a-la0):z+='0';
                        return ['0',z+a1[0]+__a[1]]
                    elif la0>=ni1a:
                        return [a1[0][:(da:=la0-ni1a)],a1[1][da:]+a1[0]]
                    else:return None
            __a,__b=tuple(map(__exp,(__a,__b)))
            if __a is None or __b is None:raise Exception;
            a1,b1=tuple(map(__dtd,(__a[0],__b[0])));
            if a1 is None or b1 is None:raise Exception;
            __a,__b=tuple(map(__etd,((__a,a1),(__b,b1))))
            if __a is None or __b is None:raise Exception;
            self.__oa=__a;self.__ob=__b;del a1,b1;__a,__b=map(self.__dtip,((__a,__pr),(__b,__pr)));
            self.__a=__a;self.__b=__b;self.__pr=__pr;del __a,__b,__pr;self.random=lambda __n,__s=None:self.__frandom(self.__pr,__n,__s);
        except Exception as e:print("Invalid command: rdeciml\n",e);

    def __dtip(self,__apr)->int:
        __a,__pr=__apr
        if (la:=len(__a[1]))<__pr:
            for _ in range(__pr-la):__a[1]+='0';
        return int(__a[0]+__a[1][:__pr]);

    def __frandom(self,__pr,__n,__s)->list:
        def rint(__a,__b,__pr):
            (z:=[__a,__b]).sort();__a,__b=z;del z;r=str(randint(__a,__b));
            if (r1:=len(r)-__pr)>0:
                return r[:r1]+'.'+r[r1:];
            else:
                z=''
                for _ in range(-r1):z+='0';
                return '0.'+z+r
        seed(__s);return [Decimal(rint(self.__a,self.__b,__pr)) for _ in range(__n)];

    def cgpr(self,__pr)->None:
        try:
            self.__pr=__pr;del __pr;self.__a,self.__b=map(self.__dtip,((self.__oa,self.__pr),(self.__ob,self.__pr)));print("New precision: "+str(self.__pr));
        except Exception as e:print("Invalid command: rdeciml.cgpr\n",e);


_Pi='3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679';_EulersNumber='2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274';


class constant:
    
    @staticmethod
    def e(pr=getpr())->Decimal|None:
        try:
            if pr>100:raise Exception;
            global _EulersNumber;return Decimal(_EulersNumber[:pr+2]);
        except:print("Invalid argument: pr -> < 100");

    def pi(pr=getpr())->Decimal|None:
        try:
            if pr>100:raise Exception;
            global _Pi;return Decimal(_Pi[:pr+2]);
        except:print("Invalid argument: pr -> < 100");


def abs(__a:float|int|str|Decimal)->Decimal|None:
    a=Decimal(str(__a))
    if (a1:=str(a))=='NaN' or a1=='Inf' or a1=='-Inf':return None;
    elif a<0:return Decimal(a1[1:]);
    else:return a;

class algbra:

    @staticmethod
    def add(*__a:float|int|str|Decimal,pr=getpr())->Decimal:
        try:
            p=pr+2
            def __add(__a:str,__b:str)->Decimal:
                try:
                    def __exp(__a)->list:
                        match len(a1:=__a.split('E')):
                            case 1:
                                match len(a2:=__a.split('e')):
                                    case 1:return a2+['0',];
                                    case 2:return a2;
                                    case _:return None;
                            case 2:return a1;
                            case _:return None;
                    a,b=map(__exp,(__a,__b))
                    if a is None or b is None:raise Exception
                    an=a[0].lstrip('-').split('.')[0];bn=b[0].lstrip('-').split('.')[0];d1=len(an)+int(a[1]);d2=len(bn)+int(b[1]);
                    if d1>d2:
                        if d1>0:getcontext().prec=p+d1;
                        else:getcontext().prec=p;
                    else:
                        if d2>0:getcontext().prec=p+d2;
                        else:getcontext().prec=p;
                    return str(Decimal(__a)+Decimal(__b))
                except:return None;
            r=str(__a[0])
            for i in __a[1:]:
                r=str(__add(r,str(i)))
                if r=='None':raise Exception;
            return deciml(r,pr)
        except:return Decimal('NaN');

    @staticmethod
    def sub(*__a:float|int|str|Decimal,pr=getpr())->Decimal:
        try:
            p=pr+2
            def __sub(__a:str,__b:str)->Decimal:
                try:
                    def __exp(__a)->list:
                        match len(a1:=__a.split('E')):
                            case 1:
                                match len(a2:=__a.split('e')):
                                    case 1:return a2+['0',];
                                    case 2:return a2;
                                    case _:return None;
                            case 2:return a1;
                            case _:return None;
                    a,b=map(__exp,(__a,__b))
                    if a is None or b is None:raise Exception
                    an=a[0].lstrip('-').split('.')[0];bn=b[0].lstrip('-').split('.')[0];d1=len(an)+int(a[1]);d2=len(bn)+int(b[1]);
                    if d1>d2:
                        if d1>0:getcontext().prec=p+d1;
                        else:getcontext().prec=p;
                    else:
                        if d2>0:getcontext().prec=p+d2;
                        else:getcontext().prec=p;
                    return str(Decimal(__a)-Decimal(__b))
                except:return None
            r=str(__a[0])
            for i in __a[1:]:
                r=str(__sub(r,str(i)))
                if r=='None':raise Exception;
            return deciml(r,pr)
        except:return Decimal('NaN');

    @staticmethod
    def mul(*__a:float|int|str|Decimal,pr=getpr())->Decimal:
        try:
            p=pr+2
            def __mul(__a:str,__b:str)->Decimal:
                try:
                    def __exp(__a)->list:
                        match len(a1:=__a.split('E')):
                            case 1:
                                match len(a2:=__a.split('e')):
                                    case 1:return a2+['0',];
                                    case 2:return a2;
                                    case _:return None;
                            case 2:return a1;
                            case _:return None;
                    a,b=map(__exp,(__a,__b))
                    if a is None or b is None:raise Exception
                    an=a[0].lstrip('-').split('.')[0];bn=b[0].lstrip('-').split('.')[0];
                    if (p1:=int(a[1])+int(b[1])+len(an)+len(bn))>0:getcontext().prec=p1+p;
                    else:getcontext().prec=p;
                    return str(Decimal(__a)*Decimal(__b))
                except:return None;
            r=str(__a[0])
            for i in __a[1:]:
                r=str(__mul(r,str(i)))
                if r=='None':raise Exception;
            return deciml(r,pr)
        except:return Decimal('NaN');

    @staticmethod
    def div(__a:float|int|str|Decimal,__b:float|int|str|Decimal,__pr=getpr())->Decimal:
        try:
            p=__pr+2
            def __exp(__a)->list:
                match len(a1:=__a.split('E')):
                    case 1:
                        match len(a2:=__a.split('e')):
                            case 1:return a2+['0',];
                            case 2:return a2;
                            case _:return None;
                    case 2:return a1;
                    case _:return None;
            a,b=map(__exp,(str(__a),str(__b)))
            if a is None or b is None:raise Exception
            an=a[0].lstrip('-').split('.')[0];bn=b[0].lstrip('-').split('.')[0];
            if (p1:=int(a[1])-int(b[1])+len(an)-len(bn))>0:getcontext().prec=p1+p;
            else:getcontext().prec=p;
            return deciml(Decimal(__a)/Decimal(__b),__pr)
        except:return Decimal('NaN');
    
    @classmethod
    def log(cls,__a:float|int|str|Decimal,__b=constant.e(),__pr=getpr())->Decimal:
        try:
            p=__pr+2
            a=Decimal(str(__a));b=Decimal(str(__b));c=0;
            if b>=1:
                if a>=1:
                    while a>b:a=cls.div(a,b,p);c+=1;
                    if c!=0:getcontext().prec=len(str(c))+p;return deciml((a.ln()/b.ln())+c,__pr);
                    else:getcontext().prec=p;return deciml(a.ln()/b.ln(),__pr);
                if a<1:
                    while a<1:a=cls.mul(a,b,pr=p);c+=1;
                    if c!=0:getcontext().prec=len(str(c))+p;return deciml((a.ln()/b.ln())-c,__pr);
                    else:getcontext().prec=p;return deciml(a.ln()/b.ln(),__pr);
            if b<1:
                if a>=b:
                    while a>b:a=cls.mul(a,b,pr=p);c+=1;
                    if c!=0:getcontext().prec=len(str(c))+p;return deciml((a.ln()/b.ln())-c,__pr);
                    else:getcontext().prec=p;return deciml(a.ln()/b.ln(),__pr);
                if a<b:
                    while a<b:a=cls.div(a,b,p);c+=1;
                    if c!=0:getcontext().prec=len(str(c))+p;return deciml((a.ln()/b.ln())+c,__pr);
                    else:getcontext().prec=p;return deciml(a.ln()/b.ln(),__pr);
        except:return Decimal('NaN');

    @classmethod
    def pwr(cls,__a:float|int|Decimal|str,__b:float|int|Decimal|str,__pr=getpr())->Decimal:
        try:
            a=Decimal(str(__a));c=0;p=__pr+2;
            if (b:=Decimal(str(__b)))==(ib:=int(b)):
                r=1
                if b<0:
                    for _ in range(-ib):r=cls.mul(r,a,pr=p);
                    r=cls.div(1,r,p)
                else:
                    for _ in range(ib):r=cls.mul(r,a,pr=p);
                return deciml(r,__pr)
            elif a<0:raise Exception;
            elif b==0:return Decimal('1');
            elif a==0:return Decimal('0');
            if a>=1:
                if b>=0:
                    while a>1:a=cls.div(a,10,p);c+=1;
                    getcontext().prec=int((p1:=c*b))+p;return deciml((10**p1)*(a**b),__pr);
                if b<0:getcontext().prec=p;return deciml(a**b,__pr);
            if a<1:
                if b>=0:
                    getcontext().prec=p;return deciml(a**b,__pr);
                if b<0:
                    while a<1:a=cls.mul(a,10,pr=p);c+=1;
                    getcontext().prec=int((p1:=-c*b))+p;return deciml((10**p1)*(a**b),__pr);
        except:return Decimal('NaN');


class galgbra:

    @staticmethod
    def add(*__a:list[Decimal]|tuple[Decimal,...],pr=getpr())->tuple[Decimal,...]:
        try:return tuple(map(lambda x:algbra.add(*x,pr=pr),zip(*__a)));
        except Exception as e:print("Invalid command: galgra.add\n",e);
    
    @staticmethod
    def sub(*__a:list[Decimal]|tuple[Decimal,...],pr=getpr())->tuple[Decimal,...]:
        try:return tuple(map(lambda x:algbra.sub(*x,pr=pr),zip(*__a)));
        except Exception as e:print("Invalid command: galgra.sub\n",e);
    
    @staticmethod
    def mul(*__a:list[Decimal]|tuple[Decimal,...],pr=getpr())->tuple[Decimal,...]:
        try:return tuple(map(lambda x:algbra.mul(*x,pr=pr),zip(*__a)));
        except Exception as e:print("Invalid command: galgra.mul\n",e);
    
    @staticmethod
    def div(__a:list[Decimal]|tuple[Decimal,...],__b:list[Decimal]|tuple[Decimal,...],__pr=getpr())->tuple[Decimal,...]:
        try:return tuple(map(lambda x:algbra.div(*x,__pr),zip(__a,__b)));
        except Exception as e:print("Invalid command: galgra.div\n",e);
    
    @staticmethod
    def pwr(__a:list[Decimal]|tuple[Decimal,...],__b:list[Decimal]|tuple[Decimal,...],__pr=getpr())->tuple[Decimal,...]:
        try:return tuple(map(lambda x:algbra.pwr(*x,__pr),zip(__a,__b)));
        except Exception as e:print("Invalid command: galgra.pwr\n",e);
    
    @staticmethod
    def log(__a:list[Decimal]|tuple[Decimal,...],__b:list[Decimal]|tuple[Decimal,...],__pr=getpr())->tuple[Decimal,...]:
        try:return tuple(map(lambda x:algbra.log(*x,__pr),zip(__a,__b)));
        except Exception as e:print("Invalid command: galgra.log\n",e);
    
    @staticmethod
    def addsg(__a:Decimal,__b:list[Decimal]|tuple[Decimal,...],__pr=getpr())->tuple[Decimal,...]:
        try:__a=str(__a);return tuple(map(lambda x:algbra.add(__a,x,pr=__pr),__b));
        except Exception as e:print("Invalid command: galgra.addsg\n",e);
    
    @staticmethod
    def subgs(__a:list[Decimal]|tuple[Decimal,...],__b:Decimal,__pr=getpr())->tuple[Decimal,...]:
        try:__b=str(__b);return tuple(map(lambda x:algbra.sub(x,__b,pr=__pr),__a));
        except Exception as e:print("Invalid command: galgra.subgs\n",e);
    
    @staticmethod
    def subsg(__a:Decimal,__b:list[Decimal]|tuple[Decimal,...],__pr=getpr())->tuple[Decimal,...]:
        try:__a=str(__a);return tuple(map(lambda x:algbra.sub(__a,x,pr=__pr),__b));
        except Exception as e:print("Invalid command: galgra.subsg\n",e);

    @staticmethod
    def mulsg(__a:Decimal,__b:list[Decimal]|tuple[Decimal,...],__pr=getpr())->tuple[Decimal,...]:
        try:__a=str(__a);return tuple(map(lambda x:algbra.mul(__a,x,pr=__pr),__b));
        except Exception as e:print("Invalid command: galgra.mulsg\n",e);

    @staticmethod
    def divgs(__a:list[Decimal]|tuple[Decimal,...],__b:Decimal,__pr=getpr())->tuple[Decimal,...]:
        try:__b=str(__b);return tuple(map(lambda x:algbra.div(x,__b,__pr),__a));
        except Exception as e:print("Invalid command: galgra.divgs\n",e);
    
    @staticmethod
    def divsg(__a:Decimal,__b:list[Decimal]|tuple[Decimal,...],__pr=getpr())->tuple[Decimal,...]:
        try:__a=str(__a);return tuple(map(lambda x:algbra.div(__a,x,__pr),__b));
        except Exception as e:print("Invalid command: galgra.divsg\n",e);

    @staticmethod
    def pwrgs(__a:list[Decimal]|tuple[Decimal,...],__b:Decimal,__pr=getpr())->tuple[Decimal,...]:
        try:__b=str(__b);return tuple(map(lambda x:algbra.pwr(x,__b,__pr),__a));
        except Exception as e:print("Invalid command: galgra.pwrgs\n",e);
    
    @staticmethod
    def pwrsg(__a:Decimal,__b:list[Decimal]|tuple[Decimal,...],__pr=getpr())->tuple[Decimal,...]:
        try:__a=str(__a);return tuple(map(lambda x:algbra.pwr(__a,x,__pr),__b));
        except Exception as e:print("Invalid command: galgra.pwrsg\n",e);
    
    @staticmethod
    def loggs(__a:list[Decimal]|tuple[Decimal,...],__b:Decimal,__pr=getpr())->tuple[Decimal,...]:
        try:__b=str(__b);return tuple(map(lambda x:algbra.log(x,__b,__pr),__a));
        except Exception as e:print("Invalid command: galgra.loggs\n",e);
    
    @staticmethod
    def logsg(__a:Decimal,__b:list[Decimal]|tuple[Decimal,...],__pr=getpr())->tuple[Decimal,...]:
        try:__a=str(__a);return tuple(map(lambda x:algbra.log(__a,x,__pr),__b));
        except Exception as e:print("Invalid command: galgra.logsg\n",e);


class trig:

    @staticmethod
    def sin(__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:
            pr=__pr+2
            if (a:=Decimal(str(__a)))>(p:=algbra.mul(constant.pi(pr),'2',pr=pr)):a='0.'+str(algbra.div(a,p,pr)).split('.')[1];a=algbra.mul(a,p,pr=pr);
            elif a<algbra.mul('-1',p,pr=pr):a='-0.'+str(algbra.div(a,p,pr)).split('.')[1];a=algbra.mul(a,p,pr=pr);
            rp=None;n=a;d=1;c=1;a1=algbra.pwr(a,'2',pr);r=algbra.div(n,d,pr);
            while r!=rp:rp=r;r=algbra.add(r,algbra.div((n:=algbra.mul(n,a1,'-1',pr=pr)),(d:=d*(c+1)*((c:=c+2))),pr),pr=pr);
            return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.sin\n",e);return Decimal('NaN');

    @staticmethod
    def cos(__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:
            pr=__pr+2
            if (a:=Decimal(str(__a)))>(p:=algbra.mul(constant.pi(pr),'2',pr=pr)):a='0.'+str(algbra.div(a,p,pr)).split('.')[1];a=algbra.mul(a,p,pr=pr);
            elif a<algbra.mul('-1',p,pr=pr):a='-0.'+str(algbra.div(a,p,pr)).split('.')[1];a=algbra.mul(a,p,pr=pr);
            rp=0;n=1;d=1;c=0;r=1;a1=algbra.pwr(a,'2',pr);
            while r!=rp:rp=r;r=algbra.add(r,algbra.div((n:=algbra.mul(n,a1,'-1',pr=pr)),(d:=d*(c+1)*((c:=c+2))),pr),pr=pr);
            return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.cos\n",e);return Decimal('NaN');

    @classmethod
    def tan(cls,__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:
            pr=__pr+2
            if (a:=Decimal(str(__a)))>(p:=algbra.mul(constant.pi(pr),'2',pr=pr)):a='0.'+str(algbra.div(a,p,pr)).split('.')[1];a=algbra.mul(a,p,pr=pr);
            elif a<algbra.mul('-1',p,pr=pr):a='-0.'+str(algbra.div(a,p,pr)).split('.')[1];a=algbra.mul(a,p,pr=pr);
            r=algbra.div(cls.sin(a,pr),cls.cos(a,pr),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.tan\n",e);return Decimal('NaN');

    @classmethod
    def cosec(cls,__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:pr=__pr+2;r=algbra.div(1,cls.sin(__a),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.cosec\n",e);return Decimal('NaN');

    @classmethod
    def sec(cls,__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:pr=__pr+2;r=algbra.div(1,cls.cos(__a),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.sec\n",e);return Decimal('NaN');

    @classmethod
    def cot(cls,__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:pr=__pr+2;r=algbra.div(cls.cos(__a),cls.sin(__a),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.cot\n",e);return Decimal('NaN');

    # [-pi/2, pi/2]
    @classmethod
    def asin(cls,__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:
            pr=__pr+2;a=Decimal(str(__a));
            if a<-1 or a>1:raise Exception;
            if a>(a1:=algbra.pwr('2','-0.5',pr)):r=cls.acos(algbra.pwr(algbra.sub(1,algbra.pwr(a,'2',pr),pr=pr),'0.5',pr),pr);
            elif a<Decimal('-'+str(a1)):r=algbra.mul('-1',cls.acos(algbra.pwr(algbra.sub('1',algbra.pwr(a,'2',pr),pr=pr),'0.5',pr),pr),pr=pr);
            else:
                i=0;r=(n:=a);rn=None;a1=algbra.pwr(a,'2',pr);d1=1;d2=1;d3=1;
                while r!=rn:rn=r;i+=1;r=algbra.add(r,algbra.div((n:=algbra.mul(n,(q:=2*i),(q-1),a1,pr=pr)),(d1:=d1*4)*((d2:=d2*i)**2)*(d3:=d3+2),pr),pr=pr);
            return deciml(r,__pr)
        except Exception as e:print("Invalid command: trig.asin\n",e);return Decimal('NaN');

    # [0, pi]
    @classmethod
    def acos(cls,__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:
            pr=__pr+2;a=Decimal(str(__a));
            if a<-1 or a>1:raise Exception;
            if a>(a1:=algbra.pwr('2','-0.5',pr)):r=cls.asin(algbra.pwr(algbra.sub(1,algbra.pwr(a,'2',pr),pr=pr),'0.5',pr),pr);
            elif a<Decimal('-'+str(a1)):r=algbra.add(algbra.mul('-1',cls.asin(a,pr),pr=pr),algbra.div(constant.pi(pr),'2',pr),pr=pr);
            else:
                i=0;r=algbra.sub(algbra.div(constant.pi(pr),'2',pr),(n:=a),pr=pr);
                rn=None;a1=algbra.pwr(a,'2',pr);d1=1;d2=1;d3=1;
                while r!=rn:rn=r;i+=1;r=algbra.sub(r,algbra.div((n:=algbra.mul(n,(q:=2*i),(q-1),a1,pr=pr)),(d1:=d1*4)*((d2:=d2*i)**2)*(d3:=d3+2),pr),pr=pr);
            return deciml(r,__pr)
        except Exception as e:print("Invalid command: trig.acos\n",e);return Decimal('NaN');

    # [-pi/2, pi/2]
    @classmethod
    def atan(cls,__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:
            pr=__pr+2
            if (a:=Decimal(str(__a)))<0:r=algbra.mul('-1',cls.asec(algbra.pwr(algbra.add(algbra.pwr(a,'2',pr),'1',pr=pr),'0.5',pr),pr),pr=pr);
            else:r=cls.asec(algbra.pwr(algbra.add(algbra.pwr(a,'2',pr),'1',pr=pr),'0.5',pr),pr);
            return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.atan\n",e);return Decimal('NaN');

    # [-pi/2, pi/2]
    @classmethod
    def acosec(cls,__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:pr=__pr+2;r=cls.asin(algbra.div('1',__a,pr),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.acosec\n",e);return Decimal('NaN');

    # [0, pi]
    @classmethod
    def asec(cls,__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:pr=__pr+2;r=cls.acos(algbra.div('1',__a,pr),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.asec\n",e);return Decimal('NaN');

    # [-pi/2, pi/2]
    @classmethod
    def acot(cls,__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:pr=__pr+2;r=cls.atan(algbra.div('1',__a,pr),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: trig.acot\n",e);return Decimal('NaN');


class htrig:

    @staticmethod
    def sinh(__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:
            pr=__pr+2;r=__a;rn=None;n=__a;d=1;c=1;a1=algbra.pwr(__a,'2',pr);
            while r!=rn:rn=r;r=algbra.add(r,algbra.div((n:=algbra.mul(n,a1,pr=pr)),(d:=d*(c+1)*((c:=c+2))),pr),pr=pr);
            return deciml(r,__pr)
        except Exception as e:print("Invalid command: htrig.sinh\n",e);return Decimal('NaN');
    
    @staticmethod
    def cosh(__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:
            pr=__pr+2;r=1;rn=None;n=1;d=1;c=0;a1=algbra.pwr(__a,'2',pr);
            while r!=rn:rn=r;r=algbra.add(r,algbra.div((n:=algbra.mul(n,a1,pr=pr)),(d:=d*(c+1)*((c:=c+2))),pr),pr=pr);
            return deciml(r,__pr);
        except Exception as e:print("Invalid command: htrig.cosh\n",e);return Decimal('NaN');
    
    @classmethod
    def tanh(cls,__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:pr=__pr+2;r=algbra.div(cls.sinh(__a,pr),cls.cosh(__a,pr),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: htrig.tanh\n",e);return Decimal('NaN');
    
    @classmethod
    def cosech(cls,__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:pr=__pr+2;r=algbra.div(1,cls.sinh(__a),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: htrig.cosech\n",e);return Decimal('NaN');
    
    @classmethod
    def sech(cls,__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:pr=__pr+2;r=algbra.div(1,cls.cosh(__a),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: htrig.sech\n",e);return Decimal('NaN');
    
    @classmethod
    def coth(cls,__a:Decimal|int|float|str,__pr=getpr())->Decimal:
        try:
            pr=__pr+2
            if deciml(__a)==0:raise Exception;
            r=algbra.div(cls.cosh(__a),cls.sinh(__a),pr);return deciml(r,__pr);
        except Exception as e:print("Invalid command: htrig.coth\n",e);return Decimal('NaN');
    
class stat:

    @staticmethod
    def median(__x:list[Decimal]|tuple[Decimal,...],__pr=getpr())->Decimal:
        try:
            x=tuple(map(lambda x:Decimal(str(x)),__x));lm=algbra.div(len(x),2);(x:=list(x)).sort();
            if (i:=int(lm)-1)==lm:return x[i];
            else:return(algbra.div(algbra.add(x[i],x[i+1],pr=__pr),2,__pr));
        except Exception as e:print("Invalid command: stat.median\n",e);return Decimal('NaN');
    
    @staticmethod
    def mode(__x:list|tuple)->Decimal|tuple[Decimal,...]:
        try:
            d=dict();r=list();
            for i in __x:d[i]=d.setdefault(i,0)+1;
            c=max(d.values())
            for i in d.items():
                if i[1]==c:r.append(i[0]);
            return {"values":tuple(r),"mode":c}
        except Exception as e:print("Invalid command: stat.mode\n",e);return Decimal('NaN');


# print(deciml(22.01234485145124641E+42), deciml(0.000015646541E+100))
# print(algbra.add(0.1234567156461254845148546554, '1.1234567'), algbra.add(1.2646515484544556546, 1, 2, 5), algbra.add(1.0123456789E-5, 1.234567890E-5), algbra.add(0.000010123456789, 0.00001234567890))
# print(algbra.add(0.1234567156461254845148546554, 1.1234567), algbra.add(1.2646515484544556546, 1, 2, 5), algbra.mul(-2,-4), algbra.mul(-2.123, 1.123), algbra.mul(2E+1,-1.123), algbra.mul(12.5467E-1, 25), algbra.div(4E-1,2), algbra.div(2E+1,4), algbra.div(2.5E+1, 7.5), algbra.div(-7.5E-1, -2.5), algbra.div(7.5, -2), algbra.div(-2, 7.5))
# print(Decimal(str(2 ** 0.5)))
# a=algbra.log(0.9395227492140118E+100, 2E-11)
# print(a, len(str(a)))
# print(trig.cos(trig.acos(0)), len(str(trig.cos(trig.acos(0)))))
# print(algbra.pwr(2, 3), algbra.pwr(2, -3.5), algbra.div(constant.pi(), 1), trig.sin(trig.asin(-0.8)), trig.cos(trig.acos(-0.8)), trig.tan(trig.atan(111111111111)), trig.tan(1.5707963267947966))
# print(htrig.sinh(-10), htrig.cosh(-10))

# print(trig.asin(-1.0), trig.asin(1.0))
# print(constant.pi()/2)
# print(trig.acos(-1.0), trig.acos(1.0))
# print(trig.acot(0.0000001), trig.acot(-0.0000001))
# print(trig.asec(-1.0), trig.asec(1.0))

# r=rdeciml('.111111e-1',5E-20)
# print(r.random(5))
# print(deciml('.454245424'))

# a=stat.median([1,2,3,4,5,3,2,1,2,3])
# print(a)
# a=stat.mode(['1','2','3','4','5','3','2','1','2','3'])
# print(a)
# print(deciml('000.00000000000000000045'))

