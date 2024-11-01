def _optimize_pushback_float(self) -> None:
    import albumentations as op_blurs
    import albumentations.augmentations.transforms as op_float
    
    float_operation = (op_float.ToFloat, )
    jitter_operation = (op_float.ColorJitter,)
    
    blur_operation = (op_blurs.GaussianBlur,
                        op_blurs.Blur,
                        op_blurs.AdvancedBlur,
                        op_blurs.MedianBlur,
                        op_blurs.ZoomBlur,
                        op_blurs.MotionBlur)
    
    existFloat = False
    
    for t in self.transforms:
        if isinstance(t, float_operation):
            existFloat = True
    
    # float연산은 해당 list에 넣지 않기 그리고 만약 처음으로 colorjitter같은 연산을 만나면 그 앞에 float연산 추가
    # 이 때 한 번만 float연산을 추가시켜주어야한다. 
    if existFloat:
        optimized_trans = []
        isFloatIn = False
        float_op = None
        
        for t in self.transforms:
            if isinstance(t, float_operation):
                float_op = t        
            elif (not isFloatIn) and isinstance(t, jitter_operation + blur_operation):
                optimized_trans.append(float_op)
                optimized_trans.append(t)
                isFloatIn = True
            else:
                optimized_trans.append(t)
                
        self.transforms = optimized_trans