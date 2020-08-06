import torch

x = torch.ones(2, 2, requires_grad=True)
print(x)

'''
tensor([[1., 1.],
        [1., 1.]], requires_grad=True)
'''

y = x + 2
print(y)

'''
tensor([[3., 3.],
        [3., 3.]], grad_fn=<AddBackward0>)
'''