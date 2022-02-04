import changefinder
import ruptures as rpt
import matplotlib.pyplot as plt

#CHANGEFINDER

def change_finder(points):
    f, (ax1, ax2) = plt.subplots(2, 1)
    f.subplots_adjust(hspace=0.4)
    ax1.plot(points)
    ax1.set_title("data point")

    #Initiate changefinder function
    cf = changefinder.ChangeFinder()
    scores = [cf.update(p) for p in points]
    ax2.plot(scores)
    ax2.set_title("anomaly score")
    plt.show() 

#RUPTURES PACKAGE

def pelt_search(points, title = 'Change Point Detection: Pelt Search Method'):
    #Changepoint detection with the Pelt search method
    model="rbf"
    algo = rpt.Pelt(model=model).fit(points)
    result = algo.predict(pen=5)
    rpt.display(points, result, figsize=(10, 6))
    plt.title(title)
    plt.show()  

def binary_segm(points, title = 'Change Point Detection: Binary Segmentation Search Method'):
    #Changepoint detection with the Binary Segmentation search method
    model = "l2"  
    algo = rpt.Binseg(model=model).fit(points)
    my_bkps = algo.predict(n_bkps=5)
    # show results
    rpt.show.display(points, my_bkps, figsize=(10, 6))
    plt.title(title)
    plt.show()

def window_based(points, title='Change Point Detection: Window-Based Search Method'):  
    #Changepoint detection with window-based search method
    model = "l2"  
    algo = rpt.Window(width=10, model=model).fit(points)
    my_bkps = algo.predict(n_bkps=5)
    rpt.show.display(points, my_bkps, figsize=(10, 6))
    plt.title(title)
    plt.show()

def dynamic_program(points, title='Change Point Detection: Dynamic Programming Search Method'):   
    #Changepoint detection with dynamic programming search method
    model = "l1"  
    algo = rpt.Dynp(model=model, min_size=3, jump=5).fit(points)
    my_bkps = algo.predict(n_bkps=5)
    rpt.show.display(points, my_bkps, figsize=(10, 6))
    plt.title(title)
    plt.show()