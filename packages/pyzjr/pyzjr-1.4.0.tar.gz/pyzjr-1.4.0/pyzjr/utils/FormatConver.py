import cv2
import os
import torch
import numpy as np
from PIL import Image
from itertools import repeat
from typing import Iterable

from pyzjr.utils.check import is_pil, is_tensor, is_numpy, is_list_or_tuple, \
    is_Iterable, is_nonnegative_int

def _ntuple(n):
    def parse(x):
        if is_Iterable(x):
            return x
        return tuple(repeat(x, n))
    return parse

to_1tuple = _ntuple(1)
to_2tuple = _ntuple(2)
to_3tuple = _ntuple(3)
to_4tuple = _ntuple(4)
to_ntuple = _ntuple

def convert_suffix(file_path, format):
    """
    将文件路径中的后缀名转换为新的后缀名

    Args:
        file_path (str): 要转换后缀名的文件路径。
        format (str): 新的后缀名，不需要包含点（.）。

    Returns:
        str: 转换后的文件路径。
    """
    base_name, ext = os.path.splitext(file_path)
    new_file_path = base_name + '.' + format
    return new_file_path

def pil2cv(pil_image):
    """将PIL图像转换为OpenCV图像"""
    if pil_image.mode == 'L':
        open_cv_image = np.array(pil_image)
    else:
        open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    return open_cv_image

def cv2pil(cv_image):
    """将OpenCV图像转换为PIL图像"""
    if cv_image.ndim == 2:
        pil_image = Image.fromarray(cv_image, mode='L')
    else:
        pil_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
    return pil_image

def to_numpy(x, dtype=None):
    if is_pil(x):
        return np.array(x, dtype=dtype)
    elif is_tensor(x):
        numpy_array = x.cpu().numpy()
        if dtype is not None:
            numpy_array = numpy_array.astype(dtype)
        return numpy_array
    elif is_numpy(x):
        if dtype is not None:
            return x.astype(dtype)
        return x
    elif isinstance(x, (Iterable, int, float)):
        return np.array(x, dtype=dtype)
    elif is_list_or_tuple(x):
        return np.array(x, dtype=dtype)
    else:
        raise ValueError("Unsupported type")

def to_tensor(x, dtype=None):
    if is_tensor(x):
        if dtype is not None:
            x = x.type(dtype)
        return x
    if is_numpy(x):
        x = torch.from_numpy(x)
        if dtype is not None:
            x = x.type(dtype)
        return x
    if is_list_or_tuple(x):
        x = np.array(x)
        x = torch.from_numpy(x)
        if dtype is not None:
            x = x.type(dtype)
        return x
    else:
        raise ValueError("Unsupported type")

def SumExceptBatch(x, num_batch_dims=1):
    """
    求和“x”中除第一个“num_batch_dims”维度外的所有元素。
    case:
    x1 = torch.tensor([[1, 2], [3, 4]])
    result1 = SumExceptBatch(x1, num_batch_dims=1)
    >> tensor([3, 7])
    """
    if not is_nonnegative_int(num_batch_dims):
        raise TypeError("Number of batch dimensions must be a non-negative integer.")
    reduce_dims = list(range(num_batch_dims, x.ndimension()))
    return torch.sum(x, dim=reduce_dims)


def hwc2chw(img):
    """
    Conversion from 'HWC' to 'CHW' format.
    Example:
        hwc_image_numpy = np.random.rand(256, 256, 3)
        chw_image_numpy = hwc2chw(hwc_image_numpy)
        hwc_image_tensor = torch.rand(256, 256, 3)
        chw_image_tensor = hwc2chw(hwc_image_tensor)
    """
    if len(img.shape) == 3:
        if is_numpy(img):
            chw = np.transpose(img, axes=[2, 0, 1])
            return chw
        elif is_tensor(img):
            chw = img.permute(2, 0, 1).contiguous()
            return chw
        else:
            raise TypeError("The input data should be a NumPy array or "
                            "PyTorch tensor, but the provided type is: {}".format(type(img)))
    else:
        raise ValueError("The input data should be three-dimensional (height x width x channel), but the "
                         "provided number of dimensions is:{}".format(len(img.shape)))


def chw2hwc(img):
    """Conversion from 'CHW' to 'HWC' format."""
    if len(img.shape) == 3:
        if is_numpy(img):
            hwc = np.transpose(img, axes=[1, 2, 0])
            return hwc
        elif is_tensor(img):
            hwc = img.permute(1, 2, 0).contiguous()
            return hwc
        else:
            raise TypeError("The input data should be a NumPy array or "
                            "PyTorch tensor, but the provided type is: {}".format(type(img)))
    else:
        raise ValueError ("The input data should be three-dimensional (channel x height x width), but the "
                          "provided number of dimensions is: {}".format(len(img.shape)))


def to_bchw(tensor):
    """
    Convert to 'bchw' format
    Example:
        image_tensor = torch.rand(256, 256)
        bchw_image_tensor = to_bchw(image_tensor)
        print("Original shape:", image_tensor.shape)
        print("Converted shape:", bchw_image_tensor.shape)
    """
    if not isinstance(tensor, torch.Tensor):
        raise TypeError(f"Input type is not a Tensor. Got {type(tensor)}")

    if len(tensor.shape) < 2:
        raise ValueError(f"Input size must be a two, three or four dimensional tensor. Got {tensor.shape}")

    if len(tensor.shape) == 2:
        tensor = tensor.unsqueeze(0)

    if len(tensor.shape) == 3:
        tensor = tensor.unsqueeze(0)

    if len(tensor.shape) > 4:
        tensor = tensor.view(-1, tensor.shape[-3], tensor.shape[-2], tensor.shape[-1])

    return tensor

def image_to_tensor(image, keepdim=True):
    """
    Convert numpy images to PyTorch 4d tensor images
    'keepdim' indicates whether to maintain the current dimension, otherwise it will be changed to type 4d
    Example:
        img = np.ones((3, 3))
        image_to_tensor(img).shape
    [1, 3, 3]
        img = np.ones((4, 4, 1))
        image_to_tensor(img).shape
    [1, 4, 4]
        img = np.ones((4, 4, 3))
        image_to_tensor(img, keepdim=False).shape
    [1, 3, 4, 4]
    """
    if is_numpy(image):
        if len(image.shape) > 4 or len(image.shape) < 2:
            raise ValueError("Input size must be a two, three or four dimensional array")
    input_shape = image.shape
    tensor = torch.from_numpy(image)

    if len(input_shape) == 2:
        # (H, W) -> (1, H, W)
        tensor = tensor.unsqueeze(0)
    elif len(input_shape) == 3:
        # (H, W, C) -> (C, H, W)
        tensor = tensor.permute(2, 0, 1)
    elif len(input_shape) == 4:
        # (B, H, W, C) -> (B, C, H, W)
        tensor = tensor.permute(0, 3, 1, 2)
        keepdim = True  # no need to unsqueeze
    else:
        raise ValueError(f"Cannot process image with shape {input_shape}")

    return tensor if keepdim else tensor.unsqueeze(0)

def tensor_to_image(tensor, keepdim = False):
    """Convert PyTorch tensor image to numpy image
    Returns:
        image of the form :math:`(H, W)`, :math:`(H, W, C)` or :math:`(B, H, W, C)`.
    Example:
        img = torch.ones(1, 3, 3)
        tensor_to_image(img).shape
    (3, 3)
        img = torch.ones(3, 4, 4)
        tensor_to_image(img).shape
    (4, 4, 3)
    """
    if not isinstance(tensor, torch.Tensor):
        raise TypeError(f"Input type is not a Tensor. Got {type(tensor)}")

    if len(tensor.shape) > 4 or len(tensor.shape) < 2:
        raise ValueError("Input size must be a two, three or four dimensional tensor")

    input_shape = tensor.shape
    image = tensor.cpu().detach().numpy()

    if len(input_shape) == 2:
        # (H, W) -> (H, W)
        pass
    elif len(input_shape) == 3:
        # (C, H, W) -> (H, W, C)
        if input_shape[0] == 1:
            # Grayscale for proper plt.imshow needs to be (H,W)
            image = image.squeeze()
        else:
            image = image.transpose(1, 2, 0)
    elif len(input_shape) == 4:
        # (B, C, H, W) -> (B, H, W, C)
        image = image.transpose(0, 2, 3, 1)
        if input_shape[0] == 1 and not keepdim:
            image = image.squeeze(0)
        if input_shape[1] == 1:
            image = image.squeeze(-1)
    else:
        raise ValueError(f"Cannot process tensor with shape {input_shape}")

    return image

def imagelist_to_tensor(imagelist):
    """Converts a list of numpy images to a PyTorch 4d tensor image.
    Args:
        images: list of images, each of the form :math:`(H, W, C)`.
        Image shapes must be consistent
    Returns:
        tensor of the form :math:`(B, C, H, W)`.
    Example:
        imgs = [np.ones((4, 4, 1)),
                np.zeros((4, 4, 1))]
        image_list_to_tensor(imgs).shape
    torch.Size([2, 1, 4, 4])
    """
    if len(imagelist[0].shape) != 3:
        raise ValueError("Input images must be three dimensional arrays")
    list_of_tensors = []
    for image in imagelist:
        list_of_tensors.append(image_to_tensor(image))
    return torch.stack(list_of_tensors)

def img2tensor(im, totensor=False):
    """NumPy图像数组转换为PyTorch张量"""
    im = np.array(im)
    tensor = np.moveaxis(im, -1, 0).astype(np.float32)
    return torch.from_numpy(tensor).type(torch.FloatTensor) if totensor else tensor

def label2tensor(mask, num_classes, sigmoid, totensor=False):
    """标签或掩码图像转换为 PyTorch 张量"""
    mask = np.array(mask)
    if num_classes > 2:
        if not sigmoid:
            long_mask = np.zeros((mask.shape[:2]), dtype=np.int64)
            if len(mask.shape) == 3:
                for c in range(mask.shape[2]):
                    long_mask[mask[..., c] > 0] = c
            else:
                long_mask[mask >= 127] = 1
                long_mask[mask == 0] = 0
            mask = long_mask
        else:
            mask = np.moveaxis(mask, -1, 0).astype(np.float32)
    else:
        mask[mask >= 127] = 1
        mask[mask == 0] = 0
    return torch.from_numpy(mask).long() if totensor else mask

if __name__=="__main__":
    hwc_image_numpy = np.random.rand(256, 256, 3)
    chw_image_numpy = hwc2chw(hwc_image_numpy)
    print("Original HWC shape:", hwc_image_numpy.shape)
    print("Converted CHW shape:", chw_image_numpy.shape)
    hwc_image_tensor = torch.rand(256, 256, 3)
    chw_image_tensor = hwc2chw(hwc_image_tensor)
    print("Original HWC shape:", hwc_image_tensor.shape)
    print("Converted CHW shape:", chw_image_tensor.shape)