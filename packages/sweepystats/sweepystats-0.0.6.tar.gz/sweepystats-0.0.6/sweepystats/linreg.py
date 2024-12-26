import sweepystats as sw
import numpy as np
from tqdm import tqdm

class LinearRegression:
    """
    A class to perform linear regression based on the sweep operation. 
    """
    def __init__(self, X, y):
        # Convert inputs to NumPy arrays if they are not already
        self.X = np.array(X) if not isinstance(X, np.ndarray) else X
        self.y = np.array(y) if not isinstance(y, np.ndarray) else y

        # initialize SweepMatrix class
        XtX = np.matmul(X.T, X)
        Xty = np.matmul(X.T, y).reshape(-1, 1)
        yty = np.array([[np.dot(y, y)]])
        A = np.block([
            [XtX, Xty],
            [Xty.T, yty],
        ])
        self.A = sw.SweepMatrix(A)
        self.n = self.X.shape[0]
        self.p = self.X.shape[1]

        # vector to keep track of how many times a variable was swept
        self.swept = np.zeros(self.p)

    def is_fitted(self):
        if np.all(vector == 1):
            return True
        return False

    def include_k(self, k, force=False):
        """Include the `k`th variable in regression"""
        if self.swept[k] >= 1 and not force:
            raise ValueError(f"Variable {k} has already been swept in. Use `force=True` to sweep it in again.")
        self.A.sweep_k(k)
        self.swept[k] += 1
        return None

    def exclude_k(self, k, force=False):
        """Exclude the `k`th variable in regression"""
        if self.swept[k] <= 0 and not force:
            raise ValueError(f"Variable {k} was not in the model. Use `force=True` to sweep it out again.")
        self.A.sweep_k(k, inv=True)
        self.swept[k] -= 1
        return None

    def fit(self, verbose=True):
        """Perform least squares fitting by sweeping in all variables."""
        for k in tqdm(range(self.p), disable = not verbose):
            num_swept = self.swept[k]
            # sweep all variables in exactly 1 time
            while num_swept != 1:
                if num_swept <= 0:
                    self.include_k(k)
                else:
                    self.exclude_k(k)
                num_swept = self.swept[k]
        return None

    def coef(self, verbose=True):
        """
        Fitted coefficient values (beta hat). Only returns the beta for
        variables that have been swept in.
        """
        idx = np.where(self.swept == 1)[0]
        return self.A[idx, -1].copy()

    def coef_std(self, verbose=True):
        """Standard deviation of the fitted coefficient values"""
        sigma2 = self.sigma2()
        idx = np.where(self.swept == 1)[0]
        beta_var = self.A.A[idx, idx].copy() # A[idx, idx] is diagonals of A
        return np.sqrt(-sigma2 * beta_var)

    def resid(self, verbose=True):
        """Estimate of residuals = ||y - yhat||^2"""
        return self.A[-1, -1]

    def sigma2(self, verbose=True):
        """Estimate of sigma square."""
        n, p = self.n, self.p
        return self.resid() / (n - p)

    def cov(self, verbose=True):
        """Estimated variance-covariance of beta hat, i.e. Var(b) = sigma2 * inv(X'X)"""
        cov = self.A[0:-1, 0:-1].copy()
        idx = np.where(self.swept == 1)[0]
        return -self.sigma2() * cov[np.ix_(idx, idx)]

    def R2(self, verbose=True):
        """Computes the R2 (coefficient of determination) of fit"""
        ybar = np.mean(self.y)
        ss_tot = np.sum((self.y - ybar) ** 2)
        ss_res = self.resid()
        return 1 - ss_res / ss_tot
