import torch
from pycocotools.coco import COCO
import matplotlib.pyplot as plt
from utils.encoder import encoder
import torchvision.transforms as T

class COCODataset(torch.utils.data.Dataset):
    def __init__(self,root,json,size,tau,do_aug=False,grey=False):
        self.coco=COCO(json)
        self.root=root
        self.size=size
        self.cat_ids=self.coco.getCatIds(['person'])
        self.img_ids=self.coco.getImgIds(catIds=self.cat_ids)
        self.scale=4
        self.num_joints=12
        p_norm=([0.5,0.5,0.5],[1,1,1])  if not grey else ([0],[1])
        self.transformer=T.Compose([T.ToTensor(),T.Normalize(*p_norm)])
        #FOR TEST
        # self.transformer=T.Compose([T.ToTensor()])
        self.do_aug=do_aug
        self.grey=grey
        self.tau=tau

    def __len__(self):
        return len(self.img_ids)

    def __getitem__(self, idx):
        img_info=self.coco.loadImgs(self.img_ids[idx])[0]
        ann_ids=self.coco.getAnnIds(self.img_ids[idx],self.cat_ids)
        annos=self.coco.loadAnns(ann_ids)
        img,centermap,center_mask,kps_offset,kps_weight=encoder(img_info, self.root, annos, self.size, self.scale, self.num_joints,self.do_aug,self.tau)
        if img.mode!='RGB':img=img.convert('RGB')
        if self.grey:img=img.convert('L')
        # plt.imshow(img)
        # plt.axis('off')
        # self.coco.showAnns(annos)
        # print(annos[0]['num_keypoints'])
        # print(annos)
        # plt.show()
        return self.transformer(img), centermap, center_mask, kps_offset, kps_weight,self.img_ids[idx]
if __name__=='__main__':
    dataset=COCODataset('../../data/coco/train2017','../../data/coco/person_keypoints_train2017.json',(128,128))
    _=dataset[0]