import numpy as np
from scipy.optimize import curve_fit
import statsmodels.api as sm
import networkx as nx
from scipy.stats import ks_2samp

def Linear_func(x, a, b):
    return b*x+a

def Power_func(x, a):
    return a*x


def RSquareFun(X,y,popt):
    if len(popt)==2:
        pre_y = Linear_func(X, popt[0], popt[1])
    elif len(popt)==1:
        pre_y = Power_func(X, popt[0])
    mean = np.mean(y)  
    ss_tot = np.sum((y - mean) ** 2)  
    ss_res = np.sum((y - pre_y) ** 2)  
    r_squared = 1 - (ss_res / ss_tot)

    mse = np.sum((y - pre_y) ** 2)/ len(y)
    return r_squared, mse

def Alpha_Scaling(RG_Flow,Tracked_ID_list):
    MeanVar=np.zeros(len(RG_Flow))
    for Iter in range(len(RG_Flow)):
        X=RG_Flow[Iter]
        MeanVar[Iter]=np.mean(np.var(X,axis=1))
    
    MeanClusterSize=np.ones(len(RG_Flow))
    for Iter in range(len(Tracked_ID_list)):
        ClusterSize=[len(IDC) for IDC in Tracked_ID_list[Iter]]
        MeanClusterSize[Iter+1]=np.mean(ClusterSize)

    popt, _ = curve_fit(Linear_func, np.log(MeanClusterSize), np.log(MeanVar))
    Coeff = popt[0]
    Alpha = popt[1]
    R2, MSE= RSquareFun(np.log(MeanClusterSize), np.log(MeanVar), popt)
    Esti_Alpha_Scaling=np.exp(Coeff)*np.power(MeanClusterSize,Alpha)
    return MeanClusterSize, MeanVar, Coeff, Alpha, R2, MSE, Esti_Alpha_Scaling

def Beta_Scaling(RG_Flow,Tracked_ID_list):
    FreeEV=np.zeros(len(RG_Flow))
    for Iter in range(len(RG_Flow)):
        X=RG_Flow[Iter]

        P_SilenceV=np.zeros(np.size(X,0))
        for ID1 in range(np.size(X,0)):
            P_SilenceV[ID1] = 1-np.count_nonzero(X[ID1,:]) / np.size(X,1)
        P_Silence=np.mean(P_SilenceV)
        FreeEV[Iter]=-1*np.log(P_Silence)

    MeanClusterSize=np.ones(len(RG_Flow))
    for Iter in range(len(Tracked_ID_list)):
        ClusterSize=[len(IDC) for IDC in Tracked_ID_list[Iter]]
        MeanClusterSize[Iter+1]=np.mean(ClusterSize)

    Needed=np.where(np.isinf(FreeEV)==0)[0]
    FreeEV=FreeEV[Needed]
    MeanClusterSize=MeanClusterSize[Needed]

    popt, _ = curve_fit(Linear_func, np.log(MeanClusterSize), np.log(FreeEV))
    Coeff = popt[0]
    Beta = popt[1]
    R2, MSE= RSquareFun(np.log(MeanClusterSize), np.log(FreeEV), popt)
    Esti_Beta_Scaling=np.exp(Coeff)*np.power(MeanClusterSize,Beta)
    return MeanClusterSize, FreeEV, Coeff, Beta, R2, MSE, Esti_Beta_Scaling

def Mu_Scaling(RG_Flow,Tracked_ID_list):
    Initial_X = RG_Flow[0]
    Average_Rank_K=[]
    Average_Evals=[]

    ClusterNum=np.array([len(Tracked_ID_list[ID1]) for ID1 in range(1,len(Tracked_ID_list))])
    Max_Range=np.max(np.where(ClusterNum>1)[0])+2
    for ID1 in range(1,Max_Range):
        x=[]
        y=[]
        for ID2 in range(len(Tracked_ID_list[ID1])):
            WithinCluster= Tracked_ID_list[ID1][ID2]
            X_WC = Initial_X[WithinCluster,:]
            X_WC=X_WC-np.mean(X_WC,axis=1).reshape(np.size(X_WC,0),1)
            Cov=np.cov(X_WC)
            Evals, _ = np.linalg.eig(Cov)
            Evals = np.sort(np.real(Evals))
            Evals = Evals[::-1]
            
            Rank = np.cumsum(np.ones(len(Evals)))
            Rank_K=Rank/len(WithinCluster)
        
            Needed_Loc=np.where(Evals>0)[0]
            Rank_K=Rank_K[Needed_Loc]
            Evals=Evals[Needed_Loc]
            x.extend(Rank_K[:]) 
            y.extend(Evals[:])

        _, bins = np.histogram(x)
        Meanx=np.zeros(len(bins)-1)
        Meany=np.zeros(len(bins)-1)
        for ID3 in range(len(bins)-1):
            Neededx=np.where((x>=bins[ID3])&(x<=bins[ID3+1]))[0]
            Meanx[ID3]=np.mean(np.array(x)[Neededx])
            Meany[ID3]=np.mean(np.array(y)[Neededx])
        Average_Rank_K.extend(Meanx)
        Average_Evals.extend(Meany)
    
    popt, _ = curve_fit(Linear_func, np.log(Average_Rank_K), np.log(Average_Evals))
    Coeff = popt[0]
    Mu = -1* popt[1]
    R2, MSE= RSquareFun(np.log(Average_Rank_K), np.log(Average_Evals), popt)
    Esti_Mu_Scaling=np.exp(Coeff)*np.power(Average_Rank_K,-1* Mu)
    return Average_Rank_K, Average_Evals, Coeff, Mu, R2, MSE, Esti_Mu_Scaling

def Theta_Scaling(RG_Flow,Tracked_ID_list):
    Tau=np.zeros(len(RG_Flow))
    ScaledT=[]
    MeanACFs=[]

    for Iter in range(len(RG_Flow)):
        X=RG_Flow[Iter]

        ACFMatrix = np.zeros_like(X)
        for ID1 in range(np.size(X,0)):
            ACFMatrix[ID1,:] = sm.tsa.acf(X[ID1,:], nlags=np.size(X,1))
        MeanACF = np.mean(ACFMatrix, axis=0)
        T = np.cumsum(np.ones(np.size(X,1)))-1

        Needed_ACF=np.where(MeanACF>0)[0]
        MeanACF=MeanACF[Needed_ACF]
        T=T[Needed_ACF]

        Cut_Off=int(np.max([np.ceil(0.01*len(T)),100]))
        popt, _ = curve_fit(Power_func, T[:Cut_Off], np.log(MeanACF[:Cut_Off]))
        Tau[Iter] = -1/popt[0]

        ScaledT.append(T/Tau[Iter])
        MeanACFs.append(MeanACF)
    
    MeanClusterSize=np.ones(len(RG_Flow))
    for Iter in range(len(Tracked_ID_list)):
        ClusterSize=[len(IDC) for IDC in Tracked_ID_list[Iter]]
        MeanClusterSize[Iter+1]=np.mean(ClusterSize)
    
    popt, _ = curve_fit(Linear_func, np.log(MeanClusterSize), np.log(Tau))
    Coeff = popt[0]
    Theta = popt[1]
    R2, MSE= RSquareFun(np.log(MeanClusterSize), np.log(Tau), popt)
    Esti_Theta_Scaling=np.exp(Coeff)*np.power(MeanClusterSize,Theta)

    return ScaledT, MeanACFs, MeanClusterSize, Tau, Coeff, Theta, R2, MSE, Esti_Theta_Scaling

def KS_Analysis(RG_Flow):
    K_S_Static=np.zeros(len(RG_Flow))
    Degrees_O=[Node[1] for Node in list(nx.degree(RG_Flow[0]))]
    for InterID in range(len(RG_Flow)):
        Degrees=[Node[1] for Node in list(nx.degree(RG_Flow[InterID]))]
        KstestResult=ks_2samp(Degrees, Degrees_O, alternative='two-sided',method='exact')
        K_S_Static[InterID]=KstestResult[0]*(KstestResult[1]<0.01)

    Mean_K_S_Static=np.mean(K_S_Static)
    return Mean_K_S_Static

def Normalized_Dynamics(RG_Flow,Tracked_ID_list,Cut_Off_Ratio):
    ClusterNum=np.array([len(Tracked_ID_list[ID1]) for ID1 in range(1,len(Tracked_ID_list))])
    Max_Range=np.max(np.where(ClusterNum>1)[0])+1
    for IterID in range(Max_Range):
        X_Current=RG_Flow[IterID]
        N=np.size(X_Current,0)
        Covariance = np.cov(X_Current)
        Evals, U = np.linalg.eig(Covariance)
        Idx = Evals.argsort()[::-1]
        EigenValues = Evals[Idx]
        EigenVectors = U[:,Idx]
        k=int(np.round(N*Cut_Off_Ratio))
        P=EigenVectors[:,:k] @ EigenVectors[:,:k].T
        phi=P@(X_Current-np.mean(X_Current,axis=1,keepdims=True))
        Normalized_activity=phi/np.std(phi,axis=1,keepdims=True)
    return Normalized_activity