import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.multitest import fdrcorrection
from pairplot.log import Log
import matplotlib as mpl
import matplotlib.patches as patches

def pairplot_long(df, column, value, correction=False,index=False,h_pad=0.2, w_pad=0.2,hue=None):
    # index column value
    # ID1 Feature1 Value1
    # ID1 Feature2 Value2
    # ID1 Feature3 Value3
    # ID1 Feature1 Value1
    # ID1 Feature2 Value2
    # ID1 Feature3 Value3
    # ID1 Feature1 Value1
    # ID1 Feature2 Value2
    # ID1 Feature3 Value3
    if index!=False:
        if pd.api.types.is_list_like(index)==True: 
            cols_to_use =index+[column]+[value]
        else:
            cols_to_use =[index]+[column]+[value]
    df = df.loc[:,cols_to_use].copy()
    
    wide_df = pd.pivot(df, index=index, columns=column, values = value)
    wide_df = wide_df.reset_index()
    # input a wide dataframe : 
    # row->ID 
    # column->data
    myplotGrid(wide_df, df[column].unique(),correction,h_pad=h_pad, w_pad=w_pad,hue=hue)

    
def pairplot_wide(wide_df, 
                  correction=False, 
                  column=False,
                  h_pad=0.1, 
                  w_pad=0.1,
                  r_mode="p",
                  diag_mode="kde",
                  is_reg=True,
                  label_font_kwargs=None,
                  r_font_kwargs=None,
                  fig_kwargs=None,
                  tick_kwargs = None,
                  legend_kwargs=None,
                  scatter_kwargs=None,
                  hist_kwargs=None,
                  kde_kwargs=None,
                  hue=None,
                  log=Log()):
                  
    if label_font_kwargs is None:
        label_font_kwargs={"size":20}
    if r_font_kwargs is None:
        r_font_kwargs={"size":20}
    if tick_kwargs == None:
        tick_kwargs={"labelsize":15}
    if legend_kwargs is None:
        legend_kwargs = {"fontsize":20,"markerscale":3}
    if fig_kwargs is None:
        fig_kwargs = {"dpi":100, "figsize":(3,3)}
    if scatter_kwargs is None:
        scatter_kwargs = {"sizes":(20,40)}
    if hist_kwargs is None:
        hist_kwargs = {}
    if kde_kwargs is None:
        kde_kwargs={}

    log.write("Creating pariplot in wide format data...") 
    log.write(" -Correlationr mode: {}".format(r_mode)) 
    #      Feature1 Feature2 Feature3
    # ID1  Value1 Value2 Value3
    # ID2  Value1 Value2 Value3
    # ID3  Value1 Value2 Value3
    if column == False:
        column_to_plot = list()
        for i in wide_df.columns:
            if pd.api.types.is_numeric_dtype(wide_df[i])==True:
                column_to_plot.append(i)
    else:
        column_to_plot = column        
    
    if hue is not None:
        hue_col = [hue]
    else:
        hue_col = []

    wide_df = wide_df.loc[:,column_to_plot + hue_col].copy()
    
    # input a wide dataframe : 
    # row->ID 
    # column->data
    myplotGrid(wide_df, 
               column_to_plot, 
               correction,
               hue=hue,
               h_pad=h_pad, 
               w_pad=w_pad, 
               r_mode=r_mode,
               diag_mode=diag_mode,
               is_reg=is_reg,
               label_font_kwargs=label_font_kwargs, 
               r_font_kwargs=r_font_kwargs,
               fig_kwargs=fig_kwargs,
               tick_kwargs=tick_kwargs,
               legend_kwargs=legend_kwargs,
               hist_kwargs=hist_kwargs,
               log=log,
               kde_kwargs=kde_kwargs,
               scatter_kwargs=scatter_kwargs)

def myplotGrid(df, 
               columns, 
               correction,
               hue,
               h_pad, 
               w_pad, 
               r_mode, 
               diag_mode,
               is_reg,
               label_font_kwargs, 
               r_font_kwargs, 
               fig_kwargs, 
               tick_kwargs,
               log,
               legend_kwargs,
               hist_kwargs,
               kde_kwargs,
               scatter_kwargs):
    
    feature_count = len(columns)
    # Create a matplot subplot area with the size of [feature count x feature count]
    fig, axis = plt.subplots(nrows=feature_count, 
                             ncols=feature_count,subplot_kw=dict(box_aspect=1),
                             **fig_kwargs)

    # set sharx and sharey
    for row_n in range(feature_count):
        for col_n in range(feature_count):
            if col_n < row_n:
                if row_n<feature_count-1:
                    axis[row_n, col_n].sharex(axis[feature_count-1, col_n])
                if col_n>0:
                    axis[row_n, col_n].sharey(axis[row_n, 0])
            if col_n == row_n:
                axis[row_n, col_n].sharex(axis[feature_count-1, col_n])
    
    #for i in range(feature_count):
    #    axis[feature_count-1, i].xaxis.set_tick_params(labelbottom=True)
    #for i in range(feature_count):
    #    axis[i, 0].yaxis.set_tick_params(labelbottom=True)


    # Setting figure size helps to optimize the figure size according to the feature count.
    fig.set_size_inches(feature_count * 4, feature_count * 4)
    
    fig.subplots_adjust(wspace=0.01, hspace=0.01 )
    fig.tight_layout(h_pad=h_pad, w_pad=w_pad)

    cmap = mpl.cm.RdBu
    norm = mpl.colors.Normalize(vmin=-1, vmax=1)
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                ax=axis, location = "right", label='r',
                fraction=0.05, 
                pad=0,  
                shrink=0.4, 
                anchor=(1,0.94))
    cbar.ax.set_title('Correlation',loc="left",y=0.98,pad=25, fontsize=20)
    cbar.ax.tick_params(labelsize=20)
    #       col0 col1 col2
    # row0  plot0 plot1 plot2
    # row1  plot3 plot4 plot5
    # row2  plot6 plot7 plot8

    # Iterate through features to plot pairwise.
    n = len(df)
    for i in range(len(columns)):
        for j in range(len(columns)):
            plot_single_pair(axis, 
                             fig = fig,
                             i=i, 
                             j=j, 
                             df = df, 
                             columns = columns,
                             dpi = fig.dpi,
                             correction = correction, 
                             hue=hue,
                             is_reg=is_reg,
                             r_mode=r_mode,
                             label_font_kwargs=label_font_kwargs,
                             r_font_kwargs=r_font_kwargs,
                             log=log,
                             diag_mode=diag_mode,
                             tick_kwargs=tick_kwargs,
                             legend_kwargs=legend_kwargs,
                             hist_kwargs=hist_kwargs,
                             kde_kwargs=kde_kwargs,
                             scatter_kwargs=scatter_kwargs)

    #fig.suptitle("{} (n={})".format(target,n),fontsize=20,y=0.92)
    
def plot_single_pair(ax, 
                    fig,
                     i, 
                     j, 
                     df, 
                     columns,
                     dpi,
                     correction,
                     hue, 
                     is_reg,
                     r_mode,
                     diag_mode,
                     label_font_kwargs,
                     r_font_kwargs,
                     log, 
                     tick_kwargs,
                     legend_kwargs,
                     hist_kwargs,
                     kde_kwargs,
                     scatter_kwargs):
    
    # j : column -> x
    x_name = columns[j]
    # i : column -> y
    y_name = columns[i]
    log.write(" -Creating subplot row #{} - {}  , column #{} - {}".format(i+1, y_name, j+1,x_name)) 
    # Plot distribution histogram if the features are the same (diagonal of the pair-plot).
    if i == j:
        tdf = df.loc[:, [x_name]].copy()
    else:
        tdf = df.loc[:, [x_name, y_name]].copy()

    if hue==None:
        tdf["color"] = "None"
        hue_order=None
    else:
        tdf["color"] = df[hue]
        hue_order = df[hue].sort_values().unique()  

    if i == j:
        #ax[i, j].hist(tdf, bins = 30, ec="black",fc="#8CBAD8")    
        #sns.histplot(data=tdf, kde=True, ax=ax[i, j])
        
        #tdf_hist = pd.melt(tdf, 
        #                   value_vars=[x_name], 
        #                   var_name='melt')
        #print(tdf)
        if diag_mode=="hist":
            sns.histplot(data=tdf, 
                        x = x_name,
                        ax=ax[i, j],
                        hue ="color",
                        hue_order=hue_order, 
                        legend=None,
                        **hist_kwargs)
        elif diag_mode=="kde":
            sns.kdeplot(data=tdf, 
                        x = x_name,
                        ax=ax[i, j],
                        hue ="color",
                        hue_order=hue_order, 
                        legend=None,
                        fill=True,
                        alpha=0.5,
                        **kde_kwargs)

    elif i>j:
        # lower triangle
        # other wise plot the pair-wise scatter plot

        tdf, hue_order = _correction(tdf, correction,x_name,y_name)

        if is_reg == True:
            sns.regplot(x=x_name, y=y_name, data=tdf, ci=None, ax=ax[i, j],scatter_kws={"s":0},truncate=False, line_kws={"color":"#cccccc", 'linestyle':'--'})
        
        legend = False
        if i==1 and j==0 and hue is not None: 
            legend=True

        sns.scatterplot(x=x_name, y=y_name, data=tdf, ax=ax[i, j],hue ="color",hue_order=hue_order, legend=legend, **scatter_kwargs)

    elif  i<j:
        # upper triangle
        #tdf = df.loc[:, [x_name,y_name]].dropna().copy()
        r,color = _calculate_r(tdf,x_name,y_name,r_mode)
        
        _print_r(ax[i, j], r, tdf ,color, r_font_kwargs)

        ax[i, j].get_xaxis().set_visible(False)
        ax[i, j].get_yaxis().set_visible(False)
        ax[i, j].set_ylim([0,1])
        ax[i, j].set_xlim([0,1])
        
        _plot_r(r, ax[i, j])

        ax[i, j].set_xlim(0,1)
        ax[i, j].set_ylim(0,1)
    if hue is not None:    
        if i==1 and j==0:
            #ax[i, j].legend(bbox_to_anchor=(0, 1),ncol=tdf["color"].nunique())
            handles, labels = ax[i,j].get_legend_handles_labels()
            #
            #title_handles = [plt.plot([],marker="", ls="")]
            #handles = title_handles + handles
            #labels = [hue] + labels
            fig.legend(handles, 
                       labels, 
                       alignment="left",
                       loc='lower left',
                       bbox_to_anchor=(0.94, 0),
                       ncol=1,
                       title="  "+hue,
                       title_fontsize=legend_kwargs["fontsize"],
                       frameon=False,
                       **legend_kwargs)
            
            #sns.move_legend(
            #        fig, "lower center",
            #        bbox_to_anchor=(.5, 1), ncol=4, frameon=False,
            #    )
            ##sns.move_legend(fig, "upper left", bbox_to_anchor=(0, 1),ncol=tdf["color"].nunique())


            #handles, labels = ax[i, j].get_legend_handles_labels()
#
            #ph = [plt.plot([],marker="", ls="")[0]]
            #handles = ph + handles
            #new_labels = ["{} :".format(hue)] + labels
#
            #leg = fig.legend(labels = new_labels,  
            #                 handles=handles, 
            #                 loc="upper left", 
            #                 markerscale=3,
            #                 bbox_to_anchor=(0.92, 0.4), 
            #                 ncol=1, title=None, frameon=False, fontsize=25)
#
            #for vpack in leg._legend_handle_box.get_children()[:1]:
            #    for hpack in vpack.get_children():
            #        hpack.get_children()[0].set_width(0)
            #sns.move_legend(ax[i,j], "upper left", bbox_to_anchor=(0.92, 0.4),ncol=1)
            ax[i,j].get_legend().remove()
            
    # Print the feature labels only on the left side of the pair-plot figure
    # and bottom side of the pair-plot figure. 
    # Here avoiding printing the labels for inner axis plots.

    _configure_xy_labels(ax,i,j,x_name, y_name, columns,label_font_kwargs,tick_kwargs)
    







####################################################################################################################################
def _configure_xy_labels(ax,i,j,x_name, y_name, columns,label_font_kwargs,tick_kwargs):
    # Print the feature labels only on the left side of the pair-plot figure
    # and bottom side of the pair-plot figure. 
    # Here avoiding printing the labels for inner axis plots.
    ax[i, j].tick_params(axis='both', which='major', **tick_kwargs)
    ax[i, j].tick_params(axis='both', which='minor', **tick_kwargs)
    # bottom row
    if i == len(columns) - 1:
        ax[i, j].set_xlabel(x_name,**label_font_kwargs)
        ax[i, j].set_ylabel("",**label_font_kwargs)   

    # first column
    if j == 0:
        if i == len(columns) - 1:
        # last row
        # corner
            ax[i, j].set_xlabel(x_name,**label_font_kwargs)
            ax[i, j].set_ylabel(y_name,**label_font_kwargs)
        else:
        # not corner
            ax[i, j].set_xlabel("",**label_font_kwargs)
            ax[i, j].set_ylabel(y_name,**label_font_kwargs)
    
    # empty
    if (i!=len(columns) - 1) & (j != 0):
        # not first column & not law row
        ax[i, j].set_xlabel("",**label_font_kwargs)
        ax[i, j].set_ylabel("",**label_font_kwargs)
    
    if (i!=len(columns) - 1):
        #ax[i, j].set_xticklabels("",**label_font_kwargs)
        plt.setp(ax[i, j].get_xticklabels(), visible=False)   
    if j!=0:
        #ax[i, j].set_yticklabels("",**label_font_kwargs)
        plt.setp(ax[i, j].get_yticklabels(), visible=False)     
####################################################################################################################################

def _calculate_r(tdf,x_name,y_name,r_mode):
    tdf = tdf.dropna()
    if r_mode == "p" or r_mode == "pearson":
        r , p = stats.pearsonr(tdf[x_name],tdf[y_name])
    elif  r_mode == "s" or r_mode == "spearman":
        r , p = stats.spearmanr(tdf[x_name],tdf[y_name], nan_policy="omit")
    
    if r > 0.5:
        color = "white"
    else: 
        color = "black"
    return r, color
        
def _print_r(ax, r, tdf ,color, r_font_kwargs):
    ax.text(.5, .5,"$r = {:.2f}$\n$N = {}$".format(r,len(tdf)), transform=ax.transAxes, ha="center",color=color,**r_font_kwargs)

def _plot_r(r, ax):
    cmap = matplotlib.cm.get_cmap('RdBu')
    if r >0:
        color = matplotlib.colors.rgb2hex(cmap(0.5 + r/2))
    else:
        color = matplotlib.colors.rgb2hex(cmap(0.5 - r/2))
    s_x= (1-abs(r))/2
    s_y= (1-abs(r))/2
    s_h= abs(r)
    s_w= abs(r)
    rect = patches.Rectangle((s_x, s_y), s_h, s_w, linewidth=0, edgecolor='r', facecolor=color)
    ax.add_patch(rect)   

def r2(x, y):
    return stats.pearsonr(x, y)[0] ** 2

def _correction(tdf, correction,x_name,y_name):
    if correction == "fdr":    
        tdf["fdr_x"] =  fdrcorrection(np.power(10, -tdf[x_name]))[0]
        tdf.loc[tdf["fdr_x"],"color"]="One"
        tdf["fdr_y"] = fdrcorrection(np.power(10, -tdf[y_name]))[0]
        tdf.loc[tdf["fdr_y"],"color"]="One"
        tdf.loc[tdf["fdr_x"]&tdf["fdr_y"],"color"]="Both"
        hue_order=["None","Both","One"]
    elif correction == "bon":
        tdf["b_x"] =  np.power(10, -tdf[x_name]) <0.05/len(tdf)/4
        tdf.loc[tdf["b_x"],"color"]="One"
        tdf["b_y"] =  np.power(10, -tdf[y_name]) <0.05/len(tdf)/4
        tdf.loc[tdf["b_y"],"color"]="One"
        tdf.loc[tdf["b_x"]&tdf["b_y"],"color"]="Both"
        hue_order=["None","Both","One"]
        #tdf = tdf.sort_values("color",ascending=False)
    else:
        hue_order=None
        pass
    return tdf, hue_order