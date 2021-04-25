import numpy as np
import scipy.linalg as la 

def sghmc(data, bs, theta0, gradU, Vhat, lr = None, epochs = 200, burnin = 100, alpha = 0.01):
    '''
    Implementation of Stochastic Gradient Hamiltonian Monte Carlo (SGHMC).
    
    Input:
    
    data: np.array((n_samples = n, n_features = m)), the dataset of the problem
    
    bs: integer, the size of each minibatch in one epoch
    
    theta0: np.array(n_parameters = p, ), initial state of the sampling chain for parameters
    
    gradU: callable function used to calculate the gradient of the target distribution w.r.t. parameters
    
    Vhat: np.array((n_parameters = p, n_parameters = p)), the estimated matrix by empirical Fisher information
    
    epochs: integer, the number of iterations to run the sampling process, default set to 200
    
    burnin: integer, the number of iterations before storing sampling points, should be less than epochs, default set to 100
    
    lr: learning rate, default set to 0.01 / n_samples
    
    alpha: momentum decay, default set to 0.1
    
    Output:
    
    sampled chain for parameters by SGHMC sampler, np.array((epochs - burnin, n_parameters = p)),
        follow the posterior target distribution
    
    '''
    
    n, m = data.shape
    p = theta0.shape[0]
    lr = 0.01 / n if lr is None else lr
    
    assert bs >= 1, 'Batch size has to be greater than or equal to 1.'
    assert bs <= n, 'Batch size has to be less than or equal to the number of samples.'
    assert alpha >= 0 and alpha <= 1, 'Momentum decay has to be in the range of [0,1].'
    assert Vhat.shape == (p, p), 'The dimension of Vhat should match the shape of parameters vector.'
    assert n % bs == 0, 'Number of data should be divisible by batch size.'
    
    # new samples
    samples = np.zeros((epochs, p))
    samples[0] = theta0
    beta_hat = lr / 2 * Vhat
    
    disp = la.cholesky(2 * lr * (alpha * np.eye(p) - 2 * beta_hat))
    
    # build mini-batchs
    n_batch = int(n / bs)
    np.random.shuffle(data)
    data = data.reshape(n_batch, bs, m)
    
    # SGHMC sampling
    for i in range(epochs - 1):
        theta = samples[i]
        r = np.sqrt(lr) * np.random.rand(p)
        
        for j in range(n_batch):
            theta += r
            gradU_tilde = gradU(theta, data[j], n_batch)
            r += -alpha * r - lr * gradU_tilde.reshape(-1) + disp @ np.random.randn(p)
        
        samples[i + 1] = theta
    
    return samples
            