import time

import torch
import numpy as np
from torchvision import transforms,  models

import cv2
from PIL import Image

"""
Image Capture
"""
cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)
#cap.set(cv2.CAP_PROP_FPS, 36)

"""
Image Preprocessing
"""
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

"""
Model Setup (mobilenet_v2)
"""
# torch.backends.quantized.engine = 'qnnpack'
net = torch.hub.load('pytorch/vision:v0.10.0', 'mobilenet_v2')  # models.quantization.mobilenet_v2(pretrained=True, quantize=True)
net.eval()
# jit model to take it from ~20fps to ~30fps
#net = torch.jit.script(net)

"""
Setup loop and run
"""
started = time.time()
last_logged = time.time()
frame_count = 0

# Read the categories
with open("./imagenet_classes.txt", "r") as f:
    categories = [s.strip() for s in f.readlines()]

with torch.no_grad():
    while True:
        # read frame
        ret, image = cap.read()

        if not ret:      
            raise RuntimeError("Failed to read frame.")
        
        # convert opencv output from BGR to RGB
        image = image[:,:, [2,1,0]]
        permuted = Image.fromarray(image)

        # preprocess
        input_tensor = preprocess(permuted)
        input_batch = input_tensor.unsqueeze(0)

        # move the input and model to GPU for speed if available
        if torch.cuda.is_available():
            input_batch = input_batch.to('cuda')
            net.to('cuda')

        # run model
        output = net(input_batch)

        # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
        probabilities = torch.nn.functional.softmax(output[0], dim=0)

        # Show top categories per image
        top5_prob, top5_catid = torch.topk(probabilities, 5)
        for i in range(top5_prob.size(0)):
            print(categories[top5_catid[i]], top5_prob[i].item())
        print('=====')

        cv2.imshow(categories[top5_catid[i]], image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(1)
        