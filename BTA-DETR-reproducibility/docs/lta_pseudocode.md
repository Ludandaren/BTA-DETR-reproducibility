# LTA Pseudocode

LTA introduces a pixel-level temperature field into multi-head attention to perform position-dependent attention-temperature modulation.

## Interface

```text
Input:  X in R^{B x C x H x W}
Output: Y in R^{B x C x H x W}
```

## Temperature Field

```text
tau_raw = sigmoid(Conv1x1(GELU(Conv3x3(X))))
tau = tau_min + (tau_max - tau_min) * tau_raw
```

where:

```text
tau_min = 0.6
tau_max = 2.0
```

## Alignment and Broadcast

```text
N = H x W
tau:     B x 1 x H x W
tau_f:   B x 1 x N x 1
QK^T:    B x heads x N x N
```

The flattened temperature field is broadcast along the attention-head dimension and key dimension. Therefore, each query position has one temperature value that modulates its attention distribution over all key positions.

## Attention

```text
Q, K, V = LinearProjection(flatten(X))
score = (Q K^T) / sqrt(d_k)
score = score / tau_f
A = softmax(score)
Y = A V
Y = ResidualAndFFN(Y)
```

## Notes

This pseudocode summarizes the alignment and broadcasting logic of the pixel-level temperature field for reproducibility documentation.
