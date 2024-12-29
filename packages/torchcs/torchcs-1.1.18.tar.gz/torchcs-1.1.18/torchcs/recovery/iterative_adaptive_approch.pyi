def iaa(Y, Phi, X0=None, niter=15, tol=1e-6, gamma=None, islog=False):
    r"""Iterative Adaptive Approch

    Parameters
    ----------
    Y : Tensor
        Observation :math:`{\bf Y} \in {\mathbb C}^{M\times S}` or :math:`{\bf Y} \in {\mathbb C}^{B\times M\times S}`, 
        (B: the size of batch, M: the number of sampling points, S: the number of snapshots)
    Phi : Tensor
        Observation matrix :math:`{\bf \Phi} \in {\mathbb C}^{M\times N}`, (N: the number of points of recovered signal)
    X0 : Tensor or None
        Initial :math:`{\bf Y} \in {\mathbb C}^{N\times 1}`
    niter : int, optional
        The number of iteration (the default is 15)
    tol : float, optional
        The tolerance of error (the default is 1e-6)
    gamma : float or None, optional
        the regularization factor, by default None
    islog : str, optional
        show progress bar and other log information.

    .. seealso::  :func:`iaaadl`.

    [1] T. Yardibi, J. Li, P. Stoica, M. Xue, and A. B. Baggeroer, “Source Localization and Sensing: A Nonparametric Iterative Adaptive Approach Based on Weighted Least Squares,” IEEE Transactions on Aerospace and Electronic Systems, vol. 46, no. 1, pp. 425–443, Jan. 2010, doi: 10.1109/TAES.2010.5417172.
    
    Examples
    ---------

    .. image:: ./_static/IAADemo.png
       :scale: 98 %
       :align: center

    The results shown in the above figure can be obtained by the following codes.

    ::

        import torch as th
        import torchbox as tb
        import torchcs as tc
        import matplotlib.pyplot as plt

        device = 'cuda:0'
        tb.setseed(2024)
        m, n = 32, 64
        x = th.zeros(n, 1, device=device)
        x[10] = x[20] = x[60] = 1
        x[15] = x[55] = 0.5
        Phi = th.randn(m, n, device=device)
        y = Phi.mm(x)

        xiaa = iaa(y, Phi, niter=15, tol=1e-6, gamma=0.0001, islog=False)
        xiaaadl = iaaadl(y, Phi, niter=15, tol=1e-6, islog=False)

        plt.figure()
        plt.grid()
        plt.plot(x.cpu(), 'go', markerfacecolor='none')
        plt.plot(xiaa.cpu(), 'b^', markerfacecolor='none')
        plt.plot(xiaaadl.cpu(), 'r+', markerfacecolor='none')
        plt.legend(['Orig', 'IAA', 'IAA-ADL'])
        plt.show()

    """

def iaaadl(Y, Phi, X0=None, niter=15, tol=1e-6, islog=False):
    r"""Iterative Adaptive Approch with Adaptive Diagonal Loading

    Parameters
    ----------
    Y : Tensor
        Observation :math:`{\bf Y} \in {\mathbb C}^{M\times S}` or :math:`{\bf Y} \in {\mathbb C}^{B\times M\times S}`, 
        (B: the size of batch, M: the number of sampling points, S: the number of snapshots)
    Phi : Tensor
        Observation matrix :math:`{\bf \Phi} \in {\mathbb C}^{M\times N}`, (N: the number of points of recovered signal)
    X0 : Tensor or None
        Initial :math:`{\bf Y} \in {\mathbb C}^{N\times 1}`
    niter : int, optional
        The number of iteration (the default is 15)
    tol : float, optional
        The tolerance of error (the default is 1e-6)
    islog : str, optional
        show progress bar and other log information.

    .. seealso::  :func:`iaa`.

    [1] Y. Xu, X. Zhang, S. Wei, J. Shi, X. Zhan, and T. Zhang, “3D Super-Resolution Imaging Method for Distributed Millimeter-wave Automotive Radar System,” Sep. 21, 2022, arXiv: arXiv:2209.11037. doi: 10.48550/arXiv.2209.11037.


    Examples
    ---------

    .. image:: ./_static/DOA1dIAAs.png
       :scale: 98 %
       :align: center

    .. image:: ./_static/DOA2dIAAs.png
       :scale: 98 %
       :align: center

    The results shown in the above figure can be obtained by the following codes.

    ::

        import torch as th
        import torchbox as tb
        import torchcs as tc
        import matplotlib.pyplot as plt


        doafile = 'data/array/doa1daz32ns10nsig5.mat'
        data = tb.loadmat(doafile)
        Y, A = th.from_numpy(data['Y']).unsqueeze(-1), th.from_numpy(data['A'])
        anggrid = th.linspace(-90, 90, A.shape[1])

        xiaa = iaa(Y, A, niter=15, tol=1e-6, gamma=0.001, islog=False)
        xiaaadl = iaaadl(Y, A, niter=15, tol=1e-6, islog=False)
        print(Y.shape, A.shape, xiaa.shape, xiaaadl.shape)

        plt = tb.plot([[xiaa, xiaaadl]], Xs=[[anggrid, anggrid]], styles=[['-b', '--r']], legends=[['IAA', 'IAA-ADL']], xlabels=r'Angle($\degree$)', titles='1D-DOA estimation with IAAs', linewidth=1)

        doafile = 'data/array/doa2daz12el12ns10nsig2.mat'
        data = tb.loadmat(doafile)
        Y, A = th.from_numpy(data['Y']).T, th.from_numpy(data['A'])
        ngridsza, ngridsel = 121, 121
        azgrid, elgrid = th.meshgrid([th.linspace(-60, 60, ngridsza), th.linspace(-60, 60, ngridsel)], indexing='xy')

        xiaa = iaa(Y, A, niter=15, tol=1e-6, gamma=0.0001, islog=False).reshape(ngridsza, ngridsel).T
        xiaaadl = iaaadl(Y, A, niter=15, tol=1e-6, islog=False).reshape(ngridsza, ngridsel).T

        print(Y.shape, A.shape, xiaa.shape, xiaaadl.shape)

        plt = tb.imshow([xiaa, xiaaadl], xlabels=r'Azimuth($\degree$)', ylabels=r'Elevation($\degree$)', titles=['2D-DOA estimation with IAA', '2D-DOA estimation with IAA-ADL'], origins='lower', extents=[(-60, 60, -60, 60)]*2)
        plt = tb.mshow([xiaa, xiaaadl], Xs=[azgrid, azgrid], Ys=[elgrid, elgrid], xlabels=r'Azimuth($\degree$)', ylabels=r'Elevation($\degree$)', titles=['2D-DOA estimation with IAA', '2D-DOA estimation with IAA-ADL'])
        plt.show()

    """


