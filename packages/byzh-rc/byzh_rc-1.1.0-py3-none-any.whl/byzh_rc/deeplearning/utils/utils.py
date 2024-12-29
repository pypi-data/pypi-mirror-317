import torch

def get_device():
    # 优先使用NPU
    try:
        import torch_npu
        return torch.device("npu")
    except ImportError:
        pass

    # 其次使用GPU
    if torch.cuda.is_available():
        return torch.device("cuda")

    # 最后使用CPU
    return torch.device("cpu")

if __name__ == '__main__':
    result = get_device()
    print(result)