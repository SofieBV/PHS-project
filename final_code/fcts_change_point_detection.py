import changefinder
import ruptures as rpt
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
from rupture_display import display_modified

#CHANGEFINDER

def change_finder(points):
    xpoints = points[1,:]
    f, (ax1, ax2) = plt.subplots(2, 1)
    f.subplots_adjust(hspace=0.4)
    ax1.plot(xpoints)
    ax1.set_title("data point")
    ax1.set_xticks(np.linspace(min(ax1.get_xticks()), max(ax1.get_xticks()),len(points[0,:])))
    ax1.set_xticklabels(points[0,:])
    ax1.tick_params('x',labelrotation=45)
    every_nth = 3
    for n, label in enumerate(ax1.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)

    #Initiate changefinder function
    cf = changefinder.ChangeFinder()
    scores = [cf.update(p) for p in xpoints]
    ax2.plot(scores)
    ax2.set_title("anomaly score")
    ax2.set_xticks(np.linspace(min(ax1.get_xticks()), max(ax1.get_xticks()),len(points[0,:])))
    ax2.set_xticklabels(points[0,:])
    ax2.tick_params('x',labelrotation=45)
    for n, label in enumerate(ax2.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
    plt.savefig('results/changefinder.png')
    plt.show() 

#RUPTURES PACKAGE

def pelt_search(points, title = 'Change Point Detection: Pelt Search Method'):
    #Changepoint detection with the Pelt search method
    xpoints = points[1,:]
    model="rbf"
    algo = rpt.Pelt(model=model).fit(xpoints)
    result = algo.predict(pen=5)
    rpt.display(xpoints, result, figsize=(10, 6))
    plt.title(title)
    plt.savefig('results/pelt_search.png')
    plt.show()  

def binary_segm(points, title = 'Change Point Detection: Binary Segmentation Search Method'):
    #Changepoint detection with the Binary Segmentation search method
    xpoints = points[1,:]
    model = "l2"  
    algo = rpt.Binseg(model=model).fit(xpoints)
    my_bkps = algo.predict(n_bkps=5)
    # show results
    rpt.show.display(xpoints, my_bkps, figsize=(10, 6))
    plt.title(title)
    plt.savefig('results/binary_segmentation.png')
    plt.show()

def window_based(points, title='Change Point Detection: Window-Based Search Method'):  
    #Changepoint detection with window-based search method
    xpoints = points[1,:]
    model = "l2"  
    algo = rpt.Window(width=10, model=model).fit(xpoints)
    my_bkps = algo.predict(n_bkps=5)
    rpt.show.display(xpoints, my_bkps, figsize=(10, 6))
    plt.title(title)
    plt.savefig('results/window_based.png')
    plt.show()

def dynamic_program(points, title='Change Point Detection: Dynamic Programming Search Method'):   
    #Changepoint detection with dynamic programming search method
    xpoints = points[1,:]
    model = "l1"  
    algo = rpt.Dynp(model=model, min_size=3, jump=5).fit(xpoints)
    my_bkps = algo.predict(n_bkps=5)
    rpt.show.display(xpoints, my_bkps, figsize=(10, 6))
    plt.title(title)
    plt.savefig('results/dynamic_programming.png')
    plt.show()

def all_methods(points, title):
    xpoints = points[1,:]
    
    model="rbf"
    algo = rpt.Pelt(model=model).fit(xpoints)
    result = algo.predict(pen=5)

    model = "l2"  
    algo = rpt.Binseg(model=model).fit(xpoints)
    my_bkps_bs = algo.predict(n_bkps=5)
    
    model = "l2"  
    algo = rpt.Window(width=10, model=model).fit(xpoints)
    my_bkps_wb = algo.predict(n_bkps=5)

    model = "l1"  
    algo = rpt.Dynp(model=model, min_size=3, jump=5).fit(xpoints)
    my_bkps_dp = algo.predict(n_bkps=5)

    all_xpoints = np.concatenate(([xpoints], [xpoints],[xpoints],[xpoints]),axis=0).T
    all_results = [result, my_bkps_bs, my_bkps_wb, my_bkps_dp]

    fig, axs = display_modified(all_xpoints, all_results, figsize=(10, 14))
    axs = axs.ravel()
    axs[0].set_title('Pelt Search Method')
    axs[1].set_title('Binary Segmentation Search Method')
    axs[2].set_title('Window-based Search Method')
    axs[3].set_title('Dynamic Programming Search Method')

    axs[3].set_xticks(np.linspace(min(axs[3].get_xticks()), max(axs[3].get_xticks()),len(points[0,:])))
    axs[3].set_xticklabels(points[0,:])
    axs[3].tick_params('x',labelrotation=45)
    every_nth = 4
    for n, label in enumerate(axs[3].xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)

    fig.tight_layout()
    fig.suptitle(title, size=16)
    fig.subplots_adjust(top=0.92)
    plt.savefig('results/{}.png'.format(title))
    plt.show()

