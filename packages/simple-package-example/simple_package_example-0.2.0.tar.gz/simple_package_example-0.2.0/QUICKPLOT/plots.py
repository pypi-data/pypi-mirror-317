import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def validate_input(data):
    if isinstance(data,dict):
        return list(data.keys()) , list(data.values())
    elif(isinstance(data,list)):
        if(len(data)== 2):
            return data[0] , data[1]
        else:
            raise ValueError("In list format, two lists are required to plot x and y ")
        
    elif(isinstance(data, pd.DataFrame)):
        if len(data.columns) == 2:
            return data.iloc[:,0] , data.iloc[:,1]
        else:
            raise ValueError("Data should have exactly two columns in DataFrame format")
    elif(isinstance(data,np.ndarray)):
        if(data.ndim == 1):
            return data,data
        elif(data.ndim == 2 and data.shape[1] == 2):
            return data[:,0] , data[:,1]
        else:
            raise ValueError("For 2D numpy arrays, shape should be (n, 2) where n is the number of data points")
        
    else:
        raise ValueError("Data must be a dictionary, list, or DataFrame")






def plot_line(data,title=None,xlabel = None,ylabel = None, color  = None, linewidth=2, marker = 'o', markersize = 8, linestyle = '-'):


    x,y = validate_input(data)
    sns.lineplot(x=x , y=y , color = color,linewidth=linewidth, marker=marker,markersize = markersize, linestyle = linestyle )
    if title:
        plt.title(title)
    if(xlabel):
        plt.xlabel(xlabel)
    if(ylabel):
        plt.ylabel(ylabel)
    





    plt.show()
    # print(x)
    # print(y)

def plot_scatterplot(data, title=None, color=None, xlabel=None, ylabel=None, marker='o', s=100, linewidth=2, linestyle='-'):
    x, y = validate_input(data)
    
    sns.scatterplot(x=x, y=y, color=color, linewidth=linewidth, marker=marker, s=s, linestyle=linestyle)
    
    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    
    plt.show()


def plot_histogram(data, title=None, xlabel=None, color=None, ylabel="Frequency", bins=10, linewidth=2):

    if isinstance(data, pd.DataFrame):
            if len(data.columns) == 1:
                y = data.iloc[:, 0]
            else:
                raise ValueError("DataFrame input must have exactly one column for histogram.")
    elif isinstance(data, (list, np.ndarray)):
        y = data
    elif isinstance(data, dict):
        y = list(data.values())  # Use values for histogram
    else:
        raise ValueError("Unsupported data format for histogram. Use DataFrame, list, array, or dictionary.")

    sns.histplot(y, color=color, bins=bins, linewidth=linewidth)
    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.show()

def plot_heatmap(data,title=None, xlabel = None , ylabel = None):
    sns.heatmap(data,annot=True, fmt = ".2f", cmap="coolwarm", linewidths=0.5 , cbar=True)
    if title:
        plt.title(title)
    if(xlabel):
        plt.xlabel(xlabel)
    if(ylabel):
        plt.ylabel(ylabel)
    plt.show()
def plot_pairplot(data,title = None,hue = "day"):
    sns.pairplot(data, hue=hue)
    if title:
        plt.suptitle(title, y=1.02,)
    plt.show()
def plot_correlation_matrix(data, title=None, annot = True):
    corr = data.corr()
    sns.heatmap(corr, annot=annot,fmt=".2f",cmap="coolwarm", linewidths=0.5,cbar = True)
    if title:
        plt.title(title)
    plt.show()
def plot_regression(data, title=None, xlabel=None, ylabel=None, color='blue', line_kws=None):
    
    x, y = validate_input(data)
    sns.regplot(x=x, y=y, color=color, line_kws=line_kws)

    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)

    plt.show()