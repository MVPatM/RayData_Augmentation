import ray.data
import ray
from ray.data._internal.logical.optimizers import LogicalOptimizer, PhysicalOptimizer
from ray.data._internal.planner.planner import Planner
from ray.data._internal.plan import ExecutionPlan
from typing import Any, Dict
import numpy as np
import albumentations as A
import time

def increase_brightness(batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    batch["image"] = np.clip(batch["image"] + 4, 0, 255)
    return batch

def decrease_brightness(batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    batch["image"] = np.clip(batch["image"] - 4, 0, 255)
    return batch

def album_randomcrop(batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    batch["image"] = A.random_crop(batch["image"], 1, 110, 0.5, 0.5)
    return batch

#image data를 map_batches()를 통해서 처리를 하는 것은 불가능하다.
#resize는 batch 형태로 처리가 불가능하다.
#resize는 전체 이미지를 한꺼번에 resize를 시켜야한다. 
def album_compose(batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    transform = A.Compose([A.Resize(1268, 1020),
                        A.Flip(0.5),
                        A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1, p=1.0),
                        A.ToGray(),
                        A.Blur(blur_limit=7, p=0.5),
                        A.RandomCrop(512, 440)
                        ])
    
    augmentation = transform(image = batch["image"])
    batch["image"] = augmentation["image"]
    return batch


start = time.time()
path = "C:\\Users\\hsy99\\test\\images"
result = ray.data.read_images(path, parallelism=4, mode="RGB").map(album_compose).write_images(path="C:\\Users\\hsy99\\test\\converted", file_format="JPEG", column='image')
end = time.time()
print(f"{end - start:.5f} sec")

"""
# Check the logical plan and physical plan of executed data pipeline
plan = result._logical_plan
print(f"Logical Plan -> {plan._dag}")

optimized_plan = LogicalOptimizer().optimize(plan)
print(f"Optimized Logical Plan -> {optimized_plan.dag}")

physical_plan = Planner().plan(optimized_plan)
print(f"physical plan -> {physical_plan.dag}")

optimized_physical_plan = PhysicalOptimizer().optimize(physical_plan)
print(f"Optimized Physical Plan -> {optimized_physical_plan.dag}")
"""