import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import gc
import scipy.stats as ss
from pairplot.log import Log

def scatter(x, y, 
            data=None,
            mode="plt",
            log=Log(), 
            verbose=True, 
            plt_kwargs=None,
            font_kwargs=None, 
            err_kwargs=None, 
            is_reg=True, 
            reg_box=None, 
            null_beta=0, 
            reg_line_kwargs = None,
            is_45_helper_line=False,
            helper_line_kwargs=None,
            
            **scatter_kwargs):
    
    if reg_box is None:
        reg_box = dict(boxstyle='round', facecolor='white', alpha=1,edgecolor="grey")
    
    if reg_line_kwargs is None:
        reg_line_kwargs ={}

    if err_kwargs is None:
        err_kwargs={"ecolor":"#cccccc","elinewidth":1}
    
    if plt_kwargs is None:
        plt_kwargs={"figsize":(8,8),"dpi":300}
    
    if scatter_kwargs is None:
        scatter_kwargs={"s":20}

    if font_kwargs is None:
        font_kwargs={'fontsize':12,'family':'sans','fontname':'Arial'}

    if helper_line_kwargs is None:
        helper_line_kwargs = {}
    
    fig, ax = plt.subplots(**plt_kwargs)
    
    if mode == "plt":
        ax.scatter(x=x,
                   y=y,
                   **scatter_kwargs)
    elif mode== "sns":
        sns.scatterplot(data=data, 
                        x=x,
                        y=y, 
                        ax=ax, 
                        **scatter_kwargs)
        x = data[x]
        y = data[y]

    xl,xh=ax.get_xlim()
    yl,yh=ax.get_ylim()

    if is_reg is True:
        reg = ss.linregress(x,y)
        #### calculate p values based on selected value , default = 0 
        log.write(" -Calculating p values based on given null slope :",null_beta, verbose=verbose)
        p =  reg[3]
        #ss.t.sf(abs(t_score), df=degree)*2
        log.write(" -Beta = ", reg[0], verbose=verbose)
        log.write(" -Beta_se = ", reg[4], verbose=verbose)
        #log.write(" -H0 beta = ", null_beta, ", recalculated p = ", "{:.2e}".format(p), verbose=verbose)
        log.write(" -H0 beta =  0",", default p = ", "{:.2e}".format(reg[3]), verbose=verbose)
        log.write(" -Peason correlation coefficient =  ", "{:.2f}".format(reg[2]), verbose=verbose)
        log.write(" -r2 =  ", "{:.2f}".format(reg[2]**2), verbose=verbose)

        if reg[0] > 0:
            #if regression coeeficient >0 : auxiliary line slope = 1
            if is_45_helper_line is True:
                
                ax.axline([min(xl,yl),min(xl,yl)], 
                          [max(xh, yh),max(xh, yh)],
                          zorder=1,**helper_line_kwargs)

            #add text
            try:
                p12=str("{:.2e}".format(p)).split("e")[0]
                pe =str(int("{:.2e}".format(p).split("e")[1]))
            except:
                p12="0"
                pe="0"
            p_text="$p = " + p12 + " \\times  10^{"+pe+"}$"
            p_latex= f'{p_text}'
            ax.text(0.98,0.02,"$y =$ "+"{:.2f}".format(reg[1]) +" $+$ "+ "{:.2f}".format(reg[0])+" $x$, "+ p_latex + ", $r =$" +"{:.2f}".format(reg[2]), va="bottom",ha="right",transform=ax.transAxes, bbox=reg_box, **font_kwargs)
        else:
            #if regression coeeficient <0 : auxiliary line slope = -1
            if is_45_helper_line is True:
                ax.axline([min(xl,yl),-min(xl,yl)], [max(xh, yh),-max(xh, yh)],zorder=1,**helper_line_kwargs)
            #add text
            try:
                p12=str("{:.2e}".format(p)).split("e")[0]
                pe =str(int("{:.2e}".format(p).split("e")[1]))
            except:
                p12="0"
                pe="0"
            p_text="$p = " + p12 + " \\times  10^{"+pe+"}$"
            p_latex= f'{p_text}'
            ax.text(0.98,0.02,"$y =$ "+"{:.2f}".format(reg[1]) +" $-$ "+ "{:.2f}".format(abs(reg[0]))+" $x$, "+ p_latex + ", $r =$" +"{:.2f}".format(reg[2]), va="bottom",ha="right",transform=ax.transAxes,bbox=reg_box,**font_kwargs)
    
        ax.axline(xy1=(xl,xl*reg[0] + reg[1]),slope=reg[0],color="#cccccc",linestyle='--',zorder=1,**reg_line_kwargs)

    return fig,ax