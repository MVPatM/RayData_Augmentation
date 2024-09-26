def _optimize_operation_order(self) -> None:
    import albumentations.augmentations.crops.transforms as op_crop
    import albumentations.augmentations.geometric.resize as op_resize
    import albumentations.augmentations.transforms as op_grayscale
                
    crop_operation = (op_crop.RandomCrop,
                      op_crop.CenterCrop,
                      op_crop.Crop,
                      op_crop.CropNonEmptyMaskIfExists,
                      op_crop.RandomSizedCrop,
                      op_crop.RandomResizedCrop,
                      op_crop.RandomCropNearBBox,
                      op_crop.RandomSizedBBoxSafeCrop,
                      op_crop.CropAndPad,
                      op_crop.RandomCropFromBorders,
                      op_crop.BBoxSafeRandomCrop)
        
    resize_operation = (op_resize.RandomScale,
                        op_resize.LongestMaxSize,
                        op_resize.SmallestMaxSize,
                        op_resize.Resize)
        
    grayscale_operation = (op_grayscale.ToGray,)
    
    resize_trans = []
    crop_trans = []
    grayscale_trans = []
        
    reordered_trans = []
        
    for t in self.transforms:
        if isinstance(t, resize_operation):
            resize_trans.append(t)
            
        if isinstance(t, crop_operation):
            crop_trans.append(t)
            
        if isinstance(t, grayscale_operation):
            grayscale_trans.append(t)
        
        
    for t in resize_trans:
        reordered_trans.append(t)
            
    for t in crop_trans:
        reordered_trans.append(t)
        
    for t in grayscale_trans:
        reordered_trans.append(t)
        
    for t in self.transforms:
        if not isinstance(t, crop_operation + resize_operation + grayscale_operation):
            reordered_trans.append(t)
        
    self.transforms = reordered_trans