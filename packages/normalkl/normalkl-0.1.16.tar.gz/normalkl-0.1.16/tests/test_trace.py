import torch
import unittest

from normalkl.trace import *

trikron = lambda A, B, C: torch.kron(A, torch.kron(B, C))

class TestTrace(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(0)
        
        d1, d2 = 4, 3
        d = d1 * d2

        tensor_d1, tensor_d2, tensor_d3 = 2, 2, 3

        dtype=torch.float64

        # Full covariance 
        self.L1 = torch.randn(d, d, dtype=dtype).tril()
        self.L2 = torch.randn(d, d, dtype=dtype).tril()
        self.covmat1 = self.L1 @ self.L1.T
        self.covmat2 = self.L2 @ self.L2.T

        self.precmat1 = torch.inverse(self.covmat1)
        self.precmat2 = torch.inverse(self.covmat2)

        self.L1_inv = torch.inverse(self.L1)
        self.L2_inv = torch.inverse(self.L2)
            
        # Cholesky factors for cholkroncov1 and cholkroncov2
        self.LU1 = torch.randn(d1, d1, dtype=dtype).tril()
        self.LV1 = torch.randn(d2, d2, dtype=dtype).tril()
        self.LU2 = torch.randn(d1, d1, dtype=dtype).tril()
        self.LV2 = torch.randn(d2, d2, dtype=dtype).tril()

        self.tensor_LU1 = torch.randn(tensor_d1, tensor_d1, dtype=dtype).tril()
        self.tensor_LV1 = torch.randn(tensor_d2, tensor_d2, dtype=dtype).tril()
        self.tensor_LW1 = torch.randn(tensor_d3, tensor_d3, dtype=dtype).tril()
        self.tensor_LU2 = torch.randn(tensor_d1, tensor_d1, dtype=dtype).tril()
        self.tensor_LV2 = torch.randn(tensor_d2, tensor_d2, dtype=dtype).tril()
        self.tensor_LW2 = torch.randn(tensor_d3, tensor_d3, dtype=dtype).tril()

        # Covariance matrices for cholkroncov1 and cholkroncov2
        self.U1 = self.LU1 @ self.LU1.T
        self.V1 = self.LV1 @ self.LV1.T
        self.U2 = self.LU2 @ self.LU2.T
        self.V2 = self.LV2 @ self.LV2.T

        self.tensor_U1 = self.tensor_LU1 @ self.tensor_LU1.T
        self.tensor_V1 = self.tensor_LV1 @ self.tensor_LV1.T
        self.tensor_W1 = self.tensor_LW1 @ self.tensor_LW1.T
        self.tensor_U2 = self.tensor_LU2 @ self.tensor_LU2.T
        self.tensor_V2 = self.tensor_LV2 @ self.tensor_LV2.T
        self.tensor_W2 = self.tensor_LW2 @ self.tensor_LW2.T

        # Cholesky Kronecker decompositions
        self.cholkroncov1 = (self.LU1, self.LV1)
        self.cholkroncov2 = (self.LU2, self.LV2)

        self.choltrikroncov1 = (self.tensor_LU1, self.tensor_LV1, self.tensor_LW1)
        self.choltrikroncov2 = (self.tensor_LU2, self.tensor_LV2, self.tensor_LW1)
        self.trikron_covmat1 = trikron(self.tensor_U1, self.tensor_V1, self.tensor_W1)
        self.trikron_covmat2 = trikron(self.tensor_U2, self.tensor_V2, self.tensor_W2)

        # Full covariance matrices
        self.kron_covmat1 = torch.kron(self.U1, self.V1)
        self.kron_covmat2 = torch.kron(self.U2, self.V2)

        # Other inputs
        self.I = torch.eye(d, dtype=dtype)
        self.v1 = torch.randn(d, dtype=dtype)
        self.v2 = torch.randn(d, dtype=dtype)
        self.s2 = torch.tensor(2.0, dtype=dtype)
        self.a2 = torch.randn(d1, dtype=dtype).square()
        self.b2 = torch.randn(d2, dtype=dtype).square()

        self.one_d1 = torch.ones(d1, dtype=dtype)
        self.one_d2 = torch.ones(d2, dtype=dtype)

        self.tensor_a2 = torch.randn(tensor_d1, dtype=dtype).square()
        self.tensor_b2 = torch.randn(tensor_d2, dtype=dtype).square()

        self.tensor_one_d1 = torch.ones(tensor_d1, dtype=dtype)
        self.tensor_one_d2 = torch.ones(tensor_d2, dtype=dtype)
        self.tensor_one_d3 = torch.ones(tensor_d3, dtype=dtype)

        self.rtol = 1e-6
        self.atol = 1e-6

    def test_trace_covmat_covmat(self):
        expected = trace_covmat_covmat(self.covmat1, self.covmat2)
        result = trace_covmat_covmat(self.covmat1, self.covmat2)
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))

    def test_trace_covmat_precmat(self):       
        expected = trace_covmat_covmat(self.covmat1, torch.inverse(self.covmat2))
        result = trace_covmat_precmat(self.covmat1, self.covmat2)
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))

    def test_trace_covmat_diagvar(self):
        expected = trace_covmat_covmat(self.covmat1, self.v2.diag())
        result = trace_covmat_diagvar(self.covmat1, self.v2)
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))

    def test_trace_covmat_diagprec(self):
        expected = trace_covmat_covmat(self.covmat1, (1 / self.v2).diag())
        result = trace_covmat_diagprec(self.covmat1, self.v2)
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))

    def test_trace_covmat_scalarvar(self):
        expected = trace_covmat_covmat(self.covmat1, self.s2 * self.I)
        result = trace_covmat_scalarvar(self.covmat1, self.s2)
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))

    def test_trace_covmat_scalarprec(self):
        expected = trace_covmat_covmat(self.covmat1, (1 / self.s2) * self.I)
        result = trace_covmat_scalarprec(self.covmat1, self.s2)
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))

    def test_trace_covmat_identity(self):
        expected = trace_covmat_covmat(self.covmat1, self.I)
        result = trace_covmat_identity(self.covmat1, _=None)
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))
        
    def test_trace_covmat_cholcov(self):
        expected = trace_covmat_covmat(self.covmat1, self.covmat2)
        result = trace_covmat_cholcov(self.covmat1, self.L2)
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))

    def test_trace_covmat_cholprec(self):
        expected = trace_covmat_covmat(self.covmat1, self.covmat2)
        result = trace_covmat_cholprec(self.covmat1, torch.linalg.cholesky(self.precmat2))
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))

    def test_trace_covmat_kroncov(self):
        expected = trace_covmat_covmat(self.covmat1, self.kron_covmat2)
        result = trace_covmat_kroncov(self.covmat1, (self.U2, self.V2))
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))

    def test_trace_covmat_kronprec(self):
        expected = trace_covmat_covmat(self.covmat1, torch.inverse(self.kron_covmat2))
        result = trace_covmat_kronprec(self.covmat1, (self.U2, self.V2))
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))

    def test_trace_covmat_cholkroncov(self):
        expected = trace_covmat_covmat(self.covmat1, self.kron_covmat2)
        result = trace_covmat_cholkroncov(self.covmat1, (self.LU2, self.LV2))
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))

    def test_trace_covmat_diagvarkron(self):
        expected = trace_covmat_covmat(self.covmat1, torch.outer(self.a2, self.b2).view(-1).diag())
        result = trace_covmat_diagvarkron(self.covmat1, (self.a2, self.b2))
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))

    def test_trace_covmat_diagvarrow(self):
        d1 = len(self.a2)
        d2 = self.covmat1.size(0) // d1
        expected = trace_covmat_covmat(self.covmat1, self.a2.view(-1, 1).repeat(1, d2).view(-1).diag())
        result = trace_covmat_diagvarrow(self.covmat1, self.a2)
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))

    def test_trace_covmat_diagvarcol(self):
        d2 = len(self.b2)
        d1 = self.covmat1.size(0) // d2
        expected = trace_covmat_covmat(self.covmat1, self.b2.view(1, -1).repeat(d1, 1).view(-1).diag())
        result = trace_covmat_diagvarcol(self.covmat1, self.b2)
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))

    def test_trace_cholcov_scalarvar(self):
        expected = trace_covmat_covmat(self.covmat1, self.s2 * self.I)
        result = trace_cholcov_scalarvar(self.L1, self.s2)
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))

    def test_trace_cholcov_cholcov(self):
        expected = trace_covmat_covmat(self.covmat1, self.covmat2)
        result = trace_cholcov_cholcov(self.L1, self.L2)
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))

    def test_trace_cholcov_precmat(self):
        expected = trace_covmat_covmat(self.covmat1, self.covmat2)
        result = trace_cholcov_precmat(self.L1, self.precmat2)
        self.assertTrue(torch.allclose(expected, result, rtol=self.rtol, atol=self.atol))


    def test_trace_cholkroncov_covmat(self):
        result = trace_cholkroncov_covmat(self.cholkroncov1, self.covmat2)
        expected = trace_covmat_covmat(self.kron_covmat1, self.covmat2)
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_cholkroncov_precmat(self):
        result = trace_cholkroncov_precmat(self.cholkroncov1, self.covmat2)
        expected = trace_covmat_covmat(self.kron_covmat1, torch.inverse(self.covmat2))
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_cholkroncov_diagvar(self):
        result = trace_cholkroncov_diagvar(self.cholkroncov1, self.v2)
        expected = trace_covmat_covmat(self.kron_covmat1, torch.diag(self.v2))
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_cholkroncov_diagprec(self):
        result = trace_cholkroncov_diagprec(self.cholkroncov1, self.v2)
        expected = trace_covmat_covmat(self.kron_covmat1, torch.diag(1 / self.v2))
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_cholkroncov_scalarvar(self):
        result = trace_cholkroncov_scalarvar(self.cholkroncov1, self.s2)
        expected = trace_covmat_covmat(self.kron_covmat1, self.s2 * self.I)
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_cholkroncov_scalarprec(self):
        result = trace_cholkroncov_scalarprec(self.cholkroncov1, self.s2)
        expected = trace_covmat_covmat(self.kron_covmat1, (1 / self.s2) * self.I)
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_cholkroncov_identity(self):
        result = trace_cholkroncov_identity(self.cholkroncov1, None)
        expected = trace_covmat_covmat(self.kron_covmat1, self.I)
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_cholkroncov_cholcov(self):
        result = trace_cholkroncov_cholcov(self.cholkroncov1, self.L2)
        expected = trace_covmat_covmat(self.kron_covmat1, self.covmat2)
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_cholkroncov_cholprec(self):
        result = trace_cholkroncov_cholprec(self.cholkroncov1, torch.linalg.cholesky(self.precmat2))
        expected = trace_covmat_covmat(self.kron_covmat1, self.covmat2)
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_cholkroncov_kroncov(self):
        result = trace_cholkroncov_kroncov(self.cholkroncov1, (self.U2, self.V2))
        expected = trace_covmat_covmat(self.kron_covmat1, self.kron_covmat2)
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_cholkroncov_kronprec(self):
        result = trace_cholkroncov_kronprec(self.cholkroncov1, (self.U2, self.V2))
        expected = trace_covmat_covmat(self.kron_covmat1, torch.inverse(self.kron_covmat2))
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_cholkroncov_cholkroncov(self):
        result = trace_cholkroncov_cholkroncov(self.cholkroncov1, self.cholkroncov2)
        expected = trace_covmat_covmat(self.kron_covmat1, self.kron_covmat2)
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_cholkroncov_diagvarrow(self):
        amat2 = torch.kron(self.a2, self.one_d2).diag()
        result = trace_cholkroncov_diagvarrow(self.cholkroncov1, self.a2)
        expected = trace_covmat_covmat(self.kron_covmat1, amat2)
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_cholkroncov_diagvarcol(self):
        bmat2 = torch.kron(self.one_d1, self.b2).diag()
        result = trace_cholkroncov_diagvarcol(self.cholkroncov1, self.b2)
        expected = trace_covmat_covmat(self.kron_covmat1, bmat2)
        self.assertTrue(torch.allclose(result, expected))

    # choltrikroncov_*

    def test_trace_choltrikroncov_covmat(self):
        result = trace_choltrikroncov_covmat(self.choltrikroncov1, self.covmat2)
        expected = trace_covmat_covmat(self.trikron_covmat1, self.covmat2)
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_choltrikroncov_precmat(self):
        result = trace_choltrikroncov_precmat(self.choltrikroncov1, self.covmat2)
        expected = trace_covmat_covmat(self.trikron_covmat1, torch.inverse(self.covmat2))
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_choltrikroncov_diagvar(self):
        result = trace_choltrikroncov_diagvar(self.choltrikroncov1, self.v2)
        expected = trace_covmat_covmat(self.trikron_covmat1, torch.diag(self.v2))
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_choltrikroncov_diagprec(self):
        result = trace_choltrikroncov_diagprec(self.choltrikroncov1, self.v2)
        expected = trace_covmat_covmat(self.trikron_covmat1, torch.diag(1 / self.v2))
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_choltrikroncov_scalarvar(self):
        result = trace_choltrikroncov_scalarvar(self.choltrikroncov1, self.s2)
        expected = trace_covmat_covmat(self.trikron_covmat1, self.s2 * self.I)
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_choltrikroncov_scalarprec(self):
        result = trace_choltrikroncov_scalarprec(self.choltrikroncov1, self.s2)
        expected = trace_covmat_covmat(self.trikron_covmat1, (1 / self.s2) * self.I)
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_choltrikroncov_identity(self):
        result = trace_choltrikroncov_identity(self.choltrikroncov1, None)
        expected = trace_covmat_covmat(self.trikron_covmat1, self.I)
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_choltrikroncov_cholcov(self):
        result = trace_choltrikroncov_cholcov(self.choltrikroncov1, self.L2)
        expected = trace_covmat_covmat(self.trikron_covmat1, self.covmat2)
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_choltrikroncov_cholprec(self):
        result = trace_choltrikroncov_cholprec(self.choltrikroncov1, torch.linalg.cholesky(self.precmat2))
        expected = trace_covmat_covmat(self.trikron_covmat1, self.covmat2)
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_choltrikroncov_diagvarrow(self):
        tensor_amat2 = trikron(self.tensor_a2, self.tensor_one_d2, self.tensor_one_d3).diag()
        result = trace_choltrikroncov_diagvarrow(self.choltrikroncov1, self.tensor_a2)
        expected = trace_covmat_covmat(self.trikron_covmat1, tensor_amat2)
        self.assertTrue(torch.allclose(result, expected))

    def test_trace_choltrikroncov_diagvarcol(self):
        tensor_bmat2 = trikron(self.tensor_one_d1, self.tensor_b2, self.tensor_one_d3).diag()
        result = trace_choltrikroncov_diagvarcol(self.choltrikroncov1, self.tensor_b2)
        expected = trace_covmat_covmat(self.trikron_covmat1, tensor_bmat2)
        self.assertTrue(torch.allclose(result, expected))
