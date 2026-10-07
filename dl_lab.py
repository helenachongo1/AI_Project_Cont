import torch
import joblib
from torchvision import models
import torch.nn as nn

# Load AlexNet
alexnet = models.alexnet(pretrained=False)
rcnn_feat = nn.Sequential(*list(alexnet.children())[:-1])

rcnn_feat.load_state_dict(
    torch.load("C:/Users/Acer/Downloads/rcnn_alexnet_features.pth", map_location="cpu")
)

rcnn_feat.eval()

# Load SVM
svm_rcnn = joblib.load("C:/Users/Acer/Downloads/rcnn_svm.pkl")

print("Model loaded successfully")
