
from pycamia import info_manager

__info__ = info_manager(
    project = "PyCAMIA",
    package = "micomputing",
    author = "Yuncheng Zhou",
    create = "2022-03",
    fileinfo = "File containing U-net and convolutional networks.",
    help = "Use `from micomputing import *`.",
    requires = "batorch"
).check()

__all__ = """
    U_Net
    CNN
    FCN
    RNN
    NeuralODE
    Convolution_Block
    Convolution
    Models
""".split()
    
import math

with __info__:
    import batorch as bt
    from batorch import nn
    from pycamia import touch, avouch, execblock
    from pycamia import Path, ByteSize, SPrint, infinite_itemize

def parse(string):
    if string.count('(') > 1 or string.count(')') > 1: raise TypeError("Invalid to parse: " + string + ". ")
    if string.count('(') == 0 and string.count(')') == 0: string += '()'
    return eval('("' + string.lower().replace('(', '", (').replace(')', ',)').replace('(,)', '()') + ')')

def cat(*tensors): return bt.cat(tensors, 1)
def combine(list_of_items, reduction):
    if len(list_of_items) >= 2:
        z = reduction(list_of_items[0], list_of_items[1])
        for i in range(2, len(list_of_items)):
            z = reduction(z, list_of_items[i])
    else: z = list_of_items[0]
    return z

Convolution = {
    0: lambda ic, oc, *_: nn.Linear(ic, oc), 
    1: nn.Conv1d, 
    2: nn.Conv2d, 
    3: nn.Conv3d
}

MaxPool = {
    0: lambda *_: (lambda x: x), 
    1: nn.MaxPool1d, 
    2: nn.MaxPool2d, 
    3: nn.MaxPool3d
}

ConvTranspose = {
    0: lambda *_: (lambda x: x), 
    1: nn.ConvTranspose1d, 
    2: nn.ConvTranspose2d, 
    3: nn.ConvTranspose3d
}

class BatchNorm(nn.Module):
    def __init__(self, idim, ch):
        super().__init__()
        self.major = nn.BatchNorm1d(ch)
        self.idim = idim
        
    def __class_getitem__(cls, idim):
        if idim in [1, 2, 3]: return getattr(nn, f"BatchNorm{idim}d")
        return lambda ch: cls(idim, ch)
    
    def forward(self, x):
        if self.idim == 0:
            return self.major(x.unsqueeze(-1)).squeeze(-1)
        else: return self.major(x)

class Convolution_Block(nn.Module):
    '''
    Args:
        dimension (int): The dimension of the images. Defaults to 2. 
        in_channels (int): The input channels for the block. 
        out_channels (int): The output channels for the block. 
        mid_channels (int): The middle channels for the block. 
        conv_num (int): The number of convolution layers. Defaults to 1. 
        kernel_size (int): The size of the convolution kernels. Defaults to 3. 
        padding (int): The image padding for the convolutions. Defaults to 1. 
        initializer (str): A string indicating the initialing strategy. Possible values 
            are normal(0, 0.1) or uniform(-0.1, 0.1) or constant(0) (all parameters can be changed)
        linear_layer (bool): Whether the convolutions are used for 1x1 images (equivalent to linear layers). 
        activation_function (class): The activation function. 
        final_activation (class): The activation function after the final convolution. 
        active_args (dict): The arguments for the activation function. 
        conv_block (str): A string with possible values in ('conv', 'dense', 'residual'), 
            indicating which kind of block the U-Net is using: normal convolution layers, 
            DenseBlock or ResidualBlock. Defaults to 'conv'.
        res_type (function): The combining type for the residual connections.
    '''
    
    def __init__(self, in_channels, out_channels, mid_channels=None, **params):
        super().__init__()
        default_values = {'dimension': 2, 'conv_num': 1, 'kernel_size': 3, 'padding': 1, 'linear_layer': False, 'initializer': "normal(0, 0.1)", 'conv_block': 'conv', 'res_type': bt.add, 'activation_function': nn.ReLU, 'final_activation': ..., 'active_args': {}}
        param_values = {}
        param_values.update(default_values)
        param_values.update(params)
        self.__dict__.update(param_values)
        self.in_channels = in_channels
        self.out_channels = out_channels
        if mid_channels is None:
            if self.linear_layer: self.mid_channels = 5 * self.out_channels
            else: self.mid_channels = self.out_channels
        else:
            self.mid_channels = mid_channels
            
        if self.linear_layer: self.kernel_size = 1; self.padding = 0
        
        if isinstance(self.padding, str): self.padding = {'SAME': self.kernel_size // 2, 'ZERO': 0, 'VALID': 0}.get(self.padding.upper(), self.kernel_size // 2)
        if self.activation_function is None: self.activation_function = lambda *a, **k: (lambda x: x)
        if self.final_activation == ...: self.final_activation = self.activation_function
        if self.final_activation is None: self.final_activation = lambda *a, **k: (lambda x: x)
        
        self.layers = nn.ModuleList()
        for i in range(self.conv_num):
            ic = self.in_channels if i == 0 else ((self.mid_channels * i + self.in_channels) if self.conv_block == 'dense' else self.mid_channels)
            oc = self.out_channels if i == self.conv_num - 1 else self.mid_channels
            conv = Convolution[self.dimension](ic, oc, self.kernel_size, 1, self.padding)
            initialize_model, initialize_params = parse(self.initializer)
            eval('nn.init.%s_' % initialize_model)(conv.weight, *initialize_params)
            if self.conv_block != 'dense': self.layers.append(conv)
            oc = (self.mid_channels * i + self.in_channels) if self.conv_block == 'dense' else oc
            if not self.linear_layer: self.layers.append(BatchNorm[self.dimension](oc))
            if i < self.conv_num-1: self.layers.append(self.activation_function(**self.active_args))
            if self.conv_block == 'dense': self.layers.append(conv)

    def forward(self, x):
        self.memory_used = ByteSize(0)
        need_squeeze = False
        original_shape = x.shape
        if self.linear_layer and x.n_space_dim == 0:
            need_squeeze = True
            x = x.view(*x.shape.python_repr, *((1,) * self.dimension))
        if self.conv_block == 'dense':
            conv_results = [x]
            conv_layer = True
            for layer in self.layers:
                try:
                    if conv_layer: x = layer(bt.cat([bt.crop_as(l, conv_results[-1]) for l in conv_results], 1))
                    else: x = layer(x)
                except Exception as e:
                    raise e.__class__(f"In layer {layer}. " + e.__str__())
                self.memory_used += x.byte_size()
                conv_layer = layer.__class__.__name__.startswith('Conv')
                if conv_layer: conv_results.append(x)
            result = self.final_activation(**self.active_args)(x)
        else:
            y = x
            for layer in self.layers:
                try: y = layer(y)
                except Exception as e:
                    raise e.__class__(f"In layer {layer}. " + e.__str__())
                self.memory_used += ByteSize(y.numel() * y.element_size())
            y = y.as_subclass(bt.Tensor).special_from(x)
            if self.conv_block == 'residual': z = self.res_type(bt.crop_as(x, y), y)
            else: z = y
            result = self.final_activation(**self.active_args)(z)
        result = result.as_subclass(bt.Tensor).special_from(x)
        if need_squeeze: result = result.view(original_shape.with_feature(result.feature))
        elif self.padding == self.kernel_size // 2:
            return bt.crop_as(result, x.space)
        return result

class U_Net(nn.Module):
    '''
    Args:
        dimension (int): The dimension of the images. Defaults to 2 (see U-Net). 
        depth (int): The depth of the U-Net. Defaults to 4 indicating 4 pooling layers and 4 up-sampling layers (see U-Net).
        conv_num (int): The number of continuous convolutions in one block. Defaults to 2. 
        padding (int or str): Indicate the type of padding used. Defaults to 'SAME' though it is 0 in conventional U-Net. 
        in_channels (int): The number of channels for the input. Defaults to 1 (see U-Net).
        out_channels (int): The number of channels for the output. Defaults to 2 (see U-Net).
        block_channels (int): The number of channels for the first block if a number is provided. Defaults to 64 (see U-Net). 
            If a list is provided, the length should be the same as the number of blocks plus two (2 * depth + 3). It represents the channels before and after each block (with the output channels included). 
            Or else, a function may be provided to compute the output channels given the block index (-1 ~ 2 * depth + 1) [including input_channels at -1 and output_channels at 2 * depth + 1]. 
        bottleneck_out_channels (int): The number of channels for the bottleneck output. Defaults to 0. 
        kernel_size (int): The size of the convolution kernels. Defaults to 3 (see U-Net). 
        pooling_size (int): The size of the pooling kernels. Defaults to 2 (see U-Net). 
        // keep_prob (float): The keep probability for the dropout layers. 
        conv_block (str): A string with possible values in ('conv', 'dense', 'residual'), indicating which kind of block the U-Net is using: normal convolution layers, DenseBlock or ResidualBlock. 
        multi_arms (str): A string with possible values in ('shared(2)', 'seperate(2)'), indicating which kind of encoder arms are used. 
        multi_arms_combine (function): The combining type for multi-arms. See skip_type for details. 
        skip_type (function): The skip type for the skip connections. Defaults to catenation (cat; see U-Net). Other possible skip types include torch.mul or torch.add. 
        res_type (function): The combining type for the residual connections. It should be torch.add in most occasions. 
        activation_function (class): The activation function used after the convolution layers. Defaults to nn.ReLU. 
        active_args (dict): The arguments for the activation function. Defaults to {}. 
        initializer (str): A string indicating the initialing strategy. Possible values are normal(0, 0.1) or uniform(-0.1, 0.1) or constant(0) (all parameters can be changed)
        with_softmax (bool): Whether a softmax layer is applied at the end of the network. Defaults to True. 
        cum_layers (list): A list consisting two numbers [n, m] indicating that the result would be a summation of the upsamples of the results of the nth to the mth (included) blocks, block_numbers are in range 0 ~ 2 * depth. 
            The negative indices are allowed to indicate the blocks in a inversed order with -1 representing the output for the last block. 
    '''
    
    class Softmax(nn.Module):
        def forward(self, x): return nn.functional.softmax(x, 1)
    
    class Encoder_Block(nn.Module):
        
        def __init__(self, in_channels, out_channels, has_pooling, params):
            super().__init__()
            block_params = params.copy()
            block_params.update({'in_channels': in_channels, 'out_channels': out_channels, 'has_pooling': has_pooling})
            self.__dict__.update(block_params)
            if has_pooling: self.pooling = MaxPool[self.dimension](self.pooling_size, ceil_mode = True)
            self.conv_block = Convolution_Block(**block_params)

        def forward(self, x):
            if self.has_pooling: y = self.pooling(x)
            else: y = x
            return self.conv_block(y)
            
    class Decoder_Block(nn.Module):
        
        def __init__(self, list_of_encoders, in_channels, out_channels, params, copies_of_inputs):
            super().__init__()
            block_params = params.copy()
            block_params.update({'in_channels': in_channels, 'out_channels': out_channels})
            self.__dict__.update(block_params)
            if self.skip_type == cat: to_channels = in_channels - list_of_encoders[0].out_channels
            else: assert all([in_channels == encoder.out_channels for encoder in list_of_encoders]); to_channels = in_channels
            self.upsampling = ConvTranspose[self.dimension](in_channels * copies_of_inputs, to_channels, self.pooling_size, self.pooling_size, 0)
            block_params.update({'in_channels': to_channels + sum([encoder.out_channels for encoder in list_of_encoders]), 'out_channels': out_channels})
            self.conv_block = Convolution_Block(**block_params)

        def forward(self, x, list_of_encoder_results):
            y = self.upsampling(x)
            if self.padding == self.kernel_size // 2:
                to_combine = list_of_encoder_results + [bt.crop_as(y, list_of_encoder_results[0])]
            else: to_combine = [bt.crop_as(encoder_result, y) for encoder_result in list_of_encoder_results] + [y]
            joint = combine(to_combine, self.skip_type)
            return self.conv_block(joint)


    def __init__(self, **params):
        super().__init__()
        default_values = {'dimension': 2, 'depth': 4, 'conv_num': 2, 'padding': 'SAME', 'in_channels': 1, 'out_channels': 2, 'block_channels': 64, 'kernel_size': 3, 'pooling_size': 2, 'keep_prob': 0.5, 'conv_block': 'conv', 'multi_arms': "shared", 'multi_arms_combine': cat, 'skip_type': cat, 'res_type': bt.add, 'activation_function': nn.ReLU, 'active_args': {}, 'initializer': "normal(0, 0.1)", 'with_softmax': True, 'cum_layers': -1, 'bottleneck_out_channels': 0}
        param_values = {}
        param_values.update(default_values)
        param_values.update(params)
        self.__dict__.update(param_values)
        
        if isinstance(self.block_channels, int):
            self.block_channels = [self.in_channels] + [self.block_channels << min(i, 2 * self.depth - i) for i in range(2 * self.depth + 1)] + [self.out_channels]
        bchannels = self.block_channels
        if not callable(self.block_channels): self.block_channels = lambda i: bchannels[i + 1]
        
        if isinstance(self.padding, str): self.padding = {'SAME': self.kernel_size // 2, 'ZERO': 0, 'VALID': 0}.get(self.padding.upper(), self.kernel_size // 2)
        
        if isinstance(self.cum_layers, int): self.cum_layers = [self.cum_layers, self.cum_layers]
        l, u = self.cum_layers
        l = (l + 2 * self.depth + 1) % (2 * self.depth + 1)
        u = (u + 2 * self.depth + 1) % (2 * self.depth + 1)
        if l > u: l, u = u, l
        self.cum_layers = [max(l, self.depth), min(u, 2 * self.depth)]
        
        param_values = {k: self.__dict__[k] for k in param_values}
        
        self.arm_type, self.arm_num = parse(self.multi_arms)
        self.arm_num = 1 if len(self.arm_num) == 0 else self.arm_num[0]
        if self.arm_type == 'shared': self.dif_arm_num = 1
        else: self.dif_arm_num = self.arm_num
        
        for iarm in range(self.dif_arm_num):
            for k in range(self.depth + 1):
                setattr(self, 'block%d_%d' % (k, iarm), self.Encoder_Block(self.block_channels(k - 1), self.block_channels(k), k != 0, param_values))
        
        if self.bottleneck_out_channels > 0:
            param_values = {k: v for k, v in param_values.items() if k not in ('in_channels', 'out_channels')}
            setattr(self, 'bottleneck_out', Convolution_Block(self.block_channels(self.depth) * self.arm_num, self.bottleneck_out_channels, **param_values))

        for k in range(self.cum_layers[0], self.depth + 1):
            conv = Convolution[self.dimension](self.block_channels(k), self.block_channels(2 * self.depth + 1), 1, 1, 0)
            initialize_model, initialize_params = parse(self.initializer)
            eval('nn.init.%s_' % initialize_model)(conv.weight, *initialize_params)
            if k < self.cum_layers[1]:
                setattr(self, 'block%dout' % k, nn.Sequential(conv, self.activation_function(**self.active_args)))
                setattr(self, 'out%dupsample' % k, ConvTranspose[self.dimension](
                    self.block_channels(2 * self.depth + 1), self.block_channels(2 * self.depth + 1), self.pooling_size, self.pooling_size, 0
                ))
            else: setattr(self, 'block%dout' % k, conv)

        for k in range(self.depth + 1, self.cum_layers[1] + 1):
            setattr(self, 'block%d' % k, self.Decoder_Block(
                [getattr(self, 'block%d_%d' % (2 * self.depth - k, iarm)) for iarm in range(self.dif_arm_num)] * (self.arm_num // self.dif_arm_num), 
                self.block_channels(k - 1), self.block_channels(k), param_values, 
                self.arm_num if k == self.depth + 1 and self.multi_arms_combine == cat else 1
            ))
            conv = Convolution[self.dimension](self.block_channels(k), self.block_channels(2 * self.depth + 1), 1, 1, 0)
            initialize_model, initialize_params = parse(self.initializer)
            eval('nn.init.%s_' % initialize_model)(conv.weight, *initialize_params)
            if k < self.cum_layers[1]:
                setattr(self, 'block%dout' % k, nn.Sequential(conv, self.activation_function(**self.active_args)))
                setattr(self, 'out%dupsample' % k, ConvTranspose[self.dimension](
                    self.block_channels(2 * self.depth + 1), self.block_channels(2 * self.depth + 1), self.pooling_size, self.pooling_size, 0
                ))
            else: setattr(self, 'block%dout' % k, conv)

        if self.with_softmax: self.softmax = self.Softmax()
        self.to(bt.get_device().main_device)
        
    @property
    def bottleneck(self):
        if self.bottleneck_out_channels > 0:
            result = getattr(self, f'block{self.depth}result', None)
            if result is None: return
            return self.bottleneck_out(result).mean(...)
        else: return

    def forward(self, x):
        size = x.size()[1:]
        if len(size) == self.dimension and self.in_channels == 1: x = x.unsqueeze(1)
        elif len(size) == self.dimension + 1 and self.in_channels * self.arm_num == size[0]: pass
        else: raise ValueError(f"The input tensor does not correspond to the U-Net structure: got {size}, but requires ([{self.in_channels * self.arm_num}], n_1, ⋯, n_{self.dimension}). ")
        
        assert size[0] % self.arm_num == 0
        inputs = x.split(size[0] // self.arm_num, 1)
        assert len(inputs) == self.arm_num
        
        for i, y in enumerate(inputs):
            for k in range(self.depth + 1):
                y = getattr(self, 'block%d_%d' % (k, 0 if self.arm_type == 'shared' else i))(y)
                setattr(self, 'block%d_%dresult' % (k, i), y)
        
        to_combine = [getattr(self, 'block%d_%dresult' % (self.depth, i)) for i in range(self.arm_num)]
        z = combine(to_combine, self.multi_arms_combine)
        setattr(self, 'block%dresult' % self.depth, z)
        
        for k in range(self.depth + 1, self.cum_layers[1] + 1):
            z = getattr(self, 'block%d' % k)(z, [getattr(self, 'block%d_%dresult' % (2 * self.depth - k, iarm)) for iarm in range(self.arm_num)])
            setattr(self, 'block%dresult' % k, z)

        t = 0
        for k in range(self.cum_layers[0], self.cum_layers[1] + 1):
            setattr(self, 'block_out%dresult' % k, getattr(self, 'block%dout' % k)(getattr(self, 'block%dresult' % k)) + t)
            if k < self.cum_layers[1]: t = getattr(self, 'out%dupsample' % k)(getattr(self, 'block_out%dresult' % k))
        
        if self.with_softmax: return self.softmax(getattr(self, 'block_out%dresult' % k))
        else: return getattr(self, 'block_out%dresult' % k)
        
    def optimizer(self, lr=0.001): return bt.Optimization(bt.optim.Adam, self.parameters(), lr)

    def loss(self, x, y):
        y_hat = self(x)
        clamped = y_hat.clamp(1e-10, 1.0)
        self.y_hat = y_hat
        return - bt.sum(y * bt.log(clamped), 1).mean().mean()
        
    def __getitem__(self, i):
        if self.arm_num == 1 and i <= self.depth: i = (i, 0)
        return getattr(self, 'block%dresult' % i if isinstance(i, int) else 'block%d_%dresult' % i)
        
    def __iter__(self):
        for i in range(2 * self.depth + 1):
            if i <= self.depth:
                for iarm in range(self.arm_num):
                    yield 'block%d_%dresult' % (i, iarm), (i, iarm)
            else: yield 'block%dresult' % i, i

class CNN(U_Net):
    '''
    Args:
        dimension (int): The dimension of the images. Defaults to 2 (see VGG). 
        blocks (int): The number of the downsampling blocks. Defaults to 5 blocks (see VGG).
        conv_num (int or list of length 'blocks'): The number of continuous convolutions in one block. Defaults to [2, 2, 3, 3, 3] (see VGG).
            If the numbers for all blocks are the same, one can use one integer.
        padding (int or str): Indicate the type of padding used. Defaults to 'SAME' indicating a same output shape as the input. 
        in_channels (int): The number of channels for the input. Defaults to 1 (see VGG).
        out_elements (int): The number of channels for the output, as the number of classification. Defaults to 1000 for 1000 classes.
        layer_channels (int or list of length 'blocks'): The number of channels for each block. Defaults to [64, 128, 256, 512, 512] (see VGG). 
            Or else, a function may be provided to compute the output channels given the block index (-1 ~ 2 * depth + 1). 
        kernel_size (int): The size of the convolution kernels. Defaults to 3 (see VGG). 
        pooling_size (int): The size of the pooling kernels. Defaults to 2 (see VGG). 
        // keep_prob (float): The keep probability for the dropout layers. 
        conv_block (str): A string with possible values in ('conv', 'dense', 'residual'), indicating which kind of block the U-Net is using: normal convolution layers, DenseBlock or ResidualBlock. 
        multi_arms (str): A string with possible values in ('shared(2)', 'seperate(2)'), indicating which kind of encoder arms are used. 
        multi_arms_combine (function): The combining type for multi-arms. Defaults to catenation (cat). Other possible skip types include torch.mul or torch.add. 
        res_type (function): The combining type for the residual connections. It should be torch.add in most occasions. 
        activation_function (class): The activation function used after the convolution layers. Defaults to nn.ReLU. 
        active_args (dict): The arguments for the activation function. Defaults to {}. 
        initializer (str): A string indicating the initialing strategy. Possible values are normal(0, 0.1) or uniform(-0.1, 0.1) or constant(0) (all parameters can be changed)
        with_softmax (bool): Whether a softmax layer is applied at the end of the network. Defaults to True. 
    '''
    
    def __init__(self, dimension = 2, blocks = 5, conv_num = 2, padding = 'SAME', 
        in_channels = 1, out_elements = 2, layer_channels = 64, kernel_size = 3, 
        pooling_size = 2, keep_prob = 0.5, conv_block = 'conv', multi_arms = "shared", 
        multi_arms_combine = cat, res_type = bt.add, activation_function = nn.ReLU,
        active_args = {}, initializer = "normal(0, 0.1)", with_softmax = True):
        depth = blocks - 1
        if isinstance(layer_channels, int):
            maxlc = layer_channels
            layer_channels = [in_channels]
            multiplier = math.pow(maxlc / in_channels, 1 / (depth + 1))
            for i in range(depth):
                layer_channels.append(int(layer_channels[-1] * multiplier))
            layer_channels.append(maxlc)
            layer_channels.extend([0] * depth)
            layer_channels.append(out_elements)
        super().__init__(dimension = dimension, depth = depth, conv_num = conv_num, 
            padding = padding, in_channels = in_channels, out_channels = out_elements, 
            block_channels = layer_channels, kernel_size = kernel_size, 
            pooling_size = pooling_size, keep_prob = keep_prob, conv_block = conv_block,
            multi_arms = multi_arms, multi_arms_combine = multi_arms_combine, skip_type = None,
            res_type = res_type, activation_function = activation_function, active_args = active_args,
            initializer = initializer, with_softmax = with_softmax, cum_layers = depth)

    def forward(self, x):
        wsm = self.with_softmax
        self.with_softmax = False
        if wsm: r = self.softmax(super().forward(x).flatten(2).mean(-1))
        else: r = super().forward(x).flatten(2).mean(-1)
        self.with_softmax = wsm
        return r
        
class FCN(nn.Module):
    '''
    Fully connected network, with hidden layers of increased and then decreased sizes. 
        For layer_elements = 64 and layers = 8 and in_elements = out_elements = 8, 
        the layer sizes are [8, 16, 32, 64, 64, 32, 16, 8]. 
    
    Args:
        layers (int): Indicate the number of fully connected layers. 
        in_elements (int): The number of elements for the input. Defaults to 1.
        out_elements (int): The number of elements for the output, as the number of classification. Defaults to 1000 for 1000 classes.
        layer_elements (int or list of length 'layers'): The number of channels for each block. In a VGG, it should be [64, 128, 256, 512, 512]. 
            Or else, a function may be provided to compute the output channels given the block index (-1 ~ 2 * depth + 1). 
        kernel_size (int): The size of the convolution kernels. Defaults to 3. 
        keep_prob (float): The keep probability for the dropout layers. 
        activation_function (class): The activation function used after the convolution layers. Defaults to nn.ReLU. 
        active_args (dict): The arguments for the activation function. Defaults to {}. 
        initializer (str): A string indicating the initialing strategy. Possible values are normal(0, 0.1) or uniform(-0.1, 0.1) or constant(0) (all parameters can be changed)
        with_softmax (bool): Whether a softmax layer is applied at the end of the network. Defaults to True. 
    '''

    class Softmax(nn.Module):
        def forward(self, x): return nn.functional.softmax(x, 1)
    def __init__(self, layers = 4, in_elements = 1, out_elements = 2, layer_elements = 64, 
        keep_prob = 0.5, activation_function = nn.ReLU, active_args = {}, 
        initializer = "normal(0, 0.1)", with_softmax = True):
        if isinstance(layer_elements, int):
            maxlc = layer_elements
            layer_elements = [in_elements]
            multiplier = bt.pow(maxlc / in_elements, 1 / (layers // 2 - 1))
            for i in range(layers // 2 - 1):
                layer_elements.append(int(layer_elements[-1] * multiplier))
            layer_elements.append(maxlc)
            if layers % 2 == 0: layer_elements.extend(layer_elements[-2::-1])
            else: layer_elements.extend(layer_elements[::-1])
            layer_elements[-1] = out_elements
        if isinstance(layer_elements, list):
            lc = layer_elements.copy()
            layer_elements = lambda i: lc[i]
        self.layers = []
        for l in range(layers):
            fcl = nn.Linear(layer_elements(l), layer_elements(l+1))
            initialize_model, initialize_params = parse(initializer)
            eval('nn.init.%s_' % initialize_model)(fcl.weight, *initialize_params)
            self.layers.append(fcl)
            if l < layers - 1:
                self.layers.append(activation_function(**active_args))
                self.layers.append(nn.Dropout(keep_prob))
            elif with_softmax:
                self.layers.append(self.Softmax())
        self.struct = nn.Sequential(*self.layers)
        self.to(bt.get_device().main_device)

    def forward(self, x):
        return self.struct(x)


class MultiVariate(list):
    def __init__(self, *args, main_index=0, main_grad_index=1):
        if len(args) > 1: args = (list(args),)
        super().__init__(*args)
        self.main_index = main_index
        self.main_grad_index = main_grad_index
        
    for op in """
        __add__ __iadd__ __radd__
        __sub__ __isub__ __rsub__
        __mul__ __imul__ __rmul__
        __div__ __idiv__ __rdiv__
        __truediv__ __itruediv__ __rtruediv__
        __floordiv__ __ifloordiv__ __rfloordiv__""".split():
        execblock(f"""
        def {op}(self, other):
            if isinstance(other, MultiVariate):
                return MultiVariate((getattr(a, '{op}')(b) for a, b in zip(self, other)), main_index=self.main_index, main_grad_index=self.main_grad_index)
            return MultiVariate((getattr(a, '{op}')(other) for a in self), main_index=self.main_index, main_grad_index=self.main_grad_index)
        """)
            
    for op in """
        abs norm max min item detach""".split():
        execblock(f"""
        def {op}(self): return MultiVariate((a.{op}() for a in self), main_index=self.main_index, main_grad_index=self.main_grad_index)
        """)
            
    for prop in """
        shape""".split():
        execblock(f"""
        @property
        def {prop}(self): return [a.{prop} for a in self]
        """)
        
    def __str__(self): return ' : '.join([str(a.round(decimals=4).tolist()) for a in self])
            
    def cat(self): return bt.cat([a.flatten() for a in self])
    
    def max_item(self): return bt.tensor(self.max().item()).max()
        
    @property
    def main(self): return self[self.main_index]
        
    @main.setter
    def main(self, value): self[self.main_index] = value
        
    @property
    def main_grad(self): return self[self.main_grad_index]
        
    @main_grad.setter
    def main_grad(self, value): self[self.main_grad_index] = value

def multi_variate_max(mv_x, mv_y):
    return MultiVariate((bt.max(x, y) for x, y in zip(mv_x, mv_y)), main_index=mv_x.main_index, main_grad_index=mv_x.main_grad_index)


class NeuralODE(nn.Module):
    '''
    Neural ODE structue. 
    => [main stream: inputs] main_channels
    => [coupled stream: reference maps] coupled_channels
    
    UNODE: unsupervised ODE network, the standard ODE framework.                coupled_channels = 0
    SNODE: supervised ODE, by inserting the features to the ODE framework.      coupled_channels > 0; coupled_ODE = False
    CNODE: coupled ODE, supervise the ODE framework by a coupled ODE sequence.  coupled_channels > 0; coupled_ODE = True
    R-NODE: NODE versions with regularization.                                  regularization != None
    
    Args:
        dimension (int): The dimension of the images. 
        layers (int): The number of accumulated layers, -1 means automatic number of layers. 
            When layers = -1, we have additional arguments:
                time_start (float): The starting time. Defaults to 0. 
                frequency (int): The time frequency for marching, that is the time spot for the i-th iteration when frequency=50Hz is i/(frequency=50).
                max_layers (int): The maximal number of marches. 
                rtol (float): The relative tolerance for auto layer and stopping criteria. 
                atol (float): The absolute tolerance for auto layer and stopping criteria. Together with `rtol`, they indicates a tolerance of `rtol x magnitute + atol` error for the gradient estimation before ending the algorithm. 
        method (str): A string with possible values in ('Euler', 'RK2', 'RK4'), indicating the gradient estimation method. Defaults to 'Euler'. 
        conv_num (int): The number of continuous convolutions in each layer. Defaults to 2. 
        main_channels (int): The number of channels for the main stream ODE. Defaults to 2.
        coupled_channels (int): The number of channels for the coupled stream ODE. Defaults to 0, indicating no coupled network. 
        mid_channels (int): The number of channels for the hidden layers in main stream. Defaults to 10.
        main_march_func (func): The gradient estimator of the main stream ODE. Defaults to a simple stack of `conv_num` convolution layers. 
        coupled_march_func (func): The gradient estimator of the coupled stream ODE. Defaults also to the simple stack of `conv_num` convolution layers. 
        time_points (func): The function that returns the time point at iteration i. Defaults to the linear function (with a time frequency of `frequency`). 
        auto_time_step (bool): Whether to auto decide the time step. `time_points` is disabled when it is True. Defaults to True. 
        min_step (float): The minimal step size in auto adaptive steps. 
        kernel_size (int): The size of the convolution kernels. Defaults to 3. 
        padding (int or str): Indicate the type of padding used. Defaults to 'SAME' indicating a same output shape as the input. 
        conv_block (str): A string with possible values in ('conv', 'dense', 'residual'), indicating which kind of block for the layers: normal convolution layers, DenseBlock or ResidualBlock. 
        res_type (function): The combining type for the residual connections. It should be torch.add in most occasions. 
        activation_function (class): The activation function used after the convolution layers. Defaults to nn.ReLU. 
        final_activation (class): The activation function after the final convolution. Defaults to self.activation_function. 
        active_args (dict): The arguments for the activation function. Defaults to {}. 
        initializer (str): A string indicating the initialing strategy. Possible values are normal(0, 0.1) or uniform(-0.1, 0.1) or constant(0) (all parameters can be changed)
        regularization (func): The regularization term for the delta terms. 
            The regularization function which has the arguments (i, t, dt, *[main_x, coupled_x (if used)], delta_main_x)
    '''
    
    class Softmax(nn.Module):
        def forward(self, x): return nn.functional.softmax(x, 1)
    
    def __init__(self, dimension = 2, layers = -1, method = 'Euler', conv_num = 2, kernel_size = 3, padding = 1, 
        time_start = 0., time_end = 1., frequency = 50, rtol = 1e-3, atol = 1e-3, max_layers = 1000, linear_layer = False, min_step = 0, 
        coupled_channels = 0, main_channels = 2, mid_channels = None, conv_block = 'conv', res_type = bt.add, 
        main_march_func = None, coupled_march_func = None, time_points = None, auto_time_step = True,
        activation_function = nn.ReLU, final_activation = ..., active_args = {}, initializer = "normal(0, 0.1)", 
        shared = True, coupled_ODE = True, time_channels = 1, auto_grad = False, regularization = None):
        super().__init__()
        
        if coupled_channels == True: coupled_channels = 64
        if mid_channels is None: mid_channels = main_channels
        
        params = dict(dimension=dimension, mid_channels=mid_channels, linear_layer=linear_layer, conv_num=conv_num, kernel_size=kernel_size, padding=padding, 
            activation_function=activation_function, final_activation=final_activation, active_args=active_args, conv_block=conv_block, res_type=res_type, initializer=initializer)
        avouch(layers >= 0 or shared, "Unshared Neural ODE network should have fixed number of layers. ")
        if coupled_channels > 0:
            if coupled_ODE:
                if shared:
                    if coupled_march_func is not None: self.coupled_march_func = coupled_march_func
                    else: self.coupled_march_func = Convolution_Block(in_channels=coupled_channels + time_channels, out_channels=coupled_channels, **params)
                    self.coupled_march = infinite_itemize(self.coupled_march_func, n=layers)
                else:
                    self.coupled_march = []
                    for i in range(layers):
                        if coupled_march_func is not None: setattr(self, f'coupled_march_func_{i}', coupled_march_func(i))
                        else: setattr(self, f'coupled_march_func_{i}', Convolution_Block(in_channels=coupled_channels + time_channels, out_channels=coupled_channels, **params))
                        self.coupled_march.append(getattr(self, f'coupled_march_func_{i}'))
        if shared:
            if main_march_func is not None: self.main_march_func = main_march_func
            else: self.main_march_func = Convolution_Block(in_channels=main_channels + coupled_channels + time_channels, out_channels=main_channels, **params)
            self.main_march = infinite_itemize(self.main_march_func, n=layers)
        else:
            self.main_march = []
            for i in range(layers):
                if main_march_func is not None: setattr(self, f'main_march_func_{i}', main_march_func(i))
                else: setattr(self, f'main_march_func_{i}', Convolution_Block(in_channels=main_channels + coupled_channels + time_channels, out_channels=main_channels, **params))
                self.main_march.append(getattr(self, f'main_march_func_{i}'))
        self.method = method
        self.layers = layers
        self.time_start = time_start
        self.time_end = time_end
        self.frequency = layers if layers >= 0 else frequency
        self.rtol = rtol
        self.atol = atol
        self.max_layers = max_layers
        self.shared = shared
        self.coupled_ODE = coupled_ODE
        self.auto_grad = auto_grad
        self.coupled_channels = coupled_channels
        self.time_channels = time_channels
        self.regularization = regularization
        
        if time_points is None:
            if layers >= 0: self.time_end = self.time_start + layers / self.frequency
            time_points = bt.arange(int((self.time_end - self.time_start) * self.frequency + 1)).float() / self.frequency + self.time_start
        self.time_points = time_points
        self.auto_time_step = auto_time_step
        self.min_step = min_step
    
    def time(self, t, n_channel):
        return t * bt.ones(self.reference.shape.with_feature((n_channel,)), dtype=self.reference.dtype, device=self.reference.device)
    
    def error_ratio(self, x0, x1=None, dx=None):
        if x1 is not None and dx is not None or x1 is None and dx is None:
            raise TypeError("Function tolerant takes arguments (x0, x1) or (x0, dx). ")
        elif x1 is None: x1 = x0 + dx
        else: dx = x1 - x0
        error = dx.abs().max()
        tolerance = self.rtol * multi_variate_max(x0.abs().max(), x1.abs().max()).item() + self.atol
        return bt.tensor_to((error / tolerance).item(), x0[0]).max()
    
    def integrate(self, init_x: MultiVariate, diff_func, ts, t0 = None, time_inv = False, steps = None, output_sequence=False, 
                  order=0.9, min_factor=0.2, max_factor=10.): # auto step size parameters
        self.memory_used = ByteSize(0)
        x = init_x
        if steps is None and self.layers >= 0: steps = self.layers
        ts = bt.tensor_to(ts, x[0])
        if t0 is None: t0 = ts[0]
        if not isinstance(t0, bt.Tensor): t0 = bt.tensor(t0)
        
        i_iter = 0
        cur_time_point = t0
        cur_time_step = bt.tensor_to(1. / self.frequency, x[0])
        i_coming_t1 = 0
        coming_t1 = ts[0]
        
        self.log = SPrint()
        if time_inv: self.log(f": Integrating an inversed process...")
        else:
            self.log(f": Integrating a forward process...")
            self.output_sequence = []
        
        while True:
            if not self.auto_grad: self.memory_used = ByteSize(0)
            if time_inv:
                if i_iter >= self.n_iter:
                    self.log("# Stopping the iterations: scheduled steps reached. ")
                    break
                i = int(self.n_iter - i_iter - 1)
            else:
                if steps is not None and i_iter >= steps:
                    self.log("# Stopping the iterations: scheduled steps reached. ")
                    break
                i = i_iter

            t = cur_time_point
            dt = cur_time_step
            
            if bt.equals(coming_t1, t):
                i_coming_t1 += 1
                complete = i_coming_t1 >= len(ts)
                if output_sequence or complete:
                    self.log(f"* Recording sequence value (fetching sequential grad) at time {t}. ")
                    if not time_inv: # In forward process. 
                        self.output_sequence.append(x.main)
                    else: # In backward process: only when self.auto_grad = False. 
                        cur_grad = None if self.output_sequence_grad is None else (self.ouput_sequence_grad[i] if i < len(self.output_sequence_grad) else None)
                        # if cur_grad is not None: x.main_grad = x.main_grad + cur_grad
                if complete: break
                coming_t1 = ts[i_coming_t1]
            if coming_t1 < t + dt:
                dt = coming_t1 - t
            
            self.log(f"> Iteration {i} at time {t}(+{dt}), targeting {coming_t1}. ")
            if self.auto_time_step:
                for _ in range(3): # The maximal time-out number of iteration. 
                    # Adjust the step size using Runge-Kutta Adaptive Step-Size
                    method_ref = "RK2" if self.method != "RK2" else "RK4"
                    grad = diff_func(i, t, dt, x)
                    grad_ref = diff_func(i, t, dt, x, method = method_ref)
                    error_ratio = self.error_ratio(grad_ref, grad) # error / tolerance
                    if error_ratio > 1: # reduce dt when out of tolerance
                        self.log(f"\t| Reducing dt when error rate {error_ratio} > 1 for grad({self.method})={grad} and reference({method_ref})={grad_ref}")
                        factor = 0.9 * error_ratio ** (-order) # 0.9 is a safety setting to avoid local minimum and underflow. 
                        factor = min(max(factor, min_factor), max_factor) # clamp the factor, within [0.2, 10] by default. 
                        cur_time_step = (cur_time_step * factor).clamp(self.min_step)
                        dt = cur_time_step
                    else: break
                else: self.log(f"! Warning: auto time step time out at {t}(+{dt}).")
                cur_time_point = t + dt
            else:
                grad = diff_func(i, t, dt, x)
            
            dx = dt * grad
            error_ratio = self.error_ratio(x, dx=dx)
            if steps is None and (error_ratio < 1 or i_iter >= self.max_layers):
                if i_iter >= self.max_layers: self.log(f"# Stopping the iterations: maximal steps ({self.max_layers}) reached. ")
                else: self.log(f"# Stopping the iterations: converged (with an error ratio of {error_ratio} for x_t={x} and grad={grad}). ")
                if i_iter < 5: print(f"Warning: only {i_iter} NFEs for the ODE. ")
                if i_iter >= self.max_layers: print(f"Warning: reached {self.max_layers} NFE in ODE. ")
                break
            self.log(f". Accept step with an error ratio of {error_ratio} for x_t={x} and grad={grad}). ")
            x = (x - dx) if time_inv else (x + dx)
            
            i_iter += 1
        self.n_iter = i_iter
        return x
    
    # The major marching function
    def march(self, i, t, dt, x, march_funcs, method=None):
        avouch(dt > 0, f'underflow in dt {dt}')
        avouch(bt.isfinite(x).all(), f'infinite x: {x}')
        
        # Select the marching function and the time point for iteration i. 
        if isinstance(march_funcs, infinite_itemize) and march_funcs.is_infinite:
            march_func = march_funcs.obj
        elif i < len(march_funcs): march_func = march_funcs[int(i)]
        else: march_func = march_funcs.obj
        
        # Add the time tensor if necessary. 
        if self.time_channels > 0:
            step = lambda t, x: march_func(bt.cat(x, self.time(t, n_channel=self.time_channels), []))
        else: step = lambda t, x: march_func(x)

        # Solve the ODE using numerical methods. 
        if method is None: method = self.method
        if method == 'Euler':
            grad = step(t, x)
            self.memory_used += getattr(march_func, 'memory_used', 0)
        elif method.startswith('RK'):
            rank = int(method[2:])
            butcher_table = [
                # Order 1: Euler
                [[0     , 0     ], 
                 [0     , 1     ]], 
                # Order 2: Heun Method
                [[0     , 0     , 0     ], 
                 [1     , 1     , 0     ], 
                 [0     , 1 / 2 , 1 / 2 ]],
                # Order 3: 
                [[0     , 0     , 0     , 0     ], 
                 [1     , 1     , 0     , 0     ], 
                 [1 / 2 , 1 / 4 , 1 / 4 , 0     ], 
                 [0     , 1 / 6 , 1 / 6 , 2 / 3 ]], 
                # Order 4
                [[0     , 0     , 0     , 0     , 0     ], 
                 [1 / 2 , 1 / 2 , 0     , 0     , 0     ], 
                 [1 / 2 , 0     , 1 / 2 , 0     , 0     ], 
                 [1     , 0     , 0     , 1     , 0     ], 
                 [0     , 1 / 6 , 1 / 3 , 1 / 3 , 1 / 6 ]], 
                # Order 5
                [[0     , 0         , 0         , 0         , 0             , 0         , 0     ], 
                 [1 / 4 , 1 / 4     , 0         , 0         , 0             , 0         , 0     ], 
                 [3 / 8 , 3 / 32    , 9 / 32    , 0         , 0             , 0         , 0     ], 
                 [12/13 , 1932/2197 , -7200/2197, 7296/2197 , 0             , 0         , 0     ], 
                 [1     , 439 / 216 , -8        , 3680/513  , -845 / 4104   , 0         , 0     ], 
                 [1 / 2 , -8 / 27   , 2         , -3544/2565, 1859 / 4104   , -11 / 40  , 0     ], 
                 [0     , 16 / 135  , 0         , 6656/12825, 28561 / 56430 , -9 / 50   , 2 / 55]]
            ][rank]
            num_eq = len(butcher_table) - 1
            Ks = []
            for i in range(num_eq + 1):
                ci, *ai_ = butcher_table[i]
                if len(Ks) == 0: grad = bt.zeros_like(x[0])
                else: grad = bt.tensor_to(bt.stack([a * k for a, k in zip(ai_, Ks)], bt.func_dim).sum(bt.func_dim), x[0])
                if i == num_eq: break
                Ks.append(step(t + ci * dt, x + dt * grad))
            self.memory_used += num_eq * getattr(march_func, 'memory_used', 0)
        
        return grad
    
    def forward_diff_func(self, i, t, dt, x, method=None):
        if self.coupled_channels > 0:
            main_x, coupled_x = x
            grad_main_x = self.march(i, t, dt, bt.cat(main_x, coupled_x, []), self.main_march, method=method)
            if self.coupled_ODE: # CNODE
                grad_coupled_x = self.march(i, t, dt, coupled_x, self.coupled_march, method=method)
            else: grad_coupled_x = bt.zeros_like(coupled_x)
            return MultiVariate([grad_main_x, grad_coupled_x]) # SNODE / CNODE
        return MultiVariate([self.march(i, t, dt, x[0], self.main_march, method=method)]) # UNODE
    
    def forward_func(self, init_x, coupled_init_x=None, steps=None, output_sequence=False):
        self.reference = init_x
        self.output_sequence = []
        if self.coupled_channels > 0:
            self.output, self.coupled = self.integrate(MultiVariate([init_x, coupled_init_x]), self.forward_diff_func, self.time_points, steps=steps, output_sequence=output_sequence)
        else: self.output, = self.integrate(MultiVariate([init_x]), self.forward_diff_func, self.time_points, steps=steps, output_sequence=output_sequence)
        if output_sequence:
            return self.output, self.output_sequence
        else: return self.output
    
    def UNODE_backward_diff_func(self, i, t, dt, x, method=None):
        main_x, d_main = x
        with bt.enable_grad():
            main_x = main_x.detach().requires_grad_(True)
            delta_main_x = self.march(i, t, dt, main_x, self.main_march, method=method)
            reg_grad_delta = 0
            if self.regularization is not None:
                reg_delta_main_x = delta_main_x.detach().requires_grad_(True)
                reg = self.regularization(i, t, dt, main_x, reg_delta_main_x)
                if reg is not None and reg.requires_grad:
                    reg.backward()
                    reg_grad_main = reg_delta_main_x.grad
                    if reg_grad_main is not None: reg_grad_delta = reg_grad_main
            delta_main_x.backward(d_main.detach() + reg_grad_delta)
        return MultiVariate([delta_main_x.detach(), -main_x.grad])
    
    def SNODE_backward_diff_func(self, i, t, dt, x):
        main_x, d_main, d_coupled = x
        with bt.enable_grad():
            main_x = main_x.detach().requires_grad_(True)
            coupled_x = self.coupled.detach().requires_grad_(True)
            delta_main_x = self.march(i, t, dt, bt.cat(main_x, coupled_x, []), self.main_march, method=method)
            reg_grad_delta = 0
            if self.regularization is not None:
                reg_delta_main_x = delta_main_x.detach().requires_grad_(True)
                reg = self.regularization(i, t, dt, main_x, coupled_x, reg_delta_main_x)
                if reg is not None and reg.requires_grad:
                    reg.backward()
                    reg_grad_main = reg_delta_main_x.grad
                    if reg_grad_main is not None: reg_grad_delta = reg_grad_main
            delta_main_x.backward(d_main.detach() + reg_grad_delta)
        return MultiVariate([delta_main_x.detach(), -main_x.grad, -coupled_x.grad])
    
    def CNODE_backward_diff_func(self, i, t, dt, x):
        main_x, coupled_x, d_main, d_coupled = x
        with bt.enable_grad():
            main_x = main_x.detach().requires_grad_(True)
            coupled_x = coupled_x.detach().requires_grad_(True)
            delta_main_x = self.march(i, t, dt, bt.cat(main_x, coupled_x, []), self.main_march, method=method)
            delta_coupled_x = self.march(i, t, dt, coupled_x, self.coupled_march, method=method)
            reg_grad_delta = 0
            if self.regularization is not None:
                reg_delta_main_x = delta_main_x.detach().requires_grad_(True)
                reg = self.regularization(i, t, dt, main_x, coupled_x, reg_delta_main_x)
                if reg is not None and reg.requires_grad:
                    reg.backward()
                    reg_grad_main = reg_delta_main_x.grad
                    if reg_grad_main is not None: reg_grad_delta = reg_grad_main
            delta_coupled_x.backward(d_coupled.detach())
            delta_main_x.backward(d_main.detach() + reg_grad_delta)
        return MultiVariate([delta_main_x.detach(), delta_coupled_x.detach(), -main_x.grad, -coupled_x.grad], main_grad_index=2)
    
    def backward(self, output_grad):
        output_grad = output_grad.as_subclass(bt.Tensor).view(self.output.shape)
        inits = []
        if self.coupled_channels > 0:
            if self.coupled_ODE:
                inits = MultiVariate([self.output, self.coupled, output_grad, bt.zeros_like(self.coupled)], main_grad_index=2)
                ret = self.integrate(inits, self.CNODE_backward_diff_func, self.time_points[::-1], output_sequence=self.use_output_sequence)[2:]
            else:
                inits = MultiVariate([self.output, output_grad, bt.zeros_like(self.coupled)])
                ret = self.integrate(inits, self.SNODE_backward_diff_func, self.time_points[::-1], output_sequence=self.use_output_sequence)[1:]
        else:
            inits = MultiVariate([self.output, output_grad])
            ret = self.integrate(inits, self.UNODE_backward_diff_func, self.time_points[::-1], output_sequence=self.use_output_sequence)[1:]
        # for mlayer in ([self.main_march[0]] if self.shared else self.main_march):
        #     for p in mlayer.parameters(): p.grad = -p.grad
        # if self.coupled_channels > 0:
        #     for mlayer in ([self.coupled_march[0]] if self.shared else self.coupled_march):
        #         for p in mlayer.parameters(): p.grad = -p.grad
        return ret
    
    class Autograd_Func(bt.autograd.Function):
        @staticmethod
        def forward(ctx, self, init_x, coupled_init_x=None):
            ctx.self = self
            with bt.no_grad():
                return self.forward_func(init_x, coupled_init_x=coupled_init_x, steps=self.n_steps, output_sequence=self.use_output_sequence)
        
        @staticmethod
        def backward(ctx, output_grad, output_sequence_grad = None):
            ctx.self.output_sequence_grad = output_sequence_grad
            return None, *ctx.self.backward(output_grad), None
    
    def forward(self, init_x, coupled_init_x=None, steps=None, output_sequence=False):
        if self.auto_grad: return self.forward_func(init_x, coupled_init_x=coupled_init_x, steps=steps, output_sequence=output_sequence)
        x_has_grad = init_x.requires_grad
        if not init_x.requires_grad: init_x.requires_grad = True
        self.n_steps = steps
        self.use_output_sequence = output_sequence
        if self.coupled_channels == 0: ret = self.Autograd_Func.apply(self, init_x)
        else: ret = self.Autograd_Func.apply(self, init_x, coupled_init_x)
        if not x_has_grad: init_x.grad = None; init_x.requires_grad = False
        def convert(r):
            if isinstance(r, (tuple, list)):
                return r.__class__(convert(s) for s in r)
            r = r.as_subclass(init_x.__class__)
            if isinstance(init_x, bt.Tensor): return r.special_from(init_x)
            return r
        return convert(ret)

class RNN(nn.Module):
    '''
    Recurrent Neural Network structue. 
    
    Args:
        dimension (int): The dimension of the images. 
        layers (int): The number recurrent layers. 
        conv_num (int): The number of continuous convolutions in each layer. Defaults to 2. 
        main_channels (int): The number of channels for the main sequence. Defaults to 2.
        hidden_channels (int): The number of channels for the hidden features. Defaults to 0, indicating no coupled network. 
        mid_channels (int): The number of channels for the hidden layers. Defaults to 10.
        kernel_size (int): The size of the convolution kernels. Defaults to 3. 
        padding (int or str): Indicate the type of padding used. Defaults to 'SAME' indicating a same output shape as the input. 
        conv_block (str): A string with possible values in ('conv', 'dense', 'residual'), indicating which kind of block for the layers: normal convolution layers, DenseBlock or ResidualBlock. 
        res_type (function): The combining type for the residual connections. It should be torch.add in most occasions. 
        activation_function (class): The activation function used after the convolution layers. Defaults to nn.ReLU. 
        final_activation (class): The activation function after the final convolution. Defaults to self.activation_function. 
        active_args (dict): The arguments for the activation function. Defaults to {}. 
        initializer (str): A string indicating the initialing strategy. Possible values are normal(0, 0.1) or uniform(-0.1, 0.1) or constant(0) (all parameters can be changed)
    '''
    
    class Softmax(nn.Module):
        def forward(self, x): return nn.functional.softmax(x, 1)
    
    def __init__(self, dimension = 2, layers = 10, conv_num = 2, kernel_size = 3, padding = 1, frequency = 50, linear_layer = False,
        main_channels = 2, hidden_channels = 0, mid_channels = None, conv_block = 'conv', res_type = bt.add, 
        activation_function = nn.ReLU, final_activation = ..., active_args = {}, initializer = "normal(0, 0.1)", regularization = None):
        super().__init__()
        
        if hidden_channels == True: hidden_channels = 64
        if mid_channels is None: mid_channels = main_channels
        
        params = dict(dimension=dimension, mid_channels=mid_channels, linear_layer=linear_layer, conv_num=conv_num, kernel_size=kernel_size, padding=padding, 
            activation_function=activation_function, final_activation=final_activation, active_args=active_args, conv_block=conv_block, res_type=res_type, initializer=initializer)
        avouch(layers >= 0, "RNN network should have fixed number of layers. ")
        if hidden_channels > 0: self.init_hidden = None
        self.step_layer = Convolution_Block(main_channels + hidden_channels, main_channels + hidden_channels, **params)
        
        self.n_layer = layers
        self.hidden_channels = hidden_channels
    
    def forward(self, input_x, init_hidden=None, n_output_step=None):
        """input_x: ({n_batch}, [n_feature], 'steps', n_1, n_2)"""
        self.memory_used = ByteSize(0)
        n_batch, n_feature, n_input_step, *shape = input_x.shape
        if self.hidden_channels > 0:
            self.init_hidden = bt.zeros({n_batch}, [self.hidden_channels], *shape)
            self.memory_used += self.init_hidden.byte_size()
        if n_output_step is None: n_output_step = n_input_step
        hidden = self.init_hidden
        output_x = None
        outputs = []
        for i in range(self.n_layer):
            if i < n_input_step: layer_input = input_x[:, :, i]
            else: layer_input = output_x
            output = self.step_layer(bt.cat(layer_input, hidden, []))
            self.memory_used += getattr(self.step_layer, 'memory_used', 0)
            output_x = output[:, :n_feature]
            hidden = output[:, n_feature:]
            if i >= self.n_layer - n_output_step: outputs.append(output_x)
        return bt.stack(outputs, '2'), hidden

class Models(bt.nn.Module):
    
    def __init__(self, **sub_models):
        super().__init__()
        self.device = sub_models.pop('device', bt.default_device())
        for name, model in sub_models.items():
            setattr(self, name, model.to(self.device))
        self.best_score = 0
    
    def initialize(self, weight, bias):
        def initializer(layer):
            if hasattr(layer, 'weight') and isinstance(layer.weight, torch.Tensor):
                initialize_model, initialize_params = parse(weight)
                getattr(layer.weight.data, f'{initialize_model}_')(*initialize_params)
            if hasattr(layer, 'bias') and isinstance(layer.bias, torch.Tensor):
                initialize_model, initialize_params = parse(bias)
                getattr(layer.bias.data, f'{initialize_model}_')(*initialize_params)
        for name in self.sub_networks:
            if not name or name.startswith('#'): continue
            getattr(self, name).apply(initializer)
            
    def load(self, directory, epoch='best', **kwargs):
        checkpoint_dir = Path(directory)
        if isinstance(epoch, str):
            candidates = [ckpt_file for ckpt_file in checkpoint_dir if ckpt_file.name.endswith(epoch)]
            if len(candidates) == 0: raise FileNotFoundError(f"Cannot find checkpoint with label {epoch}. ")
            if len(candidates) > 1: raise FileNotFoundError(f"Multiple checkpoints found with label {epoch}: {candidates}. ")
            ckpt_file = candidates[0]
            token = ckpt_file.name.replace('epoch', '').replace(epoch, '').strip().strip('_')
        else: ckpt_file = f"epoch{epoch}.ckpt"
        kwargs.setdefault('weights_only', True)
        self.load_state_dict(bt.load(checkpoint_dir / ckpt_file, map_location=self.device, **kwargs))
        return touch(lambda: eval(token), None)
            
    def save(self, directory, epoch, score=0):
        avouch(0 <= score <= 1, TypeError("Model score should be between [0, 1] in method 'save'. "))
        checkpoint_dir = Path(directory).mkdir()
        if score > self.best_score:
            for ckpt_file in checkpoint_dir:
                if ckpt_file.name.endswith('_best'): ckpt_file.remove()
            bt.save(self.state_dict(), checkpoint_dir / f"epoch{epoch}_best.ckpt")
            self.best_score = score
        bt.save(self.state_dict(), checkpoint_dir / f"epoch{epoch}.ckpt")

if __name__ == "__main__":
#    unet = U_Net(multi_arms="seperate(3)", block_channels=16)
#    print(unet(bt.rand(10, 3, 100, 100)).size())
#    print(*[x + ' ' + str(unet[i].size()) for x, i in unet], sep='\n')
    unet = U_Net(
        dimension=3, 
        in_channels=2, 
        out_channels=3, 
        block_channels=4, 
        with_softmax=False, 
        initializer="normal(0.0, 0.9)", 
#        conv_block='dense', 
#        conv_num=4, 
#        active_args={'inplace': True}
    )
    print(unet(bt.rand(10, 2, 50, 50, 50)).size())
    print(*[x + ' ' + str(unet[i].size()) for x, i in unet], sep='\n')