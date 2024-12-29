import numpy as np
from numpy import linalg as LA
from scipy.linalg import pinv
class ReLORETA():
  # lambda1: ReLORETA regularisation parameter
  # epsilo:  the threshold to stop eLORETA. It is usually set to a high value to let max_iter stop the algorithm. 
  # max_iter: The maximum number of iteration
  # W: The block diagonal weight matrix of size k*k, obtained from the eLORETA function
  # K: The lead field matrix of size m*k
  # X: The input EEG matrix of size m*n
  # m: the number of electrodes
  # k: number of voxels (dipoles or source points) set by user
  # n_source: number of voxels (dipoles or source points) set by user
  # dimension: Leadfield matrix dimension
  # n: number of EEG samples in the X matrix
  # lambda2: eLORETA regularisation parameter
  # n_source: number of source points
 
  def __init__(self,lambda2 = 0.05, dimension=3,n_source=82, epsilon=1e-29, max_iter=100,lambda1=1,lr=1e8): # alpha could be 0.1
    self.max_iter=max_iter
    self.lambda2=lambda2
    self.dimension=dimension
    self.n_source=n_source
    self.epsilon=epsilon
    self.lambda1=lambda1
    self.lr=lr
    self.y=[]
    self.W=[]
    self.K=[]
    self.er=[]
  @property
  def get(self):
      return self.max_iter, self.lambda2, self.dimension, self.n_source, self.epsilon, self.lambda1
  @get.setter
  def set(self, values):
    self.max_iter, self.lambda2, self.dimension, self.n_source, self.epsilon, self.lambda1=values

  def eloreta_source_localization(self,eeg_data, leadfield, noise_cov):
      """
      Perform source localization using the eLORETA method.

      Parameters:
          eeg_data (numpy.ndarray): EEG data matrix (channels x time points)
          leadfield (numpy.ndarray): Lead field matrix (channels x sources)
          noise_cov (numpy.ndarray): Noise covariance matrix (channels x channels)

      Returns:
          numpy.ndarray: Source activity matrix (sources x time points)
      """
      # Regularization parameter (small value to stabilize inversion)
      lambda2 = 0.05

      # Step 1: Whitening the data using noise covariance matrix
      whitener = pinv(np.sqrt(noise_cov))
      whitened_eeg = np.dot(whitener, eeg_data)
      whitened_leadfield = np.dot(whitener, leadfield)

      # Step 2: Compute the source covariance matrix
      leadfield_t = whitened_leadfield.T
      source_cov = np.dot(leadfield_t, whitened_leadfield) + lambda2 * np.eye(leadfield.shape[1])

      # Step 3: Compute the eLORETA inverse operator
      inverse_operator = np.dot(np.linalg.pinv(source_cov), leadfield_t)

      # Step 4: Compute source activity
      source_activity = np.dot(inverse_operator, whitened_eeg)

      return source_activity
  def fit(self, X,K,source_points=[],real_source=[]):
    # real_source: The real source coordinates. A list of three elements, x,y, and z
    # source_points: The dipoles (source points) coordinates. For example, if the source has 30 points, 
    # source_points will be a list including 30 points' coordinates. Each point's coordinates should be a list with 3 elements, i. e. x,y, and z
    epsilon=self.epsilon
    max_iter=self.max_iter
    lambda1=self.lambda1
    lr=self.lr
    X=np.array(X)
    K_all=[]
    X_rel_all=[]
    pow_all=[]
    source_points=np.array(source_points)
    real_source=np.array(real_source)

    K_all.append(K)

    # y=np.array(y)
    k=K.shape[1]
    n=X.shape[1]
    m=K.shape[0]
    R=np.identity(m)
    flag=0
    I=np.identity(m)
    lambda1=lambda1
    iter=0
    k_stop=0 # number of times the objective function can not improve
    E=[]
    y_rel_all=[]
    noise_cov = np.identity(m)
    y = self.eloreta_source_localization(X, K, noise_cov)
    self.y=y.copy()
    self.power()
    pow_all.append(self.pow)
    y_rel_all.append(y)
    # Calculating objective function before the update
    X_rel=K.dot(y)
    X_rel_all.append(X_rel)
    Ei=(LA.norm(X-X_rel,ord='fro'))       # For testing. Active the Ei above if you want the original
    E.append(Ei)
    print("Iteration {}\n".format(iter))
    print("ReLORETA error {}\n".format(abs(E[0])))
    if real_source.shape[0]!=0:
      self.localisation_error(source_points, real_source)
      le=self.error
      print("Localisation error {}\n".format(le))
  
  
    while flag==0:
      iter=iter+1
      print("Iteration {}\n".format(iter))
      #Calculating D
      t1=R.dot(K).dot(y)  #### Bottleneck: here we can also use K_new. In this case you need to set K_new=K.copy() before starting the while loop
      t2=t1-X
      t3=np.transpose(K.dot(y))  #### Bottleneck: X shoul be replaced in each iteration
      D=2*t2.dot(t3)
      #Updating R
      t4=np.linalg.inv(I+(lambda1*I))
      R=R-lr*t4.dot(D)    ### Bottleneck: 0.1 could be removed
      #Updating leadfield matrix
      K_new=R.dot(K)
      self.K=K_new.copy()
      K_all.append(K_new)
      # Calculating objective function after the update
      noise_cov = np.identity(m)
      y = self.eloreta_source_localization(X, K_new, noise_cov)
      self.y=y.copy()
      self.power()
      pow_all.append(self.pow)
      #####################
      # self.fit(K_new,X,dimension,n_source)
      # y=self.y.copy()
      #####################
      y_rel_all.append(y)
      X_rel=K_new.dot(y)
      X_rel_all.append(X_rel)
      ###############
      # Ei=(LA.norm(X-X_rel,ord='fro'))**2   # The original objective function
      # Ei=Ei/m
      ###############
      Ei=(LA.norm(X-X_rel,ord='fro'))       # For testing. Uncomment the above code if you want the original activation function. You may need to adjust lr then. 
      ###############
      E.append(Ei)
      print("ReLORETA error {}\n".format(abs(E[iter])))
      if real_source.shape[0]!=0:
        self.localisation_error(source_points, real_source)
        le=self.error
        print("Localisation error {}\n".format(le))
      # Levenberg-Marquardt 
      if abs(E[iter]-E[iter-1])<epsilon:
        k_stop=k_stop+1

      if k_stop >= 1:
        print("Minimum error achieved")
        flag=1
      elif iter >= max_iter:
        print("Maximum iterations exceeded")
        flag=1
      else:
        if E[iter]-E[iter-1]<=0:
          lambda1=lambda1*0.1
        else:
          lambda1=lambda1*10

    self.E=E.copy()
    self.y=y.copy()
    self.y_rel=y.copy()
    self.K_rel=K_new.copy()
    self.y_rel_all=y_rel_all.copy()
    self.X_rel=X_rel.copy()
    self.X_rel_all=X_rel_all.copy()
    self.K_all=K_all.copy()
    self.pow_all=pow_all.copy()
  #Calculating the source power
  def power(self):
    dim=self.dimension
    n_source=self.n_source
    y=self.y.copy()
    y=np.array(y)
    pow=[]
    if dim==1:
      for i in range(y.shape[0]):
        pow.append(np.mean(y[i,:]**2))
    else:
      for i in range(n_source):
        yy=y[i*3:i*3+3,:]
        yy=np.sum(yy**2,axis=0)
        pow.append(np.mean(yy))
    self.pow=np.array(pow).copy()
  # Localising the source
  def localise(self,source_points):
    #source_points is n_source*3
    source_points=list(source_points)
    self.power()
    pow=self.pow.copy()
    source=source_points[np.argmax(pow)]
    self.source=source.copy()
  # Calculating the localisation error
  def localisation_error(self,source_points, real_source):
    real_source=list(real_source)
    self.localise(source_points)
    source=self.source.copy()
    error=LA.norm(source-real_source,ord=2)
    self.error=error.copy()

def plot_numpy_array(array, title='Numpy Array Plot'):
    """
    Plot a 1D numpy array.

    Parameters:
        array (numpy.ndarray): 1D array to plot.
        title (str): Title of the plot.
    """

    plt.plot(array)
    plt.title(title)
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.grid(True)
    plt.show()