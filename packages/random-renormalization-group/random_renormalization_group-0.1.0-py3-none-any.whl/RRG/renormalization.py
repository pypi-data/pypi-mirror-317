import networkx as nx
import faiss
import time
import scipy as spy
from datasketch import MinHash
import copy
import numpy as np

def Random_Fourier_Feature_Hashing(X,TargetDim):
    N = np.size(X,0)
    d = np.size(X,1)
    W = np.random.normal(loc=0, scale=1, size=(d, TargetDim))
    b = np.random.uniform(0, 2*np.pi, size=TargetDim)
    B = np.repeat(b[:, np.newaxis], N, axis=1).T
    Z = 1/2* (1+ np.sign(np.cos(X @ W + B)))
    Z = np.uint8(Z)
    return Z

def Random_Cauchy_Feature_Hashing(X,TargetDim):
    N = np.size(X,0)
    d = np.size(X,1)
    W = spy.stats.cauchy.rvs(loc=0, scale=1, size=(d, TargetDim))
    b = np.random.uniform(0, 2*np.pi, size=TargetDim)
    B = np.repeat(b[:, np.newaxis], N, axis=1).T
    Z = 1/2* (1+ np.sign(np.cos(X @ W + B)))
    Z = np.uint8(Z)
    return Z

def Random_Hyperplane_Hashing(X,TargetDim):
    d = np.size(X,1)
    W = np.random.normal(loc=0, scale=1, size=(d, TargetDim))
    Z = 1/2* (1+ np.sign(X @ W))
    Z = np.uint8(Z)
    return Z

def Random_Min_Hashing(X,TargetDim):
    Z=np.zeros((len(X),TargetDim))
    for ID1 in range(len(X)):
        Hashing_Code=MinHash(num_perm=TargetDim)
        Hashing_Code.update_batch(X[ID1])
        Z[ID1,:]=Hashing_Code.hashvalues
    return Z

def Neighbor_Generator(X,UnitNum):
    Y=[]
    for Unit in range(UnitNum):
        Neighbors = [Unit] + list(X.neighbors(Unit))
        Y.append(np.array(Neighbors))
    return Y


def Normalization_Function(X_Current,Method_Type):
    if Method_Type=="Linear_Kernel":
        Normalized_X=X_Current-np.mean(X_Current,axis=1).reshape(np.size(X_Current,0),1)
    elif Method_Type=="Gaussian_Kernel":
        Normalized_X=X_Current-np.mean(X_Current,axis=1).reshape(np.size(X_Current,0),1)
        Std=np.std(Normalized_X,axis=1).reshape(np.size(Normalized_X,0),1)
        Normalized_X=np.divide(Normalized_X,Std,out=Normalized_X,where=Std!=0)
    elif Method_Type=="Cauchy_Kernel":
        Normalized_X=X_Current-np.min(X_Current,axis=1).reshape(np.size(X_Current,0),1)
        SumV=np.sum(Normalized_X,axis=1).reshape(np.size(Normalized_X,0),1)
        Normalized_X=np.divide(Normalized_X,SumV,out=Normalized_X,where=SumV!=0)
    return Normalized_X

def Binary_Hashing_Index(Z):
    if np.size(Z,0)<=50000:
        Dim=8*np.size(Z,1)
        Index = faiss.IndexBinaryFlat(Dim)
        Index.nprobe = 2
    elif (np.size(Z,0)>50000)&(np.size(Z,0)<=500000):
        Dim=8*np.size(Z,1)
        Index = faiss.IndexBinaryHash(Dim,Dim)
        Index.nprobe = 2
    elif np.size(Z,0)>500000:
        Dim=8*np.size(Z,1)
        Index = faiss.IndexBinaryHash(Dim,int(np.max([np.min([np.ceil(Dim/100),32]),16])))
        Index.nprobe = 2
    return Index


def KNN_with_Hashing_Index(Z):
    StartT=time.time()
    Index=Binary_Hashing_Index(Z)
    Index.add(Z)
    Num_neighbors=2
    D, I = Index.search(Z, Num_neighbors)
    EndT=time.time()
    print(['KNN search costs-', EndT-StartT])
    return D,I

def Hashing_Function(Normalized_X,TargetDim,Method_Type):
    if Method_Type=="Linear_Kernel":
        Z=Random_Hyperplane_Hashing(Normalized_X,TargetDim)
    elif Method_Type=="Gaussian_Kernel":
        Z=Random_Fourier_Feature_Hashing(Normalized_X,TargetDim)
    elif Method_Type=="Cauchy_Kernel":
        Z=Random_Cauchy_Feature_Hashing(Normalized_X,TargetDim)
    return Z

def Renormalization_Function(X_Current,TargetDim,Iter,Method_Type):
    Normalized_X=Normalization_Function(X_Current,Method_Type)
    Z=Hashing_Function(Normalized_X,TargetDim,Method_Type)
    _,I=KNN_with_Hashing_Index(Z)
    G = nx.empty_graph(np.size(I,0))
    Edge = np.vstack((np.arange(0, np.size(I, 0)), I[:,1])).T
    G.add_edges_from(Edge)
    Clusters=[list(c) for c in list(nx.connected_components(G))]
    ClusterNum=nx.number_connected_components(G)
    print(['There are', ClusterNum, 'macro-units after', Iter+1, 'times of renormalization'])
    X_New=np.zeros((ClusterNum, np.size(X_Current,1)))
    Corase_ID = []
    for ID1 in range(ClusterNum):
        X_New[ID1,:]=np.sum(X_Current[Clusters[ID1],:],axis=0)
        Corase_ID.append(Clusters[ID1])
    return X_New, Corase_ID

def Network_Renormalization_Function(X_Current,TargetDim,Iter,Method_Type): 
    UnitNum=nx.number_of_nodes(X_Current)
    Y=Neighbor_Generator(X_Current,UnitNum)
    Z=Random_Min_Hashing(Y,TargetDim)
    Z=Hashing_Function(Z,TargetDim,Method_Type)
    _,I=KNN_with_Hashing_Index(Z)
    G = nx.empty_graph(np.size(I,0))
    Edge = np.vstack((np.arange(0, np.size(I, 0)), I[:,1])).T

    G.add_edges_from(Edge)
    Potential_Clusters=[list(c) for c in list(nx.connected_components(G))]
    Potential_ClusterNum=nx.number_connected_components(G)
    Edge_To_Remove=[]
    for ID1 in range(Potential_ClusterNum):
        Unit_list=Potential_Clusters[ID1]
        if len(Unit_list)>1:
            H = nx.induced_subgraph(X_Current,Unit_list)
            Potential_H = nx.induced_subgraph(G,Unit_list)
            Wrong_Edge=list(set(list(Potential_H.edges))-set(list(H.edges)))
            Edge_To_Remove.extend(Wrong_Edge)

    for Wrong_Edge in Edge_To_Remove:
        G.remove_edge(*Wrong_Edge)

    Clusters=[list(c) for c in list(nx.connected_components(G))]
    ClusterNum=nx.number_connected_components(G)
    print(['There are', ClusterNum, 'macro-units after', Iter+1, 'times of renormalization'])


    X_New=copy.deepcopy(X_Current)
    Pre_Corase_ID = []
    Mappings={}
    for ID1 in range(ClusterNum):
        Unit_list=Clusters[ID1]
        Pre_Corase_ID.append(Unit_list)
        Unit0 = Unit_list[0]
        Mappings[Unit0]=ID1
        for Unit in Unit_list[1:]:
            if X_New.has_node(Unit):
                Neighbors = list(X_New.neighbors(Unit))
                New_edges = [(Unit0, Nei) for Nei in Neighbors if Unit0!=Nei]
                X_New.add_edges_from(New_edges)
                X_New.remove_node(Unit)
    Corase_ID = []
    Unit_Mappings={}
    for ID_1,ID_2 in enumerate(X_New.nodes()):
        Unit_Mappings[ID_2]=ID_1
        Corase_ID.append(Pre_Corase_ID[Mappings[ID_2]])
    X_New = nx.relabel_nodes(X_New, Unit_Mappings)
    
    return X_New, Corase_ID

def Tracking_System(Corase_ID_list):
    Tracked_ID_list = []
    for IterID in range(len(Corase_ID_list)):
        if IterID==0:
            Tracked_ID_list.append(Corase_ID_list[0])
        else:
            Tracked_ID = []
            if len(Corase_ID_list[IterID])>0:
                for CoarseID in range(len(Corase_ID_list[IterID])):
                    UnitsToTrack=Corase_ID_list[IterID][CoarseID]
                    Searched_ID=[]
                    for IDSearch in range(len(UnitsToTrack)):
                        Search_ID=1
                        while len(Tracked_ID_list[IterID-Search_ID])==0:
                            Search_ID=Search_ID+1
                        Searched_ID=Searched_ID+Tracked_ID_list[IterID-Search_ID][UnitsToTrack[IDSearch]]
                    Tracked_ID.append(Searched_ID)
            Tracked_ID_list.append(Tracked_ID)
    return Tracked_ID_list

def Renormalization_Flow(X_Initial,Iteration_Num,TargetDim,Method_Type,Data_Type):
    RG_Flow=[]
    RG_Flow.append(X_Initial)
    Corase_ID_list=[]
    for Iter in range(Iteration_Num):
        StartT=time.time()
        X_Current=RG_Flow[Iter]
        if Data_Type=="Dynamics":
            X_New, Corase_ID=Renormalization_Function(X_Current,TargetDim,Iter,Method_Type)
            if np.shape(X_New)[0]==1:
                break
        elif Data_Type=="Structure":
            X_New, Corase_ID=Network_Renormalization_Function(X_Current,TargetDim,Iter,Method_Type)
            if nx.number_of_edges(X_New)==0:
                break
        RG_Flow.append(X_New)
        Corase_ID_list.append(Corase_ID)
        EndT=time.time()
        print(['The', Iter+1, 'time of renormalization costs-', EndT-StartT])
    Tracked_ID_list=Tracking_System(Corase_ID_list)
    return RG_Flow,Tracked_ID_list
    