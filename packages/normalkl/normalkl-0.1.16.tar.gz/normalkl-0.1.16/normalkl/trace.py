""" Functions that compute trace term of the KL divergence for different covariance types. """

import torch

def trikron(A, B, C):
    return torch.kron(A, torch.kron(B, C))

# trace_covmat_*

def trace_covmat_covmat(covmat1, covmat2):
    """ Computes trace term: Tr(M2^{-1} M1) / 2 """
    return 0.5 * torch.trace(torch.inverse(covmat2) @ covmat1)
    
def trace_covmat_precmat(covmat1, precmat2):
    """ Computes trace term: Tr(M2 M1) / 2 """
    return 0.5 * torch.trace(precmat2 @ covmat1)
    
def trace_covmat_diagvar(covmat1, diagvar2):
    """ Computes trace term: Tr(diag(v2)^{-1} M1) / 2 """
    return 0.5 * torch.sum(covmat1.diag() / diagvar2)

def trace_covmat_diagprec(covmat1, diagprec2):
    """ Computes trace term: Tr(diag(v2) M1) / 2 """
    return 0.5 * torch.sum(covmat1.diag() * diagprec2)

def trace_covmat_scalarvar(covmat1, scalarvar2):
    """ Computes trace term: Tr(scalarvar2^{-1} covmat1) / 2 """
    return 0.5 * torch.trace(covmat1) / scalarvar2.abs().squeeze()

def trace_covmat_scalarprec(covmat1, scalarprec2):
    """ Computes trace term: Tr(scalarprec2 I covmat1) / 2 """
    return 0.5 * torch.trace(covmat1) * scalarprec2.abs().squeeze()

def trace_covmat_identity(covmat1, _):
    """ Computes trace term: Tr(I covmat1)/2 """
    return 0.5 * torch.trace(covmat1)

def trace_covmat_cholcov(covmat1, cholcov2):
    """ Computes trace term: Tr((L2 L2^T)^{-1} M1) / 2 """
    L2_inv = torch.inverse(cholcov2)
    return 0.5 * torch.trace(L2_inv.T @ L2_inv @ covmat1)
    
def trace_covmat_cholprec(covmat1, cholprec2):
    """ Computes trace term: Tr((L2 L2^T) M1) / 2 """
    return 0.5 * torch.trace(cholprec2 @ cholprec2.T @ covmat1)

def trace_covmat_kroncov(covmat1, kroncov2):
    """ Computes trace term: Tr((U2 kron V2)^{-1} M1) / 2 """
    U2, V2 = kroncov2
    UV2 = torch.kron(U2, V2)
    return 0.5 * torch.trace(torch.linalg.solve(UV2, covmat1))
    
def trace_covmat_kronprec(covmat1, kronprec2):
    """ Computes trace term: Tr((U2 kron V2) M1) / 2 """
    U2, V2 = kronprec2
    UV2 = torch.kron(U2, V2)
    return 0.5 * torch.trace(UV2 @ covmat1)

def trace_covmat_cholkroncov(covmat1, cholkroncov2):
    """ Computes trace term: Tr((LU2 LU2^T kron LV2 LV2^T)^{-1} M1) / 2 """
    LU2, LV2 = cholkroncov2
    U2 = LU2 @ LU2.T
    V2 = LV2 @ LV2.T
    U2_inv = torch.inverse(U2)
    V2_inv = torch.inverse(V2)
    
    return 0.5 * torch.trace(torch.kron(U2_inv, V2_inv) @ covmat1)

def trace_covmat_choltrikroncov(covmat1, choltrikroncov2):
    """ Computes trace term: Tr((LU2 LU2^T kron LV2 LV2^T kron LW2 LW2^T)^{-1} M1) / 2 """
    LU2, LV2, LW2 = choltrikroncov2
    U2 = LU2 @ LU2.T
    V2 = LV2 @ LV2.T
    W2 = LW2 @ LW2.T
    U2_inv = torch.inverse(U2)
    V2_inv = torch.inverse(V2)
    W2_inv = torch.inverse(W2)
    
    return 0.5 * torch.trace(trikron(U2_inv, V2_inv, W2_inv) @ covmat1)
    
def trace_covmat_diagvarkron(covmat1, diagvarkron2):
    """ Computes Tr(diag(vec(ba^T))^{-1} M1)/2 """
    diagvarrow, diagvarcol = diagvarkron2
    kron = torch.outer(diagvarrow, diagvarcol).view(-1)
    return 0.5 * torch.sum(covmat1.diag() / kron)

def trace_covmat_diagvarrow(covmat1, diagvarrow2):
    """ Computes Tr(diag(vec(1a^T))^{-1} M1)/2 """
    d1 = len(diagvarrow2)
    d2 = covmat1.size(0) // d1
    kron = diagvarrow2.view(-1, 1).repeat(1, d2).view(-1)
    return 0.5 * torch.sum(covmat1.diag() / kron)

def trace_covmat_diagvarcol(covmat1, diagvarcol2):
    """ Computes Tr(diag(vec(b1^T))^{-1} M1)/2 """
    d2 = len(diagvarcol2)
    d1 = covmat1.size(0) // d2
    kron = diagvarcol2.view(1, -1).repeat(d1, 1).view(-1)
    return 0.5 * torch.sum(covmat1.diag() / kron)

# trace_precmat_*

def trace_precmat_covmat(precmat1, covmat2):
    """ Computes trace term: Tr(M2^{-1} M1) / 2 """
    return 0.5 * torch.trace(torch.inverse(covmat2) @ torch.inverse(precmat1))
    
def trace_precmat_precmat(precmat1, precmat2):
    """ Computes trace term: Tr(M2 M1) / 2 """
    return 0.5 * torch.trace(precmat2 @ torch.inverse(precmat1))

# trace_cholcov_*

def trace_cholcov_scalarvar(cholcov1, scalarvar2):
    """ Computes trace term: Tr(scalarvar2^{-1} cholcov1) / 2 """
    return 0.5 * torch.sum(cholcov1 ** 2) / scalarvar2.abs().squeeze()

def trace_cholcov_cholcov(cholcov1, cholcov2):
    """ Computes trace term: Tr((L2 L2^T)^{-1} (L1 L1^T)) / 2 """

    L2_inv = torch.inverse(cholcov2)
    C = cholcov1.T @ L2_inv.T
    return 0.5 * (C ** 2).sum()

def trace_cholcov_precmat(cholcov1, precmat2):
    """ Computes trace term: Tr(precmat2 (L1 L1^T)) / 2 """

    return 0.5 * torch.trace(precmat2 @ cholcov1 @ cholcov1.T)

# trace_cholkroncov_*

def trace_cholkroncov_covmat(cholkroncov1, covmat2):
    """ Computes trace term: Tr(M2^{-1} (LU1 LU1^T kron LV1 LV1^T)) / 2 """
    LU1, LV1 = cholkroncov1
    U1 = LU1 @ LU1.T
    V1 = LV1 @ LV1.T
    return 0.5 * torch.trace(torch.inverse(covmat2) @ torch.kron(U1, V1))

def trace_cholkroncov_precmat(cholkroncov1, precmat2):
    """ Computes trace term: Tr(M2 (LU1 LU1^T kron LV1 LV1^T)) / 2 """
    LU1, LV1 = cholkroncov1
    U1 = LU1 @ LU1.T
    V1 = LV1 @ LV1.T
    return 0.5 * torch.trace(precmat2 @ torch.kron(U1, V1))

def trace_cholkroncov_diagvar(cholkroncov1, diagvar2):
    """ Computes trace term: Tr(diag(v2)^{-1} (LU1 LU1^T kron LV1 LV1^T)) / 2 """
    LU1, LV1 = cholkroncov1
    U1_diag = LU1.square().sum(1)
    V1_diag = LV1.square().sum(1)
    return 0.5 * torch.sum(torch.outer(U1_diag, V1_diag).view(-1) / diagvar2)

def trace_cholkroncov_diagprec(cholkroncov1, diagprec2):
    """ Computes trace term: Tr(diag(v2) (LU1 LU1^T kron LV1 LV1^T)) / 2 """
    LU1, LV1 = cholkroncov1
    U1_diag = LU1.square().sum(1)
    V1_diag = LV1.square().sum(1)
    return 0.5 * torch.sum(torch.outer(U1_diag, V1_diag).view(-1)  * diagprec2)

def trace_cholkroncov_scalarvar(cholkroncov1, scalarvar2):
    """ Computes trace term: Tr(scalarvar2^{-1} (LU1 LU1^T kron LV1 LV1^T)) / 2 """
    LU1, LV1 = cholkroncov1
    return 0.5 * torch.sum(LU1 ** 2) * torch.sum(LV1 ** 2) / scalarvar2

def trace_cholkroncov_scalarprec(cholkroncov1, scalarprec2):
    """ Computes trace term: Tr(scalarprec2 I (LU1 LU1^T kron LV1 LV1^T)) / 2 """
    LU1, LV1 = cholkroncov1
    return 0.5 * torch.sum(LU1 ** 2) * torch.sum(LV1 ** 2) * scalarprec2

def trace_cholkroncov_identity(cholkroncov1, _):
    """ Computes trace term: Tr(I (LU1 LU1^T kron LV1 LV1^T))/2 """
    LU1, LV1 = cholkroncov1
    return 0.5 * torch.trace(LU1 @ LU1.T) * torch.trace(LV1 @ LV1.T)

def trace_cholkroncov_cholcov(cholkroncov1, cholcov2):
    """ Computes trace term: Tr((L2 L2.T)^{-1} (LU1 LU1.T kron LV1 LV1.T )) / 2 """
    L2_inv = torch.inverse(cholcov2)
    LU1, LV1 = cholkroncov1
    U1 = LU1 @ LU1.T
    V1 = LV1 @ LV1.T
    return 0.5 * torch.trace(L2_inv.T @ L2_inv @ torch.kron(U1, V1))

def trace_cholkroncov_cholprec(cholkroncov1, cholprec2):
    """ Computes trace term: Tr((L2 L2.T) (LU1 LU1.T kron LV1 LV1.T )) / 2 """
    L2 = cholprec2
    LU1, LV1 = cholkroncov1
    U1 = LU1 @ LU1.T
    V1 = LV1 @ LV1.T
    return 0.5 * torch.trace(L2 @ L2.T @ torch.kron(U1, V1))

def trace_cholkroncov_kroncov(cholkroncov1, kroncov2):
    """ Computes trace term: Tr((U2 kron V2)^{-1} (LU1 LU1^T kron LV1 LV1^T)) / 2 """
    LU1, LV1 = cholkroncov1
    U2, V2 = kroncov2
    U2_inv = torch.inverse(U2)
    V2_inv = torch.inverse(V2)
    return 0.5 * torch.trace(LU1.T @ U2_inv @ LU1) * torch.trace(LV1.T @ V2_inv @ LV1)

def trace_cholkroncov_kronprec(cholkroncov1, kronprec2):
    """ Computes trace term: Tr((U2 kron V2) (LU1 LU1^T kron LV1 LV1^T)) / 2 """
    LU1, LV1 = cholkroncov1
    U2, V2 = kronprec2
    return 0.5 * torch.trace(LU1.T @ U2 @ LU1) * torch.trace(LV1.T @ V2 @ LV1)

def trace_cholkroncov_cholkroncov(cholkroncov1, cholkroncov2):
    """ Computes trace term: Tr((LU2 LU2^T kron LV2 LV2^T)^{-1} (LU1 LU1^T kron LV1 LV1^T)) / 2 """
    LU1, LV1 = cholkroncov1
    LU2, LV2 = cholkroncov2
    LU2_inv = torch.inverse(LU2)
    LV2_inv = torch.inverse(LV2)

    LU1TLU2_invT = LU1.T @ LU2_inv.T
    trace_LU1TLU2_invT = LU1TLU2_invT.square().sum()
    LV1TLV2_invT = LV1.T @ LV2_inv.T
    trace_LV1TLV2_invT = LV1TLV2_invT.square().sum()

    return 0.5 * trace_LU1TLU2_invT * trace_LV1TLV2_invT

def trace_cholkroncov_cholkronprec(cholkroncov1, cholkronprec2):
    """ Computes trace term: Tr((LU2 LU2^T kron LV2 LV2^T) (LU1 LU1^T kron LV1 LV1^T)) / 2 """
    LU1, LV1 = cholkroncov1
    LU2, LV2 = cholkronprec2
    LU1TLU2 = LU1.T @ LU2
    trace_U2U1 = LU1TLU2.square().sum()
    LV1TLV2 = LV1.T @ LV2
    trace_V2V1 = LV1TLV2.square().sum()

    return 0.5 * trace_U2U1 * trace_V2V1

def trace_cholkroncov_diagvarrow(cholkroncov1, diagvarrow2): # TODO: avoid kronecker here, can be much faster
    """ Computes Tr(diag(vec(1a^T))^{-1} (LU1 LU1^T kron LV1 LV1^T))/2 """
    LU1, LV1 = cholkroncov1
    U1 = LU1 @ LU1.T
    V1 = LV1 @ LV1.T
    covmat1 = torch.kron(U1, V1)
    d1 = len(U1)
    d2 = len(V1)

    kron = diagvarrow2.view(-1, 1).repeat(1, d2).view(-1)
    print('d', d1, d2, diagvarrow2.shape)
    print(covmat1.shape, kron.shape, 444)
    return 0.5 * torch.sum(covmat1.diag() / kron)

def trace_cholkroncov_diagvarcol(cholkroncov1, diagvarcol2): # TODO: avoid kronecker here, can be much faster
    """ Computes Tr(diag(vec(b1^T))^{-1} (LU1LU1^T kron LV1 LV1^T))/2 """
    LU1, LV1 = cholkroncov1
    U1 = LU1 @ LU1.T
    V1 = LV1 @ LV1.T
    covmat1 = torch.kron(U1, V1)
    d1 = len(U1)
    d2 = len(V1)

    kron = diagvarcol2.view(1, -1).repeat(d1, 1).view(-1)
    return 0.5 * torch.sum(covmat1.diag() / kron)

# trace_choltrikroncov_*

def trace_choltrikroncov_covmat(choltrikroncov1, covmat2):
    """ Computes trace term: Tr(M2^{-1} (LU1 LU1^T kron LV1 LV1^T kron LW1 LW1^T)) / 2 """
    LU1, LV1, LW1 = choltrikroncov1
    U1 = LU1 @ LU1.T
    V1 = LV1 @ LV1.T
    W1 = LW1 @ LW1.T
    return 0.5 * torch.trace(torch.inverse(covmat2) @ trikron(U1, V1, W1))

def trace_choltrikroncov_precmat(choltrikroncov1, precmat2):
    """ Computes trace term: Tr(M2 (LU1 LU1^T kron LV1 LV1^T kron LW1 LW1^T)) / 2 """
    LU1, LV1, LW1 = choltrikroncov1
    U1 = LU1 @ LU1.T
    V1 = LV1 @ LV1.T
    W1 = LW1 @ LW1.T
    return 0.5 * torch.trace(precmat2 @ trikron(U1, V1, W1))

def trace_choltrikroncov_diagvar(choltrikroncov1, diagvar2):
    """ Computes trace term: Tr(diag(v2)^{-1} (LU1 LU1^T kron LV1 LV1^T kron LW1 LW1^T)) / 2 """
    LU1, LV1, LW1 = choltrikroncov1
    U1_diag = LU1.square().sum(1)
    V1_diag = LV1.square().sum(1)
    W1_diag = LW1.square().sum(1)
    return 0.5 * torch.sum(torch.einsum('a,b,c->abc',U1_diag, V1_diag, W1_diag).view(-1) / diagvar2)

def trace_choltrikroncov_diagprec(choltrikroncov1, diagprec2):
    """ Computes trace term: Tr(diag(v2) (LU1 LU1^T kron LV1 LV1^T kron LW1 LW1^T)) / 2 """
    LU1, LV1, LW1 = choltrikroncov1
    U1_diag = LU1.square().sum(1)
    V1_diag = LV1.square().sum(1)
    W1_diag = LW1.square().sum(1)
    return 0.5 * torch.sum(torch.einsum('a,b,c->abc',U1_diag, V1_diag, W1_diag).view(-1) * diagprec2)

def trace_choltrikroncov_scalarvar(choltrikroncov1, scalarvar2):
    """ Computes trace term: Tr(scalarvar2^{-1} (LU1 LU1^T kron LV1 LV1^T kron LW1 LW1^T)) / 2 """
    LU1, LV1, LW1 = choltrikroncov1
    return 0.5 * torch.sum(LU1 ** 2) * torch.sum(LV1 ** 2) * torch.sum(LW1 ** 2) / scalarvar2

def trace_choltrikroncov_scalarprec(choltrikroncov1, scalarprec2):
    """ Computes trace term: Tr(scalarprec2 I (LU1 LU1^T kron LV1 LV1^T kron LW1 LW1^T)) / 2 """
    LU1, LV1, LW1 = choltrikroncov1
    return 0.5 * torch.sum(LU1 ** 2) * torch.sum(LV1 ** 2) * torch.sum(LW1 ** 2) * scalarprec2

def trace_choltrikroncov_identity(choltrikroncov1, _):
    """ Computes trace term: Tr(I (LU1 LU1^T kron LV1 LV1^T kron LW1 LW1^T))/2 """
    LU1, LV1, LW1 = choltrikroncov1

    return 0.5 * torch.sum(LU1 ** 2) * torch.sum(LV1 ** 2) * torch.sum(LW1 ** 2)

def trace_choltrikroncov_cholcov(choltrikroncov1, cholcov2):
    """ Computes trace term: Tr((L2 L2.T)^{-1} (LU1 LU1.T kron LV1 LV1.T kron LW1 LW1.T)) / 2 """
    L2_inv = torch.inverse(cholcov2)
    LU1, LV1, LW1 = choltrikroncov1
    U1 = LU1 @ LU1.T
    V1 = LV1 @ LV1.T
    W1 = LW1 @ LW1.T
    return 0.5 * torch.trace(L2_inv.T @ L2_inv @ trikron(U1, V1, W1))

def trace_choltrikroncov_cholprec(choltrikroncov1, cholprec2):
    """ Computes trace term: Tr((L2 L2.T) (LU1 LU1.T kron LV1 LV1.T )) / 2 """
    L2 = cholprec2
    LU1, LV1, LW1 = choltrikroncov1
    U1 = LU1 @ LU1.T
    V1 = LV1 @ LV1.T
    W1 = LW1 @ LW1.T
    return 0.5 * torch.trace(L2 @ L2.T @ trikron(U1, V1, W1))

def trace_choltrikroncov_diagvarrow(choltrikroncov1, diagvarrow2): # TODO: avoid kronecker here, can be much faster
    """ Computes Tr(diag(vec(1a^T))^{-1} (LU1 LU1^T kron LV1 LV1^T kron LW1 LW1^T))/2 """
    LU1, LV1, LW1 = choltrikroncov1
    U1 = LU1 @ LU1.T
    V1 = LV1 @ LV1.T
    W1 = LW1 @ LW1.T
    covmat1 = trikron(U1, V1, W1)
    d1 = len(U1)
    d2 = len(V1)
    d3 = len(W1)

    kron = diagvarrow2.view(-1, 1, 1).repeat(1, d2, d3).view(-1)
    return 0.5 * torch.sum(covmat1.diag() / kron)

def trace_choltrikroncov_diagvarcol(choltrikroncov1, diagvarcol2): # TODO: avoid kronecker here, can be much faster
    """ Computes Tr(diag(vec(b1^T))^{-1} (LU1LU1^T kron LV1 LV1^T kron LW1 LW1^T))/2 """
    LU1, LV1, LW1 = choltrikroncov1
    U1 = LU1 @ LU1.T
    V1 = LV1 @ LV1.T
    W1 = LW1 @ LW1.T
    covmat1 = trikron(U1, V1, W1)
    d1 = len(U1)
    d2 = len(V1)
    d3 = len(W1)

    kron = diagvarcol2.view(1, -1, 1).repeat(d1, 1, d3).view(-1)
    return 0.5 * torch.sum(covmat1.diag() / kron)


