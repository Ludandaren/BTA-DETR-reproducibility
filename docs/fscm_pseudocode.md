# FSCM Pseudocode

FSCM combines frequency-domain texture analysis and spatial directional convolution to model heterogeneous tumor texture and irregular lesion boundaries.

## Interface

```text
Input:  X in R^{B x C x H x W}
Output: Y in R^{B x C x H x W}
```

## Pseudocode

```text
function FSCM(X):
    X_proj = Conv1x1(X)

    X_fft = RFFT2D(X_proj)
    M_lf, M_mf, M_hf = BuildFrequencyMasks(r1=0.25, r2=0.50)
    w_lf = SE(GAP(log(1 + abs(X_fft)) * M_lf))
    w_mf = SE(GAP(log(1 + abs(X_fft)) * M_mf))
    w_hf = SE(GAP(log(1 + abs(X_fft)) * M_hf))
    X_freq = IRFFT2D(X_fft * (w_lf*M_lf + w_mf*M_mf + w_hf*M_hf))

    X_local = DepthwiseConv3x3(X_proj)
    X_spatial = DepthwiseConv5x1(X_local)
    X_spatial = DepthwiseConv1x5(X_spatial)

    X_fused = DepthwiseConv3x3(ReLU(BN(Conv1x1(concat(X_freq, X_spatial)))))
    Y = ResidualAdapter(X) + alpha * Conv1x1(X_fused)

    return Y
```

## Hyperparameters

```text
r1 = 0.25
r2 = 0.50
alpha initialization = 0.2
```

## Notes

This pseudocode summarizes the FSCM processing flow and key hyperparameter definitions for reproducibility documentation.
