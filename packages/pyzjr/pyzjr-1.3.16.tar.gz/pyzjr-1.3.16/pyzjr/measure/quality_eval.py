import cv2
import torch
import numpy as np
import scipy.ndimage as ndi
from skimage.filters import sobel
import torch.nn.functional as F
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
from pyzjr.utils.check import is_numpy, is_tensor

def GradientMetric(img, size=11):
    """
    计算指示图像中模糊强度的度量(0表示无模糊, 1表示最大模糊)
    但实际上还是要根据我们的标准图与模糊图得到模糊区间
    :param img: 单通道进行处理,灰度图
    :param size: 重新模糊过滤器的大小
    :return: 模糊度量值
    """
    image = np.array(img, dtype=np.float32) / 255
    n_axes = image.ndim
    shape = image.shape
    blur_metric = []

    slices = tuple([slice(2, s - 1) for s in shape])
    for ax in range(n_axes):
        filt_im = ndi.uniform_filter1d(image, size, axis=ax)
        im_sharp = np.abs(sobel(image, axis=ax))
        im_blur = np.abs(sobel(filt_im, axis=ax))
        T = np.maximum(0, im_sharp - im_blur)
        M1 = np.sum(im_sharp[slices])
        M2 = np.sum(T[slices])
        blur_metric.append(np.abs((M1 - M2)) / M1)

    return np.max(blur_metric) if len(blur_metric) > 0 else 0.0

def LaplacianMetric(img):
    """
    计算图像的拉普拉斯变换的方差作为模糊度量。
    拉普拉斯变换是一种边缘检测算子，对图像进行二阶微分。
    清晰的图像在边缘处会有较大的二阶微分值，而模糊的图像边缘会变得平滑，
    导致二阶微分值减小。因此，拉普拉斯变换的方差可以作为图像模糊程度的一个度量。
    方差越大，表示图像越清晰；方差越小，表示图像越模糊。

    :param img: 输入图像，应为灰度图
    :return: 拉普拉斯变换的方差值，作为模糊度量
    """
    return cv2.Laplacian(img, cv2.Lap_64F).var()

def calculate_psnr(input_, target_):
    """计算两张图片的PSNR"""
    img1 = np.array(input_)
    img2 = np.array(target_)
    psnr = peak_signal_noise_ratio(img1, img2)
    return psnr

def calculate_psnrv2(input_, target_):
    psnr = 0
    if is_numpy(input_) and is_numpy(target_):
        mse = np.mean((input_ - target_) ** 2)
        if mse == 0:
            return float('inf')
        max_pixel = max(np.max(input_), np.max(target_))
        psnr = 10 * np.log10((max_pixel ** 2) / mse)
    elif is_tensor(input_) and is_tensor(target_):
        psnr = 10 * torch.log10(1 / F.mse_loss(input_, target_)).item()
    return psnr

def calculate_ssim(input_, target_, win_size=7):
    """计算两张图片的 SSIM"""
    input_img = np.array(input_)
    target_img = np.array(target_)
    height, width = input_img.shape[:2]
    win_size = min(win_size, min(height, width))
    win_size = win_size + 1 if win_size % 2 == 0 else win_size
    ssim_value = structural_similarity(input_img, target_img, win_size=win_size, channel_axis=-1)
    return ssim_value

def calculate_ssimv2(input_, target_, ksize=11, sigma=1.5):
    ssim_map = 0
    if is_numpy(input_) and is_numpy(target_):
        C1 = (0.01 * 255)**2
        C2 = (0.03 * 255)**2

        img1 = input_.astype(np.float64)
        img2 = target_.astype(np.float64)
        kernel = cv2.getGaussianKernel(ksize, sigma)
        window = np.outer(kernel, kernel.transpose())
        mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]
        mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
        mu1_sq = mu1**2
        mu2_sq = mu2**2
        mu1_mu2 = mu1 * mu2
        sigma1_sq = cv2.filter2D(img1**2, -1, window)[5:-5, 5:-5] - mu1_sq
        sigma2_sq = cv2.filter2D(img2**2, -1, window)[5:-5, 5:-5] - mu2_sq
        sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2

        ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) *
                                                            (sigma1_sq + sigma2_sq + C2))
    return ssim_map.mean()

if __name__=="__main__":
    img1 = cv2.imread('221.png')
    img2 = cv2.imread('220.png')

    if img1.shape != img2.shape:
        print("Images must have the same dimensions.")
        exit()

    psnr = calculate_psnr(img1, img2)
    print(f'PSNR: {psnr:.2f} dB')
    psnr = calculate_psnrv2(img1, img2)
    print(f'PSNR V2: {psnr:.2f} dB')

    ssim_score = calculate_ssim(img1, img2)
    print(f'SSIM: {ssim_score:.4f}')
    ssim_score = calculate_ssimv2(img1, img2)
    print(f'SSIM V2: {ssim_score:.4f}')