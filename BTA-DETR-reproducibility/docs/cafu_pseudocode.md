# CAFU Pseudocode

CAFU is designed to adaptively fuse local spatial texture information and channel semantic information.

## Interface

```text
Input:  X in R^{B x C x H x W}
Output: Y in R^{B x C x H x W}
```

## Pseudocode

```text
function CAFU(X):
    U = Conv3x3(X)

    X_spatial = Conv3x3(U)
    X_channel = Conv1x1(ReLU(Conv1x1(U)))

    G = sigmoid(Conv1x1(ReLU(Conv1x1(U))))

    Y = G * X_spatial + (1 - G) * X_channel
    Y = ResidualAdapter(X) + Y

    return Y
```

## Notes

This pseudocode summarizes the algorithmic structure of CAFU for reproducibility documentation.
