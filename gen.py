import numpy as np
from pypinyin import lazy_pinyin

class Data:
    def __init__(self,filename:str) -> None:
        self.head=np.ones(10000,np.int8)*0x7f7f7f7f
        self.nxt=np.ones(10000,np.int8)*0x7f7f7f7f
        self.to=np.zeros(10000,np.int8)
        self.v=['' for i in range(10000)]
        self.cnt=0
        self.p=0
        self._gen(self.read(filename))

    def read(self,filename:str) -> list|None:
        ret=[]
        try:
            f=open(filename,"r",encoding="utf-8")
            for name in f:
                ret.append(lazy_pinyin(name,0,"ignore"))
                self.p+=1
                self.v[self.p]=name.strip()
        except IOError:
            print("Read file error.")
            return None
        except Exception:
            print("Other errors occurred during reading file.")
            return None
        finally:
            f.close()
        return ret
    
    def findCh(self,root:int,v:str,new=False) -> int|None:
        for i in self._nxt(root):
            p=self.to[i]
            if self.v[p]==v:
                return p
        if new:
            return self._newCh(root,v)
        else:
            return None

    def _newCh(self,root:int,v:str):
        self.cnt+=1
        self.p+=1
        self.nxt[self.cnt]=self.head[root]
        self.head[root]=self.cnt
        self.to[self.cnt]=self.p
        self.v[self.p]=v
        return self.p

    def _nxt(self,root:int):
        path=self.head[root]
        while path!=0x7f7f7f7f:
            yield path
            path=self.nxt[path]

    def _gen(self,py:list):
        for id,name in enumerate(py,1):
            for word in name:
                root=0
                for ch in word:
                    root=self.findCh(root,ch,True)
                self.cnt+=1
                self.nxt[self.cnt]=self.head[root]
                self.head[root]=self.cnt
                self.to[self.cnt]=id


class Search(Data):
    def __init__(self,filename) -> None:
        super().__init__(filename)

    def __call__(self, t:str):
        ret=self.find(t[0])
        for ch in t:
            ret=ret&self.find(ch)
        return ret

    def find(self,ch:int,root=0) -> set:
        sub=self.findCh(root,ch)
        if sub is None:
            return set()
        return self.dfs(sub)

    def dfs(self,root:int) -> set:
        ret=[]
        que=np.ndarray(100,'i8')
        top=0
        que[top]=root
        while top>=0:
            root=que[top]
            top-=1
            for i in self._nxt(root):
                p=self.to[i]
                if len(self.v[p])>1:
                    ret.append(p)
                    continue
                top+=1
                que[top]=p 
        return set(ret)


if __name__ == '__main__':
    obj=Search("name.txt")
    print(obj("so"))
    