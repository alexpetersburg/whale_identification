import torch
from backbone.model_irse import IR_50, IR_101, IR_152, IR_SE_50, IR_SE_101, IR_SE_152
from backbone.model_resnet import ResNet_50, ResNet_101, ResNet_152
from config import configurations

if __name__ == '__main__':
    cfg = configurations[1]
    INPUT_SIZE = cfg['INPUT_SIZE']
    device = cfg['DEVICE']
    PATH = 'model/Backbone_ResNet_50_Epoch_150_Batch_67050_Time_2022-12-25-14-57_checkpoint.pth'
    BACKBONE_RESUME_ROOT = cfg['BACKBONE_RESUME_ROOT']
    BACKBONE_NAME = cfg['BACKBONE_NAME']
    BACKBONE_DICT = {'ResNet_50': ResNet_50(INPUT_SIZE),
                     'ResNet_101': ResNet_101(INPUT_SIZE),
                     'ResNet_152': ResNet_152(INPUT_SIZE),
                     'IR_50': IR_50(INPUT_SIZE),
                     'IR_101': IR_101(INPUT_SIZE),
                     'IR_152': IR_152(INPUT_SIZE),
                     'IR_SE_50': IR_SE_50(INPUT_SIZE),
                     'IR_SE_101': IR_SE_101(INPUT_SIZE),
                     'IR_SE_152': IR_SE_152(INPUT_SIZE)}
    BACKBONE = BACKBONE_DICT[BACKBONE_NAME]
    print("=" * 60)
    print(BACKBONE)
    print("{} Backbone Generated".format(BACKBONE_NAME))

    x = torch.randn(1, 3, 112, 112, requires_grad=True,)
    x.to(device)

    model = BACKBONE
    model.load_state_dict(torch.load(PATH))
    model.eval()

    torch.onnx.export(
        model.to(device),
        x.to(device),
        "./best_model.onnx",
        export_params=True,
        opset_version=11,
        do_constant_folding=True,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={
            "input": {0: "batch_size"},
            "output": {0: "batch_size"},
        },
    )
