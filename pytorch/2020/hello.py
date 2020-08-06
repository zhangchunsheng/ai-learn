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

print(y.grad_fn)
'''
<AddBackward0 object at 0x7fdcd798a518>
'''

z = y * y * 3
out = z.mean()

print(z, out)
'''
tensor([[27., 27.],
        [27., 27.]], grad_fn=<MulBackward0>) tensor(27., grad_fn=<MeanBackward0>)
'''